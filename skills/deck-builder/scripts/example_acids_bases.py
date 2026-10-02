"""Example: Grade 7 Acids, Bases and Neutralisation class deck (3 topics x 3 questions).

A rudimentary pilot: it shows the build/review flow. Diagrams are drafts; final art should come
from the art team or a separate diagram/image bot prompted with the ART NEEDED briefs.
Run:  python example_acids_bases.py out.pptx
"""
import sys
from deckkit import *
import figs

prs = new_deck()
G = 'green'; R = 'red'


# ================================================================ front
title_slide(prs, ['Acids, Bases and', 'Neutralisation'], 7)
plan_slide(prs, 'Acids, Bases and Neutralisation',
           ['Acids and bases around us', 'Indicators and their colour changes', 'Neutralisation in daily life'],
           'Solve a question first, learn the idea behind it, then use the same thought process on '
           'Olympiad-style variants.')

# ================================================================ TOPIC 1
section_slide(prs, 1, 'Acids and Bases Around Us')

q1 = Q(1, ['Match the substances in Column I with the acids they contain.',
           'Column I:     P. Curd        Q. Vinegar        R. Ant sting        S. Tamarind',
           'Column II:    1. Acetic acid        2. Formic acid        3. Lactic acid        4. Tartaric acid',
           'Which option matches them correctly?'],
       ['P–1, Q–3, R–2, S–4', 'P–2, Q–1, R–3, S–4', 'P–3, Q–1, R–2, S–4', 'P–3, Q–1, R–4, S–2'], 'C', opt_w=2.6)
N1 = ('Q1 — Answer (C) P–3, Q–1, R–2, S–4.\nCurd: lactic acid (P–3) removes A and B. Ant sting: formic acid (R–2) '
      'removes D. Check C: vinegar = acetic acid (Q–1), tamarind = tartaric acid (S–4).\n'
      'Teaching move: start with the pair you are surest of and eliminate; you rarely need all four.')
q1.ask(prs, N1)
q1.solve(prs, [
    dict(y=2.45, h=0.55, lines=['Curd → lactic acid (the acid that makes milk sour).', [S('So P–3. ', color=G, bold=True), S('A and B say otherwise.')]], cross='AB'),
    dict(y=3.05, h=0.55, lines=['Ant sting → formic acid.', [S('So R–2. ', color=G, bold=True), S('D says R–4.')]], cross='D'),
    dict(y=3.65, h=0.55, lines=['Check C: vinegar → acetic acid (Q–1), tamarind → tartaric acid (S–4).']),
    dict(y=4.25, h=0.4, lines=[[S('Answer: (C)', color=G, bold=True, size=13)]], tick=True),
], N1, key_idea=(['Each natural acid comes from a known source. Start with the pair you are surest of, then eliminate.'], 0.8))

# --- theory 1a
sl = blank(prs)
concept_header(sl, 'Acids, Bases and Neutral Substances', 'Acids & Bases', recall='ESSENTIAL RECALL 1', counter='1/2')
cards = [
    card(sl, 0.12, 0.62, 3.2, 3.6, 'Acids', 'yellow',
         ['• Taste sour.', '• Found in foods: lemon, curd, tamarind, vinegar.',
          '• Lab acids: hydrochloric acid, sulphuric acid. Strong acids are corrosive.']),
    card(sl, 3.40, 0.62, 3.2, 3.6, 'Bases', 'cyan',
         ['• Taste bitter and feel soapy to touch.', '• Found in soap, baking soda, lime water, window cleaner, milk of magnesia.',
          [S('• Bases that dissolve in water are called '), S('alkalis', color='cyan', bold=True), S('. Not all bases dissolve.')]]),
    card(sl, 6.68, 0.62, 3.2, 3.6, 'Neutral', 'pink',
         ['• Neither acidic nor basic.', '• Examples: pure water, sugar solution, common salt solution.']),
]
arts = [art_needed(sl, 0.27, 3.0, 2.9, 1.1, 'Icons: lemon, curd bowl, tamarind, vinegar bottle'),
        art_needed(sl, 3.55, 3.0, 2.9, 1.1, 'Icons: soap bar, baking soda, lime water bottle'),
        art_needed(sl, 6.83, 3.0, 2.9, 1.1, 'Icons: glass of water, sugar, salt')]
