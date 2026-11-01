#!/usr/bin/env python3
"""Render all original synthetic examples; use --preview for PNG+PDF."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from arch_diagram_lab.cli import main
preview=['--preview','both'] if '--preview' in sys.argv else []
for path in sorted((ROOT/'examples').glob('*.json')):
    if main(['render',str(path),'-o',str(ROOT/'generated'/(path.stem+'.svg'))]+preview):
        raise SystemExit(2)
