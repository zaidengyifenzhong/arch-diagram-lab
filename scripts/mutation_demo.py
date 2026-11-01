#!/usr/bin/env python3
"""Two reproducible edits: rename module, then reroute feedback explicitly."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from arch_diagram_lab.cli import main
from arch_diagram_lab.core import render,validate
source=ROOT/'examples/01-overview.json'
out=ROOT/'generated/04-edited-overview.json'
assert main(['edit',str(source),'--node','scheduler','--label','Epoch arbiter','-o',str(out)])==0
spec=json.loads(out.read_text())
feedback=next(e for e in spec['edges'] if e['id']=='feedback')
feedback['to_side']='right'
feedback['via']=[[975,451]]
feedback['label_at']=[805,438]
spec['title']='Edit demonstration | Rename + reroute'
spec['takeaway']='Stable node IDs preserve connections when labels and explicit routes change.'
validate(spec)
out.write_text(json.dumps(spec,indent=2)+'\n')
assert main(['render',str(out),'-o',str(out.with_suffix('.svg'))]+(['--preview','both'] if '--preview' in sys.argv else []))==0
