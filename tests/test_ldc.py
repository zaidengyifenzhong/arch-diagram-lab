import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class LDCTests(unittest.TestCase):
 def test_source_scope_and_pages(self):
  data=json.loads((R/'gallery/figures.json').read_text());pid='eurosys-2026-ldc'
  fs=[f for f in data['items'] if f['paper_id']==pid]
  self.assertEqual([(f['figure_number'],f['pdf_page']) for f in fs],[(1,2),(4,6)])
  catalog=json.loads((R/'catalog/papers.json').read_text())['papers']
  self.assertEqual(len(catalog),100);self.assertNotIn(pid,{p['paper_id'] for p in catalog})
  self.assertEqual(sum(p['public_gallery']['figure_count'] for p in catalog),183)
  records={f['id']:f for f in json.loads((R/'gallery/licenses.json').read_text())['items']}
  for f in fs:
   self.assertIn('样本外补充',f['paper_short']);self.assertIn('不计入固定100篇',f['source_note'])
   self.assertEqual(f['license_name'],'CC BY 4.0');r=records[f['id']]
   self.assertEqual(r['source_git_blob'],'237975d1776e471c120c094009c3327fb0bd253c')
   self.assertEqual(r['source_pdf_sha256'],'0c18f5368823618b8bab286120632092092080fc047d8675863add7538c4b01d')
   self.assertIn('9541333a7c61ead35ae2af0d5ad12de6d7e01f60',f['source_page_url'])
   self.assertTrue(r['license_evidence_url'].endswith('#page=1'))
  scope=json.loads((R/'gallery/scope.json').read_text())
  self.assertIn({'paper_id':pid,'fixed_100_sample':False,'figure_numbers':[1,4]},scope['supplemental_papers'])
