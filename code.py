from tools import *
import leven1
import leven2
import leven3
from threading import *

def lev():
    lex = parseLex("data/lexicon-2syll-0100words.lex")
    test = parseTest("data/test-2syll-0100words.test")
    hmm = parseModeleDiscret()
    leven2.levenshtein_btw_files(lex, test, hmm)
    writeModeleDiscret(hmm, "base")
def app():
    lex = parseLex("data/lexicon-2syll-0100words.lex")
    test = parseTest("data/test-2syll-0100words.test")
    hmm = parseModeleDiscret()
    hmm = leven3.learn(hmm)
    leven2.levenshtein_btw_files(lex, test, hmm)
    writeModeleDiscret(hmm, "appris")

def base():
    lex = parseLex("data/lexicon-2syll-0100words.lex")
    test = parseTest("data/test-2syll-0100words.test")
    leven1.levenshtein_btw_files(lex, test)


if __name__ == "__main__":

    t = Thread()
    print("hmm:")
    #lev()
    print("hmm + apprentissage:")
    app()
    print("normal:")
    base()
