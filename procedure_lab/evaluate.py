"""Execute the frozen fictional deck once per arm and persist responses before scoring."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from . import model
from .engine import analyze
from .server import REPAIRS

GOLD = Path(__file__).with_name("gold.json")
GOLD_HASH = "e90d223d2032d50955eb0c5e0973da9ea4f4cf80e205e828ceb2e6f9b06d39e1"
MODEL = "llama3.2:1b"


def save(path, obj):
    with path.open("x") as output:
        json.dump(obj, output, indent=2, allow_nan=False)
        output.write("\n")


def attempt(folder, case_id, mode, text):
    row = {"id": case_id, "arm": mode, "input": text, "classification": None}
    try:
        data = model.run(text, mode, MODEL)
        row.update(data)
        if mode == "proposal":
            replay = analyze(text, data["result"])
            row["replay"] = replay
            row["classification"] = {"divergent": "ambiguous", "single_reading": "clear",
                                     "abstained": "outside_scope"}[replay["status"]]
        else:
            row["classification"] = data["result"]["classification"]
    except (model.ModelError, ValueError) as exc:
        row["error"] = str(exc)
        if hasattr(exc, "receipt"):
            row["receipt"] = exc.receipt
    save(folder / f"{case_id}-{mode}.json", row)
    return row


def correct_actions(row, expected):
    cases = row.get("replay", {}).get("cases", [])
    return [sorted(set(c["actions"].values())) for c in cases] == expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    out = parser.parse_args().output
    raw = GOLD.read_bytes()
    if hashlib.sha256(raw).hexdigest() != GOLD_HASH:
        parser.error("Gold deck differs from frozen revision")
    inventory = model.status(MODEL)
    if not inventory["available"]:
        parser.error(inventory["reason"])
    out.mkdir(parents=True, exist_ok=False)
    save(out / "start.json", {"utc": datetime.now(timezone.utc).isoformat(),
                              "gold_sha256": GOLD_HASH, "runtime": inventory,
                              "sources": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                          for p in [Path(__file__), Path(model.__file__), Path(__file__).with_name("engine.py")]}})
    scores = []
    for case in json.loads(raw)["cases"]:
        ambiguous = len(case["starts_at"]) == 2
        expected = "ambiguous" if ambiguous else "clear"
        proposal = attempt(out, case["id"], "proposal", case["procedure"])
        direct = attempt(out, case["id"], "direct", case["procedure"])
        right = correct_actions(proposal, case["allowed_actions"])
        witness = proposal.get("replay", {}).get("witness") or {}
        outcome = {"id": case["id"], "expected": expected, "proposal": proposal["classification"],
                   "direct": direct["classification"], "all_actions_correct": right,
                   "correct_witness": ambiguous and right and witness.get("position") == "after_label"}
        if ambiguous:
            fixed = attempt(out, case["id"]+"-repair", "proposal",
                            case["procedure"]+" "+REPAIRS["first_item_placed"])
            outcome["paired_repair_correct"] = (outcome["correct_witness"] and fixed["classification"]=="clear"
                                                  and correct_actions(fixed,[["rush"],["rush"],["regular"]]))
        scores.append(outcome)
        print(json.dumps(outcome), flush=True)
    totals = {}
    for arm in ("proposal","direct"):
        totals[arm] = {"classification_correct_of_8":sum(s[arm]==s["expected"] for s in scores),
                       "false_alarms_of_4_clear":sum(s[arm]=="ambiguous" and s["expected"]=="clear" for s in scores),
                       "valid_in_scope_of_8":sum(s[arm] in ("clear","ambiguous") for s in scores)}
    totals["all_actions_correct_of_8"] = sum(s["all_actions_correct"] for s in scores)
    totals["correct_witness_of_4"] = sum(s["correct_witness"] for s in scores)
    totals["paired_repairs_correct_of_4"] = sum(s.get("paired_repair_correct",False) for s in scores)
    save(out / "summary.json", {"scores":scores,"totals":totals,"independent_semantic_review":"pending"})


if __name__ == "__main__":
    main()
