from tools import *
import leven1
import leven2
import leven3




if __name__ == "__main__":

    lex = parseLex("data/lexicon-3syll-0500words.lex")
    phonemes = parsePhonemes()
    test = parseTest("data/test-3syll-0500words.test")
    hmm = parseModeleDiscret()
    print("hmm:")
    leven2.levenshtein_btw_files(lex, test, hmm)
    print("hmm + apprentissage:")
    hmm = leven3.learn()
    leven2.levenshtein_btw_files(lex, test, hmm)

    print("normal:")
    leven1.levenshtein_btw_files(lex, test)

