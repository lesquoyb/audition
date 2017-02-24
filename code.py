
class Parcours:

    SUB = 0
    INS = 1
    OMI = 2
    NOP = 3

    def __init__(self):
        self.transfo = []

    def addTransfo(self, type, values):
        self.transfo.insert(0, (type, values)) #values étant un couple

    def compter(self):
        ns, ni, no = 0,0,0
        n = {}
        ins = {}
        for op, val in self.transfo:
            if op == self.SUB:
                ns += 1
                n[val] = n[val] + 1 if val in n.keys() else 1
                n[(val[1],val[0])] = n[val]
            elif op == self.INS:
                ni += 1
                ins[val] = ins[val] + 1 if val in ins.keys() else 1
                ins[val[1], val[0]] = ins[val]
            elif op == self.OMI:
                no += 1

        return ns, ni, no, n, ins


    def print(self):
        r = ""
        for typ, transfo in self.transfo:
            #print(typ, transfo)
            bef, aft = transfo
            r += " (" + bef + "=>" + aft + ")" #TODO
        return r


def parseYolo(fileName):
    f = open(fileName)
    assoc = []
    for line in f.readlines():
        line = line[:-1]
        key = line.split("\t")[0]
        val = line.split("\t")[1].split(" ")
        assoc += [(key, val)]
    return assoc


def parseLex(fileName):
    f = open(fileName)
    assoc = {}
    for line in f.readlines():
            line = line[:-1]
            key = line.split("\t")[0]
            val = line.split("\t")[1].split(" ")
            if key in assoc:
                if val not in assoc[key]:
                    assoc[key] += [val]
            else:
                assoc[key] = [val]
    return assoc

def parseModeleDiscret():
    f = open("data/modele_discret_initialise.dat")

    f.readline() #BALEK - Psub;Pins;Pomi
    line = f.readline()[:-1]
    (psub,pins,pomi) = tuple(line.split(";"))

    proba_sub = {}
    proba_ins = {}

    f.readline() #BALEK #Une ligne par symbole de reference; ....
    line = f.readline()[0:-1]
    phons = line.split(";")[1:]

    for i in range(len(phons)):
        line = f.readline()[:-1]
        phon = line.split(";")[0]
        data = line.split(";")[1:]
        for j in range (len(data)):
            proba_sub[(phon, phons[j])] = float(data[j])

    f.readline()[-1] #BALEK - Proba insertions...

    line = f.readline()[:-1]
    data = line.split(";")[1:]

    for i in range(len(phons)):
        proba_ins[(phons[i])] = float(data[i])

    return (float(psub), float(pins), float(pomi), proba_sub, proba_ins)

def parsePhonemes():
    return open("data/liste_symboles.dat").read().split("\n")[:-1]


from math import log
def Levenshtein(st1, st2, t ):
    (psub, pins, pomi, proba_sub, proba_ins) = t
    d =[[0]*len(st2) for i in range(len(st1))]

    for i in range(len(st1)):
        d[i][0] = i
    for i in range(len(st2)):
        d[0][i] = i

    for i in range(1,len(st1)):
        for j in range(1,len(st2)):
            del_c = - log(pomi)
            ins_c = -log(pins) - log(proba_ins[st1[i]])
            sub_c = 0 if st1[i] == st2[j] else -log(psub) - log(proba_sub[(st1[i], st2[j])])
            d[i][j] = min(d[i-1][j] + del_c, d[i][j-1] + ins_c, d[i-1][j-1] + sub_c)
    parcours = Parcours()
    i,j = len(st1)-1, len(st2)-1
    while i >= 0 or j >= 0:
        typ = -1
        vals = ("","")
        val = d[i][j]
        if i>0 and d[i-1][j] < val: # INS
            ti = i -1
            tj = j
            val = d[ti][tj]

            typ = 0
            vals = (st1[i], "")
        if j>0:
            if d[i][j-1] < val: # OMI
                ti = i
                tj = j -1
                val = d[ti][tj]

                typ = 1
                vals = ( "", st2[j])
            if i>0:
                ti = i -1
                tj = j -1
                if d[i-1][j-1] < val: # SUB
                    typ = 2
                    vals = (st1[i], st2[j])

        if typ == -1 : # SAME
            typ = 3
            vals = (st1[i], st2[j])
            ti = i -1
            tj = j -1

        parcours.addTransfo(typ, vals)
        i,j = ti,tj
    for l in d:
        for i in l:
            s = " %d " % i if l == d[0] or i == l[0] else "%0.1f" % i
            print(s, end=" ")
        print()
    return d[-1][-1], parcours


def levenshtein_btw_files(lex, test):
    """Pour chaque suite de phonèmes du fichier test
          • Comparaison à toutes les suites de phonèmes du fichier lexique
          avec la distance de Levenshtein
          • La distance la plus faible identifie le mot reconnu
          • Comparer le mot du test avec le mot reconnu pour compter les erreur
    """
    t = parseModeleDiscret()
    l =""
    f = open("yolooooo", "w")
    parcours = None
    (psub, pins, pomi, proba_sub, proba_ins) = t
    for k,v in test:
        mini = 99999
        nom = k
        lit = ""
        for kl,vl in lex.items():
            for it in vl:
                d, parcours = Levenshtein(v ,it, t)
                if d < mini:
                    mini = d
                    nom = kl
                    lit = it

                l += k + " " + str(v) + " => " + kl + " " + str(it) + (" Erreur " if d > 0 else " Correct ") + str(d) + " <=> " + parcours.print() + "\n"
                print(k + " " + kl + " " +parcours.print())
                #print(l)

        ns, ni, no, n, ins = parcours.compter()
        psub = (ns + 1) / (ns + ni + no + 3)
        pins, pomi, proba_sub, proba_ins
        t = (psub, pins, pomi, proba_sub, proba_ins)
    #f.write(l)
    f.close()



if __name__ == "__main__":

    lex = parseLex("data/lexicon-2syll-0500words.lex")
    phonemes = parsePhonemes()
    test = parseYolo("data/test-2syll-0100words.test")
    levenshtein_btw_files(lex, test)
