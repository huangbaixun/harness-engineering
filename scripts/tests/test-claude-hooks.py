import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class ClaudeHooks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.project=Path(self.tmp.name)
        (self.project/'.harness').mkdir()
    def event(self,mode,extra=None):
        return subprocess.run([sys.executable,str(ROOT/'scripts/claude_hook.py'),mode],input=json.dumps({'cwd':str(self.project),**(extra or {})}),text=True,capture_output=True)
    def config(self,**values): (self.project/'.harness/config.json').write_text(json.dumps(values))
    def test_no_default_auto_commit_or_empty_formatter(self):
        hooks=json.loads((ROOT/'hooks/hooks.json').read_text())
        commands=[h['command'] for groups in hooks['hooks'].values() for group in groups for h in group['hooks']]
        self.assertFalse(any('stop-commit-progress' in c or 'post-format' in c or 'post-observe' in c for c in commands))
    def test_stop_runs_real_checks_and_blocks_failure(self):
        for exit_code in (0,7):
            self.config(verification_commands=[[sys.executable,'-c',f'raise SystemExit({exit_code})']])
            r=self.event('stop'); self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(json.loads(r.stdout).get('decision'),None if exit_code==0 else 'block')
    def test_unconfigured_stop_not_passed(self):
        r=self.event('stop'); self.assertEqual(json.loads(r.stdout)['decision'],'block')
    def test_stop_does_not_loop(self):
        r=self.event('stop',{'stop_hook_active':True}); self.assertEqual(r.returncode,0,r.stderr); self.assertNotIn('decision',json.loads(r.stdout))
    def test_checkpoint_context_is_shared_and_bounded(self):
        (self.project/'docs').mkdir(); (self.project/'docs/harness-progress.json').write_text('{"in_progress":"neutral","next_action":"continue"}')
        r=self.event('session-start'); self.assertEqual(r.returncode,0,r.stderr)
        context=json.loads(r.stdout)['hookSpecificOutput']['additionalContext']; self.assertIn('neutral',context); self.assertLess(len(context),6000); self.assertNotIn('EXTREMELY_IMPORTANT',context)
    def test_direct_secret_path_blocked_but_example_allowed(self):
        for name,expected in (('.env',2),('.env.production',2),('.env.example',0),('main.py',0)):
            r=self.event('protect',{'tool_name':'Write','tool_input':{'file_path':str(self.project/name)}}); self.assertEqual(r.returncode,expected,r.stderr)
    def test_malformed_event_fails_without_echo(self):
        r=subprocess.run([sys.executable,str(ROOT/'scripts/claude_hook.py'),'protect'],input='{secret',capture_output=True,text=True)
        self.assertEqual(r.returncode,2); self.assertNotIn('{secret',r.stderr)
    def test_telemetry_off_by_default_and_explicit_opt_in(self):
        r=self.event('observe',{'session_id':'s','tool_name':'Read'}); self.assertEqual(r.returncode,0,r.stderr); self.assertFalse((self.project/'.harness/telemetry.jsonl').exists())
        self.config(telemetry_enabled=True)
        r=self.event('observe',{'session_id':'s','tool_name':'Read','tool_input':{'content':'DO_NOT_LOG'}}); self.assertEqual(r.returncode,0,r.stderr)
        line=(self.project/'.harness/telemetry.jsonl').read_text(); self.assertNotIn('DO_NOT_LOG',line); data=json.loads(line); self.assertIsNone(data['cost_usd']); self.assertIsNone(data['total_tokens'])
    def test_legacy_issue_pull_is_opt_in_without_network(self):
        from unittest.mock import patch
        sys.path.insert(0,str(ROOT/'scripts'))
        import claude_hook
        (self.project/'docs').mkdir()
        (self.project/'docs/features.json').write_text('{"github":{"enabled":true},"features":[]}')
        with patch('claude_hook.subprocess.run') as run:
            run.return_value.stderr=''
            claude_hook.sync_if_enabled(self.project.resolve())
            run.assert_called_once()
        (self.project/'features.json').write_text('{"github":{"enabled":false},"features":[]}')
        with patch('claude_hook.subprocess.run') as run:
            claude_hook.sync_if_enabled(self.project.resolve()); run.assert_not_called()
    def test_compat_cmd_bash_path_preserves_hook_protocol(self):
        self.config(verification_commands=[[sys.executable,'-c','raise SystemExit(7)']])
        r=subprocess.run(['bash',str(ROOT/'scripts/stop-typecheck.cmd')],input=json.dumps({'cwd':str(self.project)}),capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(json.loads(r.stdout)['decision'],'block')
    def test_retired_commit_keeps_user_index_and_head(self):
        def git(*args): return subprocess.check_output(['git',*args],cwd=self.project,text=True).strip()
        git('init','-q'); git('config','user.name','Fixture'); git('config','user.email','fixture@example.invalid')
        (self.project/'base').write_text('base'); git('add','base'); git('commit','-qm','base')
        (self.project/'user-work').write_text('staged'); git('add','user-work'); before=(git('rev-parse','HEAD'),git('diff','--cached'))
        r=subprocess.run(['bash',str(ROOT/'scripts/stop-commit-progress')],cwd=self.project,env={**os.environ,'CLAUDE_PROJECT_DIR':str(self.project)},capture_output=True,text=True)
        self.assertEqual((git('rev-parse','HEAD'),git('diff','--cached')),before); self.assertIn('retired',r.stderr)
if __name__=='__main__': unittest.main()