tip = tip_bar(sl, 4.4, 'Olympiad Tip:', ['Never taste or touch a chemical to identify it. Olympiad questions test acids and bases with indicators (next section).'])
add_clicks(sl, [cards[0] + [arts[0]], cards[1] + [arts[1]], cards[2] + [arts[2]], tip])

# --- theory 1b
sl = blank(prs)
concept_header(sl, 'Acids in Nature', 'Acids & Bases', recall='ESSENTIAL RECALL 1', counter='2/2')
pairs = [('Lemon, orange', 'Citric acid'), ('Curd', 'Lactic acid'), ('Vinegar', 'Acetic acid'),
         ('Tamarind', 'Tartaric acid'), ('Ant sting', 'Formic acid'), ('Tomato, spinach', 'Oxalic acid'),
         ('Amla', 'Ascorbic acid (vitamin C)')]
steps = []
for k, (src, acid) in enumerate(pairs):
    y = 0.7 + k * 0.5
    steps.append([label(sl, 0.4, y, 2.2, 0.38, src, 'yellow', color='000000', size=12),
                  text(sl, 2.7, y, 0.5, 0.38, '→', 16, 'white', anchor='m', align='c'),
                  text(sl, 3.25, y, 3.2, 0.38, acid, 14, 'cyan', bold=True, anchor='m')])
art = art_needed(sl, 6.7, 0.7, 3.1, 3.3, 'One small icon per source, beside each row (lemon, curd, vinegar, tamarind, ant, tomato, amla).')
tip = tip_bar(sl, 4.4, 'Olympiad Tip:', ['Match-the-column questions pair a source with its acid. Learn this table in both directions.'])
add_clicks(sl, [steps[0] + [art]] + steps[1:] + [tip])

q2 = Q(2, ['Read the statements below.',
           'I.     Soaps and detergents are basic in nature.',
           'II.    All bases are alkalis.',
           'III.   Baking soda is basic in nature.',
           'IV.   We should never taste a substance to find out whether it is an acid or a base.',
           'Which of the statements are correct?'],
       ['I, III and IV only', 'I, II and III only', 'II and IV only', 'I, II, III and IV'], 'A', opt_w=2.6)
N2 = ('Q2 — Answer (A) I, III and IV only.\nII is false: alkalis are bases that dissolve in water, so every alkali is a base '
      'but not every base is an alkali. Removing II removes B and D; C misses I and III.')
q2.ask(prs, N2)
q2.solve(prs, [
    dict(y=2.8, h=0.5, hl=[(1, G)], lines=[[S('I  ✔  ', color=G, bold=True), S('Soaps and detergents feel soapy: a property of bases.')]]),
    dict(y=3.3, h=0.75, hl=[(2, R)], cross='BD', lines=[[S('II  ✖  ', color=R, bold=True), S('Only bases that dissolve in water are alkalis. Every alkali is a base, but not every base is an alkali.')]]),
    dict(y=4.05, h=0.5, hl=[(3, G), (4, G)], cross='C', lines=[[S('III, IV  ✔  ', color=G, bold=True), S('Baking soda is basic; tasting chemicals can harm you.')]]),
    dict(y=4.6, h=0.4, lines=[[S('Answer: (A)', color=G, bold=True, size=13)]], tick=True),
], N2, key_idea=(['Test each statement. One false statement rules out every option that contains it.'], 0.7))

q3 = Q(3, ['Read the Assertion (A) and the Reason (R).',
           'Assertion (A): Curd tastes sour.',
           'Reason (R): Curd is made from milk.',
           'Choose the correct option.'],
       ['Both A and R are true, and R is the correct explanation of A.',
        'Both A and R are true, but R is not the correct explanation of A.',
        'A is true, but R is false.', 'A is false, but R is true.'], 'B', opt_w=4.6)
N3 = ('Q3 — Answer (B).\nA is true (curd contains lactic acid). R is true (curd is made from milk). But R does not explain '
      'the sour taste — milk is not sour; the lactic acid formed in curd is. So both true, R not the explanation.')
