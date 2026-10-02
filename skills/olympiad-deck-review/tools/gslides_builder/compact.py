"""Shrink a batchUpdate JSON file by merging repeated text-style requests.

Usage:  python compact.py batch.json START [END]
Prints the compacted requests from index START up to END (or the end) as one
line of JSON, ready to paste into the connector's update call. The total number
of requests is printed to stderr. Splitting into chunks keeps each call small.
"""
import json, sys


def u16(s):
    return len(s.encode('utf-16-le'))//2


def compact(r):
    """Fold a 'style the whole text' request and a 'style the same full range'
    request into one, so each text box needs fewer requests."""
    texts, allidx, out = {}, {}, []
    for q in r:
        k = next(iter(q)); v = q[k]
        if k == 'insertText' and 'cellLocation' not in v:
            texts[v['objectId']] = u16(v['text'])
        if k == 'updateTextStyle' and 'cellLocation' not in v:
            tr = v['textRange']; o = v['objectId']
            if tr['type'] == 'ALL':
                allidx[o] = len(out)
            elif tr.get('startIndex') == 0 and tr.get('endIndex') == texts.get(o) and o in allidx:
                base = out[allidx[o]]['updateTextStyle']
                base['style'].update(v['style'])
                base['fields'] = ','.join(dict.fromkeys(base['fields'].split(',') + v['fields'].split(',')))
                continue
        out.append(q)
    return out


def rnd(o):
    """Round floats so the JSON stays short."""
    if isinstance(o, float):
        return int(o) if o == int(o) else round(o, 3)
    if isinstance(o, dict):
        return {k: rnd(v) for k, v in o.items()}
    if isinstance(o, list):
        return [rnd(v) for v in o]
    return o


if __name__ == '__main__':
    r = json.load(open(sys.argv[1], encoding='utf-8'))
    a = int(sys.argv[2])
    b = int(sys.argv[3]) if len(sys.argv) > 3 else None
    r = rnd(compact(r))
    print(len(r), file=sys.stderr)
    print(json.dumps(r[a:b], separators=(',', ':')))
