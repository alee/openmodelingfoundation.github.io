"""Check lockfile updates with image-owned dependencies and failed resolution."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path('.github/scripts/update-npm-lock.sh').resolve()


class LockfileTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'package.json').write_text(json.dumps({
            'name': 'lockfile-fixture', 'version': '1.0.0',
            'workspaces': ['packages/hugoautogen'],
        }))
        workspace = self.root / 'packages/hugoautogen'
        workspace.mkdir(parents=True)
        (workspace / 'package.json').write_text(json.dumps({
            'name': 'workspace-fixture', 'version': '1.0.0', 'private': True,
        }))
        self.lock = self.root / 'package-lock.json'
        self.lock.write_text('{"lockfileVersion": 3, "packages": {}}\n')

    def run_update(self):
        return subprocess.run(['sh', str(SCRIPT)], cwd=self.root,
                              capture_output=True, text=True, timeout=30,
                              env=dict(os.environ, npm_config_offline='true'))

    def test_resolve_workspace_without_writing_installed_dependencies(self):
        installed = self.root / 'node_modules'
        installed.mkdir()
        sentinel = installed / '.package-lock.json'
        sentinel.write_text('installed tree must remain unchanged\n')
        sentinel.chmod(0o444)
        installed.chmod(0o555)
        self.addCleanup(installed.chmod, 0o755)
        result = self.run_update()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(sentinel.read_text(), 'installed tree must remain unchanged\n')
        lock = json.loads(self.lock.read_text())
        self.assertEqual(lock['packages']['node_modules/workspace-fixture']['resolved'],
                         'packages/hugoautogen')
        self.assertTrue(lock['packages']['node_modules/workspace-fixture']['link'])

    def test_failed_resolution_preserves_original_lockfile(self):
        manifest = self.root / 'package.json'
        manifest.write_text('{"name": "broken-manifest",')
        before = self.lock.read_bytes()
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.lock.read_bytes(), before)
        self.assertFalse((self.root / 'node_modules').exists())


if __name__ == '__main__':
    unittest.main()
