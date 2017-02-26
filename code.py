from tools import *
import leven1
import leven2
import leven3
from threading import *

def lev():
    lex = parseLex("data/lexicon-3syll-0500words.lex")
    test = parseTest("data/test-3syll-0500words.test")
    hmm = parseModeleDiscret()
    leven2.levenshtein_btw_files(lex, test, hmm)

def app():
    lex = parseLex("data/lexicon-3syll-0500words.lex")
    test = parseTest("data/test-3syll-0500words.test")
    hmm = parseModeleDiscret()
    for i in range(5):
        hmm = leven3.learn(hmm, "data/train-25000items.train")
    writeModeleDiscret(hmm, "appris_2syll_100words")
    leven2.levenshtein_btw_files(lex, test, hmm)

def base():
    lex = parseLex("data/lexicon-3syll-0500words.lex")
    test = parseTest("data/test-3syll-0500words.test")
    leven1.levenshtein_btw_files(lex, test)


if __name__ == "__main__":

    print("hmm:")
    lev()
    print("hmm + apprentissage:")
    app()
    print("normal:")
    base()
