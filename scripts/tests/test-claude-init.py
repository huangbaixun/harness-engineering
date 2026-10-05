import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class ClaudeInit(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="claude space ' "); self.addCleanup(self.tmp.cleanup); self.project=Path(self.tmp.name)/'project'; self.project.mkdir()
    def init(self,*args): return subprocess.run([sys.executable,str(ROOT/'scripts/harness_init.py'),'--tool','claude','--project',str(self.project),*args],capture_output=True,text=True)
    def test_adoption_preserves_instructions_and_permission_bytes(self):
        original=b'User rules\r\n  \r\n'; (self.project/'CLAUDE.md').write_bytes(original)
        (self.project/'.claude').mkdir(); settings=self.project/'.claude/settings.json'; settings.write_text('{"permissions":{"deny":["Bash(curl *)"]}}\n'); before=settings.read_bytes()
        r=self.init('--adopt-existing'); self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue((self.project/'CLAUDE.md').read_bytes().startswith(original)); self.assertEqual(settings.read_bytes(),before)
        self.assertFalse((self.project/'AGENTS.md').exists())
        config=json.loads((self.project/'.harness/config.json').read_text()); self.assertEqual(config['tool'],'claude'); self.assertEqual(config['verification_commands'],[])
        self.assertTrue((self.project/'.claude/skills/executing-plans/scripts/task-start').is_file())
        r=self.init('--adopt-existing'); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(json.loads(r.stdout)['changes'],[])
        runtime=self.project/'.claude/harness/scripts/claude_hook.py'
        r=subprocess.run([sys.executable,str(runtime),'session-start'],input=json.dumps({'cwd':str(self.project)}),capture_output=True,text=True); self.assertEqual(r.returncode,0,r.stderr)
    def test_existing_conflict_writes_nothing(self):
        (self.project/'CLAUDE.md').write_text('keep'); r=self.init(); self.assertEqual(r.returncode,2); self.assertEqual(sorted(p.name for p in self.project.iterdir()),['CLAUDE.md'])
    def test_plugin_delivery_copies_no_runtime_or_permissions(self):
        r=self.init('--delivery','plugin'); self.assertEqual(r.returncode,0,r.stderr); self.assertFalse((self.project/'.claude').exists()); self.assertIn('installed plugin root',(self.project/'CLAUDE.md').read_text())
    def test_dry_run_zero_writes(self):
        self.assertEqual(self.init('--dry-run').returncode,0); self.assertEqual(list(self.project.iterdir()),[])
if __name__=='__main__': unittest.main()
