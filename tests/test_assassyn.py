import json, unittest
from pathlib import Path
R = Path(__file__).resolve().parents[1]
class AssassynTests(unittest.TestCase):
 def test_exact_source_and_supplemental_scope(self):
  data=json.loads((R/'gallery/figures.json').read_text())
  fs=[f for f in data['items'] if f['paper_id']=='isca-2025-assassyn']
  self.assertEqual([f['figure_number'] for f in fs],[9,10])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100)
  self.assertNotIn('isca-2025-assassyn',{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  licenses={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   self.assertEqual(f['pdf_page'],8)
   self.assertEqual(f['license_name'],'CC BY 4.0')
   l=licenses[f['id']]
   self.assertEqual(l['source_git_blob'],'8623bdf88f94c8b9584042b4c60eb7fd713d5f9c')
   self.assertEqual(l['source_pdf_sha256'],'25f4c9c011703b3bcb557a231860bedb3d9aa4c930fbe0530c7df598e0a66ee2')
   self.assertIn('2b510990e04d5a7ba213af6c21049b303869dd56',f['source_page_url'])
   self.assertTrue(l['license_evidence_url'].endswith('#page=1'))
   self.assertEqual(l['dpi'],240)
