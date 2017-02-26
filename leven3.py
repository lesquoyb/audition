from tools import *
from leven2 import Levenshtein



def learn() :
    train = parseTrain("data/train-01000items.train")
    (psub, pins, pomi, proba_sub, proba_ins) = parseModeleDiscret()

    for passe in range(5):
        for mot, ref, test in train:
            t = (psub, pins, pomi, proba_sub, proba_ins)
            d, parcours = Levenshtein(ref, test, t)
            ns, ni, no, n, ins = parcours.compter()
            psub = (ns + 1) / (ns + ni + no + 3)
            for c in proba_sub.keys():
                proba_sub[c] = float(n[c]) / sum( [ n[k] + 1 for k in n.keys() if c[0] == k[0] ] ) if c in n.keys() else 0
            for k in proba_ins.keys():
                proba_ins[k] = float(ins[k]) / sum([ins[key]+1 for key in ins.keys()]) if k in ins.keys() else 0

    return psub, pins, pomi, proba_sub, proba_ins
