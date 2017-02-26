from tools import *
from leven2 import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("lex")
parser.add_argument("modeleHMM")
parser.add_argument("test")

if __name__ == "__main__":
    args = parser.parse_args()

    lex = parseLex(args.lex)
    hmm = parseModeleDiscret(args.modeleHMM)
    test = parseTest(args.test)

    levenshtein_btw_files(lex, test, hmm)
