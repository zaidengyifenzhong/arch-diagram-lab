"""CLI: python -m arch_diagram_lab {validate,render,edit} ..."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from .core import SpecError, render, validate

def main(argv=None):
    p=argparse.ArgumentParser(description='Semantic architecture-diagram JSON → editable SVG. Standard library only; optional Inkscape previews.')
    sub=p.add_subparsers(dest='command',required=True)
    v=sub.add_parser('validate',help='Validate IDs, references, roles, direction, labels and basic geometry')
    v.add_argument('spec',type=Path)
    r=sub.add_parser('render',help='Render an editable SVG, optionally export PNG/PDF via Inkscape')
    r.add_argument('spec',type=Path); r.add_argument('-o','--output',required=True,type=Path)
    r.add_argument('--monochrome',action='store_true',help='Export grayscale colors while preserving labels and line patterns')
    r.add_argument('--preview',choices=['png','pdf','both'])
    e=sub.add_parser('edit',help='Rename one node label without losing IDs or routes; writes a new JSON spec')
    e.add_argument('spec',type=Path); e.add_argument('--node',required=True); e.add_argument('--label',required=True)
    e.add_argument('-o','--output',required=True,type=Path)
    args=p.parse_args(argv)
    try:
        spec=json.loads(args.spec.read_text(encoding='utf-8')); validate(spec)
        if args.command=='validate':
            print(f'VALID: {args.spec} ({len(spec["nodes"])} nodes, {len(spec.get("edges",[]))} edges)'); return 0
        if args.command=='edit':
            target=next((n for n in spec['nodes'] if n['id']==args.node),None)
            if target is None: raise SpecError(f'unknown node: {args.node}')
            target['label']=args.label; validate(spec)
            data=json.dumps(spec,indent=2,ensure_ascii=False)+'\n'
        else:
            if args.output.suffix.lower()!='.svg': raise SpecError('render output must end in .svg')
            if args.preview and not shutil.which('inkscape'): raise SpecError('preview requires Inkscape; omit --preview for dependency-free SVG')
            data=render(spec,monochrome=args.monochrome)
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(data,encoding='utf-8')
        print(f'WROTE: {args.output}')
        if args.command=='render' and args.preview:
            for ext in (['png','pdf'] if args.preview=='both' else [args.preview]):
                output=args.output.with_suffix('.'+ext)
                subprocess.run(['inkscape',str(args.output),'--export-type='+ext,'--export-filename='+str(output)],check=True,capture_output=True,text=True)
                print(f'WROTE: {output}')
        return 0
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr); return 2
