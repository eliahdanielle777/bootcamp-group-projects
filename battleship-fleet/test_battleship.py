import unittest
import battleship


class TestBattleshipShots(unittest.TestCase):

    def setUp(self):
        self.state = {
            "ships": {
                "carrier": ["A1", "A2", "A3", "A4", "A5"],
                "battleship": ["C1", "C2", "C3", "C4"],
                "cruiser": ["E1", "E2", "E3"],
                "submarine": ["G1", "G2", "G3"],
                "destroyer": ["I1", "I2"]
            },
            "shots": []
        }

    def test_state_contains_all_ships(self):
        self.assertEqual(
            set(self.state["ships"].keys()),
            {
                "carrier",
                "battleship",
                "cruiser",
                "submarine",
                "destroyer"
            }
        )

    def test_legal_shots_exclude_already_fired_cells(self):
        state = {
            "ships": self.state["ships"],
            "shots": ["A1", "B7"]
        }

        legal = battleship.generate_legal_shots(state)

        self.assertNotIn("A1", legal)
        self.assertNotIn("B7", legal)
        self.assertIn("C3", legal)

    def test_apply_shot_hit_not_yet_sunk(self):
        state = {
            "ships": self.state["ships"],
            "shots": []
        }

        result = battleship.apply_shot(state, "A1")

        self.assertEqual(result["result"], "hit")
        self.assertIn("A1", state["shots"])

    def test_apply_shot_miss(self):
        state = {
            "ships": self.state["ships"],
            "shots": []
        }

        result = battleship.apply_shot(state, "B7")

        self.assertEqual(result["result"], "miss")
        self.assertIn("B7", state["shots"])

    def test_apply_shot_sinks_destroyer(self):
        state = {
            "ships": self.state["ships"],
            "shots": ["I1"]
        }

        result = battleship.apply_shot(state, "I2")

        self.assertEqual(result["result"], "sunk:destroyer")
        self.assertIn("I2", state["shots"])

    def test_cannot_fire_at_same_cell_twice(self):
        state = {
            "ships": self.state["ships"],
            "shots": ["A1"]
        }

        with self.assertRaises(ValueError):
            battleship.apply_shot(state, "A1")

    def test_fleet_not_defeated_until_all_ships_are_sunk(self):
        state = {
            "ships": self.state["ships"],
            "shots": [
                "A1", "A2", "A3", "A4", "A5",
                "C1", "C2", "C3", "C4",
                "E1", "E2", "E3",
                "G1", "G2", "G3",
                "I1"
            ]
        }

        result = battleship.apply_shot(state, "I2")

        self.assertEqual(result["result"], "sunk:destroyer")
        self.assertTrue(result["fleet_defeated"])

    def test_fleet_not_defeated_when_one_ship_remains(self):
        state = {
            "ships": self.state["ships"],
            "shots": [
                "A1", "A2", "A3", "A4", "A5",
                "C1", "C2", "C3", "C4",
                "E1", "E2", "E3",
                "G1", "G2", "G3"
            ]
        }

        result = battleship.apply_shot(state, "I1")

        self.assertEqual(result["result"], "hit")
        self.assertFalse(result["fleet_defeated"])

    def test_parse_state_with_all_ships(self):
        text = (
            "carrier:A1,A2,A3,A4,A5;"
            "battleship:C1,C2,C3,C4;"
            "cruiser:E1,E2,E3;"
            "submarine:G1,G2,G3;"
            "destroyer:I1,I2"
            " | A1,B7"
        )

        state = battleship.parse_state(text)

        self.assertEqual(
            state["ships"],
            self.state["ships"]
        )

        self.assertEqual(
            state["shots"],
            ["A1", "B7"]
        )


if __name__ == "__main__":
    unittest.main()

