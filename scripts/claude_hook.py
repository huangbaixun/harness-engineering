#!/usr/bin/env python3
"""Claude stdin protocol adapter. Direct-path guard supplements native permissions only."""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from harness_runtime import config_for, contained, read_object, render_context, run_verification


def read_event(mode):
    raw=sys.stdin.read()
    if not raw.strip() and mode=='session-start' and os.environ.get('CLAUDE_PROJECT_DIR'):
        return {'cwd':os.environ['CLAUDE_PROJECT_DIR']}
    try: event=json.loads(raw)
    except ValueError: raise ValueError('malformed hook event JSON') from None
    if not isinstance(event,dict): raise ValueError('hook event must be an object')
    return event


def protect(project,event):
    # No shell parsing, command approval or purported universal access barrier.
    if event.get('tool_name') not in ('Read','Write','Edit'): return 0
    inputs=event.get('tool_input')
    if not isinstance(inputs,dict): raise ValueError('direct-file event requires tool_input')
    value=inputs.get('file_path')
    if not isinstance(value,str) or not value or '\x00' in value: raise ValueError('direct-file event requires file_path')
    path=Path(value); path=path if path.is_absolute() else project/path
    for candidate in (path,path.resolve()):
        name=candidate.name
        if name=='.env' or (name.startswith('.env.') and name not in ('.env.example','.env.sample','.env.template')) or name in ('id_rsa','id_ed25519','credentials.json'):
            print('[harness-protect] direct access to a recognized secret filename is blocked; use native permissions for other access',file=sys.stderr)
            return 2
    return 0


def observe(project,event):
    enabled=config_for(project).get('telemetry_enabled',False)
    if not isinstance(enabled,bool): raise ValueError('telemetry_enabled must be boolean')
    if not enabled: return 0
    # Never persist raw input, session identifiers, outputs, arguments or inferred cost.
    tool=event.get('tool_name')
    allowed={'Read','Write','Edit','Bash','Grep','Glob','Task','Agent'}
    record={'schema_version':1,'timestamp':datetime.now(timezone.utc).isoformat(),
            'host':'claude','event':'PostToolUse','tool':tool if isinstance(tool,str) and tool in allowed else 'other',
            'duration_ms':None,'total_tokens':None,'cost_usd':None,'measurement':'event-only'}
    path=contained(project,'.harness/telemetry.jsonl'); path.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
    try: os.write(fd,(json.dumps(record)+'\n').encode('utf-8'))
    finally: os.close(fd)
    return 0


def sync_if_enabled(project):
    features=contained(project,'features.json')
    if not features.exists(): features=contained(project,'docs/features.json')
    if not features.exists(): return
    github=read_object(features).get('github',{})
    if not isinstance(github,dict) or github.get('enabled') is not True: return
    try:
        result=subprocess.run([sys.executable,str(Path(__file__).with_name('harness_sync.py')),'pull','--timeout','5'],cwd=project,capture_output=True,text=True,timeout=6)
        if result.stderr: print('[harness-sync] optional pull reported a problem; inspect explicit sync diagnostics',file=sys.stderr)
    except (OSError,subprocess.TimeoutExpired): print('[harness-sync] optional pull skipped; use local state',file=sys.stderr)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('session-start','stop','protect','observe'))
    args=parser.parse_args()
    try:
        event=read_event(args.mode)
        if not isinstance(event.get('cwd'),str) or not event['cwd']: raise ValueError('hook event requires string cwd')
        project=Path(event['cwd']).resolve()
        if not project.is_dir(): raise ValueError('hook project directory does not exist')
        if args.mode=='protect': return protect(project,event)
        if args.mode=='observe': return observe(project,event)
        if args.mode=='session-start':
            sync_if_enabled(project)
            print(json.dumps({'hookSpecificOutput':{'hookEventName':'SessionStart','additionalContext':render_context(project)}},ensure_ascii=False)); return 0
        active=event.get('stop_hook_active',False)
        if not isinstance(active,bool): raise ValueError('stop_hook_active must be boolean')
        if active:
            print(json.dumps({'systemMessage':'Verification already requested once. Inspect the failure; this event does not prove completion.'})); return 0
        result=run_verification(project,config_for(project).get('verification_commands'))
        print(json.dumps({} if result==0 else {'decision':'block','reason':'Harness verification failed or is not configured. Run the configured checks explicitly, inspect and fix failures before claiming completion.'}))
        return 0
    except (OSError,ValueError) as exc:
        print(f'[harness-hook] {exc}',file=sys.stderr); return 2

if __name__=='__main__': sys.exit(main())
