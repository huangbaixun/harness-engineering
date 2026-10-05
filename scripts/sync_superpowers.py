#!/usr/bin/env python3
"""Report exact upstream differences without modifying any source."""
import argparse
import difflib
import os
import re
import sys
from pathlib import Path


def normal_body(path):
    body=path.read_text()
    front=body.split('---',2)
    if len(front)==3:
        front[1]=re.sub(r'(?m)^name:.*$', 'name: upstream', front[1], count=1)
        body='---'.join(front)
    body=re.sub(r'(?m)^> \*\*harness local rules:\*\*[^\n]*\n\n', '', body)
    body=re.sub(r'(?m)^> harness local rules:[^\n]*\n\n', '', body)
    return body.splitlines(keepends=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version')
    parser.add_argument('--source',type=Path,help='fixed upstream checkout root')
    args=parser.parse_args()
    vendor=Path(os.environ.get('SKILLS_DIR','skills'))
    if args.source:
        upstream=args.source/'skills'; label=str(args.source)
    else:
        explicit=os.environ.get('CACHE_BASE')
        caches=[Path(explicit)] if explicit else [Path.home()/'.claude/plugins/cache/claude-plugins-official/superpowers',Path.home()/'.codex/plugins/cache/claude-plugins-official/superpowers']
        versions=[]
        for cache in caches:
            if not cache.is_dir(): continue
            for path in cache.iterdir():
                if re.fullmatch(r'\d+\.\d+\.\d+',path.name) and (path/'skills').is_dir() and (not args.version or path.name==args.version):
                    versions.append((tuple(int(v) for v in path.name.split('.')),path))
        if not versions:
            print('[sync-superpowers] no matching installed cache/version',file=sys.stderr); return 1
        _,chosen=max(versions,key=lambda item:(item[0],str(item[1]))); upstream=chosen/'skills'; label=chosen.name
    if not upstream.is_dir() or not vendor.is_dir():
        print('[sync-superpowers] upstream/vendor skills directory missing',file=sys.stderr); return 1
    print(f'Comparing vendored skills against superpowers {label}')
    matched=0
    for local in sorted(vendor.iterdir()):
        if not (local/'UPSTREAM.md').is_file() and not (upstream/local.name).is_dir(): continue
        remote=upstream/local.name
        if not remote.is_dir(): print(f'[{local.name}] MISSING upstream skill'); continue
        matched+=1
        if not (local/'SKILL.md').is_file() or not (remote/'SKILL.md').is_file():
            print(f'[{local.name}] missing SKILL.md'); continue
        delta=list(difflib.unified_diff(normal_body(local/'SKILL.md'),normal_body(remote/'SKILL.md')))
        print(f'[{local.name}] diff-lines={len(delta)}')
        remote_files={p.relative_to(remote) for p in remote.rglob('*') if p.is_file() and p.name!='SKILL.md'}
        local_files={p.relative_to(local) for p in local.rglob('*') if p.is_file() and p.name not in ('SKILL.md','harness-delta.md','UPSTREAM.md') and 'evals' not in p.relative_to(local).parts and '__pycache__' not in p.parts}
        for rel in sorted(remote_files|local_files):
            if rel not in remote_files: print(f'  companion GONE upstream: {rel}')
            elif rel not in local_files: print(f'  companion MISSING locally: {rel}')
            elif (local/rel).read_bytes()!=(remote/rel).read_bytes(): print(f'  companion CHANGED upstream: {rel}')
    if not matched:
        print('[sync-superpowers] no corresponding vendored skills',file=sys.stderr); return 1
    print('Read-only report; review each skill and provenance before accepting changes.')
    return 0

if __name__=='__main__': sys.exit(main())
