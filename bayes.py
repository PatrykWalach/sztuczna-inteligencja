
import random
import traceback
import queue
import re
import itertools
import functools
import operator


class BayesianNetwork:
    def __init__(self, *edgesOrVertices):
        self.edges = [e for e in edgesOrVertices if isinstance(e, tuple)]

        # self.edges = [*filter(functools.partial(
        #     isinstance, class_or_tuple=tuple), edgesOrVertices)]

        self.vertices = set(sum([[*e] if isinstance(e, tuple) else [e]
                                 for e in edgesOrVertices], []))

        # self.vertices = set(*sum(map(list, self.edges), []), *filter(functools.partial(
        #     isinstance, class_or_tuple=str), edgesOrVertices))

        self.P = {
            e: {} for e in self.vertices
        }

    def parents(self, vertex: str):
        return [a for a, d in self.edges if d == vertex]

    def stringQuery(self, logic: str):
        parsedLogic = parseLogic(logic)

        if parsedLogic[0] == '|':
            return self.predict(dict(logicToEvent(parsedLogic)))/self.predict(dict(logicToEvent(parsedLogic[2])))
        return self.predict(dict(logicToEvent(parsedLogic[2])))

    def verify(self):
        for v in self.vertices:
            for k in itertools.product([True, False], repeat=len(self.parents(v))):
                if (*k, True) not in self.P[v]:
                    parents = [e if s else "~"+e for e,
                               s in zip(self.parents(v), k)]
                    raise ValueError(
                        f'Not enough probabilities for event {v}\nPlease add "P({v}{"|"+",".join(parents) if len(parents) else ""})=n"')

    def probability(self, i, event):
        k, s = i
        if not s:
            return 1 - self.probability((k, True), event)

        if k not in self.P:
            raise ValueError(f'"{k}" not in the network')

        return self.P[k][(*[event[v] for v in self.parents(k)], True)]

    def predict(self,  event: dict):
        """for event = { A: True, B: False }
        returns P(A,~B)
        """

        missingVertices = set(self.vertices).difference(event.keys())

        if len(missingVertices):
            return sum(self.predict({
                **event,
                **dict(zip(missingVertices, values)),
            })
                for values in itertools.product([False, True],  repeat=len(missingVertices))
            )

        probabilities = map(functools.partial(
            self.probability, event=event), event.items())

        return functools.reduce(operator.mul, probabilities, 1)


def parseLogic(logic: str):
    """returns logic H|~MA,GR
    in ('|', 'H', (',', ('~', 'MA'), ('~', 'GR'))) format"""
    for i in range(len(logic)):
        if logic[i] in ['|', ',']:
            return logic[i], parseLogic(logic[:i]), parseLogic(logic[i+1:])

    if logic[0] == '~':
        return '~', parseLogic(logic[1:])

    return logic


def logicToEvent(logic: tuple) -> tuple:
    """returns key (('H', True), ('MA', False), ('GR', False))
    out of logic ('|', 'H', (',', ('~', 'MA'), ('~', 'GR')))"""
    if logic[0] == '|':
        return *logicToEvent(logic[1]), *logicToEvent(logic[2])
    if logic[0] == ',':
        return *logicToEvent(logic[1]), *logicToEvent(logic[2])

    if logic[0] == '~':
        return ((k, not v) for k, v in logicToEvent(logic[1]))

    return ((logic, True),)


# def logicToQuery(logic: tuple) -> tuple:
#     """returns key ('H', (('MA', False), ('GR', False)), True)
#     out of logic ('|', 'H', (',', ('~', 'MA'), ('~', 'GR')))"""
#     if logic[0] == '|':
#         return dict(logicToQuery(logic[2])), *logicToQuery(logic[1])[0]
#     if logic[0] == ',':
#         return *logicToQuery(logic[1]), *logicToQuery(logic[2])

#     if logic[0] == '~':
#         return tuple((k, not v) for k, v in logicToQuery(logic[1]))

#     return ((logic, True),)


def parseEdges(conditionalDependencies: str):
    return [tuple(e.replace('(', '').replace(')', '').split(','))
            for e in conditionalDependencies.replace('\n', '').split('),(')]


def main():
    f = open('bayes.txt')
    text = f.read()
    f.close()
    initials = re.split(
        r"^[\w:]+?$", re.sub(r'\n+', '\n', text).replace(' ', ''), flags=re.MULTILINE)

    _, initialVertices, conditionalDependencies, initialProbabilities = tuple(
        initials)
    edges = parseEdges(conditionalDependencies)
    vertices = [v.strip() for v in initialVertices.split(',')]

    n = BayesianNetwork(*edges, *vertices)

    for initialProbability in initialProbabilities.strip().split('\n'):
        m = re.match(r"P\((.+)\)=([\d\.]+)", initialProbability)
        if m == None:
            continue
        exp, P = m.group(1), m.group(2)
        m = exp.split('|')
        if len(m) == 1:
            n.P[m[0]][(True,)] = float(P)
            continue

        v, parents = tuple(m)
        initialParents = tuple(parents.split(','))
        parents = [parent.replace('~', '') for parent in initialParents]

        for parent in parents:
            if parent not in n.parents(v):
                raise ValueError(
                    f'Invalid probability at line {str(text.index(exp))}: "{initialProbability}"\n"{v}" does not depend on "{parent}"')

        missingParents = set(n.parents(v)).difference(set(parents))
        if len(missingParents):
            raise ValueError(
                f'Invalid probability at line {str(text.index(exp))}: "{initialProbability}"\n"{v}" also depends on "{missingParents}"')

        n.P[v][tuple([*[any(parent == e for parent in initialParents)
                        for e in n.parents(v)], True])] = float(P)

    n.verify()

    # queries = ['H|~MA,~GR', 'L', 'H', 'MA', 'GR', 'H|MA,GR', 'H,MA,GR',
    #            'G|MA,~GR', 'MA', 'D', 'H', 'GR']

    # for query in queries:
    #     print(f'P({query})={n.stringQuery(query)}')

    v = random.choice([*n.vertices])

    i = input(
        f'Please input queries, for example: "P({v}{"|"+",".join(n.parents(v)) if len(n.parents(v)) else ""})="\n')
    while(True):
        m = re.match(r"P\(((~?\w+\|)?~?\w+(,~?\w+)*)\)=", i)
        try:
            if m == None:
                raise ValueError('Bad query format')
            print(n.stringQuery(m.group(1)))
        except ValueError as e:
            print(e)
        i = input()


# m = parseLogic('H|~MA,~GR')
# print(m)
# vertex = m[0] if len(m) < 2 else m[1]
# print(vertex)
# # parents = n.parents(vertex)
# parents = ['GR', 'MA']
# keys = logicToEvent(m)
# print(tuple([k for _, k in sorted(
#     keys, key=lambda t: [*parents, vertex].index(t[0]))]))
if __name__ == '__main__':
    main()
