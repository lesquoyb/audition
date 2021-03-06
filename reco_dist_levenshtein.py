from tools import *
from leven1 import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("lex")
parser.add_argument("test")

if __name__ == "__main__":
    args = parser.parse_args()

    lex = parseLex(args.lex)
    test = parseTest(args.test)

    levenshtein_btw_files(lex, test)
