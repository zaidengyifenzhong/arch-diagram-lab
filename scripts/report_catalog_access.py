"""Report ID-based access coverage, not paper completion or redistribution rights."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Existing cross-paper/standalone guides not marked by the catalog prefix.
EXTRA_GUIDES = {
    'hpca-2025-concord': 'docs/reading-storage-figures.md',
    'atc2025-hotrap': 'docs/reading-storage-figures.md',
    'atc2025-solfs': 'docs/reading-storage-figures.md',
    'asplos-2025-virtuoso': 'docs/reading-virtuoso-figures.md',
    'ipdps2026-vla-quantum': 'docs/tracing-data-across-figures.md',
    'asplos-2026-rteaal': 'docs/tracing-data-across-figures.md',
}


def render():
    papers = json.loads((ROOT / 'catalog/papers.json').read_text())['papers']
    by_id = {p['paper_id']: p for p in papers}
    assert len(by_id) == len(papers) == 100
    assets = json.loads((ROOT / 'gallery/figures.json').read_text())['items']
    originals = {f['paper_id'] for f in assets} & by_id.keys()
    guides = {p['paper_id']: 'catalog/README.md#reading-guide-' + p['paper_id']
              for p in papers if p.get('source_note', '').startswith('原文链接读图指南')}
    guides.update(EXTRA_GUIDES)
    for pid, path in guides.items():
        assert pid in by_id and (ROOT / path.split('#')[0]).is_file()
    guided = set(guides)
    missing = set(by_id) - originals - guided
    lines = ['# 固定100篇：原图与图号级导读入口盘点', '',
             '由 `python scripts/report_catalog_access.py` 按唯一 paper_id 生成；可用 `--check` 检查。', '',
             '原图口径：gallery/figures.json 中至少有一个已发布条目（沿用项目条目口径，含明确标注的机制子区域）。导读口径：有图号及物理页／官方图锚点的专门原文指南，或下表明确登记的独立／跨论文练习。原图页自身的常规图注不重复算成专门导读。仅有论文首页链接、初读数量或题名不算导读。', '',
             '这些都是入口覆盖，不是全篇深读、完整视觉审核、科学复现或授权完成率；混合／实验图在导读中仅作证据不计入原图库。样本外补充论文不进入分母。', '',
             '| 口径 | 篇数 |', '|---|---:|',
             f'| 至少一个原图条目 A | {len(originals)} |',
             f'| 至少一个图号级专门导读 B | {len(guided)} |',
             f'| 两者重叠 A∩B | {len(originals & guided)} |',
             f'| 只有原图 | {len(originals - guided)} |',
             f'| 只有导读 | {len(guided - originals)} |',
             f'| 至少一种入口 A∪B | {len(originals | guided)} |',
             f'| 两者均无 | {len(missing)} |', '',
             '## 本批变化', '',
             '本批新增 FiDe F1（正式PDF物理p4）、μShell F7（正式PDF物理p6）、DARTH-PUM F5/F6（作者稿物理p5）的目录直达说明；依据可读图注与正文核对，未完成新视觉审核，不上传图片或PDF。', '',
             '批前：A=39、B=40、交集4、并集75、两者均无25。批后数字见上表。已有 Concord／HotRAP／SolFS 跨论文指南和 Virtuoso／VLA Quantum／RTeAAL 练习已计入批前，不冒充本批新增覆盖。', '',
             '## 仍无两类入口：精确缺口', '',
             '以下只表示仓库尚无所定义的入口，不表示论文没有非实验图或禁止转载；未核实的仍留作未完成。本批未重新访问这些来源，也未重试此前被拒绝的下载。', '']
    for pid in sorted(missing):
        lines.append(f'- `{pid}` — {by_id[pid]["title"]}')
    lines += ['', '## 逐 ID 明细', '', '| 固定样本 ID | 原图入口 | 专门导读入口 |', '|---|---|---|']
    for pid in sorted(by_id):
        a = f'[已发布](../gallery/papers/{pid}.md)' if pid in originals else '—'
        b = f'[图号级导读](../{guides[pid]})' if pid in guided else '—'
        lines.append(f'| `{pid}` | {a} | {b} |')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true')
    args = parser.parse_args(); path = ROOT / 'docs/catalog-access-coverage.md'; text = render()
    if args.check:
        if path.read_text() != text: raise SystemExit('Coverage report is stale')
        print('Coverage report is current.')
    else:
        path.write_text(text)
