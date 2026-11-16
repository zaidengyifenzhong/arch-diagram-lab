import json,re,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
PID='dac-2026-sandwich'
GROUP='机器学习训练与推理系统'
SPECIFIC='Sandwich CPU LLM推理服务系统（联合配置搜索、动态形状内核生成与阶段热切换）'
class SandwichTaxonomyTests(unittest.TestCase):
 def test_canonical_navigation(self):
  d=json.loads((R/'gallery/figures.json').read_text())
  c=json.loads((R/'catalog/papers.json').read_text())
  for rows,key in [(c['papers'],'object_group'),(d['paper_objects'],'object_group'),(d['reading_guides'],'primary_object')]:
   p=next(x for x in rows if x['paper_id']==PID)
   self.assertEqual(p[key],GROUP);self.assertEqual(p['specific_object'],SPECIFIC)
  self.assertEqual(len([x for x in d['items'] if x['paper_id']==PID]),3)
 def test_visible_navigation(self):
  for f in ['catalog/README.md','gallery/README.md','gallery/papers/dac-2026-sandwich.md']:
   s=(R/f).read_text();self.assertIn(SPECIFIC,s);self.assertIn(GROUP,s)
   self.assertNotIn('Sandwich CPU LLM配置搜索与热切换运行时',s);self.assertNotIn('Sandwich CPU LLM服务系统（暂定）',s)
 def test_inline_data_exact(self):
  s=(R/'gallery/index.html').read_text()
  d=json.loads(re.search(r'<script id="gallery-data" type="application/json">(.*?)</script>',s,re.S)[1])
  self.assertEqual(d,json.loads((R/'gallery/figures.json').read_text()))
