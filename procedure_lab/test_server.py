import unittest
from unittest.mock import patch
from procedure_lab import model
from procedure_lab.server import ORIGINAL, REPAIRS, procedure_test


class DemoTests(unittest.TestCase):
    def test_demo_repair_changes_only_middle_arrival(self):
        result = procedure_test(ORIGINAL + " " + REPAIRS["first_item_placed"], "example")
        self.assertEqual([case["actions"] for case in result["cases"]], [["rush"],["rush"],["regular"]])
        self.assertEqual(result["source"], "curated_example")

    def test_unrecognized_edit_has_no_canned_replay(self):
        result = procedure_test("Choose an order at random.", "example")
        self.assertEqual((result["status"], result["cases"]), ("abstained", []))

    def test_model_failure_never_falls_back_to_demo(self):
        with patch.object(model, "propose", side_effect=model.ModelError("invalid quotation")):
            with self.assertRaisesRegex(model.ModelError, "quotation"):
                procedure_test(ORIGINAL, "model")
