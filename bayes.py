
import re
import itertools
import functools


class Network:
    def __init__(self, *edges):
        self.edges = edges
        self.P = {
            e: {} for e in self.vertecies()
        }

    def vertecies(self):
        return list(set(sum([list(e) for e in self.edges], [])))

    def parents(self, vertex: str):
        return [a for a, d in self.edges if d == vertex]

    def predict(self,  event: dict):
        """for event = { A: True, B: False }
        returns P(A,~B)
        """
        return functools.reduce(lambda acc, k: acc*self.query(k, event, value=event[k]), event.keys(), 1)

    def query(self, query: str, event={}, value=True):
        """for query = A, event = { B: True, C: False }, value = False
        returns P(~A|B,~C)
        """
        if(value == False):
            return 1-self.query(query, event)

        queryProbabilities = self.P[query]
        queryParents = self.parents(query)

        t = tuple([*[event.get(p) for p in queryParents], value])

        if t in queryProbabilities:
            return queryProbabilities[t]

        return sum([functools.reduce(lambda acc, k: acc*self.query(k[0], value=k[1]), zip(queryParents, k[0:-1]), queryProbabilities[k]) for k in queryProbabilities.keys() if k[-1]])


def main(text: str):
    initials = re.split(
        r"^[\w:]+?$", text.replace(' ', ''), flags=re.MULTILINE)

    _, initialNodes, initialConditionalDependencies, initialProbabilities = tuple(
        initials)

    n = Network(*[tuple(e.replace('(', '').replace(')', '').split(','))
                  for e in initialConditionalDependencies.replace('\n', '').split('),(')])

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
                raise ValueError('Invalid probability at line '+str(text.index(exp)) +
                                 f': "{initialProbability}"\n"{v}" does not depend on "{parent}"')

        if len(set(n.parents(v)).difference(set(parents))):
            raise ValueError('Invalid probability at line '+str(text.index(exp)) +
                             f': "{initialProbability}"\n"{v}" also depends on "{set(n.parents(v)).difference(set(parents))}"')

        n.P[v][tuple([*[any(parent == e for parent in initialParents)
                        for e in n.parents(v)], True])] = float(P)

    for v in n.vertecies():

        for k in itertools.product([True, False], repeat=len(n.parents(v))):
            if (*k, True) not in n.P[v]:
                # print(list(itertools.combinations_with_replacement([True, False], len(n.parents(v)))))
                parents = [e if s else "~"+e for e, s in zip(n.parents(v), k)]
                raise ValueError(
                    f'Not enough probabilities for event {v}\nPlease add "P({v}{"|"+",".join(parents) if len(parents) else ""})=n"')

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


if __name__ == '__main__':
    main("""Nodes:
G,D,MA,GR,H
Conditional Dependencies:
(G,MA),(D,MA),(G,GR),(D,GR),(MA,H),(GR,H)
Probabilities:
P(G)=0.3
P(D)=0.2
P(MA|G,D) = 0.03
P(MA|~G,D) = 0.02
P(MA|G,~D) = 0.01
P(MA|~G,~D) = 0.001
P(GR|G,D) = 0.08
P(GR|~G,D) = 0.05
P(GR|G,~D) = 0.04
P(GR|~G,~D) = 0.1
P(H|MA,GR) = 0.95
P(H|~MA,GR) = 0.2
P(H|MA,~GR) = 0.7
P(H|~MA,~GR) = 0.1""")
