"""Regenerate only the source-linked guide index; preserve catalog prose.

Run: python scripts/build_catalog_index.py [--check]
The source_note prefix 原文链接读图指南 identifies this kind of guide.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- source-linked-guides:start -->'
END = '<!-- source-linked-guides:end -->'


def render(text, papers):
    guides = [p for p in papers if p.get('source_note', '').startswith('原文链接读图指南')]
    lines = [START, '<a id="source-linked-reading-guides"></a>', '',
             '## 原文链接读图指南', '',
             '以下指南链接原文并提供中文读图说明；仅链接的图不计入图库图片收录。', '',
             '跨论文方法：[两张机制图怎么对照读](../docs/reading-mechanism-pairs.md)。先问两图保留了什么、改变了什么。', '']
    for paper in guides:
        anchor = 'reading-guide-' + paper['paper_id']
        heading = '## ' + paper['title'] + '\n'
        marker = f'<a id="{anchor}"></a>\n\n'
        if text.count(heading) != 1:
            raise ValueError('Expected one catalog heading: ' + paper['paper_id'])
        text = text.replace(marker, '')
        text = text.replace(heading, marker + heading)
        lines.append(f"- [{paper['title']}](#{anchor})")
    block = '\n'.join(lines + [END])
    if START in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block + after
    pos = text.index('\n## ')
    return text[:pos] + '\n' + block + '\n' + text[pos:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'catalog/README.md'
    old = path.read_text()
    new = render(old, json.loads((ROOT / 'catalog/papers.json').read_text())['papers'])
    if args.check:
        if old != new:
            raise SystemExit('Catalog guide index is stale; run scripts/build_catalog_index.py')
        print('Catalog guide index is current.')
    else:
        path.write_text(new)


if __name__ == '__main__':
    main()
