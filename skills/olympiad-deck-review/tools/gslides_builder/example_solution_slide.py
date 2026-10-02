"""Example: build the batchUpdate requests for ONE 3-pane solution slide.

Run:  python example_solution_slide.py
It writes example_slide.json. The object ids below are placeholders. Replace
PAGE_ID with the real id of the slide you want to fill (read it from the deck
with the Slides connector first). All content here is made up.

Layout: question + options on the left, working in the middle, and on the right
a "Correct Option" box plus a "Key Idea" box.
"""
import json
from lib import *
import lib

PAGE_ID = 'PAGE_ID_FROM_YOUR_DECK'   # <- the slide to fill (placeholder)

# Question, top
shape(PAGE_ID, 'ex_title', 'TEXT_BOX', 0.35, 0.12, 9.3, 0.9, bold=False, size=15, paras=[P(
    'A train travels ', B('120 km'), ' in ', B('2 hours'), '. What is its average speed?')])

# Pane dividers and labels
divider(PAGE_ID, 'ex_div1', 3.2, 1.2, 4.2)
divider(PAGE_ID, 'ex_div2', 6.75, 1.2, 4.2)
pill(PAGE_ID, 'ex_qpill', 0.35, 1.15, 1.45, 0.38, 'Options', size=14)
pill(PAGE_ID, 'ex_spill', 3.4, 1.15, 1.35, 0.38, 'Solution', size=14)

# Left pane: options, with the correct one highlighted
OPTIONS = ['(A)   30 km/h', '(B)   60 km/h', '(C)   90 km/h', '(D)   240 km/h']
CORRECT = 1
for i, text in enumerate(OPTIONS):
    y = 1.7 + i * 0.47
    if i == CORRECT:
        shape(PAGE_ID, f'ex_opt{i}', 'ROUND_RECTANGLE', 0.35, y, 2.6, 0.42, fill=DIMY,
              valign='MIDDLE', size=16, paras=[P(B(text, Y))])
    else:
        shape(PAGE_ID, f'ex_opt{i}', 'TEXT_BOX', 0.4, y, 2.6, 0.42, bold=False,
              valign='MIDDLE', size=16, paras=[P(text)])

# Middle pane: the working
shape(PAGE_ID, 'ex_steps', 'TEXT_BOX', 3.4, 1.65, 3.25, 3.75, bold=False, size=13, paras=[
    P(B('Step 1: '), 'Average speed = distance ÷ time.', below=6),
    P(B('Step 2: '), '120 km ÷ 2 h', below=4),
    P(B('= 60 km/h', Y, 16)),
])

# Right pane: correct-option box (the tick must be an Arial run: see TICK)
shape(PAGE_ID, 'ex_ans', 'ROUND_RECTANGLE', 6.95, 1.7, 2.7, 0.5, fill=DARK, outline=(Y, 2),
      align='CENTER', valign='MIDDLE', size=14, paras=[P(TICK(), B('  Correct Option: (B) 60 km/h', Y))])

# Right pane: key idea box = box + pill + text
shape(PAGE_ID, 'ex_keybox', 'ROUND_RECTANGLE', 6.95, 2.9, 2.7, 1.3, fill=KBOX, outline=(DIV, 1))
pill(PAGE_ID, 'ex_keypill', 7.25, 2.72, 1.3, 0.36, 'Key Idea', size=13)
shape(PAGE_ID, 'ex_keytxt', 'TEXT_BOX', 7.05, 3.12, 2.5, 1.0, bold=False, size=12, paras=[
    P('Speed needs ', B('both', Y), ' distance and time.')])

# A small table (e.g. a data table in the working)
grid(PAGE_ID, 'ex_table', 3.4, 4.4, 0.8, 0.3, [['d (km)', 't (h)', 'v (km/h)'], ['120', '2', '?']], 12)

with open('example_slide.json', 'w', encoding='utf-8') as f:
    json.dump(lib.reqs, f, ensure_ascii=False, separators=(',', ':'))
print('requests:', len(lib.reqs), '-> example_slide.json')
