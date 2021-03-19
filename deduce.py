import re

text = open("baza-wiedzy-negacja.txt")

initials = re.split(r"fakty.*?\n", text.read(), flags=re.IGNORECASE)
text.close()

initialRules, initialFacts = tuple(initials)

rules = [tuple(s2.split(',') for s2 in re.sub(r'\d+\.', '', s.replace("~~", "").replace(" ", "")).split("->"))
         for s in initialRules.split('\n') if s]


def check(hypothesis, facts):
    return (hypothesis.replace('~', '') in facts) ^ hypothesis.startswith('~')


def deduce(hypothesis, facts):
    """Funkcja wykonuje wnioskowanie w przód."""
    if check(hypothesis, facts):
        return True

    changed = True
    while changed:
        changed = False

        for (requirements, results), i in zip(rules, range(len(rules))):

            if not all(check(requirement, facts) for requirement in requirements):
                if not all(any(all(check(requirement, facts) for requirement in requirements) for requirements, results in rules if result in results) for result in results):
                    for result in results:
                        if result in facts:
                            facts.remove(result)
                            changed = True
                continue

            if all(r in facts for r in results):
                continue

            changed = True
            for result in results:
                facts.add(result)

    return hypothesis in facts


def deduceRight(hypothesis, facts):
    """Funkcja wykonuje wnioskowanie w tył."""
    if hypothesis in facts:
        return True

    for requirements, results in rules:
        if hypothesis not in results:
            continue

        if any(not deduceRight(r.replace('~', ''), facts) ^ r.startswith('~') for r in requirements):
            continue

        for result in results:
            facts.add(result)

        return True

    return False


for hypothesis in sorted(set(r.replace('~', '') for r in sum(list(sum(list(r), []) for r in rules), []))):
    if deduceRight(hypothesis, set(s.strip() for s in initialFacts.split(','))):
        print(hypothesis, "jest spełnione")
    else:
        print(hypothesis, "nie jest spełnione")
