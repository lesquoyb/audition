from tools import *
from leven2 import *

from math import log
def Levenshtein(st1, st2, t):
    (psub, pins, pomi, proba_sub, proba_ins) = t
    lst1 = len(st1)
    lst2 = len(st2)

    d =[[0]*(lst2+1) for i in range(lst1+1)]

    for i in range(lst1+1):
        d[i][0] = i
    for i in range(lst2+1):
        d[0][i] = i

    for i in range(0,len(st1)):
        for j in range(0,len(st2)):
            l1 = st1[i]
            l2 = st2[j]

            del_c = - log(pomi)
            ins_c = - log(pins) - ( log(proba_ins[st1[i-1]]) if i > 0 and proba_ins[st1[i-1]] != 0 else 0)
            sub_c = 0 if l1 == l2 else -log(psub) - ( log(proba_sub[(l1, l2)]) if l1 != "" and l2 != "" and proba_sub[(l1,l2)] != 0 else 0)
            d[i+1][j+1] = min(d[i][j+1] + del_c, d[i+1][j] + ins_c, d[i][j] + sub_c)


    parcours = Parcours()
    i,j = len(st1), len(st2)

    while i > 0 or j > 0:
        di = i
        dj = j

        typ = -1
        vals = ("","")

        l1 = st1[i-1]
        l2 = st2[j-1]

        val = d[i][j]

        if i == 0 : #INS
            vals = ("", l2)
            dj = j-1
            typ = 1
        elif j == 0 : #OMI
            vals = (l1, "")
            di = i-1
            typ = 2
        else :
            if d[i-1][j] <= val : #INS
                vals = (l1, "")
                di = i-1
                dj = j
                val = d[i-1][j]
                typ = 1

            if d[i][j-1] <= val : #OMI
                vals = ("", l2)
                di = i
                dj = j-1
                val = d[i][j-1]
                typ = 2

            if d[i-1][j-1] <= val : #SUB
                vals = (l1, l2)
                di = i-1
                dj = j-1
                if d[i-1][j-1] == d[i][j]: #SUB NOP
                    typ = 3
                else: #SUB
                    typ = 0

        i, j = di, dj

        parcours.addTransfo(typ, vals)
    return d[-1][-1], parcours


def levenshtein_btw_files(lex, test):
    t = parseModeleDiscret()
    l =""
    f = open("yolog", "w")
    parcours = None
    #(psub, pins, pomi, proba_sub, proba_ins) = t

    for k,v in test:
        mini = 99999
        nom = k
        lit = ""

        for kl,vl in lex.items():
            for it in vl:
                try:
                    d, parcours = Levenshtein(v ,it, t)
                except:
                    print(v, it)
                if d < mini:
                    mini = d
                    nom = kl
                    lit = it

                l = k + " " + str(v) + " => " + kl + " " + str(it) + (" Erreur " if d > 0 else " Correct ") + ("%.1f" % d) + " <=> " + parcours.print() + "\n"
                f.write(l)
        #ns, ni, no, n, ins = parcours.compter()
        #psub = (ns + 1) / (ns + ni + no + 3)
        #pins, pomi, proba_sub, proba_ins
        #t = (psub, pins, pomi, proba_sub, proba_ins)
    f.close()

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



if __name__ == "__main__":

    learn()

    t = parseModeleDiscret()
    writeModeleDiscret(t, 1)

    '''
    lex = parseLex("data/lexicon-2syll-0100words.lex")
    phonemes = parsePhonemes()
    test = parseYolo("data/test-2syll-0100words.test")
    levenshtein_btw_files(lex, test)
    '''
