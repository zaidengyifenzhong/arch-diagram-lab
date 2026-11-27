"""Report ID-based access coverage, not paper completion or redistribution rights."""
from collections import Counter
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


MISSING_REASONS = {
    'dac-2025-chord': '既有链接是 MDR-HDONN 前身稿，尚不能核定为 CHORD 的相应图。[正式 DOI](https://doi.org/10.1109/DAC63849.2025.11133168)提供检索入口；同作者的[DAC 2025 会议议程](https://62dac.conference-program.com/presentation/?id=RESEARCH147&sess=sess110)沿用 MDR-HDONN 标题，仅作演讲别名（talk alias），不能证明 arXiv 前序版与正式论文图相同，不转用前身图号。',
    'isca-2026-dejavu': '此前正式论文网页读取因文件长度16087357字节超过工具上限而失败，未换路线获取。[作者 ISCA 演讲物理p5](https://people.inf.ethz.ch/omutlu/pub/DejaVu-isca26-talk.pdf#page=5)介绍普通 DRAM 单元与行，[演讲p6](https://people.inf.ethz.ch/omutlu/pub/DejaVu-isca26-talk.pdf#page=6)介绍访问命令及时序背景；只作背景检索入口，不涉及攻击细节，也不计为正式论文图号级导读或补齐覆盖。',
}


def render():
    papers = json.loads((ROOT / 'catalog/papers.json').read_text())['papers']
    by_id = {p['paper_id']: p for p in papers}
    assert len(by_id) == len(papers) == 100
    assets = json.loads((ROOT / 'gallery/figures.json').read_text())['items']
    licenses = json.loads((ROOT / 'gallery/licenses.json').read_text())['items']
    assert len({f['id'] for f in licenses}) == len(licenses) == len(assets)
    assert {f['id']: f['license_name'] for f in assets} == {f['id']: f['license_name'] for f in licenses}
    license_counts = Counter(f['license_name'] for f in licenses)
    originals = {f['paper_id'] for f in assets} & by_id.keys()
    fixed_entries = [f for f in assets if f['paper_id'] in by_id]
    supplemental = [f for f in assets if f['paper_id'] not in by_id]
    supplemental_ids = {f['paper_id'] for f in supplemental}
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
             '<a id="gallery-summary"></a>', '',
             '## 全图库数量与许可汇总', '',
             '数量按 gallery/figures.json 的唯一条目及论文ID核算，许可分布取自 gallery/licenses.json；两份清单的条目ID和许可必须一致。这里统计图示条目，包含明确标注的机制子区域，不表示全篇完成。', '',
             '| 范围 | 论文数 | 图示条目数 |', '|---|---:|---:|',
             f'| 全图库 | {len(originals) + len(supplemental_ids)} | {len(assets)} |',
             f'| 固定100篇样本内 | {len(originals)} | {len(fixed_entries)} |',
             f'| 样本外补充 | {len(supplemental_ids)} | {len(supplemental)} |', '',
             '| 单条许可 | 条目数 |', '|---|---:|',
             *[f'| {name} | {count} |' for name, count in sorted(license_counts.items())], '',
             '单图许可与署名仍以[逐图清单](../gallery/licenses.json)为准，许可汇总不改变任何条目的适用条件。样本外论文不计入固定100篇入口覆盖。', '',
             '样本外图页：' + ' · '.join(f'[{pid}](../gallery/papers/{pid}.md)' for pid in sorted(supplemental_ids)) + '。', '',
             '## 最近一次入口扩充', '',
             '本批新增 Modern GPU 作者预印本 arXiv:2503.20481v1 的 F1/F3（物理p2/p5）及 Nugget arXiv:2509.02873v2 的 F1（官方HTML §3）静态入口。沿用已核验出处，未下载来源、未进行新的视觉审核，不上传或嵌入图片。既有版本、许可与素材暂缓审核状态保持不变。', '',
             '该次入口扩充前：A=39、B=61、交集4、并集96、两者均无4。当前入口与图库数量见上述自动汇总；入口覆盖不表示全篇完成。', '',
             '## 仍无两类入口：精确缺口', '',
             '以下只表示仓库尚无所定义的入口，不表示论文没有非实验图或禁止转载；未核实的仍留作未完成。以下分别记录本轮读取阻碍与沿用的既有缺口，未重试此前被拒绝的下载。', '']
    for pid in sorted(missing):
        lines.append(f'- `{pid}` — {by_id[pid]["title"]}：{MISSING_REASONS[pid]}')
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
