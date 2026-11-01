#!/usr/bin/env python3
"""Check local corpus integrity; not independent verification of source claims."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from arch_diagram_lab.corpus import validate_corpus, validate_expert_corpus
from arch_diagram_lab.core import SpecError
try:
    papers,figures=[json.loads((ROOT/'corpus'/name).read_text()) for name in ('papers.json','figures.json')]
    counts=validate_corpus(papers,figures)
    expert=validate_expert_corpus(json.loads((ROOT/'corpus/expert-papers.json').read_text()),[p['id'] for p in papers['records']])
    print(f"VALID pilot schema 0.1.0 (records): {counts['papers']} papers / {counts['figures']} figures")
    print(f"VALID expert schema 1 (papers[].figures): {expert['papers']} papers / {expert['figures']} figures")
    print(f"TOTAL unique records: {counts['papers']+expert['papers']} papers / {counts['figures']+expert['figures']} figures")
    print('Integrity only: source truth, PDF hashes and inspection claims are not reverified; expert schema lacks page-count upper bounds.')
except (OSError,ValueError) as exc:
    print(f'ERROR: {exc}',file=sys.stderr); raise SystemExit(2)
