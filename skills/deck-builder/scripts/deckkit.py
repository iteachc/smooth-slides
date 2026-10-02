"""deckkit: build Olympiad class decks in the house style of the latest creator deck.

Default geometry and colours follow a dark Olympiad class-deck style (10 x 5.625 in, black
background, Lato). To match YOUR creators' latest deck, measure it (see SKILL.md) and edit C,
the house-slide functions, and the assets. All coordinates are inches.

Flow per topic: section -> hook question (+ solution) -> theory -> 2-3 questions -> revision.
Everything appears one item at a time: builders return shapes, and each slide registers its
click steps with Clicks so they can be wired into the slide timing.
"""
import io, os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.environ.get('DECKKIT_ASSETS', os.path.join(HERE, 'assets'))
ASSET = lambda n: os.path.join(ASSET_DIR, n)
has_asset = lambda n: os.path.exists(ASSET(n))
NSP = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A_ = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
FONT, BLACK, SYM, TICKF = 'Lato', 'Lato Black', 'Arial', 'Segoe UI Symbol'

C = dict(
    bg='000000', white='FFFFFF', grey='C9CED6', dim='8A93A0',
    teal='00C2BB', teal2='00D9B8', cyan='34DCD6', blue='007AFF', navy='031B34',
    green='00FF00', yellow='FFFF00', gold='BF9000', orange='FF9900', red='FF0000', redline='CC0000',
    pink='FF8AF0', magenta='FF4FD8', violet='B07CFF',
    qfill='0A1A2A', optfill='333333', optline='0058B7', card='0D1117',
)
col = lambda c: C.get(c, c)
rgb = lambda c: RGBColor.from_string(col(c))


# ---------------------------------------------------------------- basics
def new_deck():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(10), Inches(5.625)
    return prs


def blank(prs, notes=None):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb('bg')
    if notes:
        sl.notes_slide.notes_text_frame.text = notes
    return sl


def S(t, **o):
    """Text segment with overrides: S('acid', color='red', bold=True)."""
    return (t, o)


def _add_runs(p, segs, size, color, bold, italic, font):
    for seg, o in segs:
        buf = ''
        for ch in seg:                              # arrows/crosses go in their own Arial run
            if ch in '→↔←':
                if buf: _run(p, buf, size, color, bold, italic, font, o); buf = ''
                _run(p, ch, size, color, bold, italic, SYM, o)
            else:
                buf += ch
        if buf: _run(p, buf, size, color, bold, italic, font, o)


def _run(p, t, size, color, bold, italic, font, o):
    r = p.add_run(); r.text = t; f = r.font
    f.name = o.get('font', font); f.size = Pt(o.get('size', size))
    f.bold = o.get('bold', bold); f.italic = o.get('italic', italic)
    f.color.rgb = rgb(o.get('color', color))


def _fill_tf(tf, lines, size, color, bold, italic, align, font, spacing):
    if isinstance(lines, str): lines = [lines]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        if spacing is not None: p.space_after = Pt(spacing)
        segs = ln if isinstance(ln, list) else [(ln, {})]
        _add_runs(p, segs, size, color, bold, italic, font)


def text(sl, x, y, w, h, lines, size=12, color='white', bold=False, italic=False, align='l',
         anchor='t', font=FONT, spacing=2, fill=None, line=None):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.06); tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    if fill: tb.fill.solid(); tb.fill.fore_color.rgb = rgb(fill)
    if line: tb.line.color.rgb = rgb(line); tb.line.width = Pt(1)
    _fill_tf(tf, lines, size, color, bold, italic, align, font, spacing)
    return tb


def shape(sl, x, y, w, h, kind=MSO_SHAPE.RECTANGLE, fill=None, line=None, lw=1.0, radius=None, dash=False):
    sh = sl.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius is not None: sh.adjustments[0] = radius
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    else: sh.fill.background()
    if line:
        sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        if dash: sh.line.dash_style = MSO_LINE.DASH
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def label(sl, x, y, w, h, lines, fill, color='white', size=12, bold=True, line=None, radius=0.15,
          font=FONT, align='c'):
    sh = shape(sl, x, y, w, h, MSO_SHAPE.ROUNDED_RECTANGLE, fill=fill, line=line, radius=radius)
    tf = sh.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.08); tf.margin_top = tf.margin_bottom = Inches(0.02)
    _fill_tf(tf, lines, size, color, bold, False, align, font, 0)
    return sh


