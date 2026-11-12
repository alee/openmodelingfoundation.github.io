"""Check bibliography completeness and the original BibTeX download."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys


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


def check_bibliography(output):
    publications = json.loads(Path('data/publications.json').read_text())
    published = Page((output / 'resources/publications/index.html').read_text())
    if not publications or published.publications != len(publications):
        raise ValueError('rendered bibliography does not contain all generated records')
    if (output / 'bibliographies/publications.bib').read_bytes() != Path('assets/bibliographies/publications.bib').read_bytes():
        raise ValueError('published BibTeX differs from its authoritative source')
    print(f'Verified {len(publications)} bibliography records and original BibTeX bytes.')


def check(output, base_url='/'):
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
