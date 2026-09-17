#!/usr/bin/env python3
"""Check generated pages and their internal links (no external requests)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys

root = Path(__file__).resolve().parents[1] / '_site'
class Page(HTMLParser):
    def __init__(self, content):
        super().__init__(); self.links = []; self.ids = set(); self.feed(content)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])

pages = {p: Page(p.read_text()) for p in root.rglob('*.html')}
errors = []
for path, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not link: continue
        target = (root / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)) if url.path else path
        target = target.resolve()
        if target.is_dir(): target /= 'index.html'
        if not target.exists(): errors.append(f'{path.relative_to(root)}: missing {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{path.relative_to(root)}: missing anchor {link}')
assert pages, 'Build the site before checking it.'
assert not list(root.rglob('*.pptx')), 'Source presentations must not be published.'
for error in errors: print(error)
print(f'Checked {len(pages)} HTML pages: {len(errors)} broken internal links.')
sys.exit(bool(errors))