q3.ask(prs, N3)
q3.solve(prs, [
    dict(y=2.45, h=0.55, hl=[(1, G)], cross='D', lines=[[S('A is true: ', color=G, bold=True), S('curd contains lactic acid.')]]),
    dict(y=3.0, h=0.55, hl=[(2, G)], cross='C', lines=[[S('R is true: ', color=G, bold=True), S('curd is made from milk.')]]),
    dict(y=3.55, h=0.95, cross='A', lines=['Does R explain WHY curd is sour? No. Milk is not sour; the lactic acid in curd is.']),
    dict(y=4.55, h=0.4, lines=[[S('Answer: (B)', color=G, bold=True, size=13)]], tick=True),
], N3, key_idea=(['First check A and R separately. Only then ask: does R explain A?'], 0.8))

revision(prs, 'Quick Revision', 'Acids & Bases', [
    ('Acids', 'yellow', 'Sour. Natural acids: citric, lactic, acetic, tartaric, formic, oxalic, ascorbic.'),
    ('Bases', 'cyan', 'Bitter and soapy. Alkalis are bases that dissolve in water.'),
    ('Neutral', 'pink', 'Neither acidic nor basic: water, sugar solution, salt solution.'),
    ('Safety', 'orange', 'Never taste or touch to test. Use indicators instead.'),
], 'Know the source of each natural acid, and remember: every alkali is a base, but not every base is an alkali.')

# ================================================================ TOPIC 2
section_slide(prs, 2, 'Indicators and Colour Changes')

tubes = svg_to_png(figs.test_tubes(['#C0392B', '#F2C200', '#C0392B', '#F2C200'], 'PQRS', 'after adding turmeric solution'))
q4 = Q(4, ['Turmeric solution is added to four test tubes P, Q, R and S.',
           'P and R turn red, while Q and S stay yellow (see figure).',
           'Which set could be the solutions in P, Q, R and S, in that order?'],
       ['Lemon juice, soap solution, vinegar, salt solution', 'Lime water, baking soda solution, soap solution, lemon juice',
        'Salt solution, lime water, soap solution, vinegar', 'Soap solution, vinegar, lime water, sugar solution'], 'D',
       opt_w=4.0, fig=(tubes, 3.2, 1.89, True, None))
N4 = ('Q4 — Answer (D).\nTurmeric turns red only in a base, so P and R are bases; Q and S are acidic or neutral.\n'
      'A: P is lemon juice (acid) ✖. C: P is salt solution (neutral) ✖. B: Q is baking soda solution (basic, would turn red) ✖.\n'
      'D: soap (base, red), vinegar (acid, yellow), lime water (base, red), sugar (neutral, yellow) ✔.\n'
      'FIGURE: rudimentary pilot draft by Claude. For the final version, prompt a diagram/image bot (or the art team) with this brief (four test tubes in a rack, P and R red, Q and S yellow).')
q4.ask(prs, N4)
q4.solve(prs, [
    dict(y=3.1, h=0.75, cross='AC', lines=['P must be a base. A puts lemon juice (acid) in P; C puts salt solution (neutral) in P.']),
    dict(y=3.85, h=0.55, cross='B', lines=['Q must NOT be a base. B puts baking soda solution in Q.']),
    dict(y=4.4, h=0.55, lines=['D: soap ✔, vinegar ✔, lime water ✔, sugar solution ✔']),
    dict(y=4.95, h=0.4, lines=[[S('Answer: (D)', color=G, bold=True, size=13)]], tick=True),
], N4, key_idea=(['Turmeric turns red only in a base. So P and R are bases; Q and S are acidic or neutral.'], 0.76, 2.28))

# --- theory 2a
sl = blank(prs)
concept_header(sl, 'Indicators', 'Indicators', recall='ESSENTIAL RECALL 2', counter='1/2')
intro = text(sl, 0.3, 0.6, 9.4, 0.4, [[S('Indicators', color='cyan', bold=True), S(' are substances that show a different colour in acidic and basic solutions.')]], 13)
cards = [
    card(sl, 0.12, 1.1, 3.2, 3.15, 'Litmus', 'violet',
         ['• Natural dye from lichens.', '• Used as red or blue paper strips.', '• Acid: blue → red.', '• Base: red → blue.']),
    card(sl, 3.40, 1.1, 3.2, 3.15, 'Turmeric', 'yellow',
         ['• Yellow in acids and neutral solutions.', '• Turns red in a base.']),
    card(sl, 6.68, 1.1, 3.2, 3.15, 'China rose', 'magenta',
         ['• Acid: dark pink (magenta).', '• Base: green.']),
]
arts = [art_needed(sl, 0.27, 3.05, 2.9, 1.05, 'Red and blue litmus strips before and after dipping'),
        art_needed(sl, 3.55, 3.05, 2.9, 1.05, 'Turmeric paper: yellow strip, red after soap'),
        art_needed(sl, 6.83, 3.05, 2.9, 1.05, 'China rose flower + magenta and green tubes')]
