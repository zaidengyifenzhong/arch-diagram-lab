import json,unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
class SageSelectionTests(unittest.TestCase):
 def test_exact_sage_selection_and_source(self):
  d=json.loads((R/'gallery/figures.json').read_text());fs=[f for f in d['items'] if f['paper_id']=='hpca-2026-sage'];self.assertEqual([f['figure_number'] for f in fs],[5,11,12])
  for f in fs:
   self.assertEqual(f['license_name'],'CC BY 4.0');self.assertIn('v4',f['source_version']);self.assertIn('arXiv',f['paper_short'])
   for path in ['gallery/index.html','gallery/papers/hpca-2026-sage.md']:
    text=(R/path).read_text();self.assertIn(f['attribution'],text);self.assertIn(f['source_note'],text)
   for key in ['decision','sha256','asset_sha256','review_note','crop_box_pdf_points']:self.assertNotIn(key,f)
  f11=next(f for f in fs if f['figure_number']==11);self.assertIn('读段构建单元',f11['source_note']);self.assertNotIn('读取重构单元',f11['source_note'])
 def test_sp2rint_not_published(self):
  d=json.loads((R/'gallery/figures.json').read_text())
  self.assertFalse(any(f['paper_id']=='dac-2026-sp2rint' for f in d['items']));self.assertFalse(any(f['paper_id']=='dac-2026-sp2rint' for f in d['reading_guides']));self.assertFalse((R/'gallery/papers/dac-2026-sp2rint.md').exists())
  self.assertFalse(any('sp2rint' in p.name.lower() for p in (R/'gallery/assets').glob('*')))
  c=json.loads((R/'catalog/papers.json').read_text());p=next(p for p in c['papers'] if p['paper_id']=='dac-2026-sp2rint');self.assertEqual(p['public_gallery']['figure_count'],0)
 def test_coverage(self):
  d=json.loads((R/'gallery/figures.json').read_text());self.assertEqual(len(d['items']),183);self.assertEqual(len({f['paper_id'] for f in d['items']}),39)
  self.assertEqual(Counter(f['license_name'] for f in d['items']),{'CC BY 4.0':166,'CC0 1.0':10,'CC BY 2.5':1,'CC BY-NC-SA 4.0':6})
  for f in ['README.md','index.html','gallery/README.md','gallery/index.html','catalog/README.md']:
   text=(R/f).read_text();self.assertIn('183',text);self.assertIn('39',text)
