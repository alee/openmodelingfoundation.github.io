"""Exercise real Hugo publication and content preparation in disposable workspaces."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import unittest

ROOT = Path.cwd()



class ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(['hugo', 'config', '--format', 'json', '--quiet'], cwd=ROOT,
                                env=dict(os.environ, HUGO_CACHEDIR=str(ROOT / '.hugo_cache')),
                                capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        config = json.loads(result.stdout)
        cache = {key.lower(): value for key, value in config['caches']['getresource'].items()}
        cls.resource_cache_max_age = cache['maxage']


    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.site = self.root / 'site'
        self.output = self.root / 'public'
        (self.site / 'layouts/partials').mkdir(parents=True)
        for name in ('render-remote-readme.html',):
            shutil.copy2(ROOT / 'layouts/partials' / name, self.site / 'layouts/partials' / name)
        self.config = {'baseURL': 'https://example.org/preview/',
                       'disableKinds': ['taxonomy', 'term', 'RSS', 'sitemap'],
                       'security': {'http': {'urls': [r'^http://127\.0\.0\.1:']}},
                       'caches': {'getresource': {'maxAge': self.resource_cache_max_age}}}
        self.responses = {'/prompt.md': (200, b'# Prompt\r\n\r\nUnicode: \xc3\xa9\n')}
        self.requests = []
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.requests.append(self.path)
                status, content = owner.responses.get(self.path, (404, b'not found'))
                self.send_response(status)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Cache-Control', 'max-age=86400')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}'


    def render(self, template, local=False):
        (self.site / 'hugo.json').write_text(json.dumps(self.config))
        (self.site / 'layouts/home.html').write_text(template)
        env = dict(os.environ, HUGO_OPEN_SCIENCE_LOCAL='1' if local else '')
        result = subprocess.run(['hugo', '--source', str(self.site), '--destination', str(self.output),
                                 '--cacheDir', str(self.root / 'cache')], env=env,
                                capture_output=True, text=True, timeout=30)
        return result


    def test_awesome_refetches_per_build_and_falls_back_after_failure(self):
        def readme(label):
            return f'# Title\n\n{label}\n\n## Papers\n<!-- OMF:PUBLICATIONS:START -->\nold papers\n<!-- OMF:PUBLICATIONS:END -->\n'.encode()
        self.responses['/README.md'] = (200, readme('First revision'))
        call = ('{{ $r := partialCached "render-remote-readme.html" '
                f'(dict "sourceRepo" "https://example.org" "rawURL" "{self.url}/README.md" '
                '"blobRoot" "https://example.org/" "rawRoot" "https://example.org/" '
                '"opts" (dict "timeout" "2s") "pubs" "Bibliography fallback") "readme" }}'
                '{{ if $r.warning }}<strong>{{ $r.warning }}</strong>Bibliography fallback'
                '{{ else }}{{ $r.rendered | safeHTML }}{{ end }}')
        # Repeated calls in one render must not refetch; later renders must.
        template = call + call
        result = self.render(template)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.requests.count('/README.md'), 1)
        self.responses['/README.md'] = (200, readme('Second revision'))
        self.assertEqual(self.render(template).returncode, 0)
        self.assertIn('Second revision', (self.output / 'index.html').read_text())
        self.assertNotIn('First revision', (self.output / 'index.html').read_text())
        self.responses['/README.md'] = (404, b'unavailable')
        self.assertEqual(self.render(template).returncode, 0)
        page = (self.output / 'index.html').read_text()
        self.assertIn('Live list unavailable', page)
        self.assertIn('Bibliography fallback', page)
        self.assertNotIn('Second revision', page)
        self.assertEqual(self.requests.count('/README.md'), 3)


if __name__ == '__main__':
    unittest.main()