def image(sl, path_or_bytes, x, y, w=None, h=None):
    src = io.BytesIO(path_or_bytes) if isinstance(path_or_bytes, bytes) else path_or_bytes
    kw = {}
    if w: kw['width'] = Inches(w)
    if h: kw['height'] = Inches(h)
    return sl.shapes.add_picture(src, Inches(x), Inches(y), **kw)


def svg_to_png(svg, dpi=220):
    import pymupdf
    return pymupdf.open(stream=svg.encode(), filetype='svg')[0].get_pixmap(dpi=dpi, alpha=True).tobytes('png')


def cross(sl, x, y):
    return shape(sl, x, y, 0.39, 0.40, MSO_SHAPE.MATH_MULTIPLY, fill='red', line='redline')


def tick(sl, x, y, size=26):
    return text(sl, x - 0.04, y - 0.12, 0.6, 0.6, [[S('✔', font=TICKF)]], size=size, color='green', bold=True)


def art_needed(sl, x, y, w, h, brief):
    """Dashed orange box: the art team draws this. Never shipped silently."""
    b = shape(sl, x, y, w, h, MSO_SHAPE.ROUNDED_RECTANGLE, fill='17110A', line='orange', dash=True, radius=0.06)
    tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.08)
    _fill_tf(tf, [[S('ART NEEDED', bold=True, color='orange', size=9)], brief], 8, 'grey', False, False, 'c', FONT, 0)
    return b


def draft_tag(sl, x, y, w=1.9):
    return label(sl, x, y, w, 0.2, 'DRAFT · final art: team or diagram bot', 'orange',
                 color='000000', size=6.5, radius=0.3)


def table(sl, x, y, col_w, row_h, rows, header_fill='violet', size=10, first_col='cyan', border='0058B7',
          body_fill='0A0F16', colors=None):
    """rows[0] = header. colors: optional {(r, c): colour} for single cells."""
    nr, nc = len(rows), len(rows[0])
    gf = sl.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(col_w)), Inches(row_h * nr))
    tb = gf.table; pr = tb._tbl.tblPr
    pr.set('firstRow', '0'); pr.set('bandRow', '0')
    sid = pr.find(A_ + 'tableStyleId')
    if sid is not None: sid.text = '{5940675A-B579-460E-94D1-54222C63F5DA}'
    for j, w in enumerate(col_w): tb.columns[j].width = Inches(w)
    for i in range(nr):
        tb.rows[i].height = Inches(row_h)
        for j in range(nc):
            cell = tb.cell(i, j)
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.01)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            c = (colors or {}).get((i, j)) or ('white' if i == 0 else (first_col if j == 0 else 'white'))
            v = rows[i][j]
            _fill_tf(cell.text_frame, [v if isinstance(v, list) else [(str(v), {})]], size, c, i == 0,
                     False, 'c', FONT, 0)
            tcPr = cell._tc.get_or_add_tcPr()
            for tag in ('lnL', 'lnR', 'lnT', 'lnB'):
                ln = etree.SubElement(tcPr, A_ + tag, w='9525')
                etree.SubElement(etree.SubElement(ln, A_ + 'solidFill'), A_ + 'srgbClr', val=col(border))
            sf = etree.SubElement(tcPr, A_ + 'solidFill')
            etree.SubElement(sf, A_ + 'srgbClr', val=col(header_fill if i == 0 else body_fill))
    return gf


