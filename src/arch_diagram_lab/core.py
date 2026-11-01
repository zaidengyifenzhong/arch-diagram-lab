"""Explicit geometry, semantic edge roles, and deterministic SVG generation.

The validator checks structural correctness, not scientific truth or complete
visual quality. Routing is deliberately explicit so authors own every arrow.
"""
import html
import math
import re

ROLES = {'data': ('#245a81', ''), 'control': ('#7b4e90', '7 4'), 'feedback': ('#a15a28', '3 4')}
KINDS = {'module', 'storage', 'external', 'new'}
SIDES = {'left', 'right', 'top', 'bottom'}

class SpecError(ValueError):
    pass

def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def anchor(node, side):
    x,y,w,h = (node[k] for k in ('x','y','w','h'))
    return {'left':(x,y+h/2), 'right':(x+w,y+h/2), 'top':(x+w/2,y), 'bottom':(x+w/2,y+h)}[side]

def validate(spec):
    errors = []
    if not isinstance(spec, dict):
        raise SpecError('spec must be an object')
    if spec.get('version') != 1:
        errors.append('version must be 1')
    for key in ('title','question','takeaway','provenance'):
        if not isinstance(spec.get(key), str) or not spec[key].strip():
            errors.append(f'{key} must be a non-empty string')
    canvas = spec.get('canvas', {})
    if not isinstance(canvas, dict): canvas = {}
    width,height = canvas.get('width',1200),canvas.get('height',680)
    if not all(number(v) and 400 <= v <= 5000 for v in (width,height)):
        errors.append('canvas dimensions must be finite numbers in [400, 5000]')
        width,height = 1200,680
    nodes = spec.get('nodes')
    edges = spec.get('edges', [])
    if not isinstance(nodes, list) or not nodes:
        errors.append('nodes must be a non-empty list'); nodes=[]
    if not isinstance(edges, list):
        errors.append('edges must be a list'); edges=[]
    ids = {}; valid_geometry = []
    for i,n in enumerate(nodes):
        if not isinstance(n, dict): errors.append(f'node {i}: must be an object'); continue
        ident = n.get('id')
        if not isinstance(ident,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',ident):
            errors.append(f'node {i}: invalid id'); continue
        if ident in ids: errors.append(f'duplicate node id: {ident}')
        ids[ident] = n
        if not isinstance(n.get('kind','module'),str) or n.get('kind','module') not in KINDS: errors.append(f'{ident}: invalid node kind')
        if not isinstance(n.get('label'), str) or not n['label'].strip(): errors.append(f'{ident}: missing label')
        vals=[n.get(k) for k in ('x','y','w','h')]
        if not all(number(v) for v in vals): errors.append(f'{ident}: geometry must be finite numbers'); continue
        x,y,w,h=vals
        if w<100 or h<58: errors.append(f'{ident}: minimum node size is 100 x 58')
        if x<24 or y<140 or x+w>width-24 or y+h>height-120: errors.append(f'{ident}: node outside diagram bounds')
        if isinstance(n.get('label'),str) and any(len(s)*10 > w-24 for s in n['label'].split('\n')):
            errors.append(f'{ident}: label too wide; insert a line break or widen node')
        if isinstance(n.get('label'),str) and len(n['label'].split('\n'))*24 > h-20:
            errors.append(f'{ident}: label too tall')
        valid_geometry.append(n)
    for i,a in enumerate(valid_geometry):
        for b in valid_geometry[i+1:]:
            if max(a['x'],b['x']) < min(a['x']+a['w'],b['x']+b['w']) and max(a['y'],b['y']) < min(a['y']+a['h'],b['y']+b['h']):
                errors.append(f"overlapping nodes: {a['id']} / {b['id']}")
    edge_ids=set()
    for i,e in enumerate(edges):
        tag=f'edge {i}'
        if not isinstance(e,dict): errors.append(f'{tag}: must be an object'); continue
        eid=e.get('id')
        if not isinstance(eid,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',eid): errors.append(f'{tag}: invalid id')
        elif eid in edge_ids: errors.append(f'duplicate edge id: {eid}')
        edge_ids.add(eid) if isinstance(eid,str) else None
        if not isinstance(e.get('from'),str) or not isinstance(e.get('to'),str) or e.get('from') not in ids or e.get('to') not in ids: errors.append(f'{tag}: unknown endpoint')
        if e.get('from') == e.get('to'): errors.append(f'{tag}: self-loops unsupported; use separate state nodes')
        if not isinstance(e.get('role'),str) or e.get('role') not in ROLES: errors.append(f'{tag}: role must be data, control, or feedback')
        if e.get('direction') != 'forward': errors.append(f'{tag}: direction must be forward; swap from/to to reverse')
        for k in ('from_side','to_side'):
            if not isinstance(e.get(k),str) or e.get(k) not in SIDES: errors.append(f'{tag}: invalid {k}')
        points=e.get('via',[])
        if not isinstance(points,list): errors.append(f'{tag}: via must be a list'); points=[]
        for p in points:
            if not isinstance(p,list) or len(p)!=2 or not all(number(v) for v in p): errors.append(f'{tag}: invalid waypoint')
            elif not (24<=p[0]<=width-24 and 140<=p[1]<=height-120): errors.append(f'{tag}: waypoint outside diagram bounds')
        if e.get('label'):
            if not isinstance(e['label'],str): errors.append(f'{tag}: label must be a string')
            at=e.get('label_at')
            if not isinstance(at,list) or len(at)!=2 or not all(number(v) for v in at): errors.append(f'{tag}: labeled edges need label_at [x, y]')
            elif not (24<=at[0]<=width-24 and 130<=at[1]<=height-110): errors.append(f'{tag}: label outside diagram bounds')
    panels=spec.get('panels',[])
    if not isinstance(panels,list): errors.append('panels must be a list'); panels=[]
    for i,p in enumerate(panels):
        if not isinstance(p,dict) or not all(number(p.get(k)) for k in ('x','y','w','h')):
            errors.append(f'panel {i}: invalid geometry'); continue
        if not isinstance(p.get('label'),str): errors.append(f'panel {i}: missing label')
        if p['x']<24 or p['y']<140 or p['w']<=0 or p['h']<=0 or p['x']+p['w']>width-24 or p['y']+p['h']>height-120:
            errors.append(f'panel {i}: outside diagram bounds')
    # Only run geometric edge checks when every referenced value is valid.
    if not errors:
        def outside(a,b,side):
            return {'left':b[0]<a[0], 'right':b[0]>a[0], 'top':b[1]<a[1], 'bottom':b[1]>a[1]}[side]
        for e in edges:
            pts=[anchor(ids[e['from']],e['from_side'])]+[tuple(p) for p in e.get('via',[])]+[anchor(ids[e['to']],e['to_side'])]
            if not outside(pts[0],pts[1],e['from_side']): errors.append(f"{e['id']}: route must leave the outside of source port")
            if not outside(pts[-1],pts[-2],e['to_side']): errors.append(f"{e['id']}: route must approach target port from outside")
            if any(a==b for a,b in zip(pts,pts[1:])): errors.append(f"{e['id']}: zero-length segment")
    if errors: raise SpecError('\n'.join(errors))
    return spec

def esc(s): return html.escape(str(s), quote=True)

def render(spec, monochrome=False):
    validate(spec)
    width=spec.get('canvas',{}).get('width',1200); height=spec.get('canvas',{}).get('height',680)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
         f'<title id="title">{esc(spec["title"])}</title><desc id="desc">{esc(spec["question"])} {esc(spec["takeaway"])} {esc(spec["provenance"])}</desc>',
         '<defs>']
    for role,(color,dash) in ROLES.items():
        out.append(f'<marker id="arrow-{role}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,4 L0,8 Z" fill="{color}"/></marker>')
    out += ['</defs>', '<rect width="100%" height="100%" fill="#fff"/>', '<g font-family="DejaVu Sans, Arial, sans-serif" fill="#182a3a">',
            f'<text x="40" y="48" font-size="28" font-weight="700">{esc(spec["title"])}</text>',
            f'<text x="40" y="82" font-size="17" fill="#526271">{esc(spec["question"])}</text>',
            f'<text x="40" y="112" font-size="13" letter-spacing="1" fill="#697582">{esc(spec["provenance"])}</text>']
    for panel in spec.get('panels',[]):
        out += [f'<rect x="{panel["x"]}" y="{panel["y"]}" width="{panel["w"]}" height="{panel["h"]}" rx="12" fill="#f7f9fc" stroke="#d5dde6"/>',f'<text x="{panel["x"]+18}" y="{panel["y"]+30}" font-size="17" font-weight="700">{esc(panel["label"])}</text>']
    nodes={n['id']:n for n in spec['nodes']}
    for e in spec.get('edges',[]):
        pts=[anchor(nodes[e['from']],e['from_side'])]+[tuple(p) for p in e.get('via',[])]+[anchor(nodes[e['to']],e['to_side'])]
        color,dash=ROLES[e['role']]
        path='M '+' L '.join(f'{x},{y}' for x,y in pts)
        out.append(f'<g id="edge-{esc(e["id"])}"><title>{esc(e["from"])} → {esc(e["to"])} ({e["role"]})</title><path d="{path}" fill="none" stroke="{color}" stroke-width="2.4" stroke-dasharray="{dash}" marker-end="url(#arrow-{e["role"]})"/></g>')
    for n in spec['nodes']:
        kind=n.get('kind','module'); fill={'module':'#edf3f9','storage':'#fff4df','external':'#f2f3f5','new':'#e4f4ec'}[kind]
        stroke='#258062' if kind=='new' else '#708398'
        out.append(f'<g id="node-{n["id"]}" data-kind="{kind}"><rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="{2 if kind=="storage" else 10}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
        lines=n['label'].split('\n')
        for j,line in enumerate(lines):
            y=n['y']+n['h']/2-(len(lines)-1)*12+j*24+6
            out.append(f'<text x="{n["x"]+n["w"]/2}" y="{y}" text-anchor="middle" font-size="18" font-weight="600">{esc(line)}</text>')
        out.append('</g>')
    for e in spec.get('edges',[]):
        if e.get('label'):
            x,y=e['label_at']; w=len(e['label'])*8.2+16
            out += [f'<rect x="{x-w/2}" y="{y-16}" width="{w}" height="23" rx="4" fill="#fff"/>',f'<text x="{x}" y="{y}" text-anchor="middle" font-size="14" fill="{ROLES[e["role"]][0]}">{esc(e["label"])}</text>']
    out += [f'<line x1="40" y1="{height-96}" x2="{width-40}" y2="{height-96}" stroke="#dce3ea"/>',f'<text x="40" y="{height-67}" font-size="17" font-weight="600">{esc(spec["takeaway"])}</text>']
    for i,(role,(color,dash)) in enumerate(ROLES.items()):
        x=40+i*240
        out += [f'<path d="M{x},{height-32} h42" stroke="{color}" stroke-width="2.4" stroke-dasharray="{dash}" marker-end="url(#arrow-{role})"/>',f'<text x="{x+56}" y="{height-27}" font-size="14">{role} (source → target)</text>']
    out.append('</g></svg>')
    svg='\n'.join(out)+'\n'
    if monochrome:
        def gray(match):
            value=match.group(0)[1:]
            if len(value)==3: value=''.join(c*2 for c in value)
            r,g,b=(int(value[i:i+2],16) for i in (0,2,4))
            y=round(.2126*r+.7152*g+.0722*b)
            return '#'+f'{y:02x}'*3
        svg=re.sub(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b',gray,svg)
    return svg
