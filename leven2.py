from tools import *
from math import log




def Levenshtein(st1, st2, hmm):
    psub, pins, pomi, proba_sub, proba_ins = hmm
    lst1 = len(st1)
    lst2 = len(st2)

    d = [[0]*(lst2+1) for i in range(lst1+1)]

    for i in range(lst1+1):
        d[i][0] = i
    for i in range(lst2+1):
        d[0][i] = i

    for i in range(0,len(st1)):
        for j in range(0,len(st2)):
            l1 = st1[i]
            l2 = st2[j]

            del_c = - log(pomi) if pomi > 0 else 0
            ins_c = - (log(pins) if pins > 0 else 0) \
                    - ( log(proba_ins[st1[i-1]]) if i > 0 and proba_ins[st1[i-1]] != 0 else 0)
            sub_c = 0 if l1 == l2 else -log(psub) - ( log(proba_sub[(l1, l2)]) if l1 != "" and l2 != "" and proba_sub[(l1,l2)] != 0 else 0)
            d[i+1][j+1] = min(d[i][j+1] + del_c, d[i+1][j] + ins_c, d[i][j] + sub_c)

    return d[-1][-1], backtrack(st1, st2, d)


def levenshtein_btw_files(lex, test, hmm):
    f = open("log2", "w")
    parcours = None
    erreurs = 0
    total = 0

    for k,v in test:
        mini = 99999
        nom = k
        lit = ""
        for kl,vl in lex.items():
            for it in vl:
                d, parcours = Levenshtein(v ,it, hmm)
                if d < mini:
                    mini = d
                    nom = kl
                    lit = it
        l = k + " " + str(v) + " => " + nom + " " + str(lit)
        total += 1
        if k != nom:
            l += " Erreur "
            erreurs += 1
        else:
            l += " Correct "
        l += ("%.1f" % mini) + " <=> " + parcours.print() + "\n"
        f.write(l)
    s = "taux d'erreur: " + str(float(erreurs)/total)
    print(s)
    f.write(s + "\n")
    f.close()
