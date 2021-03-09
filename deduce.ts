/**
 * Program wykonujący wnioskowanie.
 *
 * Program uruchomiony może być przy pomocy Deno,
 * program wczytuje bazę wiedzy z pliku baza-wiedzy.txt
 * i wykonuje wnioskowanie w tył na hipotezach podanych w argumentach lub A-H.
 *
 * @link   https://github.com/PatrykWalach/sztuczna-inteligencja
 * @file   Ten plik jest plikiem głównym tego programu.
 * @author Patryk Wałach.
 * @since  09.03.2021
 */

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

/**
 * Funkcja wykonuje wnioskowanie w przód.
 */
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

      if (requirements.some((r) => !facts.has(r))) {
        continue;
      }

      changed = true;
      for (const result of results) {
        facts.add(result);
      }
    }
  }

  return facts.has(hypothesis);
}

/**
 * Funkcja wykonuje wnioskowanie w tył.
 */
function deduceRight(hypothesis: string) {
  if (facts.has(hypothesis)) {
    return true;
  }

  for (const [requirements, results] of rules) {
    if (!results.includes(hypothesis)) {
      continue;
    }

    if (requirements.some((r) => !deduceRight(r))) {
      continue;
    }

    for (const result of results) {
      facts.add(result);
    }

    return true;
  }

  return false;
}

for (const hypothesis of Deno.args.length
  ? Deno.args
  : Array.from({ length: 1 + "H".charCodeAt(0) - "A".charCodeAt(0) }, (_, i) =>
      String.fromCharCode(i + "A".charCodeAt(0))
    )) {
  console.log(
    `${hypothesis} ${deduceRight(hypothesis) ? "" : "nie "}jest spełnione`
  );
}
