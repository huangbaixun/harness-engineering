import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'harness_state.py'
HOOK=Path(__file__).resolve().parents[1]/'codex_hook.py'
class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root=Path(self.tmp.name)
    def checkpoint(self,*args):
        return subprocess.run([sys.executable,str(SCRIPT),'checkpoint','--project',str(self.root),'--task','F007','--next-action','run tests',*args],capture_output=True,text=True)
    def test_checkpoint_retains_extension_and_steering(self):
        (self.root/'docs').mkdir(); p=self.root/'docs/harness-progress.json'; p.write_text('{"team_extension":42}')
        r=self.checkpoint('--steering','support other accelerators'); self.assertEqual(r.returncode,0,r.stderr)
        d=json.loads(p.read_text()); self.assertEqual(d['team_extension'],42); self.assertEqual(d['latest_steering'],'support other accelerators'); self.assertEqual(d['next_action'],'run tests')
    def test_legacy_file_remains_unchanged(self):
        (self.root/'docs').mkdir(); p=self.root/'docs/claude-progress.json'; p.write_text('{"in_progress":"old"}')
        r=self.checkpoint(); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(p.read_text(),'{"in_progress":"old"}')
    def test_malformed_existing_state_not_overwritten(self):
        (self.root/'docs').mkdir(); p=self.root/'docs/harness-progress.json'; p.write_text('{')
        r=self.checkpoint(); self.assertNotEqual(r.returncode,0); self.assertEqual(p.read_text(),'{')
    def test_report_measures_success_without_fabricating_cost(self):
        (self.root/'.harness').mkdir(); (self.root/'.harness/config.json').write_text(json.dumps({'verification_commands':[[sys.executable,'-c','pass']]}))
        r=subprocess.run([sys.executable,str(HOOK),'verify','--project',str(self.root),'--report','.harness/verification.json'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr); d=json.loads((self.root/'.harness/verification.json').read_text()); self.assertTrue(d['success']); self.assertGreaterEqual(d['duration_ms'],0); self.assertIsNone(d['cost_usd']); self.assertIsNone(d['total_tokens'])

if __name__=='__main__': unittest.main()
