
import random
import re
from itertools import product
from functools import partial, reduce
import operator


class BayesianNetwork:
    def __init__(self, *edges_or_vertices):
        self.edges = [e for e in edges_or_vertices if isinstance(e, tuple)]

        self.vertices = set(sum([[*e] if isinstance(e, tuple) else [e]
                                 for e in edges_or_vertices], []))

        self.P = {
            e: {} for e in self.vertices
        }

    def parents(self, vertex: str):
        return [a for a, d in self.edges if d == vertex]

    def string_query(self, logic: str):
        parsed_logic = parse_logic(logic)

        if parsed_logic[0] == '|':
            return self.predict(dict(logic_to_event(parsed_logic)))/self.predict(dict(logic_to_event(parsed_logic[2])))
        return self.predict(dict(logic_to_event(parsed_logic)))

    def verify(self):
        for v in self.vertices:
            for k in product([True, False], repeat=len(self.parents(v))):
                if (*k, True) not in self.P[v]:
                    parents = [e if s else "~"+e for e,
                               s in zip(self.parents(v), k)]
                    raise ValueError(
                        f'Not enough probabilities for event {v}\nPlease add "P({v}{"|"+",".join(parents) if len(parents) else ""})=n"')

    def probability(self, of: tuple[str, bool], event: dict):
        k, value = of
        if not value:
            return 1 - self.probability((k, True), event)

        if k not in self.P:
            raise ValueError(f'"{k}" not in the network')

        return self.P[k][(*[event[v] for v in self.parents(k)], True)]

    def predict(self,  event: dict):
        """return P(A,~B) as float

        from event = { 'A': True, 'B': False }
        """

        missing_vertices = set(self.vertices).difference(event.keys())

        if len(missing_vertices):
            return sum(
                self.predict({
                    **event,
                    **dict(zip(missing_vertices, values)),
                })
                for values in product([False, True],  repeat=len(missing_vertices))
            )

        probabilities = map(partial(
            self.probability, event=event), event.items())

        return reduce(operator.mul, probabilities, 1)


def parse_logic(logic: str):
    """return ('|', 'H', (',', ('~', 'MA'), ('~', 'GR')))

    from logic = 'H|~MA,GR'
    """
    for i in range(len(logic)):
        if logic[i] in ['|', ',']:
            return logic[i], parse_logic(logic[:i]), parse_logic(logic[i+1:])

    if logic[0] == '~':
        return '~', parse_logic(logic[1:])

    return logic


def logic_to_event(logic: tuple) -> tuple:
    """return (('H', True), ('MA', False), ('GR', False))

    from logic ('|', 'H', (',', ('~', 'MA'), ('~', 'GR')))
    """
    if logic[0] in ['|', ',']:
        return *logic_to_event(logic[1]), *logic_to_event(logic[2])

    if logic[0] == '~':
        return ((k, not v) for k, v in logic_to_event(logic[1]))

    return ((logic, True),)


def parse_edges(conditional_dependencies: str):
    return [tuple(e.replace('(', '').replace(')', '').split(','))
            for e in conditional_dependencies.replace('\n', '').split('),(')]


PROBABILITY_QUERY = r"P\(((?:~?\w+\|)?~?\w+(?:,~?\w+)*)\)="


def main():
    f = open('bayes.txt')
    text = f.read()
    f.close()
    initials = re.split(
        r"^[\w:]+?$", re.sub(r'\n+', '\n', text).replace(' ', ''), flags=re.MULTILINE)

    _, initial_vertices, conditional_dependencies, initial_probabilities = tuple(
        initials)
    edges = parse_edges(conditional_dependencies)
    vertices = [v.strip() for v in initial_vertices.split(',')]

    n = BayesianNetwork(*edges, *vertices)

    for initial_probability in initial_probabilities.strip().split('\n'):
        m = re.match(
            r"P\(((?:~?\w+\|)?~?\w+(?:,~?\w+)*)\)=([\d\.]+)", initial_probability)
        if m == None:
            continue
        exp, P = m.group(1), m.group(2)
        m = exp.split('|')
        if len(m) == 1:
            n.P[m[0]][(True,)] = float(P)
            continue

        v, parents = tuple(m)
        initial_parents = tuple(parents.split(','))
        parents = [parent.replace('~', '') for parent in initial_parents]

        for parent in parents:
            if parent not in n.parents(v):
                raise ValueError(
                    f'Incorrect probability at line {str(text.index(exp))}: "{initial_probability}"\n"{v}" does not depend on "{parent}"')

        missing_parents = set(n.parents(v)).difference(set(parents))
        if len(missing_parents):
            raise ValueError(
                f'Incorrect probability at line {str(text.index(exp))}: "{initial_probability}"\n"{v}" also depends on "{missing_parents}"')

        n.P[v][tuple([*[any(parent == e for parent in initial_parents)
                        for e in n.parents(v)], True])] = float(P)

    n.verify()

    v = random.choice([*n.vertices])

    i = input(
        f'Please input queries, for example: "P({v}{"|"+",".join(n.parents(v)) if len(n.parents(v)) else ""})="\n')
    while(True):
        m = re.match(PROBABILITY_QUERY, i)
        try:
            if m == None:
                raise ValueError('Incorrect query')
            print(n.string_query(m.group(1)))
        except ValueError as e:
            print(e)
        i = input()


def parse_query(n: BayesianNetwork, initial_probability: str):
    m = re.match(
        r"P\(((?:~?\w+\|)?~?\w+(?:,~?\w+)*)\)=([\d\.]+)", initial_probability)
    if m == None:
        raise ValueError('Incorrect probability at line')
    exp, probability = m
    l = parse_logic(exp)
    vertex = l[0] if len(l) < 2 else l[1]
    vertex = vertex if isinstance(vertex, str) else vertex[1]

    keys = logic_to_event(l)

    n.P[vertex][tuple([k for _, k in sorted(keys)])] = float(probability)


if __name__ == '__main__':
    main()
