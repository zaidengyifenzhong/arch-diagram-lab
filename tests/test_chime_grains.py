import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class ChimeGrainsTests(unittest.TestCase):
 def test_exact_fixed_versions_and_canonical(self):
  d=json.loads((R/'gallery/figures.json').read_text());c=json.loads((R/'catalog/papers.json').read_text())
  for pid,nums,ver in [('isca-2026-chime',[6,7],'2504.17584v2'),('isca-2026-grains',[6],'2606.26468v1')]:
   fs=[f for f in d['items'] if f['paper_id']==pid];self.assertEqual([f['figure_number'] for f in fs],nums)
   p=next(x for x in c['papers'] if x['paper_id']==pid);o=next(x for x in d['paper_objects'] if x['paper_id']==pid);g=next(x for x in d['reading_guides'] if x['paper_id']==pid)
   self.assertEqual(p['object_group'],o['object_group']);self.assertEqual(p['object_group'],g['primary_object']);self.assertEqual(p['specific_object'],g['specific_object'])
   for f in fs:
    self.assertIn(ver,f['source_url']);self.assertIn(ver,f['source_version']);self.assertIn('arXiv',f['paper_short']);self.assertNotIn('ISCA',f['paper_short'])
    self.assertEqual(f['license_name'],'CC BY 4.0')
    for k in ['input_png','review_status','decision','review_scope','crop_box_pdf_points','asset_sha256']:self.assertNotIn(k,f)
    for path in ['gallery/index.html','gallery/papers/'+pid+'.md']:
     s=(R/path).read_text();self.assertIn(f['attribution'],s);self.assertIn(f['source_note'],s)
 def test_coverage_presentations(self):
  for f in ['README.md','index.html','gallery/README.md','gallery/index.html','catalog/README.md']:
   s=(R/f).read_text();self.assertIn('200',s);self.assertIn('47',s)
  d=json.loads((R/'gallery/scope.json').read_text());self.assertEqual(d['coverage'],{'papers':47,'entries':200,'original_figure_entries':198,'mechanism_subregions':2})
