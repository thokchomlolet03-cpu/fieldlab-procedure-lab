"""Executable answer key for the fictional two-order packing station."""
import unittest

from procedure_lab.engine import analyze, replay


RUSH = "Rush orders go first."
FINISH = "Finish a regular order once packing has started."
PROCEDURE = RUSH + " " + FINISH


def proposal(*meanings):
    return {
        "status": "interpreted",
        "rush_priority_quote": RUSH,
        "finish_started_quote": FINISH,
        "readings": [{"starts_at": event, "quote": "packing has started"} for event in meanings],
    }


class PackingProcedureTests(unittest.TestCase):
    def test_answer_key_and_shortest_witness(self):
        r = analyze(PROCEDURE, proposal("label_printed", "first_item_placed"))
        self.assertEqual(r["status"], "divergent")
        self.assertEqual(r["searched_traces"], 4)
        self.assertEqual([case["actions"] for case in r["cases"]], [
            {"label_printed": "rush", "first_item_placed": "rush"},
            {"label_printed": "regular", "first_item_placed": "rush"},
            {"label_printed": "regular", "first_item_placed": "regular"},
        ])
        self.assertEqual(r["witness"]["events"], ["label_printed", "rush_arrived"])
        self.assertFalse(r["post_finish_control"]["diverges"])
        self.assertEqual(set(r["post_finish_control"]["actions"].values()), {"rush"})

    def test_repair_resolves_only_middle_case(self):
        original = analyze(PROCEDURE, proposal("label_printed", "first_item_placed"))
        for meaning, definition, middle in [
            ("label_printed", "Packing starts when the label is printed.", "regular"),
            ("first_item_placed", "Packing starts when the first item enters the carton.", "rush"),
        ]:
            with self.subTest(meaning=meaning):
                amended = PROCEDURE + " " + definition
                selected = proposal(meaning)
                selected["readings"][0]["quote"] = definition
                repaired = analyze(amended, selected)
                self.assertEqual(repaired["status"], "single_reading")
                self.assertIsNone(repaired["witness"])
                self.assertEqual(repaired["cases"][1]["actions"][meaning], middle)
                for i in (0, 2):
                    self.assertEqual(repaired["cases"][i]["actions"][meaning],
                                     original["cases"][i]["actions"][meaning])
                span = repaired["readings"][0]
                self.assertEqual(amended[span["start"]:span["end"]], definition)

    def test_quiet_abstention_executes_no_trace(self):
        r = analyze("Consolidate the shipments.", {
            "status": "outside_scope", "readings": [], "reason": "No queue priority specified",
        })
        self.assertEqual(r["status"], "abstained")
        self.assertIsNone(r["witness"])
        self.assertEqual(r["searched_traces"], 0)

    def test_invented_or_missing_preconditions_rejected(self):
        for name in ("rush_priority_quote", "finish_started_quote"):
            for bad in ("", None, "Allow supervisor override."):
                with self.subTest(name=name, bad=bad), self.assertRaises(ValueError):
                    analyze(PROCEDURE, proposal("label_printed") | {name: bad})

    def test_unsupported_or_unquoted_interpretations_rejected(self):
        for event, quote in [
            ("loaded_on_truck", FINISH), ("label_printed", "Invented phrase."), ("label_printed", "  "),
        ]:
            p = proposal("label_printed")
            p["readings"] = [{"starts_at": event, "quote": quote}]
            with self.subTest(p=p), self.assertRaises(ValueError):
                analyze(PROCEDURE, p)
        with self.assertRaises(ValueError):
            analyze(PROCEDURE, proposal("label_printed", "label_printed"))

    def test_reject_illegal_event_sequences(self):
        for trace in [
            [], ["first_item_placed", "rush_arrived"], ["rush_arrived", "label_printed"],
            ["label_printed", "label_printed", "rush_arrived"], ["rush_arrived", "rush_arrived"],
            ["packing_finished", "rush_arrived"],
        ]:
            with self.subTest(trace=trace), self.assertRaises(ValueError):
                replay(trace, "label_printed")


if __name__ == "__main__":
    unittest.main()
