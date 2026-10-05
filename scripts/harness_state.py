#!/usr/bin/env python3
"""Explicit minimal checkpoint for long-running work; preserves legacy files and extension fields."""
import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from codex_hook import config_for, contained, read_object


def write_json_atomic(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=None
    try:
        with tempfile.NamedTemporaryFile('w',dir=path.parent,prefix='.harness-state-',delete=False) as stream:
            temporary=Path(stream.name); json.dump(data,stream,ensure_ascii=False,indent=2); stream.write('\n')
        os.replace(temporary,path)
    finally:
        if temporary is not None and temporary.exists(): temporary.unlink()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['checkpoint'])
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--task',required=True)
    parser.add_argument('--next-action',required=True)
    parser.add_argument('--steering')
    parser.add_argument('--blocker',action='append')
    args=parser.parse_args(); project=args.project.resolve()
    try:
        config=config_for(project); path=contained(project,config.get('progress_file','docs/harness-progress.json'))
        if path.name=='claude-progress.json': raise ValueError('checkpoint uses a neutral progress file; legacy progress is read-only')
        data=read_object(path) if path.exists() else {}
        data.update({'schema_version':1,'in_progress':args.task,'next_action':args.next_action,'updated_at':datetime.now(timezone.utc).isoformat()})
        if args.steering is not None: data['latest_steering']=args.steering
        if args.blocker is not None: data['blockers']=args.blocker
        write_json_atomic(path,data)
    except (OSError,ValueError) as exc:
        print(f'[harness-state] {exc}',file=sys.stderr); return 2
    return 0

if __name__=='__main__': sys.exit(main())
