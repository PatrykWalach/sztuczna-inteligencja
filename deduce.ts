const text = await Deno.readTextFile("baza-wiedzy.txt");

const [initialRules, initialFacts] = text.split("fakty");

const facts = new Set(initialFacts.split(",").map((str) => str.trim()));

const rules = initialRules
  .split("\n")
  .filter(Boolean)
  .map((str) =>
    str
      .replaceAll(" ", "")
      .replace(/\d+\./g, "")
      .split("->")
      .map((str) => str.split(","))
  );

function deduce(hypothesis: string) {
  if (facts.has(hypothesis)) {
    return true;
  }

  let changed = true;
  while (changed) {
    changed = false;

    for (const [requirements, results] of rules) {
      if (results.every((r) => facts.has(r))) {
        continue;
      }

      if (requirements.every((r) => facts.has(r))) {
        changed = true;
        for (const result of results) {
          facts.add(result);
        }
      }
    }
  }

  return facts.has(hypothesis);
}

function deduceBackwards(hypothesis: string) {
  if (facts.has(hypothesis)) {
    return true;
  }

  for (const [requirements, results] of rules) {
    if (!results.includes(hypothesis)) {
      continue;
    }
    
    if (requirements.every((r) => deduceBackwards(r))) {
      for (const result of results) {
        facts.add(result);
      }

      return true;
    }
  }

  return false;
}

console.log(deduceBackwards("D"));
console.log(facts);
