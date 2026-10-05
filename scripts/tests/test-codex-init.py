import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/'harness_init.py'
class InitTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="harness space ' "); self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name)/'project'; self.project.mkdir()
    def init(self,*args):
        return subprocess.run([sys.executable,str(SCRIPT),'--tool','codex','--project',str(self.project),*args],capture_output=True,text=True)
    def test_dry_run_writes_nothing(self):
        r=self.init('--dry-run'); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(list(self.project.iterdir()),[])
    def test_existing_rules_conflict_is_atomic(self):
        p=self.project/'AGENTS.md'; p.write_text('original\n'); r=self.init()
        self.assertEqual(r.returncode,2); self.assertEqual(p.read_text(),'original\n'); self.assertFalse((self.project/'.harness').exists())
    def test_repeated_initialization_is_noop(self):
        r=self.init(); self.assertEqual(r.returncode,0,r.stderr)
        before={str(p.relative_to(self.project)):p.read_bytes() for p in self.project.rglob('*') if p.is_file()}
        r=self.init(); self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(before,{str(p.relative_to(self.project)):p.read_bytes() for p in self.project.rglob('*') if p.is_file()})
        config=json.loads((self.project/'.harness/config.json').read_text())
        self.assertIs(config['auto_commit'],False); self.assertIs(config['github_sync'],False)
        self.assertEqual(config['verification_commands'],[])
        skill=self.project/'.agents/skills/harness-using-harness/SKILL.md'
        self.assertTrue(skill.is_file()); self.assertTrue((self.project/'.agents/harness/scripts/validate.py').is_file())
    def test_bundled_initializer_can_initialize_another_project(self):
        r=self.init(); self.assertEqual(r.returncode,0,r.stderr)
        bundled=self.project/'.agents/harness/scripts/harness_init.py'
        other=Path(self.tmp.name)/'other'
        r=subprocess.run([sys.executable,str(bundled),'--tool','codex','--project',str(other)],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue((other/'.agents/skills/harness-using-harness/SKILL.md').is_file())
        self.assertTrue((other/'.agents/harness/third_party/superpowers/LICENSE').is_file())

    def test_plugin_delivery_has_no_duplicate_project_skills(self):
        r=self.init('--delivery','plugin'); self.assertEqual(r.returncode,0,r.stderr)
        self.assertFalse((self.project/'.agents/skills').exists())
        self.assertNotEqual(self.init('--delivery','project').returncode,0)
    def test_explicit_adoption_retains_rules(self):
        p=self.project/'AGENTS.md'; p.write_text('original rules\n')
        r=self.init('--adopt-existing'); self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(p.read_text().startswith('original rules\n'))
        before=p.read_bytes(); self.assertEqual(self.init('--adopt-existing').returncode,0); self.assertEqual(before,p.read_bytes())
    def test_adoption_preserves_all_original_bytes(self):
        original=b'original rules\n\n  \n'
        p=self.project/'AGENTS.md'; p.write_bytes(original)
        r=self.init('--adopt-existing'); self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(p.read_bytes().startswith(original))

    def test_symlink_destination_is_rejected(self):
        outside=Path(self.tmp.name)/'outside'; outside.mkdir()
        (self.project/'.agents').symlink_to(outside,target_is_directory=True)
        r=self.init(); self.assertEqual(r.returncode,2); self.assertEqual(list(outside.iterdir()),[])

if __name__=='__main__': unittest.main()
