"""Helpers that build Google Slides API batchUpdate requests: text boxes, pills,
dividers and table grids. Positions and sizes are in INCHES; the helpers convert
to EMU (914400 per inch). Each helper appends to the module-level list `reqs`.

The look is a dark "solution slide": black background, Lato font, navy labels
with a blue outline, a yellow "Correct Option" box. Change the colour constants
below to match your own deck.
"""
import json, sys
EMU = 914400
FONT = 'Lato'
Y = '#F5C518'; W = '#FFFFFF'; G = '#22C55E'; NAVY = '#0F2340'; BLUE = '#3B82F6'
DIV = '#2C4A6E'; KBOX = '#0B1426'; DARK = '#111111'; DIMY = '#3A3000'


def rgb(h):
    h = h.lstrip('#')
    return {k: int(h[i:i+2], 16)/255 for k, i in (('red', 0), ('green', 2), ('blue', 4))}


def u16(s):
    """Length in UTF-16 code units. The Slides API counts text positions this way."""
    return len(s.encode('utf-16-le'))//2


reqs = []


def shape(pid, oid, kind, x, y, w, h, fill=None, outline=None, paras=None,
          align='START', valign='TOP', size=14, bold=True):
    """Create a shape on page `pid` with object id `oid`.
    kind: 'TEXT_BOX', 'RECTANGLE', 'ROUND_RECTANGLE', ...
    outline: (hex colour, weight in pt) or None
    paras: list built with P(...), each a list of runs
    """
    reqs.append({'createShape': {'objectId': oid, 'shapeType': kind, 'elementProperties': {
        'pageObjectId': pid,
        'size': {'width': {'magnitude': int(w*EMU), 'unit': 'EMU'}, 'height': {'magnitude': int(h*EMU), 'unit': 'EMU'}},
        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': int(x*EMU), 'translateY': int(y*EMU), 'unit': 'EMU'}}}})
    props, fields = {}, []
    if kind != 'TEXT_BOX' or fill:
        if fill:
            props['shapeBackgroundFill'] = {'solidFill': {'color': {'rgbColor': rgb(fill)}}}
        else:
            props['shapeBackgroundFill'] = {'propertyState': 'NOT_RENDERED'}
        fields.append('shapeBackgroundFill')
    if outline:
        props['outline'] = {'outlineFill': {'solidFill': {'color': {'rgbColor': rgb(outline[0])}}},
                            'weight': {'magnitude': outline[1], 'unit': 'PT'}, 'propertyState': 'RENDERED'}
    elif kind != 'TEXT_BOX':
        props['outline'] = {'propertyState': 'NOT_RENDERED'}
    if 'outline' in props:
        fields.append('outline')
    if valign != 'TOP':
        props['contentAlignment'] = valign
        fields.append('contentAlignment')
    if fields:
        reqs.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': props, 'fields': ','.join(fields)}})
    if not paras:
        return
    # paras: list of (runs, opts); runs: list of (text, style)
    full = ''; spans = []; pstyles = []
    for i, (runs, popt) in enumerate(paras):
        pstart = u16(full)
        for t, st in runs:
            s = u16(full); full += t; spans.append((s, u16(full), st))
        if i < len(paras)-1:
            full += '\n'
        pstyles.append((pstart, u16(full), popt))
    reqs.append({'insertText': {'objectId': oid, 'insertionIndex': 0, 'text': full}})
    reqs.append({'updateTextStyle': {'objectId': oid, 'textRange': {'type': 'ALL'},
        'style': {'fontFamily': FONT, 'fontSize': {'magnitude': size, 'unit': 'PT'}, 'bold': bold,
                  'foregroundColor': {'opaqueColor': {'rgbColor': rgb(W)}}},
        'fields': 'fontFamily,fontSize,bold,foregroundColor'}})
    if align != 'START' or kind != 'TEXT_BOX':
        reqs.append({'updateParagraphStyle': {'objectId': oid, 'textRange': {'type': 'ALL'},
            'style': {'alignment': align}, 'fields': 'alignment'}})
    for s, e, st in spans:
        if e <= s or not st:
            continue
        style, f = {}, []
        if 'b' in st and st['b'] != bold: style['bold'] = st['b']; f.append('bold')
        if 'c' in st and st['c'] != W: style['foregroundColor'] = {'opaqueColor': {'rgbColor': rgb(st['c'])}}; f.append('foregroundColor')
        if 's' in st: style['fontSize'] = {'magnitude': st['s'], 'unit': 'PT'}; f.append('fontSize')
        if 'f' in st: style['fontFamily'] = st['f']; f.append('fontFamily')
        if f:
            reqs.append({'updateTextStyle': {'objectId': oid, 'textRange': {'type': 'FIXED_RANGE', 'startIndex': s, 'endIndex': e},
                                             'style': style, 'fields': ','.join(f)}})
    for s, e, popt in pstyles:
        if popt.get('below'):
            reqs.append({'updateParagraphStyle': {'objectId': oid,
                'textRange': {'type': 'FIXED_RANGE', 'startIndex': s, 'endIndex': max(e, s+1)},
                'style': {'spaceBelow': {'magnitude': popt['below'], 'unit': 'PT'}}, 'fields': 'spaceBelow'}})


# --- tiny text-building helpers --------------------------------------------
def P(*runs, below=0):
    """A paragraph. Pass plain strings or B(...) / C(...) runs. below = space after, in pt."""
    return ([(r, {}) if isinstance(r, str) else r for r in runs], {'below': below})


B = lambda t, c=W, s=None: (t, dict(b=True, c=c, **({'s': s} if s else {})))   # bold run
C = lambda t, c=W: (t, {'c': c, 'b': False})                                     # regular run
# Tick mark: must be an Arial run. Lato has no glyph for it and shows an empty box.
TICK = lambda c=G: ('✔', {'f': 'Arial', 'c': c, 'b': True})


def pill(pid, oid, x, y, w, h, text, size=15):
    """A rounded navy label with a blue outline, e.g. 'Solution' or 'Key Idea'."""
    shape(pid, oid, 'ROUND_RECTANGLE', x, y, w, h, fill=NAVY, outline=(BLUE, 1.5),
          paras=[P(B(text))], align='CENTER', valign='MIDDLE', size=size)


def divider(pid, oid, x, y, h):
    """A thin vertical line between panes."""
    shape(pid, oid, 'RECTANGLE', x, y, 0.02, h, fill=DIV)


def grid(pid, pre, x, y, cw, ch, rows, size, hi=None):
    """A real table. rows = list of lists of strings. cw/ch = cell width/height (in).
    hi = (row, col) of one cell to highlight in yellow. Cells containing '?' are
    also shown in bold yellow."""
    R, Cn = len(rows), len(rows[0])
    reqs.append({'createTable': {'objectId': pre, 'rows': R, 'columns': Cn, 'elementProperties': {'pageObjectId': pid,
        'size': {'width': {'magnitude': int(cw*Cn*EMU), 'unit': 'EMU'}, 'height': {'magnitude': int(ch*R*EMU), 'unit': 'EMU'}},
        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': int(x*EMU), 'translateY': int(y*EMU), 'unit': 'EMU'}}}})
    allr = {'location': {'rowIndex': 0, 'columnIndex': 0}, 'rowSpan': R, 'columnSpan': Cn}
    reqs.append({'updateTableBorderProperties': {'objectId': pre, 'tableRange': allr, 'borderPosition': 'ALL',
        'tableBorderProperties': {'tableBorderFill': {'solidFill': {'color': {'rgbColor': rgb(W)}}}, 'weight': {'magnitude': 1, 'unit': 'PT'}, 'dashStyle': 'SOLID'},
        'fields': 'tableBorderFill,weight,dashStyle'}})
    reqs.append({'updateTableCellProperties': {'objectId': pre, 'tableRange': allr,
        'tableCellProperties': {'tableCellBackgroundFill': {'solidFill': {'color': {'rgbColor': rgb('#000000')}}}, 'contentAlignment': 'MIDDLE'},
        'fields': 'tableCellBackgroundFill,contentAlignment'}})
    if hi:
        reqs.append({'updateTableCellProperties': {'objectId': pre, 'tableRange': {'location': {'rowIndex': hi[0], 'columnIndex': hi[1]}, 'rowSpan': 1, 'columnSpan': 1},
            'tableCellProperties': {'tableCellBackgroundFill': {'solidFill': {'color': {'rgbColor': rgb(DIMY)}}}}, 'fields': 'tableCellBackgroundFill'}})
    reqs.append({'updateTableColumnProperties': {'objectId': pre, 'columnIndices': list(range(Cn)),
        'tableColumnProperties': {'columnWidth': {'magnitude': int(cw*EMU), 'unit': 'EMU'}}, 'fields': 'columnWidth'}})
    reqs.append({'updateTableRowProperties': {'objectId': pre, 'rowIndices': list(range(R)),
        'tableRowProperties': {'minRowHeight': {'magnitude': int(ch*EMU), 'unit': 'EMU'}}, 'fields': 'minRowHeight'}})
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            loc = {'rowIndex': r, 'columnIndex': c}
            ish = (r, c) == hi or v == '?'
            reqs.append({'insertText': {'objectId': pre, 'cellLocation': loc, 'insertionIndex': 0, 'text': v}})
            reqs.append({'updateTextStyle': {'objectId': pre, 'cellLocation': loc, 'textRange': {'type': 'ALL'},
                'style': {'fontFamily': FONT, 'fontSize': {'magnitude': size, 'unit': 'PT'}, 'bold': ish,
                          'foregroundColor': {'opaqueColor': {'rgbColor': rgb(Y if ish else W)}}},
                'fields': 'fontFamily,fontSize,bold,foregroundColor'}})
            reqs.append({'updateParagraphStyle': {'objectId': pre, 'cellLocation': loc, 'textRange': {'type': 'ALL'},
                'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}})
