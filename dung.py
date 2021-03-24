from itertools import combinations
import re
from queue import PriorityQueue


class c:
    ORANGE = '\033[38;5;208m'
    GREEN = '\033[38;5;118m'
    GRAY = '\033[38;5;246m'
    END = '\033[0;0m'


def formatState(state: bool):
    if state is True:
        return 'In'
    return 'Out'


def colorState(state: str):
    return state.replace('In', f'{c.GREEN}In{c.END}').replace('Out', f'{c.ORANGE}Out{c.END}')


def allMax(l: list, **kargs):
    return [n for n in l if kargs.get('key')(n) is max(map(kargs.get('key'), l))]


def allMin(l: list, **kargs):
    return [n for n in l if kargs.get('key')(n) is min(map(kargs.get('key'), l))]


def isConflictFree(A: list, R: list):
    return lambda s:  all(all(
        not R[A.index(a)][A.index(b)] for b in s
    ) for a in s)


def main(text: str):
    initials = re.split(r"Attacks.*?\n", text, flags=re.IGNORECASE)

    initialArgs, initialAttacks = tuple(initials)
    A = re.compile(r'Args.*?\n', re.IGNORECASE).sub('',
                                                    initialArgs).replace('\n', '').replace(' ', '').split(',')

    R = [[False]*len(A) for a in A]

    for attack in initialAttacks.replace('\n', '').replace(' ', '').split('),('):
        a, d = tuple(attack.replace(")", '').replace('(', '').split(','))
        R[A.index(d)][A.index(a)] = True

    subsets = sum(map(lambda r: list(
        combinations(A, r)), range(1, len(A)+1)), [])

    stableExtensions = list(filter(lambda s:  isConflictFree(A, R)(
        s) and all(any(R[A.index(a)][A.index(b)] for b in s) for a in A if a not in s), subsets))

    formatRow = "{:>20}" + " {:>8}" * len(A)

    print(formatRow.format('', *A))
    for stableExtension, i in zip(stableExtensions, range(len(stableExtensions))):
        print(colorState(formatRow.format('or' if i else 'Stable semantics',
                                          *[formatState(a in stableExtension) for a in A])))

    for groundedExtension, i in zip(allMin(stableExtensions, key=len), range(len(stableExtensions))):
        print(colorState(formatRow.format('or' if i else 'Grounded semantics',
                                          *[formatState(a in groundedExtension) for a in A])))

    for prefferredExtension, i in zip(allMax(stableExtensions, key=len), range(len(stableExtensions))):
        print(colorState(formatRow.format('or' if i else 'Prefferred semantics',
                                          *[formatState(a in prefferredExtension) for a in A])))


with open("dung.txt") as f:
    main(f.read())
