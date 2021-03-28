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


def allMin(l: list, **kargs):
    return [n for n in l if kargs.get('key')(n) is min(map(kargs.get('key'), l))]


def allMax(l: list, **kargs):
    return [n for n in l if kargs.get('key')(n) is max(map(kargs.get('key'), l))]


def isConflictFree(A: list, R: list):
    return lambda s:  all(all(
        not R[A.index(a)][A.index(b)] for b in s
    ) for a in s)


def isAcceptable(A: list, R: list, E: list, a):
    return all(any(R[A.index(b)][A.index(c)] for c in E) for b in A if R[A.index(a)][A.index(b)])


def isAdmissible(A: list, R: list):
    return lambda S: isConflictFree(A, R)(S) and all(isAcceptable(A, R, S, a) for a in S)


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

    completeExtensions = list(
        filter(lambda E: isAdmissible(A, R)(E) and all(a in E for a in A if isAcceptable(A, R, E, a)), subsets))

    admissibleSets = list(filter(
        isAdmissible(A, R), subsets))

    formatRow = "{:>20}" + " {:>8}" * len(A)

    print(formatRow.format('', *A))
    for prefferredExtension, i in zip(allMax(admissibleSets, key=len), range(len(admissibleSets))):
        print(colorState(formatRow.format('or' if i else 'Prefferred semantics',
                                          *[formatState(a in prefferredExtension) for a in A])))

    for groundedExtension, i in zip(allMin(completeExtensions, key=len), range(len(completeExtensions))):
        print(colorState(formatRow.format('or' if i else 'Grounded semantics',
                                          *[formatState(a in groundedExtension) for a in A])))


with open("dung.txt") as f:
    main(f.read())
