import json, unittest
from pathlib import Path
R = Path(__file__).resolve().parents[1]
class XTRATests(unittest.TestCase):
 def test_exact_source_and_supplemental_scope(self):
  pid='sosp-2026-xtra'
  fs=[f for f in json.loads((R/'gallery/figures.json').read_text())['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(3,5)])
  ls={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   r=ls[f['id']]
   self.assertEqual(r['source_git_blob'],'aa0c709a68468b07bcfb868ceaa3f4b4046976f0')
   self.assertEqual(r['source_pdf_sha256'],'40b34fa1dd59b318df3de14a9dc97e355f928618b9fcc96b3a5a7325d89b5ddb')
   self.assertEqual(r['license_name'],'CC BY 4.0')
   self.assertIn('0e6058eb31c7321ad89b619a6b7bc3ff02622b8f',r['source_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
   self.assertIn('样本外补充',f['source_note'])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[3]},scope['supplemental_papers'])

 def test_canonical_summary_link(self):
  self.assertIn('../docs/catalog-access-coverage.md#gallery-summary',(R/'catalog/README.md').read_text())
