import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from arch_diagram_lab.corpus import validate_corpus, validate_expert_corpus
from arch_diagram_lab.core import SpecError
class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.p,self.f=[json.loads((ROOT/'corpus'/name).read_text()) for name in ('papers.json','figures.json')]
    def test_live_corpus(self):
        counts=validate_corpus(self.p,self.f)
        self.assertGreater(counts['papers'],0); self.assertGreater(counts['figures'],0)
    def test_unknown_paper(self):
        self.f['records'][0]['paper_id']='absent'
        with self.assertRaisesRegex(SpecError,'unknown paper_id'): validate_corpus(self.p,self.f)
    def test_page_out_of_range(self):
        self.f['records'][0]['pdf_page_1based']=999
        with self.assertRaisesRegex(SpecError,'page out of range'): validate_corpus(self.p,self.f)
    def test_results_excluded(self):
        self.f['records'][0]['evidence_status']['experimental_result_chart']=True
        with self.assertRaisesRegex(SpecError,'result charts excluded'): validate_corpus(self.p,self.f)
    def test_duplicate(self):
        self.f['records'].append(copy.deepcopy(self.f['records'][0]))
        with self.assertRaisesRegex(SpecError,'duplicate id'): validate_corpus(self.p,self.f)
    def test_envelope(self):
        with self.assertRaisesRegex(SpecError,'schema_version'): validate_corpus({},self.f)

class ExpertCorpusTests(unittest.TestCase):
    def setUp(self): self.doc=json.loads((ROOT/'corpus/expert-papers.json').read_text())
    def test_expert_schema(self): self.assertGreater(validate_expert_corpus(self.doc)['figures'],0)
    def test_different_schema_rejected(self):
        self.doc['schema_version']='0.1.0'
        with self.assertRaisesRegex(SpecError,'schema_version 1'): validate_expert_corpus(self.doc)
    def test_cross_corpus_duplicate(self):
        with self.assertRaisesRegex(SpecError,'across corpora'): validate_expert_corpus(self.doc,[self.doc['papers'][0]['id']])
    def test_duplicate_figure(self):
        self.doc['papers'][0]['figures'].append(copy.deepcopy(self.doc['papers'][0]['figures'][0]))
        with self.assertRaisesRegex(SpecError,'duplicate figure'): validate_expert_corpus(self.doc)
    def test_anchor_mismatch(self):
        self.doc['papers'][0]['figures'][0]['pdf_page']=99
        with self.assertRaisesRegex(SpecError,'source anchor'): validate_expert_corpus(self.doc)
    def test_missing_inspection(self):
        self.doc['papers'][0].pop('inspection')
        with self.assertRaisesRegex(SpecError,'missing inspection'): validate_expert_corpus(self.doc)
