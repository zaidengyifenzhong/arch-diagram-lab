"""Regenerate only the noscript fallback from the published figure manifest."""
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTICE = '以下为完整非实验图示回退列表，含明确标注的机制子区域／非整图；启用JavaScript可筛选。'


def render(items):
    esc = html.escape
    parts = ['<noscript><p>' + NOTICE + '</p><div class="no-script-list">']
    for item in items:
        page = 'papers/' + item['paper_id'] + '.md'
        parts += ['<article><h2>' + esc(item['paper_short'] + ' · ' + item['figure_title']) + '</h2>',
                  '<p>' + esc(item['figure_type']) + '</p>',
                  '<img loading="lazy" src="' + esc(item['asset'], quote=True) + '" alt="' + esc(item['alt_text'], quote=True) + '">']
        for key in ('source_note', 'paper_notice', 'reuse_notice'):
            if item.get(key):
                parts.append('<p>' + esc(item[key]) + '</p>')
        parts.append('<p><a href="' + esc(page, quote=True) + '">读图、来源与署名</a> · <a href="' + esc(item['license_url'], quote=True) + '">' + esc(item['license_name']) + '</a></p></article>')
    return ''.join(parts) + '</div></noscript>'


def build():
    path = ROOT / 'gallery/index.html'
    source = path.read_text()
    items = json.loads((ROOT / 'gallery/figures.json').read_text())['items']
    assert len({item['id'] for item in items}) == len(items)
    output, count = re.subn(r'<noscript>.*?</noscript>', lambda _: render(items), source, flags=re.S)
    if count != 1:
        raise ValueError('Expected exactly one noscript block')
    return path, output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path, output = build()
    if args.check:
        if path.read_text() != output:
            raise SystemExit('Gallery fallback is stale')
        print('Gallery fallback is current.')
    else:
        path.write_text(output)
