"""Check published prompt integrity, prefix links and bibliography completeness."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.publications = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.links.append(attrs)
        if tag == 'li' and 'publication-item' in attrs.get('class', '').split():
            self.publications += 1


def check_prompts(output, base_url='/'):
    pin = json.loads(Path('data/open-science-source.json').read_text())
    source = json.loads((output / 'prompts/open-science-source.json').read_text())
    local = os.environ.get('HUGO_OPEN_SCIENCE_LOCAL') == '1'
    if source['mode'] != ('local-preview' if local else 'pinned'):
        raise ValueError('published prompt source mode does not match the build')
    if set(source['files']) != set(pin['files']):
        raise ValueError('published prompt inventory does not match the pin')
    if local:
        if source.get('revision') or source.get('release'):
            raise ValueError('local preview must not claim a published commit or release')
    elif source['revision'] != pin['revision'] or source['files'] != pin['files']:
        raise ValueError('published source revision/checksums do not match the pin')
    prefix = urlsplit(base_url).path.rstrip('/')
    page = Page((output / 'resources/open-science-assistant/index.html').read_text())
    for name, expected in source['files'].items():
        content = (output / 'prompts' / name).read_bytes()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError(f'{name}: published SHA-256 mismatch')
        if local and content != (Path('assets/open-science-local') / name).read_bytes():
            raise ValueError(f'{name}: local source bytes changed during publication')
        links = [link for link in page.links if link.get('href') == f'{prefix}/prompts/{name}']
        if not any('download' in link for link in links) or not any('download' not in link for link in links):
            raise ValueError(f'{name}: missing read/download links under {prefix or "/"}')
    hrefs = {link.get('href') for link in page.links}
    if f'{prefix}/prompts/open-science-source.json' not in hrefs:
        raise ValueError('missing prompt source metadata link')
    if not local:
        revision_link = f'{pin["repository"]}/tree/{pin["revision"]}/{pin["source_directory"]}'
        if revision_link not in hrefs:
            raise ValueError('missing pinned source revision link')
        if pin.get('release') and f'{pin["repository"]}/releases/tag/{pin["release"]}' not in hrefs:
            raise ValueError('missing pinned release link')
    print(f'Verified four prompt downloads and source links under {prefix or "/"}.')


def check_bibliography(output):
    publications = json.loads(Path('data/publications.json').read_text())
    published = Page((output / 'resources/publications/index.html').read_text())
    if not publications or published.publications != len(publications):
        raise ValueError('rendered bibliography does not contain all generated records')
    if (output / 'bibliographies/publications.bib').read_bytes() != Path('assets/bibliographies/publications.bib').read_bytes():
        raise ValueError('published BibTeX differs from its authoritative source')
    print(f'Verified {len(publications)} bibliography records and original BibTeX bytes.')


def check(output, base_url='/'):
    check_prompts(output, base_url)
    check_bibliography(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--base-url', default='/')
    args = parser.parse_args()
    try:
        check(args.output, args.base_url)
    except (OSError, ValueError, KeyError) as error:
        print(f'ERROR: generated content: {error}', file=sys.stderr)
        sys.exit(1)
