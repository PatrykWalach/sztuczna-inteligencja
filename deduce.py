import re

text = open("baza-wiedzy.txt")

initials = text.read().split("fakty")

text.close()

initialRules, initialFacts = tuple(initials)

facts = set(s.strip() for s in initialFacts.split(','))
rules = [tuple(s2.split(',') for s2 in re.sub(r'\d+\.', '', s.replace("~~", "").replace(" ", "")).split("->"))
         for s in initialRules.split('\n') if s]


def deduce(hypothesis):
    if hypothesis in facts:
        return True
    changed = True
    for requirements, results in rules:
        if all(r in facts for r in results):
            continue

        if any(r not in facts for r in requirements):
            continue

        changed = True

        for result in results:
            facts.add(result)

    return hypothesis in facts


def deduceRight(hypothesis):
    global facts
    if hypothesis in facts:
        return True

    for requirements, results in rules:
        if hypothesis not in results:
            continue

        if any(not deduceRight(r.replace('~', '')) ^ r.startswith('~') for r in requirements):
            continue

        for result in results:
            facts.add(result)

        return True

    return False


for hypothesis in sorted(set(r.replace('~', '') for r in sum(list(sum(list(r), []) for r in rules), []))):
    if deduceRight(hypothesis):
        print(hypothesis, "jest spełnione")
    else:
        print(hypothesis, "nie jest spełnione")
