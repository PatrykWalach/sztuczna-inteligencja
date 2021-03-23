import re
from queue import PriorityQueue


def outLen(vertices: list, edges: list, fullfilled: list, d: int):
    return len([a for a, i in zip(edges[d], range(len(vertices))) if a is True and fullfilled[i] is not True])


def dung(vertices: list, edges: list, fullfilled: list):
    visited = [False]*len(vertices)
    queue = PriorityQueue()
    for e in sorted([(outLen(vertices, edges, fullfilled, d), d)
                     for d in range(len(vertices))]):
        queue.put(e)

    while(not queue.empty()):
        w, d = queue.get()

        if visited[d]:
            continue

        visited[d] = True

        # if fullfilled[d] is not None:
        #     continue

        if any(fullfilled[a] for a in range(len(vertices)) if edges[d][a]):
            fullfilled[d] = False
        elif all(fullfilled[a] is False for a in range(len(vertices)) if edges[d][a]):
            fullfilled[d] = True

        for e in [a for a in range(len(vertices)) if edges[a][d]]:
            queue.put((outLen(vertices, edges, fullfilled, e), e))


class c:
    ORANGE = '\033[38;5;208m'
    GREEN = '\033[38;5;118m'
    GRAY = '\033[38;5;246m'
    END = '\033[0;0m'


def printVertices(vertices: list,  fullfilled: list,):
    for v in range(len(vertices)):
        if fullfilled[v] is True:
            print(' · '+vertices[v] + f' is {c.GREEN}In{c.END}')
        elif fullfilled[v] is False:
            print(' · '+vertices[v] + f' is {c.ORANGE}Out{c.END}')
        else:
            print(' · '+vertices[v] + f' is {c.GRAY}Unknown{c.END}')


def resolveNither(vertices: list, edges: list, fullfilled: list, u: int):
    fullfilled[u] = True
    dung(vertices, edges,  fullfilled)
    return fullfilled


def trueLen(l: list):
    return len([e for e in l if e is True])


def allMax(l: list, **kargs):
    return [n for n in l if n is max(l, key=kargs.get('key'))]


def allMin(l: list, **kargs):
    return [n for n in l if n is min(l, key=kargs.get('key'))]


def main():
    text = open("dung.txt")

    initials = re.split(r"Attacks.*?\n", text.read(), flags=re.IGNORECASE)
    text.close()

    initialArgs, initialAttacks = tuple(initials)

    vertices = re.compile(r'Args.*?\n', re.IGNORECASE).sub('',
                                                           initialArgs).strip().split(',')

    edges = [[False]*len(vertices) for v in vertices]

    for attack in initialAttacks.split('),('):
        a, d = tuple(attack.replace(")", '').replace('(', '').split(','))
        edges[vertices.index(d)][vertices.index(a)] = True

    fullfilled = [None]*len(vertices)

    dung(vertices, edges, fullfilled)
    print('Stable semantics:')
    printVertices(vertices, fullfilled)

    resolvedStates = [resolveNither(vertices, edges, fullfilled.copy(), v) for v in range(
        len(vertices)) if fullfilled[v] is None]

    print('Grounded semantics:')
    for states, i in zip(allMin(resolvedStates, key=trueLen), range(len(resolvedStates))):
        if i:
            print('or:')
        printVertices(vertices, states)

    print('Prefferred semantics:')
    for states, i in zip(allMax(resolvedStates, key=trueLen), range(len(resolvedStates))):
        if i:
            print('or:')
        printVertices(vertices, states)


main()