tip = tip_bar(sl, 4.45, 'Olympiad Tip:', ['Turmeric and phenolphthalein only “switch on” in a base. They cannot tell an acid from a neutral solution.'])
add_clicks(sl, [[intro], cards[0] + [arts[0]], cards[1] + [arts[1]], cards[2] + [arts[2]], tip])

# --- theory 2b: colour chart, one row per click
sl = blank(prs)
concept_header(sl, 'Indicator Colour Chart', 'Indicators', recall='ESSENTIAL RECALL 2', counter='2/2')
cw = [2.4, 2.4, 2.4, 2.2]
table(sl, 0.3, 0.75, cw, 0.48, [['Indicator', 'In acid', 'In base', 'In neutral']], size=12)
rows = [['Litmus', 'Blue → red', 'Red → blue', 'No change'],
        ['Turmeric', 'Stays yellow', 'Red', 'Stays yellow'],
        ['China rose', 'Dark pink', 'Green', 'No change'],
        ['Phenolphthalein', 'Colourless', 'Pink', 'Colourless']]
rc = [{(0, 1): 'FF6B6B', (0, 2): '6BA8FF'}, {(0, 1): 'yellow', (0, 2): 'FF6B6B'},
      {(0, 1): 'magenta', (0, 2): 'green'}, {(0, 2): 'magenta'}]
steps = [[table(sl, 0.3, 1.23 + k * 0.52, cw, 0.52, [r], size=12, header_fill='0A0F16', colors=rc[k])] for k, r in enumerate(rows)]
tip = tip_bar(sl, 4.45, 'Olympiad Tip:', ['Phenolphthalein is a lab indicator: colourless in acid, pink in base. You will see it again in neutralisation.'])
add_clicks(sl, steps + [tip])

q5 = Q(5, ['A solution X turns China rose indicator green.',
           'Which of these will X also do?',
           'I.     Turn red litmus blue',
           'II.    Turn turmeric solution red',
           'III.   Turn blue litmus red',
           'IV.   Turn phenolphthalein pink'],
       ['I and II only', 'I, II and IV only', 'III only', 'II and IV only'], 'B', opt_w=2.6)
N5 = ('Q5 — Answer (B) I, II and IV only.\nGreen with China rose means X is basic. A base turns red litmus blue (I), turmeric red (II) '
      'and phenolphthalein pink (IV). Turning blue litmus red (III) is what an acid does.')
q5.ask(prs, N5)
q5.solve(prs, [
    dict(y=2.8, h=0.55, hl=[(2, G), (3, G)], cross='CD', lines=[[S('I, II  ✔  ', color=G, bold=True), S('a base turns red litmus blue and turmeric red.')]]),
    dict(y=3.35, h=0.55, hl=[(4, R)], lines=[[S('III  ✖  ', color=R, bold=True), S('turning blue litmus red is what an ACID does.')]]),
    dict(y=3.9, h=0.55, hl=[(5, G)], cross='A', lines=[[S('IV  ✔  ', color=G, bold=True), S('phenolphthalein turns pink in a base.')]]),
    dict(y=4.5, h=0.4, lines=[[S('Answer: (B)', color=G, bold=True, size=13)]], tick=True),
], N5, key_idea=(['China rose turns green only in a base, so X is basic.'], 0.62))

q6 = Q(6, ['Three unlabelled bottles contain dilute hydrochloric acid, sodium hydroxide solution and',
           'sugar solution. Raj has ONLY red litmus paper.',
           'Which plan identifies all three bottles?'],
       ['Dip red litmus in each. The one that turns it blue is sodium hydroxide. Dip that blue strip into the other two: the one that turns it red is the acid.',
        'It cannot be done with only red litmus paper.',
        'Mix the bottles two at a time. The pair that gets warm is the acid and the base, so the third bottle is sugar solution.',
        'Dip red litmus in each. The bottle that leaves it unchanged is sugar solution.'], 'A', opt_w=8.3, opt_h=0.5)
