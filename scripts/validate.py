#!/usr/bin/env python3
"""Offline structural validation and regression runner (Python standard library)."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def validate(root):
    errors=[]
    required=['.claude-plugin/plugin.json','hooks/hooks.json','LICENSE','README.md','CONTRIBUTING.md','CHANGELOG.md']
    required += [f'skills/{name}/SKILL.md' for name in ('using-harness','init','audit','evolve')]
    for name in required:
        if not (root/name).is_file(): errors.append(f'MISSING: {name}')
    paths=list(root.glob('skills/*/evals/evals.json'))+list(root.glob('commands/evals/evals.json'))
    paths += [root/name for name in ('plugin.json','.claude-plugin/plugin.json','.codex-plugin/plugin.json','hooks/hooks.json','hooks/codex.json','features.json') if (root/name).exists()]
    for path in paths:
        try:
            data=json.loads(path.read_text())
            if not isinstance(data,dict): raise ValueError('expected JSON object')
            if path.name=='plugin.json':
                for field in ('name','version','description'):
                    if not isinstance(data.get(field),str) or not data[field]: raise ValueError(f'missing {field}')
            if path.name=='evals.json':
                if not isinstance(data.get('evals'),list): raise ValueError('missing evals array')
                for case in data['evals']:
                    if not all(k in case for k in ('id','prompt','expected_output','assertions')): raise ValueError('incomplete eval')
            if path.parent.name=='hooks' and not isinstance(data.get('hooks'),dict): raise ValueError('missing hooks object')
        except (OSError,ValueError) as exc: errors.append(f'{path.relative_to(root)}: {exc}')
    manifests=[]
    for name in ('plugin.json','.claude-plugin/plugin.json','.codex-plugin/plugin.json'):
        path=root/name
        if not path.exists(): continue
        try:
            manifest=json.loads(path.read_text())
            manifests.append((name,manifest.get('name'),manifest.get('version')))
            if name=='plugin.json':
                extension=manifest.get('extensions',{}).get('com.openai')
                if not isinstance(extension,dict) or not extension.get('hooks'):
                    raise ValueError('explicit OpenAI hooks override required; do not fall back to Claude hooks')
                for field,value in (('skills',manifest.get('skills')),('hooks',extension['hooks'])):
                    if not isinstance(value,str) or not value.startswith('./'):
                        raise ValueError(f'{field} must be an explicit ./ relative path')
                    target=(root/value).resolve()
                    if not target.is_relative_to(root) or not target.exists():
                        raise ValueError(f'{field} path missing or escapes plugin root')
                hook_data=json.loads((root/extension['hooks']).read_text())
                if not isinstance(hook_data,dict) or not isinstance(hook_data.get('hooks'),dict):
                    raise ValueError('OpenAI hooks target must contain a hooks object')
        except (OSError,ValueError,AttributeError) as exc: errors.append(f'{name}: {exc}')
    if len({(name,version) for _,name,version in manifests})>1:
        errors.append('plugin manifest identities/versions disagree')
    for path in root.glob('skills/*/SKILL.md'):
        body=path.read_text()
        front=body.split('---',2)
        if len(front)!=3 or front[0].strip() or not all(f'{key}:' in front[1] for key in ('name','description')):
            errors.append(f'{path.relative_to(root)}: missing skill frontmatter')
    for path in root.glob('scripts/*.sh'):
        r=subprocess.run(['bash','-n',str(path)],capture_output=True,text=True)
        if r.returncode: errors.append(f'{path.relative_to(root)}: {r.stderr.strip()}')
    for err in errors: print(err,file=sys.stderr)
    return not errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--structure-only',action='store_true')
    args=parser.parse_args(); root=args.root.resolve()
    if not validate(root): return 1
    print('PASS structure',flush=True)
    if args.structure_only: return 0
    tests=sorted(list(root.glob('scripts/tests/test-*.sh'))+list(root.glob('scripts/tests/test-*.py')))
    if not tests:
        print('FAIL: no regression files discovered',file=sys.stderr); return 1
    failed=[]
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    for path in tests:
        command=['bash' if path.suffix=='.sh' else sys.executable,str(path)]
        try: result=subprocess.run(command,cwd=root,env=env,timeout=120)
        except subprocess.TimeoutExpired:
            failed.append(path.name); print(f'FAIL timeout: {path.name}',file=sys.stderr); continue
        if result.returncode: failed.append(path.name)
    print(f'{len(tests)-len(failed)}/{len(tests)} regression files passed',flush=True)
    if failed: print('FAIL: '+', '.join(failed),file=sys.stderr)
    return int(bool(failed))

if __name__=='__main__': sys.exit(main())
