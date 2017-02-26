from tools import *
from leven1 import *

if __name__ == "__main__":
    lex = parseLex("data/lexicon-2syll-0100words.lex")
    test = parseTest("data/test-2syll-0100words.test")

    levenshtein_btw_files(lex, test)