N6 = ('Q6 — Answer (A).\nRed litmus shows only a base. Acid and sugar both leave it red, so D cannot separate them, but B is too '
      'pessimistic. Once a strip is blue (from NaOH), it detects an acid: acid turns it back red, sugar leaves it blue.\n'
      'C finds the sugar bottle but cannot tell which warm bottle is the acid; it also involves feeling chemicals by hand.')
q6.ask(prs, N6)
q6.solve(prs, [
    dict(x=0.33, w=9.4, y=3.58, h=0.32, lines=[[S('Key idea: ', color=G, bold=True), S('red litmus only detects a base, but a strip turned blue by a base can then detect an acid.')]]),
    dict(x=0.33, w=9.4, y=3.92, h=0.48, cross='BD', lines=[[S('Step 1: ', color='teal2', bold=True), S('Red litmus in all three: only sodium hydroxide turns it blue. Acid and sugar both leave it red, so D is incomplete, and B is wrong.')]]),
    dict(x=0.33, w=9.4, y=4.42, h=0.32, lines=[[S('Step 2: ', color='teal2', bold=True), S('Dip the now-blue strip into the other two. The acid turns it red; sugar solution leaves it blue.')]]),
    dict(x=0.33, w=9.4, y=4.76, h=0.32, cross='C', lines=['C finds sugar, but cannot tell which warm bottle is the acid.']),
    dict(x=0.33, w=9.4, y=5.1, h=0.35, lines=[[S('Answer: (A)', color=G, bold=True, size=13)]], tick=True),
], N6)

revision(prs, 'Quick Revision', 'Indicators', [
    ('Litmus', 'violet', 'Acid: blue → red.   Base: red → blue.'),
    ('Turmeric', 'yellow', 'Red only in a base; yellow in acid and neutral.'),
    ('China rose', 'magenta', 'Acid: dark pink.   Base: green.'),
    ('Phenolphthalein', 'pink', 'Pink only in a base; colourless otherwise.'),
], 'A colour change tells you the nature of a solution. If an indicator only changes in a base, it cannot separate acids from neutral solutions.')

# ================================================================ TOPIC 3
section_slide(prs, 3, 'Neutralisation in Daily Life')

beaker = svg_to_png(figs.beaker_dropper('dilute HCl', 'NaOH solution + phenolphthalein'))
q7 = Q(7, ['Phenolphthalein is added to sodium hydroxide solution in a beaker.',
           'Dilute hydrochloric acid is then added drop by drop, with stirring.',
           'I.     The solution is pink at the start.',
           'II.    The pink colour disappears once all the base is neutralised.',
           'III.   The beaker becomes slightly cold.',
           'IV.   Salt and water are formed.',
           'Which statements are correct?'],
       ['I and III only', 'II and IV only', 'I, II and IV only', 'I, II, III and IV'], 'C', opt_w=2.6,
       fig=(beaker, 2.9, 2.29, True, None))
N7 = ('Q7 — Answer (C) I, II and IV only.\nI: NaOH is a base, phenolphthalein is pink ✔. II: once the base is used up, the solution is no '
      'longer basic, so the pink goes ✔. III: neutralisation releases heat, so the beaker gets slightly WARM ✖. IV: acid + base → salt + water ✔.\n'
      'FIGURE: rudimentary pilot draft by Claude. For the final version, prompt a diagram/image bot (or the art team) with this brief (dropper of dilute HCl over a beaker of pink solution).')
q7.ask(prs, N7)
q7.solve(prs, [
    dict(y=3.35, h=0.5, hl=[(2, G)], lines=[[S('I  ✔  ', color=G, bold=True), S('NaOH is a base, so phenolphthalein is pink.')]]),
    dict(y=3.85, h=0.75, hl=[(3, G)], cross='B', lines=[[S('II  ✔  ', color=G, bold=True), S('acid uses up the base. With no base left, the pink colour goes.')]]),
], N7, key_idea=(['Phenolphthalein is pink only in a base. Acid + base → salt + water + heat.'], 0.62, 2.65))
q7.solve(prs, [
    dict(y=2.7, h=0.75, hl=[(4, R)], cross='AD', lines=[[S('III  ✖  ', color=R, bold=True), S('neutralisation gives out heat. The beaker gets slightly WARM.')]]),
    dict(y=3.45, h=0.75, hl=[(5, G)], lines=[[S('IV  ✔  ', color=G, bold=True), S('acid + base → salt + water (here, sodium chloride + water).')]]),
    dict(y=4.25, h=0.4, lines=[[S('Answer: (C)', color=G, bold=True, size=13)]], tick=True),
], N7, crossed='B')

