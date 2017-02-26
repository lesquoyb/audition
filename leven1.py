from tools import *
from math import log


def Levenshtein(st1, st2):
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

            del_c = 1
            ins_c = 1
            sub_c = 0 if l1 == l2 else 1
            d[i+1][j+1] = min(d[i][j+1] + del_c, d[i+1][j] + ins_c, d[i][j] + sub_c)

    return d[-1][-1], backtrack(st1, st2, d)


def levenshtein_btw_files(lex, test):
    l =""
    f = open("log", "w")
    parcours = None

    for k,v in test:
        mini = 99999
        nom = k
        lit = ""

        for kl,vl in lex.items():
            for it in vl:
                try:
                    d, parcours = Levenshtein(v, it)
                except:
                    print(v, it)
                if d < mini:
                    mini = d
                    nom = kl
                    lit = it

        l = k + " " + str(v) + " => " + nom + " " + str(lit) + (" Erreur " if mini > 0 else " Correct ") + ("%.1f" % mini) + " <=> " + parcours.print() + "\n"
        f.write(l)
    f.close()
