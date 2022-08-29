#!/usr/bin/env python3

import argparse
import random
import re

from termcolor import colored, cprint

BRACKET = re.compile(r" ?\([^(]*\) ?")
SPACES = re.compile("  *")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=argparse.FileType("r"))
    parser.add_argument("-b", dest="both", action="store_true", default=False)
    args = parser.parse_args()

    pairs = []
    for line in args.data:
        src, tgt = line.strip().split("\t")
        pairs.append((src, tgt))
        if args.both:
            pairs.append((tgt, src))
    random.shuffle(pairs)

    total = 0
    correct = 0
    learn_round = 0

    while pairs:
        learn_round += 1
        missed_pairs = set()
        for i, (src, tgt) in enumerate(pairs):
            total += 1
            cprint(f"{i + 1}/{len(pairs)}", 'white', attrs=['bold'], end='')
            if missed_pairs:
                cprint(f" + {len(missed_pairs)}", 'yellow', end='')
            print(f": {tgt}")
            possible_answers = (
                SPACES.sub(" ", BRACKET.sub(" ", src)).strip().split(", "))
            answer = input()
            if answer.strip() in possible_answers:
                cprint("CORRECT", 'green', end='')
                if len(possible_answers) == 1:
                    print()
                else:
                    print(f": {', '.join(possible_answers)}")
                correct += 1
            else:
                print(f"{colored('WRONG', 'red')}: '{src}'")
                missed_pairs.add((src, tgt))
            print()

        pairs = []
        if missed_pairs:
            print(
                f"Round {learn_round} finished, "
                f"{len(missed_pairs)} errors to resolve.")
            for _ in range(min(4, learn_round)):
                pairs.extend(missed_pairs)
            random.shuffle(pairs)
    print(f"Done, accuracy {100 * correct / total:.2f}%.")


if __name__ == "__main__":
    main()