# --- theory 3a: neutralisation equation, one pill per click
sl = blank(prs)
concept_header(sl, 'Neutralisation', 'Neutralisation', recall='ESSENTIAL RECALL 3', counter='1/2')
intro = text(sl, 0.3, 0.62, 9.4, 0.6, [[S('When an acid and a base react, they cancel each other out. This is '), S('neutralisation', color='cyan', bold=True), S('.')]], 13)
parts = [('Acid', 'FF6B6B'), ('+', None), ('Base', 'cyan'), ('→', None), ('Salt', 'yellow'), ('+', None), ('Water', '6BA8FF'), ('+', None), ('Heat', 'orange')]
x = 0.35; eq = []
for t, c in parts:
    if c:
        eq.append(label(sl, x, 1.45, 1.35, 0.5, t, '000000', color=c, size=18, line=c)); x += 1.45
    else:
        eq.append(text(sl, x - 0.05, 1.45, 0.45, 0.5, t, 20, 'white', anchor='m', align='c')); x += 0.35
ex = text(sl, 0.3, 2.2, 6.0, 0.9, [[S('Example: ', color='teal2', bold=True), S('hydrochloric acid + sodium hydroxide → sodium chloride + water')],
                                   'The heat makes the mixture slightly warm.'], 12.5, spacing=6)
art = art_needed(sl, 6.6, 2.15, 3.2, 2.1, 'Beaker diagram: base + phenolphthalein (pink) turning colourless as acid is added (same art as Q7)')
after = text(sl, 0.3, 3.2, 6.0, 0.9, ['The solution formed is neither acidic nor basic (if the amounts are just right).'], 12.5)
tip = tip_bar(sl, 4.45, 'Olympiad Tip:', ['Watch for traps: neutralisation gives out heat (warm, not cold), and adding a NEUTRAL substance like sugar neutralises nothing.'])
add_clicks(sl, [[intro], eq[0:1], eq[1:3], eq[3:5], eq[5:9], [ex, art], [after], tip])

# --- theory 3b: daily life cards
sl = blank(prs)
concept_header(sl, 'Neutralisation in Daily Life', 'Neutralisation', recall='ESSENTIAL RECALL 3', counter='2/2')
data = [('Indigestion', 'yellow', ['Too much acid in the stomach.', [S('Fix: '), S('milk of magnesia', color='cyan', bold=True), S(' (a mild base).')]], 'Stomach + antacid bottle'),
        ('Ant bite', 'cyan', ['Ant injects formic acid into the skin.', [S('Fix: rub '), S('baking soda', color='cyan', bold=True), S(' paste or calamine.')]], 'Ant on an arm, red bump'),
        ('Soil', 'pink', ['Acidic soil: add ', [S('quicklime / slaked lime', color='cyan', bold=True), S('.')], 'Basic soil: add organic matter (compost).'], 'Farmer spreading lime on a field'),
        ('Factory waste', 'teal2', ['Acidic waste would harm water life.', [S('Fix: '), S('neutralise with a base', color='cyan', bold=True), S(' before release.')]], 'Factory pipe into a river')]
steps = []
for k, (head, colr, lines, brief) in enumerate(data):
    x = 0.12 + k * 2.46
    steps.append(card(sl, x, 0.62, 2.36, 3.7, head, colr, lines, size=10.5) + [art_needed(sl, x + 0.1, 2.95, 2.16, 1.25, brief)])
tip = tip_bar(sl, 4.5, 'Olympiad Tip:', ['Every fix adds a base to cancel an acid. Ask: where is the acid — stomach, skin, soil or water?'])
add_clicks(sl, steps + [tip])

