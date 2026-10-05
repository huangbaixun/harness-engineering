import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'sync-superpowers.sh'
class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='sync space '); self.addCleanup(self.tmp.cleanup); self.root=Path(self.tmp.name)
        self.cache=self.root/'cache'; self.vendor=self.root/'skills'; (self.vendor/'test').mkdir(parents=True)
        (self.vendor/'test/SKILL.md').write_text('---\nname: harness:test\ndescription: fixture\n---\nlocal\n')
        for version in ('6.3.0','6.4.1','6.10.0'):
            p=self.cache/version/'skills/test'; p.mkdir(parents=True); (p/'SKILL.md').write_text('---\nname: test\ndescription: fixture\n---\nupstream\n'); (p/'helper.txt').write_text('helper')
    def run_sync(self):
        return subprocess.run(['bash',str(SCRIPT)],cwd=self.root,env={**os.environ,'CACHE_BASE':str(self.cache),'SKILLS_DIR':str(self.vendor)},capture_output=True,text=True)
    def test_numeric_selection_and_read_only(self):
        before=(self.vendor/'test/SKILL.md').read_bytes(); r=self.run_sync()
        self.assertEqual(r.returncode,0,r.stderr); self.assertIn('6.10.0',r.stdout)
        self.assertIn('helper.txt',r.stdout); self.assertEqual(before,(self.vendor/'test/SKILL.md').read_bytes())
    def test_no_cache_is_visible_failure(self):
        r=subprocess.run(['bash',str(SCRIPT)],env={**os.environ,'CACHE_BASE':str(self.root/'missing')},capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0); self.assertIn('cache',r.stderr)
    def test_explicit_version_limits_comparison(self):
        r=subprocess.run(['bash',str(SCRIPT),'--version','6.4.1'],cwd=self.root,env={**os.environ,'CACHE_BASE':str(self.cache),'SKILLS_DIR':str(self.vendor)},capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr); self.assertIn('6.4.1',r.stdout); self.assertNotIn('6.10.0',r.stdout)

if __name__=='__main__': unittest.main()
