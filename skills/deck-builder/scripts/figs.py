"""Draft SVG figures (pilot). White line art on transparent bg for a black slide."""


def test_tubes(fills, labels, caption):
    W, H = 560, 330
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             # rack
             '<rect x="30" y="175" width="500" height="16" rx="3" fill="#6B4A2B" stroke="#C9A27A" stroke-width="2"/>',
             '<rect x="45" y="191" width="12" height="70" fill="#6B4A2B"/><rect x="503" y="191" width="12" height="70" fill="#6B4A2B"/>',
             '<rect x="30" y="258" width="500" height="10" rx="3" fill="#6B4A2B" stroke="#C9A27A" stroke-width="2"/>']
    for i, (fill, lab) in enumerate(zip(fills, labels)):
        cx = 100 + i * 120
        x0, x1, top, bot = cx - 22, cx + 22, 40, 230
        liquid_top = 120
        parts.append(  # liquid
            f'<path d="M{x0+3},{liquid_top} L{x1-3},{liquid_top} L{x1-3},{bot-22} A19,19 0 0 1 {x0+3},{bot-22} Z" fill="{fill}"/>')
        parts.append(  # glass
            f'<path d="M{x0},{top} L{x0},{bot-22} A22,22 0 0 0 {x1},{bot-22} L{x1},{top}" fill="none" stroke="#E8F4FF" stroke-width="3"/>')
        parts.append(f'<ellipse cx="{cx}" cy="{top}" rx="24" ry="5" fill="none" stroke="#E8F4FF" stroke-width="3"/>')
        parts.append(f'<rect x="{x0+7}" y="{liquid_top+8}" width="5" height="70" rx="2" fill="#FFFFFF" opacity="0.35"/>')
        parts.append(f'<text x="{cx}" y="300" font-family="Arial" font-size="30" font-weight="bold" fill="#FFFFFF" text-anchor="middle">{lab}</text>')
    parts.append(f'<text x="{W/2}" y="325" font-family="Arial" font-size="22" font-style="italic" fill="#B8BEC8" text-anchor="middle">{caption}</text>')
    parts.append('</svg>')
    return ''.join(parts)


def beaker_dropper(drop_label, beaker_label, liquid='#FF4FD8'):
    W, H = 520, 410
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<!-- dropper -->
<rect x="242" y="10" width="36" height="46" rx="16" fill="#3A3F48" stroke="#E8F4FF" stroke-width="2"/>
<path d="M248,56 L272,56 L268,150 L260,170 L252,150 Z" fill="#DDF3FF" fill-opacity="0.25" stroke="#E8F4FF" stroke-width="2.5"/>
<path d="M251,110 L269,110 L267,150 L260,166 L253,150 Z" fill="#CFE8FF" fill-opacity="0.8"/>
<path d="M260,182 q-6,10 0,14 q6,-4 0,-14 Z" fill="#CFE8FF"/>
<text x="292" y="98" font-family="Arial" font-size="30" fill="#FFFFFF">{drop_label}</text>
<line x1="290" y1="90" x2="274" y2="98" stroke="#B8BEC8" stroke-width="1.5"/>
<!-- beaker -->
<path d="M150,215 L160,370 Q160,385 175,385 L345,385 Q360,385 360,370 L370,215" fill="none" stroke="#E8F4FF" stroke-width="3.5"/>
<path d="M162,262 L358,262 L351,368 Q350,378 340,378 L180,378 Q170,378 169,368 Z" fill="{liquid}" fill-opacity="0.85"/>
<path d="M140,212 L150,215 M370,215 L380,212" stroke="#E8F4FF" stroke-width="3.5"/>
<line x1="345" y1="290" x2="358" y2="290" stroke="#E8F4FF" stroke-width="2"/>
<line x1="345" y1="320" x2="358" y2="320" stroke="#E8F4FF" stroke-width="2"/>
<line x1="345" y1="350" x2="358" y2="350" stroke="#E8F4FF" stroke-width="2"/>
<text x="260" y="404" font-family="Arial" font-size="24" fill="#FFFFFF" text-anchor="middle">{beaker_label}</text>
</svg>'''
