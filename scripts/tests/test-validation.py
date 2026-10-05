import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / 'validate.py'

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ['LICENSE','README.md','CONTRIBUTING.md','CHANGELOG.md']:
            (self.root/name).write_text('fixture\n')
        for name, data in [('.claude-plugin/plugin.json', {'name':'harness','version':'1','description':'fixture','license':'MIT'}), ('hooks/hooks.json', {'hooks':{}})]:
            target=self.root/name; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(data))
        for name in ['using-harness','init','audit','evolve']:
            target=self.root/'skills'/name/'SKILL.md'; target.parent.mkdir(parents=True)
            target.write_text(f'---\nname: harness:{name}\ndescription: fixture\n---\n')
    def run_validator(self):
        return subprocess.run([sys.executable,str(VALIDATOR),'--structure-only','--root',str(self.root)],capture_output=True,text=True)
    def test_valid_project_passes(self):
        r=self.run_validator(); self.assertEqual(r.returncode,0,r.stderr)
    def test_missing_skill_fails(self):
        (self.root/'skills/using-harness/SKILL.md').unlink()
        r=self.run_validator(); self.assertNotEqual(r.returncode,0); self.assertIn('skills/using-harness/SKILL.md',r.stderr)
    def test_invalid_json_fails(self):
        (self.root/'.claude-plugin/plugin.json').write_text('{')
        r=self.run_validator(); self.assertNotEqual(r.returncode,0); self.assertIn('plugin.json',r.stderr)
    def test_broken_shell_fails(self):
        target=self.root/'scripts/bad.sh'; target.parent.mkdir(); target.write_text('#!/bin/bash\nif then\n')
        self.assertNotEqual(self.run_validator().returncode,0)

if __name__=='__main__': unittest.main()
