#!/usr/bin/env python3

import argparse
import random
import re

from termcolor import colored, cprint

BRACKET = re.compile(r" ?\([^(]*\) ?")
SPACES = re.compile("  *")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=argparse.FileType("r"), nargs="+")
    parser.add_argument(
        "-b", "--both", dest="both", action="store_true", default=False,
        help="Test in both directions.")
    parser.add_argument(
        "-r", "--reverse", dest="reverse", action="store_true", default=False,
        help="Test in reverse direction than the source file.")
    parser.add_argument(
        "-s", "--sample", dest="sample", type=int, default=None,
        help="Number randomly sampled pairs to test.")
    args = parser.parse_args()

    pairs = []
    for handle in args.data:
        for line in handle:
            src, tgt = line.strip().split("\t")
            if not args.reverse:
                pairs.append((src, tgt))
            if args.both or args.reverse:
                pairs.append((tgt, src))
        handle.close()
    random.shuffle(pairs)

    if args.sample is not None:
        pairs = random.sample(pairs, args.sample)

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
                print(colored("CORRECT: ", 'green') + ', '.join(possible_answers))
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
            for _ in range(min(3, learn_round)):
                pairs.extend(missed_pairs)
            random.shuffle(pairs)
    print(f"Done, accuracy {100 * correct / total:.2f}%.")


if __name__ == "__main__":
    main()
