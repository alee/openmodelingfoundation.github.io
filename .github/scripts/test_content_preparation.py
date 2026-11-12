"""Verify bibliography regeneration after workspace mounts are applied."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class PreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_bibliography_preparation_replaces_stale_mounted_data(self):
        bib = self.root / 'publications.bib'
        output = self.root / 'data/publications.json'
        output.parent.mkdir()
        output.write_text('[{"key":"stale"}]')
        bib.write_text('@article{fresh, title={Fresh source}, author={Doe, Jane}, year={2026}}\n')
        env = dict(os.environ, PUBLICATIONS_BIB_PATH=str(bib), PUBLICATIONS_JSON_PATH=str(output))
        command = ['sh', '.github/scripts/prepare-content.sh']
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([entry['key'] for entry in json.loads(output.read_text())], ['fresh'])
        output.unlink()
        self.assertEqual(subprocess.run(command, env=env, capture_output=True, timeout=60).returncode, 0)
        self.assertTrue(output.exists())
        bib.unlink()
        marker = self.root / 'server-started'
        fake_bin = self.root / 'bin'
        fake_bin.mkdir()
        fake_hugo = fake_bin / 'hugo'
        fake_hugo.write_text(f'#!/bin/sh\ntouch "{marker}"\n')
        fake_hugo.chmod(0o755)
        env['PATH'] = str(fake_bin) + os.pathsep + env['PATH']
        result = subprocess.run(['sh', '.github/scripts/serve-site.sh'], env=env,
                                capture_output=True, timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists(), 'server started after failed content preparation')



if __name__ == '__main__':
    unittest.main()
