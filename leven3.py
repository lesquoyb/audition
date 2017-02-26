from tools import *
from leven2 import Levenshtein



def learn(hmm, fileName="data/train-01000items.train") :
    train = parseTrain(fileName)
    parcours_list = []

    for mot, ref, test in train:
        parcours_list += [Levenshtein(ref, test, hmm)[1]]


    ns, ni, no, n, ins = 0, 0, 0, {}, {}
    psub, pins, pomi, proba_sub, proba_ins = hmm

    for parcours in parcours_list:
        compte = parcours.compter()
        ns += compte[0]
        ni += compte[1]
        no += compte[2]
        for e in compte[3].keys():
            n[e] = n[e] + compte[3][e] if e in n.keys() else compte[3][e]
        for e in compte[4].keys():
            ins[e] = ins[e] + compte[4][e] if e in ins.keys() else compte[4][e]


    psub = max((ns + 1) / (ns + ni + no + 3), INC_MIN)
    for c in proba_sub.keys():
        proba_sub[c] = max(float(n[c]) / sum( [ n[k] + 1 for k in n.keys() if c[0] == k[0] ] ) if c in n.keys() else INC_MIN, INC_MIN)

    sm = sum( [ins[key]+1 for key in ins.keys()] )
    for k in proba_ins.keys():
        proba_ins[k] = max(float(ins[k]) / sm, INC_MIN) if k in ins.keys() else INC_MIN
    return psub, pins, pomi, proba_sub, proba_ins
