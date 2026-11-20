import unittest,json,hashlib,re
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
class RestoredExpansionTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.d=json.loads((R/'gallery/figures.json').read_text());c.fs=c.d['items'];c.scope=json.loads((R/'gallery/scope.json').read_text());c.cat=json.loads((R/'catalog/papers.json').read_text())
 def test_exact_new_scope(self):
  self.assertEqual(len(self.fs),185);self.assertEqual(len({f['paper_id'] for f in self.fs}),40);self.assertEqual(len(self.scope['approved_subregions']),2)
  self.assertEqual(Counter(f['license_name'] for f in self.fs),{'CC BY 4.0':168,'CC0 1.0':10,'CC BY 2.5':1,'CC BY-NC-SA 4.0':6})
 def test_held_whole_figures_stay_out(self):
  self.assertEqual(len(self.scope['held_mixed_whole_figures']),7);self.assertFalse(set(self.scope['held_mixed_whole_figures'])&{f['id'] for f in self.fs})
 def test_subregions_clear_everywhere(self):
  ids={x['id'] for x in self.scope['approved_subregions']}
  for f in self.fs:
   if f['id'] not in ids:continue
   for k in ['figure_title','alt_text','source_note']:self.assertIn('非整图',f[k])
   self.assertIn('排除',f['source_note']);self.assertIn('未重新读取或渲染原PDF',f['source_note'])
   for name in ['gallery/index.html','gallery/papers/dac-2026-zkflex.md']:
    s=(R/name).read_text();self.assertIn(f['figure_title'],s);self.assertIn(f['modifications'],s)
 def test_no_private_fields(self):
  forbidden=['input_png','review_status','decision','review_scope']
  for f in self.fs:
   for k in forbidden:self.assertNotIn(k,f)
  for name in ['gallery/figures.json','gallery/index.html','gallery/licenses.json']:
   s=(R/name).read_text()
   for bad in ['/workspace/','/home/','file://','chatgpt.site'] :self.assertNotIn(bad,s)
 def test_dcc_fixed_version_and_canonical(self):
  fs=[f for f in self.fs if f['paper_id']=='isca-2026-dcc'];self.assertEqual([f['figure_number'] for f in fs],[1,3,4,5])
  p=next(p for p in self.cat['papers'] if p['paper_id']=='isca-2026-dcc');o=next(o for o in self.d['paper_objects'] if o['paper_id']==p['paper_id'])
  for k in ['object_group','specific_object']:self.assertEqual(p[k],o[k])
  for f in fs:self.assertEqual(f['paper_short'],'DCC · arXiv v5');self.assertIn('2511.15503v5',f['source_page_url']);self.assertIn('不声称',f['source_note'])
 def test_local_static_entry_not_deployment_claim(self):
  self.assertEqual((R/'.nojekyll').read_bytes(),b'');s=(R/'index.html').read_text();self.assertIn('gallery/index.html',s);self.assertIn('不表示托管已启用',s)
  self.assertIn('未开启 GitHub Pages',(R/'README.md').read_text())
