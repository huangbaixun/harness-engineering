import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'codex_hook.py'
class HookTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="context ' space "); self.addCleanup(self.tmp.cleanup); self.root=Path(self.tmp.name)
        (self.root/'.harness').mkdir(); (self.root/'docs').mkdir()
        self.config={'schema_version':1,'progress_file':'docs/harness-progress.json','verification_commands':[]}
        self.save()
        (self.root/'features.json').write_text(json.dumps({'features':[{'id':'F007','name':'adapt','status':'building'},{'id':'F001','status':'done'}]}))
    def save(self): (self.root/'.harness/config.json').write_text(json.dumps(self.config))
    def event(self,mode,payload):
        return subprocess.run([sys.executable,str(SCRIPT),mode],input=json.dumps(payload),capture_output=True,text=True)
    def verify(self):
        return subprocess.run([sys.executable,str(SCRIPT),'verify','--project',str(self.root)],capture_output=True,text=True)
    def test_session_features_without_progress(self):
        r=self.event('session-start',{'cwd':str(self.root)}); self.assertEqual(r.returncode,0,r.stderr)
        context=json.loads(r.stdout)['hookSpecificOutput']['additionalContext']; self.assertIn('F007',context); self.assertNotIn('F001',context)
        self.assertLess(len(context),6000)
    def test_default_lifecycle_never_invokes_external_tools(self):
        import shlex
        bin_dir=self.root/'bin'; bin_dir.mkdir(); log=self.root/'external-calls'
        for name in ('gh','git','curl','wget'):
            p=bin_dir/name; p.write_text('#!/bin/sh\nprintf called >> '+shlex.quote(str(log))+'\nexit 93\n'); p.chmod(0o755)
        env={**os.environ,'PATH':str(bin_dir)+os.pathsep+os.environ.get('PATH','')}
        self.config['verification_commands']=[[sys.executable,'-c','pass']]; self.save()
        for mode in ('session-start','stop'):
            r=subprocess.run([sys.executable,str(SCRIPT),mode],input=json.dumps({'cwd':str(self.root)}),env=env,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
        self.assertFalse(log.exists())

    def test_legacy_progress_is_read_only(self):
        p=self.root/'docs/claude-progress.json'; p.write_text(json.dumps({'in_progress':'legacy task','completed_features':[]})); before=p.read_bytes()
        r=self.event('session-start',{'cwd':str(self.root)}); self.assertIn('legacy task',r.stdout); self.assertEqual(p.read_bytes(),before)
    def test_progress_prefers_neutral_file(self):
        (self.root/'docs/harness-progress.json').write_text('{"in_progress":"neutral"}')
        (self.root/'docs/claude-progress.json').write_text('{"in_progress":"legacy"}')
        r=self.event('session-start',{'cwd':str(self.root)}); self.assertIn('neutral',r.stdout); self.assertNotIn('legacy',r.stdout)
    def test_invalid_event_never_echoes_payload(self):
        for payload in ['secret-raw',[],{'cwd':3}]:
            r=self.event('session-start',payload); self.assertNotEqual(r.returncode,0); self.assertNotIn('secret-raw',r.stderr)
    def test_empty_verification_is_not_success(self): self.assertNotEqual(self.verify().returncode,0)
    def test_argv_failure_propagates(self):
        self.config['verification_commands']=[[sys.executable,'-c','raise SystemExit(3)']]; self.save(); self.assertNotEqual(self.verify().returncode,0)
    def test_successful_verify_is_silent(self):
        self.config['verification_commands']=[[sys.executable,'-c','print("fixture noisy")']]; self.save()
        r=self.verify(); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(r.stdout,'')
    def test_shell_text_is_rejected(self):
        self.config['verification_commands']=['echo okay']; self.save(); self.assertNotEqual(self.verify().returncode,0)
    def test_progress_path_must_stay_in_project(self):
        self.config['progress_file']='../outside.json'; self.save(); r=self.event('session-start',{'cwd':str(self.root)}); self.assertNotEqual(r.returncode,0)
    def test_stop_failure_blocks_once(self):
        r=self.event('stop',{'cwd':str(self.root),'stop_hook_active':False}); self.assertEqual(json.loads(r.stdout)['decision'],'block')
        r=self.event('stop',{'cwd':str(self.root),'stop_hook_active':True}); self.assertNotIn('decision',json.loads(r.stdout)); self.assertIn('systemMessage',json.loads(r.stdout))
    def test_pretool_is_explicitly_unsupported(self):
        r=self.event('pre-tool',{'cwd':str(self.root),'tool_name':'unknown'}); self.assertNotEqual(r.returncode,0); self.assertIn('not registered',r.stderr)
    def test_invalid_progress_fails_visibly(self):
        (self.root/'docs/harness-progress.json').write_text('{'); r=self.event('session-start',{'cwd':str(self.root)}); self.assertNotEqual(r.returncode,0)

if __name__=='__main__': unittest.main()
