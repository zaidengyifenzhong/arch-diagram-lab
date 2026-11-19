import importlib.util
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog_index', ROOT / 'scripts/build_catalog_index.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs).get('href', ''))


class CatalogIndexTests(unittest.TestCase):
    def test_current_index_and_targets(self):
        text = (ROOT / 'catalog/README.md').read_text()
        papers = json.loads((ROOT / 'catalog/papers.json').read_text())['papers']
        self.assertEqual(module.render(text, papers), text)
        block = text.split(module.START)[1].split(module.END)[0]
        targets = re.findall(r'\]\(#([^)]*)\)', block)
        guides = [p for p in papers if p.get('source_note', '').startswith('原文链接读图指南')]
        self.assertEqual(targets, ['reading-guide-' + p['paper_id'] for p in guides])
        for target, paper in zip(targets, guides):
            marker = f'<a id="{target}"></a>\n\n## {paper["title"]}\n'
            self.assertEqual(text.count(marker), 1)
            self.assertIn(paper['source_note'], text)

    def test_gallery_github_target(self):
        parser = Links()
        parser.feed((ROOT / 'gallery/index.html').read_text())
        link = 'https://github.com/zaidengyifenzhong/arch-diagram-lab/blob/main/catalog/README.md#source-linked-reading-guides'
        self.assertIn(link, parser.links)
        target = urlsplit(link)
        self.assertEqual(target.scheme, 'https')
        self.assertIn(f'<a id="{target.fragment}"></a>\n\n## 原文链接读图指南', (ROOT / 'catalog/README.md').read_text())
