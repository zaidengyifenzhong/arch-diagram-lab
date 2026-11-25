import json, unittest
from pathlib import Path
R = Path(__file__).resolve().parents[1]
class LoopPointTests(unittest.TestCase):
 def test_exact_source_and_supplemental_scope(self):
  pid='taco-2026-looppoint'
  fs=[f for f in json.loads((R/'gallery/figures.json').read_text())['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(2,5),(4,13)])
  ls={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   r=ls[f['id']]
   self.assertEqual(r['source_git_blob'],'571fa9ff4d9abcd7455bc3fd79555f1ed1fe4a24')
   self.assertEqual(r['source_pdf_sha256'],'3fd534206680a9e1772b708d84bf5e5b2b66e1902150cd1fa9a340eb9e9e36bc')
   self.assertEqual(r['license_name'],'CC BY 4.0')
   self.assertIn('027cf9c84a73616667a9c349c733a39cd4e334da',r['source_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
   self.assertIn('样本外补充',f['source_note'])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[2,4]},scope['supplemental_papers'])
