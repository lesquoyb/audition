class Parcours:

    SUB = 0
    INS = 1
    OMI = 2
    NOP = 3

    def __init__(self):
        self.transfo = []

    def addTransfo(self, type, values): #values étant un couple
        self.transfo.insert(0, (type, values))

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


def parseTest(fileName):
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

def parseTrain(fileName):
    f = open(fileName)
    assoc = []
    for line in f.readlines():
        line = line[:-1]
        dt = line.split("\t")
        mot = dt[0]
        ref = (dt[1])[1:-1].split(" ")
        test = (dt[2])[1:-1].split(" ")
        assoc += [(mot, ref, test)]
    return assoc

def parseModeleDiscret(mod_file="data/modele_discret_initialise.dat"):
    f = open(mod_file)

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

def writeModeleDiscret(modele, iter):
    psub, pins, pomi, proba_sub, proba_ins = modele

    f = open("model_iter" + str(iter) + ".dat", "w")

    f.write("Psub;Pins;Pomi\n")
    f.write( "%.3f" % psub + ";" + "%.3f" % pins + ";" + "%.3f" % pomi + "\n")

    f.write("#Une ligne par symbole de reference; une colonne par symbole de test\n")

    f.write("\t")
    phonemes = parsePhonemes()
    for phon in phonemes:
        f.write(";" + phon)
    f.write("\n")

    for phon in phonemes:
        f.write(phon)
        for phon2 in phonemes:
            f.write(";" + "%.3f" % proba_sub[(phon, phon2)])
        f.write("\n")

    f.write("Proba insertions...\n")

    f.write("<ins>")
    for phon in phonemes:
        f.write(";" + "%.3f" % proba_ins[(phon)])

    f.close()

def parsePhonemes(list_symb="data/liste_symboles.dat"):
    return open(list_symb).read().split("\n")[:-1]



def backtrack(st1, st2, d):
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

    return parcours
