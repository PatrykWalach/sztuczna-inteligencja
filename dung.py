import re

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


def edgesLen(d):
    return len(
        [e for e in edges[vertices.index(d)] if e is True]
        # list(filter(lambda e: e is True, edges[vertices.index(d)]))
    )


fullfilled = [None]*len(vertices)


def dung(fullfilled):
    visited = [False]*len(vertices)
    queue = sorted(vertices, key=edgesLen)

    while(len(queue)):
        d = queue.pop(0)

        if visited[vertices.index(d)]:
            continue
        visited[vertices.index(d)] = True

        for e in sorted([vertices[a]
                         for a in range(len(vertices)) if edges[a][vertices.index(d)]], key=edgesLen, reverse=True):
            queue.insert(0, e)

        if fullfilled[vertices.index(d)] is not None:
            continue

        if any(fullfilled[a] for a in range(len(vertices)) if edges[vertices.index(d)][a]):
            fullfilled[vertices.index(d)] = False
        elif all(fullfilled[a] is False for a in range(len(vertices)) if edges[vertices.index(d)][a]):
            fullfilled[vertices.index(d)] = True


class c:
    ORANGE = '\033[38;5;208m'
    GREEN = '\033[38;5;118m'
    GRAY = '\033[38;5;246m'
    END = '\033[0;0m'


def printVertices(fullfilled):
    for v in range(len(vertices)):
        if fullfilled[v] is True:
            print(' · '+vertices[v] + f' is {c.GREEN}In{c.END}')
        elif fullfilled[v] is False:
            print(' · '+vertices[v] + f' is {c.ORANGE}Out{c.END}')
        else:
            print(' · '+vertices[v] + f' is {c.GRAY}Nither{c.END}')


def resolveNither(u):
    fullfilledCopy = fullfilled.copy()
    fullfilledCopy[u] = True
    dung(fullfilledCopy)
    return fullfilledCopy


def trueLen(l):
    return len([e for e in l if l is True])


def allMax(l, **kargs):
    return [n for n in resolvedStates if kargs.get('key', lambda x:x)(resolvedStates) is max(map(kargs.get('key', lambda x:x), resolvedStates))]


def allMin(l, **kargs):
    return [n for n in resolvedStates if kargs.get('key', lambda x:x)(resolvedStates) is min(map(kargs.get('key', lambda x:x), resolvedStates))]


dung(fullfilled)
print('Stable semantics:')
printVertices(fullfilled)


resolvedStates = [resolveNither(v) for v in range(
    len(vertices)) if fullfilled[v] is None]


print('Grounded semantics:')
for states, i in zip(allMin(resolvedStates, key=trueLen), range(len(resolvedStates))):
    if i:
        print('or:')
    printVertices(states)

print('Prefferred semantics:')
for states, i in zip(allMax(resolvedStates, key=trueLen), range(len(resolvedStates))):
    if i:
        print('or:')
    printVertices(states)
