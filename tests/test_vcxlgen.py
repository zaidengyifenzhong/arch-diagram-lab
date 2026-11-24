import json, unittest
from pathlib import Path
R = Path(__file__).resolve().parents[1]
class VCXLGenTests(unittest.TestCase):
 def test_exact_source_and_supplemental_scope(self):
  pid='asplos-2026-vcxlgen'
  fs=[f for f in json.loads((R/'gallery/figures.json').read_text())['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(4,5),(6,7)])
  ls={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   r=ls[f['id']]
   self.assertEqual(r['source_git_blob'],'155054ad656dec2d65d69f81d3c4b57b7660d60c')
   self.assertEqual(r['source_pdf_sha256'],'7b94d57e9f5e67e92cf3acf554c45b77e9877838ada07aeaad484acf32228113')
   self.assertEqual(r['license_name'],'CC BY 4.0')
   self.assertIn('7d759dda2b5628601d8338c563449a7fbd31edeb',r['source_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
   self.assertIn('样本外补充',f['source_note'])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[4,6]},scope['supplemental_papers'])
