#!/usr/bin/env python3
"""Offline, conflict-first Codex project initialization. No global settings or hooks activated."""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BEGIN='<!-- harness:begin -->'
END='<!-- harness:end -->'


def build_plan(project, delivery, adopt_existing=False):
    template=ROOT/'docs/templates/codex'
    rules=(template/'AGENTS.md.template').read_text().replace('{{DELIVERY}}',delivery)
    existing=project/'AGENTS.md'
    if adopt_existing and existing.is_file():
        body=existing.read_text()
        if BEGIN in body or END in body:
            if body.count(BEGIN)!=1 or body.count(END)!=1 or body.index(BEGIN)>body.index(END):
                raise ValueError('AGENTS.md has malformed harness managed markers')
            body=re.sub(re.escape(BEGIN)+'.*?'+re.escape(END),rules.rstrip(),body,flags=re.S)
        else: body=body.rstrip()+'\n\n'+rules
        rules=body
    config=(template/'harness.json.template').read_text().replace('{{DELIVERY}}',delivery)
    plan=[(project/'AGENTS.md',rules.encode()),(project/'.harness/config.json',config.encode())]
    if not (project/'features.json').exists():
        features={'schema_version':'2.1','features':[],'github':{'enabled':False}}
        plan.append((project/'features.json',(json.dumps(features,indent=2)+'\n').encode()))
    if delivery=='project':
        for folder in ('scripts','references','commands','agents','docs/templates','docs/decisions'):
            for path in sorted((ROOT/folder).rglob('*')):
                if not path.is_file() or '__pycache__' in path.parts or path.suffix=='.pyc' or 'tests' in path.parts: continue
                # Claude lifecycle scripts must not be implicitly available as a Codex entrypoint.
                plan.append((project/'.agents/harness'/path.relative_to(ROOT),path.read_bytes()))
        plan.append((project/'.agents/harness/LICENSE',(ROOT/'LICENSE').read_bytes()))
        for path in sorted((ROOT/'skills').rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix=='.pyc': continue
            rel=path.relative_to(ROOT/'skills')
            plan.append((project/'.agents/skills'/('harness-'+rel.parts[0])/Path(*rel.parts[1:]),path.read_bytes()))
    return plan


def apply_plan(project, plan, dry_run=False, adopt_existing=False):
    conflicts=[]
    for target,data in plan:
        for parent in [target,*target.parents]:
            if parent==project: break
            if parent.is_symlink(): conflicts.append(str(parent.relative_to(project))); break
        if target.exists() and (not target.is_file() or target.read_bytes()!=data):
            if not (adopt_existing and target==project/'AGENTS.md' and target.is_file()):
                conflicts.append(str(target.relative_to(project)))
    if conflicts: raise ValueError('conflicting existing paths: '+', '.join(sorted(set(conflicts))))
    changes=[(p,d) for p,d in plan if not p.exists() or p.read_bytes()!=d]
    report={'delivery_files':len(plan),'changes':[str(p.relative_to(project)) for p,_ in changes], 'dry_run':dry_run}
    if not dry_run:
        for target,data in changes:
            target.parent.mkdir(parents=True,exist_ok=True)
            # Exclusive creation for new paths; no silently clobbered files.
            with target.open('wb' if target.exists() else 'xb') as stream: stream.write(data)
    print(json.dumps(report,ensure_ascii=False))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tool',choices=['codex'],required=True)
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--delivery',choices=['project','plugin'],default='project')
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--adopt-existing',action='store_true',help='append/update only the managed AGENTS.md block')
    args=parser.parse_args(); project=args.project.resolve()
    try:
        plan=build_plan(project,args.delivery,args.adopt_existing)
        apply_plan(project,plan,args.dry_run,args.adopt_existing)
    except (OSError,ValueError) as exc:
        print(f'[harness-init] {exc}',file=sys.stderr); return 2
    return 0

if __name__=='__main__': sys.exit(main())
