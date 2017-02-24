
class Parcours:

    SUB = 0
    INS = 1
    OMI = 2

    def __init__(self):
        self.transfo = []

    def addTransfo(self, type, values):
        self.transfo += [(type, values)] #values étant un couple

    def compter(self):
        ns, ni, no = 0,0,0
        for transfo in self.transfo:
            if transfo[0] == self.SUB:
                pass





    def print(self):
        r = ""
        for transfo in self.transfo.reverse():
            r += "yolo" #TODO
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

    line = f.readline()[-1] #BALEK - Proba insertions...

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
    corresp = ""
    i,j = len(st1)-1, len(st2)-1
    while (i,j) != (0,0):
        c = ""
        val = d[i][j]
        if i>0 and d[i-1][j] < val: # INS
            ti = i -1
            tj = j
            val = d[ti][tj]
            c = "=>" + st2[j]
        if j>0:
            if d[i][j-1] < val: # OMI
                ti = i
                tj = j -1
                val = d[ti][tj]
                c = st1[i] + "=>"
            if i>0:
                ti = i -1
                tj = j -1
                if d[i-1][j-1] < val: # SUB
                    c = st1[i] + "=>" + st2[j]

                if d[i-1][j-1] == val : # SAME
                    c = st1[i]
        corresp += c
        i,j = ti,tj
    return d[-1][-1], corresp


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

    for k,v in test:
        mini = 99999
        nom = k
        lit = ""
        for kl,vl in lex.items():
            for it in vl:
                d, corresp = Levenshtein(v ,it, t)
                if d < mini:
                    mini = d
                    nom = kl
                    lit = it
                l += k + " " + str(v) + " => " + kl + " " + str(it) + ("Erreur" if d > 0 else "Correct") + str(d) + " <=> " + str(corresp) + "\n"
                f.write(l)
    f.close()



if __name__ == "__main__":

    lex = parseLex("data/lexicon-2syll-0500words.lex")
    phonemes = parsePhonemes()
    test = parseYolo("data/test-2syll-0100words.test")
    levenshtein_btw_files(lex, test)
