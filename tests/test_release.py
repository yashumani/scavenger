"""Release integrity and reproducibility regressions."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_release as b
import release_check as r
import simulate


class ReleaseTests(unittest.TestCase):
    def minimal(self,root):
        (root/'release-files.txt').write_text('SKILL.md\n')
        (root/'SKILL.md').write_text('test package')

    def test_reproducible_archive(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();self.minimal(root)
            self.assertEqual(b.build(root,root/'a.zip'),b.build(root,root/'b.zip'))
            self.assertEqual(b.verify(root/'a.zip'),{'scavenger/SKILL.md':b'test package'})

    def test_unlisted_private_file_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();self.minimal(root);(root/'.env').write_text('SYNTHETIC_PRIVATE_CANARY')
            b.build(root,root/'a.zip')
            self.assertEqual(list(b.verify(root/'a.zip')),['scavenger/SKILL.md'])

    def test_archive_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();self.minimal(root);p=root/'a.zip';b.build(root,p)
            before=p.read_bytes()
            with self.assertRaises(FileExistsError):b.build(root,p)
            self.assertEqual(p.read_bytes(),before)

    def test_allowlist_traversal_and_duplicates_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve()
            for entry in ['../outside\n','/absolute\n','x\\y\n','C:/file\n','a\na\n']:
                (root/'release-files.txt').write_text(entry)
                with self.subTest(entry=entry),self.assertRaises(ValueError):b.files(root)

    @unittest.skipUnless(os.name=='posix','POSIX symlink test')
    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();self.minimal(root);(root/'target').write_text('data')
            (root/'SKILL.md').unlink();(root/'SKILL.md').symlink_to(root/'target')
            with self.assertRaises(ValueError):b.build(root,root/'a.zip')

    def test_zip_slip_member_rejected_without_extraction(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('scavenger/../../escape','payload')
            with self.assertRaises(ValueError):b.verify(p)
            self.assertFalse((Path(d)/'escape').exists())

    def test_checksum_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();self.minimal(root);b.build(root,root/'a.zip')
            with zipfile.ZipFile(root/'a.zip') as original,zipfile.ZipFile(root/'bad.zip','w') as changed:
                for info in original.infolist():
                    changed.writestr(info,b'tampered' if info.filename.endswith('SKILL.md') else original.read(info))
            with self.assertRaisesRegex(ValueError,'checksum'):b.verify(root/'bad.zip')

    def test_missing_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('scavenger/SKILL.md','data')
            with self.assertRaisesRegex(ValueError,'Missing manifest'):b.verify(p)

    def test_repository_audit(self):
        self.assertEqual(r.audit(ROOT)['policy_findings'],0)

    def test_own_package_smoke(self):
        result=r.smoke(ROOT)
        self.assertTrue(result['reproducible']);self.assertEqual(result['smoke_commands_passed'],5)
        self.assertFalse(result['agent_host_installation_tested'])

    def test_deterministic_simulations(self):
        result=simulate.run()
        self.assertEqual(result['gate_combinations_checked'],243)
        self.assertEqual(result['invalid_score_mutations_rejected'],1000)
        self.assertEqual(result['agent_runs'],0)

    def test_host_cases_are_not_misrepresented_as_executed(self):
        cases=json.loads((ROOT/'evals/host-cases.json').read_text())
        self.assertEqual(cases['execution_status'],'not-run')
        self.assertEqual(len(cases['cases']),12)


if __name__=='__main__':unittest.main()