q8 = Q(8, ['Match each problem with the substance used to treat it.',
           'P. Indigestion        Q. Ant bite        R. Acidic soil        S. Acidic factory waste',
           '1. Baking soda paste      2. Milk of magnesia      3. Slaked lime      4. A basic substance, before release',
           'Which option is correct?'],
       ['P–2, Q–1, R–3, S–4', 'P–1, Q–2, R–3, S–4', 'P–2, Q–3, R–1, S–4', 'P–4, Q–1, R–3, S–2'], 'A', opt_w=2.6)
N8 = ('Q8 — Answer (A) P–2, Q–1, R–3, S–4.\nIndigestion: milk of magnesia (swallowed mild base) → P–2, removes B and D. '
      'Ant bite: baking soda paste on skin → Q–1, removes C. R–3 (slaked lime for acidic soil), S–4.')
q8.ask(prs, N8)
q8.solve(prs, [
    dict(y=2.45, h=0.55, cross='BD', lines=[[S('P: ', color=G, bold=True), S('stomach acid → milk of magnesia, a base you can swallow. P–2.')]]),
    dict(y=3.0, h=0.55, cross='C', lines=[[S('Q: ', color=G, bold=True), S('formic acid in the skin → baking soda paste. Q–1.')]]),
    dict(y=3.55, h=0.55, lines=['R: slaked lime for acidic soil (R–3); S: neutralise with a base (S–4).']),
    dict(y=4.15, h=0.4, lines=[[S('Answer: (A)', color=G, bold=True, size=13)]], tick=True),
], N8, key_idea=(['Each fix adds a base to cancel an acid. Match by where the acid is.'], 0.8))

q9 = Q(9, ['Which of these is NOT an example of neutralisation?'],
       ['Rubbing baking soda paste on an ant sting', 'Taking milk of magnesia for acidity',
        'Adding slaked lime to acidic soil', 'Adding sugar to lemon juice so it tastes less sour'], 'D', opt_w=4.3)
N9 = ('Q9 — Answer (D).\nA, B and C each have a base reacting with an acid. Sugar is neutral: it only hides the sour taste; the citric '
      'acid is still there. Trap: “tastes less sour” sounds like neutralisation but is not.')
q9.ask(prs, N9)
q9.solve(prs, [
    dict(y=1.6, h=0.75, cross='ABC', lines=['A, B, C: a base (baking soda, milk of magnesia, slaked lime) reacts with an acid.']),
    dict(y=2.4, h=0.75, lines=['D: sugar is neutral. It only hides the sour taste; the citric acid is still there.']),
    dict(y=3.2, h=0.4, lines=[[S('Answer: (D)', color=G, bold=True, size=13)]], tick=True),
], N9, key_idea=(['Neutralisation needs an acid AND a base reacting to form a salt and water.'], 0.75))

revision(prs, 'Quick Revision', 'Neutralisation', [
    ('Reaction', 'yellow', 'Acid + base → salt + water + heat (gets warm).'),
    ('Indicator', 'magenta', 'Phenolphthalein: pink in base, goes colourless once the base is used up.'),
    ('Daily life', 'cyan', 'Milk of magnesia, baking soda, slaked lime, treating factory waste.'),
    ('Trap', 'orange', 'Sugar or water only dilute or mask taste. They do not neutralise.'),
], 'Neutralisation always needs both an acid and a base, and it always gives out heat.')

# ================================================================ answer key
sl = blank(prs)
concept_header(sl, 'Answer Key', 'Summary')
key = [['Q', '1', '2', '3', '4', '5', '6', '7', '8', '9'], ['Answer', 'C', 'A', 'B', 'D', 'B', 'A', 'C', 'A', 'D']]
t = table(sl, 0.6, 1.0, [1.2] + [0.85] * 9, 0.55, key, size=16)
tp = [text(sl, 0.6, 2.4 + k * 0.55, 8.8, 0.5, [[S(h, color=c, bold=True), S(b)]], 13) for k, (h, c, b) in enumerate([
    ('Topic 1  ', 'yellow', 'Acids and bases around us: Q1, Q2, Q3'),
    ('Topic 2  ', 'magenta', 'Indicators: Q4, Q5, Q6'),
    ('Topic 3  ', 'cyan', 'Neutralisation: Q7, Q8, Q9')])]
add_clicks(sl, [[t]] + [[x] for x in tp])

out = sys.argv[1] if len(sys.argv) > 1 else 'g7_ab.pptx'
prs.save(out)
print('saved', out, len(prs.slides), 'slides')
