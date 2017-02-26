from tools import *
from leven3 import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("modl_init")
parser.add_argument("donnees_app")
parser.add_argument("modl_appris")

if __name__ == "__main__":
    args = parser.parse_args()

    hmm = parseModeleDiscret(args.modl_init)
    hmm = learn(hmm, args.donnees_app)

    writeModeleDiscret(hmm, args.modl_appris)