# ---------------------------------------------------------------- click reveals
def add_clicks(sl, steps):
    """steps: list of click steps; each a list of shapes that appear together on that click."""
    steps = [s for s in steps if s]
    if not steps: return
    ids = iter(range(3, 100000)); pars = []
    for step in steps:
        eff = []
        for k, sh in enumerate(step):
            a, b = next(ids), next(ids)
            eff.append(
                f'<p:par><p:cTn id="{a}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" '
                f'nodeType="{"clickEffect" if k == 0 else "withEffect"}"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                f'<p:childTnLst><p:set><p:cBhvr><p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/>'
                f'</p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{sh.shape_id}"/></p:tgtEl><p:attrNameLst>'
                f'<p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/>'
                f'</p:to></p:set></p:childTnLst></p:cTn></p:par>')
        o, i = next(ids), next(ids)
        pars.append(f'<p:par><p:cTn id="{o}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>'
                    f'<p:childTnLst><p:par><p:cTn id="{i}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                    f'<p:childTnLst>{"".join(eff)}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    sl._element.append(etree.fromstring(
        f'<p:timing xmlns:p="{NSP}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
        f'<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
        f'<p:childTnLst>{"".join(pars)}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0">'
        f'<p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0">'
        f'<p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par>'
        f'</p:tnLst></p:timing>'))


# ---------------------------------------------------------------- house slides
def logo(sl, x, y, w):
    """Brand logo from assets/logo.png; without it, three plain shapes stand in."""
    if has_asset('logo.png'):
        return image(sl, ASSET('logo.png'), x, y, w=w)
    s = w / 3.6
    shape(sl, x, y, s, s, MSO_SHAPE.ROUNDED_RECTANGLE, fill='blue', radius=0.1)
    shape(sl, x + s * 1.15, y, s * 1.2, s, MSO_SHAPE.PENTAGON, fill='teal')
    return shape(sl, x + s * 2.3, y, s * 1.2, s, MSO_SHAPE.CHEVRON, fill='green')


def bulb(sl, x, y, h):
    """Light-bulb icon from assets/bulb.png; without it, a yellow dot."""
    if has_asset('bulb.png'):
        return image(sl, ASSET('bulb.png'), x, y, h=h)
    return shape(sl, x + h * 0.15, y + h * 0.1, h * 0.7, h * 0.7, MSO_SHAPE.OVAL, fill='yellow')


def title_slide(prs, title_lines, grade, notes=None):
    sl = blank(prs, notes)
    shape(sl, 8.56, 0, 1.44, 5.625, fill='teal')
    logo(sl, 0.43, 0.23, 1.91)
    text(sl, 0.38, 0.84, 3.2, 0.5, "Let’s study about", 18, 'teal', bold=True, italic=True)
    n = len(title_lines); y0 = 2.6 - 0.41 * n
    for k, t in enumerate(title_lines):
        text(sl, 0.18, y0 + 0.78 * k, 8.3, 0.82, t, 37, 'white', font=BLACK, align='c')
    text(sl, 0.45, 4.25, 5.2, 0.4, f'Science Olympiad Class | Grade {grade}', 14, 'teal2', font='Calibri')
    shape(sl, 0.45, 4.75, 2.63, 0.03, fill='green')
    return sl


def plan_slide(prs, heading, topics, plan_text, notes=None):
    sl = blank(prs, notes)
    shape(sl, 6.9, 2.28, 2.94, 2.94, MSO_SHAPE.OVAL, fill='0B3B37')
    text(sl, 0.25, 0.29, 9.5, 0.6, heading, 28, 'cyan', font=BLACK)
    items = [text(sl, 0.45, 1.05 + 0.36 * k, 6.3, 0.36,
                  [[S(f'{k + 1:02d}  ', color='teal', bold=True), S(t)]], 15) for k, t in enumerate(topics)]
    h = text(sl, 1.15, 2.6, 4.6, 0.6, 'What we’ll do in today’s class!', 21, 'yellow', bold=True)
    b = text(sl, 1.15, 3.2, 5.6, 1.4, plan_text, 15)
    add_clicks(sl, [[it] for it in items] + [[h, b]])
    return sl


SECTION_FILLS = ['blue', 'pink', 'teal2', 'yellow']


def section_slide(prs, n, title, sub="Let’s go ahead and solve questions on this topic", notes=None):
    sl = blank(prs, notes)
    shape(sl, 0, 2.0, 10, 1.8, fill=SECTION_FILLS[(n - 1) % 4])
    text(sl, 0.34, 0.6, 2.6, 0.5, f'SECTION {n}', 23, 'blue', bold=True, font='Calibri')
    logo(sl, 8.63, 0.15, 1.31)
    text(sl, 0.14, 2.5, 9.7, 0.81, title, 36, 'navy', bold=True)
    text(sl, 0.34, 4.59, 6, 0.42, sub, 13, 'green', bold=True, italic=True)
    return sl


def concept_header(sl, title, tag, tag_color='teal', counter=None, recall=None):
    """Theory slide header: blue title pill top-left, topic tag top-right."""
    if recall:
        label(sl, 0.07, 0.07, 1.55, 0.22, recall, 'magenta', color='000000', size=8, radius=0.3)
    t = label(sl, 0.12 if not recall else 1.75, 0.07 if not recall else 0.04, 0.3 + 0.165 * len(title), 0.44,
              title, 'blue', size=20, font=BLACK, bold=False, radius=0.12)
    label(sl, 8.4 - (0.1 if counter else -0.3), 0.08, 1.25, 0.24, tag, '000000', color=tag_color, size=8,
          line=tag_color, radius=0.25)
    if counter:
        text(sl, 9.6, 0.06, 0.4, 0.3, counter, 9, 'dim')
    return t


def card(sl, x, y, w, h, head, head_fill, lines, size=10.5, head_color='000000', line=None):
    """Card with coloured header (Essential Recall style). Returns [border, header, body]."""
    border = shape(sl, x, y, w, h, MSO_SHAPE.ROUNDED_RECTANGLE, fill='card', line=line or head_fill, lw=1.5, radius=0.04)
    hd = label(sl, x + 0.1, y + 0.08, w - 0.2, 0.3, head, head_fill, color=head_color, size=12, radius=0.2)
    body = text(sl, x + 0.08, y + 0.45, w - 0.16, h - 0.5, lines, size, spacing=3)
    return [border, hd, body]


def tip_bar(sl, y, label_text, lines, h=0.5):
    bar = shape(sl, 0.07, y, 9.86, h, MSO_SHAPE.ROUNDED_RECTANGLE, fill='0A0A00', line='yellow', lw=1.5, radius=0.1)
    bl = bulb(sl, 0.18, y + (h - 0.38) / 2, 0.38)
    lab = text(sl, 0.58, y, 1.4, h, label_text, 13, 'yellow', bold=True, anchor='m')
    body = text(sl, 2.0, y, 7.85, h, lines, 10.5, anchor='m')
    return [bar, bl, lab, body]


def revision(prs, title, tag, rows, takeaway):
    """End-of-topic revision: rows of (label, colour, text) revealed one per click, then a takeaway bar."""
    sl = blank(prs)
    concept_header(sl, title, tag)
    steps = []
    for k, (head, colr, body) in enumerate(rows):
        y = 0.75 + k * 0.82
        steps.append([label(sl, 0.25, y, 2.2, 0.6, head, colr, color='000000', size=13),
                      text(sl, 2.6, y, 7.2, 0.65, body, 12, anchor='m')])
    y = 0.75 + len(rows) * 0.82 + 0.1
    bar = shape(sl, 0.07, y, 9.86, 0.55, MSO_SHAPE.ROUNDED_RECTANGLE, fill='0A0A00', line='yellow', lw=1.5, radius=0.1)
    lab = label(sl, 0.15, y + 0.1, 1.5, 0.35, 'Key Takeaway', 'yellow', color='000000', size=11)
    tx = text(sl, 1.75, y, 8.1, 0.55, takeaway, 11, anchor='m')
    add_clicks(sl, steps + [[bar, lab, tx]])
    return sl


# ---------------------------------------------------------------- questions
class Q:
    """One question; render .ask() then .solve() slides in the same anchored layout.

    stem: list of lines (first line starts after 'Qn. ').
    opts: 4 option strings.  fig: optional (png_bytes, w, h, draft:bool, art_brief).
    """

    def __init__(self, num, stem, opts, answer, box_h=None, opt_w=4.0, opt_h=0.42, fig=None, box_w=None,
                 source='★ Olympiad practice'):
        self.num, self.stem, self.opts, self.answer = num, stem, opts, answer
        self.box_h = box_h or (0.14 + len(stem) * 0.255 + 0.12)
        self.opt_w, self.opt_h, self.fig, self.source = opt_w, opt_h, fig, source
        self.box_w = box_w or (6.32 if fig else 9.6)

    # layout anchors (identical on every slide of this question)
    def line_y(self, i): return 0.17 + i * 0.255
    def opt_y(self, k): return 0.12 + self.box_h + 0.12 + k * (self.opt_h + 0.08)
    @property
    def cross_x(self): return 0.90 + self.opt_w + 0.06
    @property
    def steps_x(self): return self.cross_x + 0.5
    @property
    def steps_w(self): return 9.95 - self.steps_x
    @property
    def opts_bottom(self): return self.opt_y(3) + self.opt_h

    def _base(self, sl):
        shape(sl, 0.22, 0.12, self.box_w, self.box_h, MSO_SHAPE.ROUNDED_RECTANGLE, fill='qfill', line='blue',
              lw=1.5, radius=0.06)
        for i, ln in enumerate(self.stem):
            segs = ln if isinstance(ln, list) else [(ln, {})]
            if i == 0:
                segs = [S(f'Q{self.num}. ', color='teal2', bold=True, size=13)] + [(t, dict(o, bold=True)) for t, o in segs]
            text(sl, 0.32, self.line_y(i), self.box_w - 0.2, 0.3, [segs], 12)
        if self.fig:
            png, w, h, draft, brief = self.fig
            fx = 0.22 + self.box_w + 0.12
            if png:
                image(sl, png, fx, 0.12, w=w)
                if draft: draft_tag(sl, fx + (w - 1.9) / 2, 0.12 + h + 0.02)
            else:
                art_needed(sl, fx, 0.12, w, h, brief)
        self.opt_boxes = []
        for k, o in enumerate(self.opts):
            y = self.opt_y(k)
            text(sl, 0.33, y, 0.53, self.opt_h, f'({"ABCD"[k]})', 12, 'orange', bold=True, align='c',
                 anchor='m', fill='optfill', line='optline')
            self.opt_boxes.append(text(sl, 0.90, y, self.opt_w, self.opt_h, o, 11, anchor='m',
                                       fill='optfill', line='optline'))

    def ask(self, prs, notes=None):
        sl = blank(prs, notes)
        self._base(sl)
        label(sl, 9.95 - 1.55, 5.625 - 0.36, 1.5, 0.26, self.source, '000000', color='yellow', size=9,
              line='yellow', radius=0.2)
        return sl

    def solve(self, prs, clicks, notes=None, crossed=(), key_idea=None):
        """clicks: list of dicts {lines, y, h, cross:[letters], tick:bool, overlay:[(x,y,w,h,lines,colour)]}.
        crossed: letters already eliminated on earlier solution slides (drawn statically).
        key_idea: (lines, h) shown as the first click at the top of the steps column."""
        sl = blank(prs, notes)
        self._base(sl)
        for L in crossed:
            cross(sl, self.cross_x, self.opt_y('ABCD'.index(L)) + (self.opt_h - 0.4) / 2)
        steps = []
        if key_idea:
            lines, h, *rest = key_idea
            ky = rest[0] if rest else self.opt_y(0)
            kx, kw = (rest[1], rest[2]) if len(rest) > 1 else (self.steps_x, self.steps_w)
            box = shape(sl, kx, ky, kw, h, MSO_SHAPE.RECTANGLE, fill='000000', line='gold', lw=1.5)
            kl = text(sl, kx + 0.02, ky + 0.02, 1.0, 0.32, 'Key Idea:', 12, 'green', bold=True)
            bl = bulb(sl, kx + 0.85, ky + 0.02, 0.3)
            kb = text(sl, kx + 0.02, ky + 0.3, kw - 0.04, h - 0.32, lines, 11)
            steps.append([box, kl, bl, kb])
        for c in clicks:
            group = []
            if c.get('lines'):
                group.append(text(sl, c.get('x', self.steps_x), c['y'], c.get('w', self.steps_w), c.get('h', 0.6),
                                  c['lines'], c.get('size', 11.5), spacing=3))
            for i, colr in c.get('hl', []):          # recolour a stem line in place (true/false)
                ln = self.stem[i]
                segs = [(t, {}) for t, o in ln] if isinstance(ln, list) else [(ln, {})]
                group.append(text(sl, 0.32, self.line_y(i), self.box_w - 0.2, 0.3, [segs], 12, colr,
                                  fill='qfill'))
            for L in c.get('cross', []):
                group.append(cross(sl, self.cross_x, self.opt_y('ABCD'.index(L)) + (self.opt_h - 0.4) / 2))
            if c.get('tick'):
                k = 'ABCD'.index(self.answer)
                y = self.opt_y(k)
                hl = text(sl, 0.90, y, self.opt_w, self.opt_h, self.opts[k], 11, 'green', anchor='m',
                          fill='optfill', line='green')
                group += [hl, tick(sl, self.cross_x, y + (self.opt_h - 0.4) / 2)]
            for extra in c.get('shapes', []):
                group.append(extra(sl))
            steps.append(group)
        add_clicks(sl, steps)
        return sl
