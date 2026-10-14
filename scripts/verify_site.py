import json
from html.parser import HTMLParser
from pathlib import Path
import re

class EmbeddedData(HTMLParser):
    def __init__(self, target):
        super().__init__()
        self.target, self.active, self.chunks = target, False, []
    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('id') == self.target:
            self.active = True
    def handle_endtag(self, tag):
        if tag == 'script':
            self.active = False
    def handle_data(self, text):
        if self.active:
            self.chunks.append(text)

root = Path(__file__).resolve().parents[1]
section = root / 'site/sections/2-3'
embedded = EmbeddedData('lesson-data')
embedded.feed((section / 'index.html').read_text(encoding='utf-8'))
public = json.loads((section / 'data.json').read_text(encoding='utf-8'))
assert json.loads(''.join(embedded.chunks)) == public
assert public == json.loads((root / 'content/section-2-3.json').read_text(encoding='utf-8'))
assert len(public['lesson']['questions']) == 11
assert [q['number'] for q in public['textbook']['exercises']] == list(range(1,65))
linked = {link['number'] for q in public['lesson']['questions'] for link in q['relatedExercises']}
assert linked == set(range(1,65))
assert public['audit']['sourceReviewed'] and public['audit']['solutionsReviewed']
for filename in (root / 'site').rglob('*'):
    if filename.is_file():
        assert filename.suffix.lower() != '.pdf'
        if filename.suffix.lower() in ('.html','.json','.js','.css'):
            text = filename.read_text(encoding='utf-8')
            assert not re.search(r'[A-Za-z]:[\\/]|Users[/\\]yiyan|ghp_[A-Za-z0-9]+',text), filename
for record in public['lesson']['questions'] + public['textbook']['exercises']:
    for key in ('sourceImage','solutionImage'):
        if key in record:
            assert (section / record[key]).is_file(),record[key]
print('Verified identical embedded/public/source data, 64 exercise routes, all assets, reviewed content, and clean public site.')
