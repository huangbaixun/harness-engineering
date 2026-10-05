#!/usr/bin/env python3
"""Offline, conflict-first Claude/Codex project initialization. No global settings or hooks activated."""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BEGIN='<!-- harness:begin -->'
END='<!-- harness:end -->'


def build_plan(project, delivery, adopt_existing=False, tool="codex"):
    prefix=".agents" if tool=="codex" else ".claude"
    instruction="AGENTS.md" if tool=="codex" else "CLAUDE.md"
    template=ROOT/'docs/templates/codex'
    rules=(template/'AGENTS.md.template').read_text().replace('{{DELIVERY}}',delivery)
    runtime=prefix+'/harness' if delivery=='project' else '<installed plugin root>'
    layout='Project resources: `.agents/harness`; skills: `.agents/skills/<name>` (upstream sibling layout, harness: names).' if delivery=='project' else 'Resolve resources and skills from the installed plugin root; no project runtime is copied.'
    rules=rules.replace('{{RUNTIME_ROOT}}',runtime).replace('{{RESOURCE_LAYOUT}}',layout.replace(".agents",prefix))
    if tool=="claude": rules=rules.replace("AGENTS.md", "CLAUDE.md").replace("Codex", "Claude Code")
    existing=project/instruction
    if adopt_existing and existing.is_file():
        body=existing.read_bytes().decode('utf-8')
        if BEGIN in body or END in body:
            if body.count(BEGIN)!=1 or body.count(END)!=1 or body.index(BEGIN)>body.index(END):
                raise ValueError('AGENTS.md has malformed harness managed markers')
            body=re.sub(re.escape(BEGIN)+'.*?'+re.escape(END),lambda _: rules.rstrip(),body,flags=re.S)
        else: body=body+('\n' if body.endswith('\n') else '\n\n')+rules
        rules=body
    config=(template/'harness.json.template').read_text().replace('{{DELIVERY}}',delivery)
    if tool=='claude': config=config.replace('\"codex\"','\"claude\"')
    config_path=project/'.harness/config.json'
    if config_path.is_file():
        existing_config=json.loads(config_path.read_text())
        if not isinstance(existing_config,dict) or any(existing_config.get(k)!=v for k,v in {'schema_version':1,'tool':tool,'delivery':delivery}.items()):
            raise ValueError('existing harness configuration is incompatible with selected delivery')
        config=config_path.read_bytes().decode('utf-8')

    plan=[(project/instruction,rules.encode(),None),(project/'.harness/config.json',config.encode(),None)]
    if not (project/'features.json').exists():
        features={'schema_version':'2.1','features':[],'github':{'enabled':False}}
        plan.append((project/'features.json',(json.dumps(features,indent=2)+'\n').encode(),None))
    if delivery=='project':
        for folder in ('scripts','references','commands','agents','docs/templates','docs/decisions','third_party'):
            for path in sorted((ROOT/folder).rglob('*')):
                if not path.is_file() or '__pycache__' in path.parts or path.suffix=='.pyc' or 'tests' in path.parts: continue
                # Claude lifecycle scripts must not be implicitly available as a Codex entrypoint.
                plan.append((project/prefix/'harness'/path.relative_to(ROOT),path.read_bytes(),path.stat().st_mode & 0o777))
        plan.append((project/prefix/'harness/LICENSE',(ROOT/'LICENSE').read_bytes(),None))
        skill_root=ROOT/'skills' if (ROOT/'skills').is_dir() else ROOT.parent/'skills'
        for path in sorted(skill_root.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix=='.pyc': continue
            rel=path.relative_to(skill_root)
            name=rel.parts[0]
            plan.append((project/prefix/'skills'/name/Path(*rel.parts[1:]),path.read_bytes(),path.stat().st_mode & 0o777))
    return plan


def apply_plan(project, plan, dry_run=False, adopt_existing=False):
    conflicts=[]
    for target,data,mode in plan:
        for parent in [target,*target.parents]:
            if parent==project: break
            if parent.is_symlink() or (parent!=target and parent.exists() and not parent.is_dir()):
                conflicts.append(str(parent.relative_to(project))); break
        if target.exists() and (not target.is_file() or target.read_bytes()!=data):
            if not (adopt_existing and target in (project/'AGENTS.md',project/'CLAUDE.md') and target.is_file()):
                conflicts.append(str(target.relative_to(project)))
    if conflicts: raise ValueError('conflicting existing paths: '+', '.join(sorted(set(conflicts))))
    changes=[(p,d,m) for p,d,m in plan if not p.exists() or p.read_bytes()!=d or (m is not None and p.stat().st_mode & 0o777 != m)]
    report={'delivery_files':len(plan),'changes':[str(p.relative_to(project)) for p,_,_ in changes], 'dry_run':dry_run}
    if not dry_run:
        for target,data,mode in changes:
            target.parent.mkdir(parents=True,exist_ok=True)
            # Exclusive creation for new paths; no silently clobbered files.
            with target.open('wb' if target.exists() else 'xb') as stream: stream.write(data)
            if mode is not None: target.chmod(mode)
    print(json.dumps(report,ensure_ascii=False))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tool',choices=['codex','claude'],required=True)
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--delivery',choices=['project','plugin'],default='project')
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--adopt-existing',action='store_true',help='append/update only the managed instruction block')
    args=parser.parse_args(); project=args.project.resolve()
    try:
        plan=build_plan(project,args.delivery,args.adopt_existing,args.tool)
        apply_plan(project,plan,args.dry_run,args.adopt_existing)
    except (OSError,ValueError) as exc:
        print(f'[harness-init] {exc}',file=sys.stderr); return 2
    return 0

if __name__=='__main__': sys.exit(main())
