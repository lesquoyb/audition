from tools import *
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

    return d[-1][-1], backtrack(st1, st2, d)


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
