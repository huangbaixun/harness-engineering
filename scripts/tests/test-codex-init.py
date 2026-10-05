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
        skill=self.project/'.agents/skills/using-harness/SKILL.md'
        self.assertTrue(skill.is_file()); self.assertTrue((self.project/'.agents/harness/scripts/validate.py').is_file())
    def test_bundled_initializer_can_initialize_another_project(self):
        r=self.init(); self.assertEqual(r.returncode,0,r.stderr)
        bundled=self.project/'.agents/harness/scripts/harness_init.py'
        other=Path(self.tmp.name)/'other'
        r=subprocess.run([sys.executable,str(bundled),'--tool','codex','--project',str(other)],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue((other/'.agents/skills/using-harness/SKILL.md').is_file())
        self.assertTrue((other/'.agents/harness/third_party/superpowers/LICENSE').is_file())

    def test_native_helpers_keep_layout_and_executable_modes(self):
        r=self.init(); self.assertEqual(r.returncode,0,r.stderr)
        helper=self.project/'.agents/skills/executing-plans/scripts/task-start'
        sibling=self.project/'.agents/skills/subagent-driven-development/scripts/task-brief'
        self.assertTrue(sibling.is_file())
        import os
        self.assertTrue(os.access(helper,os.X_OK))
        r=subprocess.run([str(helper)],capture_output=True,text=True)
        self.assertEqual(r.returncode,2); self.assertIn('usage:',r.stderr)
        subprocess.run(['git','init','-q',str(self.project)],check=True,capture_output=True)
        subprocess.run(['git','-C',str(self.project),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--allow-empty','-qm','fixture'],check=True,capture_output=True)
        plan=self.project/'plan.md'; plan.write_text('# Plan\n### Task 1: fixture\nRun checks.\n')
        r=subprocess.run([str(helper),str(plan),'1'],cwd=self.project,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr); self.assertIn('base:',r.stdout)
        base=subprocess.check_output(['git','-C',str(self.project),'rev-parse','HEAD'],text=True).strip()
        done=helper.parent/'task-done'
        r=subprocess.run([str(done),str(plan),'1',base,'--',sys.executable,'-c','print("passed")'],cwd=self.project,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr); self.assertIn('Task 1: complete',r.stdout)


    def test_regular_file_ancestor_conflict_writes_nothing(self):
        (self.project/'.agents').write_text('keep')
        r=self.init(); self.assertEqual(r.returncode,2)
        self.assertEqual(sorted(p.name for p in self.project.iterdir()),['.agents'])

    def test_plugin_rules_reference_plugin_runtime(self):
        r=self.init('--delivery','plugin'); self.assertEqual(r.returncode,0,r.stderr)
        rules=(self.project/'AGENTS.md').read_text()
        self.assertNotIn('python3 .agents/harness/',rules)
        self.assertIn('installed plugin root',rules)

    def test_reinitialization_preserves_custom_verification(self):
        self.assertEqual(self.init().returncode,0)
        p=self.project/'.harness/config.json'; d=json.loads(p.read_text())
        d['verification_commands']=[[sys.executable,'-m','unittest']];d['custom_extension']=42
        p.write_text(json.dumps(d,indent=2)+'\n');before=p.read_bytes()
        r=self.init();self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(p.read_bytes(),before)

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
        original=b'original rules\r\n\r\n  \r\n'
        p=self.project/'AGENTS.md'; p.write_bytes(original)
        r=self.init('--adopt-existing'); self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(p.read_bytes().startswith(original))

    def test_symlink_destination_is_rejected(self):
        outside=Path(self.tmp.name)/'outside'; outside.mkdir()
        (self.project/'.agents').symlink_to(outside,target_is_directory=True)
        r=self.init(); self.assertEqual(r.returncode,2); self.assertEqual(list(outside.iterdir()),[])

if __name__=='__main__': unittest.main()
