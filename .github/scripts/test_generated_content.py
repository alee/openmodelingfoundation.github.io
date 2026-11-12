"""Exercise real Hugo publication and content preparation in disposable workspaces."""
import hashlib
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
NAMES = [f'open-science-{name}.md' for name in ('agent', 'audit-report', 'tutor', 'sandbox')]


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
        for name in ('open-science-resources.html', 'open-science-fetch.html', 'render-remote-readme.html'):
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

    def prompt_template(self, expected):
        return ('{{ $r := partial "open-science-fetch.html" '
                f'(dict "url" "{self.url}/prompt.md" "sha256" "{expected}") '
                '}}{{ with $r }}{{ $copy := resources.Copy "prompts/example.md" . }}'
                '<a href="{{ $copy.RelPermalink }}">Read</a>{{ end }}')

    def setup_local(self):
        source = self.site / 'assets/open-science-local'
        source.mkdir(parents=True)
        for name in NAMES:
            (source / name).write_bytes((name + '\nlocal draft\n').encode())
        pin = {'repository': 'https://github.com/openmodelingfoundation/skills',
               'source_directory': 'prompts/open-science', 'revision': 'a' * 40,
               'release': 'v2026.11', 'files': {name: '0' * 64 for name in NAMES}}
        (self.site / 'data').mkdir()
        (self.site / 'data/open-science-source.json').write_text(json.dumps(pin))
        return source, pin

    def test_remote_bytes_and_prefix_preserved(self):
        content = self.responses['/prompt.md'][1]
        result = self.render(self.prompt_template(hashlib.sha256(content).hexdigest()))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.output / 'prompts/example.md').read_bytes(), content)
        self.assertIn('/preview/prompts/example.md', (self.output / 'index.html').read_text())

    def test_remote_checksum_and_missing_source_fail_even_with_warm_cache(self):
        content = self.responses['/prompt.md'][1]
        template = self.prompt_template(hashlib.sha256(content).hexdigest())
        self.assertEqual(self.render(template).returncode, 0)
        self.responses['/prompt.md'] = (200, b'different bytes')
        result = self.render(template)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SHA-256 mismatch', result.stdout + result.stderr)
        self.responses['/prompt.md'] = (404, b'missing')
        result = self.render(template)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('source not found', result.stdout + result.stderr)
        self.responses['/prompt.md'] = (403, b'unavailable')
        result = self.render(template)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('retrieval failed', result.stdout + result.stderr)

    def test_local_drafts_have_actual_hashes_without_release_claim(self):
        source, _ = self.setup_local()
        template = '{{ $r := partialCached "open-science-resources.html" site }}{{ $r.metadata.RelPermalink }}'
        result = self.render(template, local=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        metadata = json.loads((self.output / 'prompts/open-science-source.json').read_text())
        self.assertEqual(metadata['mode'], 'local-preview')
        self.assertNotIn('revision', metadata)
        self.assertNotIn('release', metadata)
        for name in NAMES:
            content = (source / name).read_bytes()
            self.assertEqual((self.output / 'prompts' / name).read_bytes(), content)
            self.assertEqual(metadata['files'][name], hashlib.sha256(content).hexdigest())
        (source / NAMES[0]).unlink()
        result = self.render(template, local=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Local open science source missing', result.stdout + result.stderr)

    def test_invalid_pin_fails_before_network_access(self):
        _, pin = self.setup_local()
        pin['revision'] = 'main'
        (self.site / 'data/open-science-source.json').write_text(json.dumps(pin))
        result = self.render('{{ partial "open-science-resources.html" site }}')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('40-character commit', result.stdout + result.stderr)
        self.assertEqual(self.requests, [])

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
