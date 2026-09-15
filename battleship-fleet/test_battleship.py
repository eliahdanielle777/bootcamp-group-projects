# Import Python's built-in unittest module so we can create and run tests.
import unittest

# Import the battleship_final module, which contains the functions being tested.
import battleship_final


# Define a test class that inherits from unittest.TestCase.
class TestBattleshipShots(unittest.TestCase):

    # setUp() runs automatically before every test method.
    def setUp(self):

        # Create a dictionary representing the starting Battleship game state.
        self.state = {

            # "ships" is a dictionary containing each ship and its occupied cells.
            "ships": {

                # Each ship name is a key, and its board positions are stored in a list.
                "carrier": ["A1", "A2", "A3", "A4", "A5"],

                # The battleship occupies four cells.
                "battleship": ["C1", "C2", "C3", "C4"],

                # The cruiser occupies three cells.
                "cruiser": ["E1", "E2", "E3"],

                # The submarine occupies three cells.
                "submarine": ["G1", "G2", "G3"],

                # The destroyer occupies two cells.
                "destroyer": ["I1", "I2"]
            },

            # "shots" stores all cells where shots have already been fired.
            "shots": []
        }


    # Test that the game state contains all five required ships.
    def test_state_contains_all_ships(self):

        # assertEqual checks whether the two values are exactly equal.
        self.assertEqual(

            # .keys() gets all keys from the ships dictionary.
            # set() converts those keys into a set so their order does not matter.
            set(self.state["ships"].keys()),

            # This is the expected set of ship names.
            {
                "carrier",
                "battleship",
                "cruiser",
                "submarine",
                "destroyer"
            }
        )


    # Test that previously fired cells are excluded from legal shots.
    def test_legal_shots_exclude_already_fired_cells(self):

        # Create a new state for this particular test.
        state = {

            # Reuse the ships dictionary from the setup state.
            "ships": self.state["ships"],

            # A1 and B7 have already been fired at.
            "shots": ["A1", "B7"]
        }

        # Call generate_legal_shots() from battleship_final.
        # The returned value is stored in the variable called legal.
        legal = battleship_final.generate_legal_shots(state)

        # assertNotIn checks that A1 does not appear in the legal shots.
        self.assertNotIn("A1", legal)

        # B7 should also not appear because it has already been fired at.
        self.assertNotIn("B7", legal)

        # C3 has not been fired at, so it should be a legal shot.
        self.assertIn("C3", legal)


    # Test that firing at a ship produces a "hit" result.
    def test_apply_shot_hit_not_yet_sunk(self):

        # Create a state containing the ships but no previous shots.
        state = {
            "ships": self.state["ships"],
            "shots": []
        }

        # Fire a shot at A1.
        # apply_shot() returns a dictionary containing information about the shot.
        result = battleship_final.apply_shot(state, "A1")

        # Check that the returned result is exactly "hit".
        self.assertEqual(result["result"], "hit")

        # Check that A1 was added to the state's list of shots.
        self.assertIn("A1", state["shots"])


    # Test that firing at an empty cell produces a "miss" result.
    def test_apply_shot_miss(self):

        # Create a state with no shots fired yet.
        state = {
            "ships": self.state["ships"],
            "shots": []
        }

        # Fire at B7, which does not contain a ship.
        result = battleship_final.apply_shot(state, "B7")

        # The expected result is "miss".
        self.assertEqual(result["result"], "miss")

        # B7 should still be recorded as a fired shot.
        self.assertIn("B7", state["shots"])


    # Test that firing at the final cell of the destroyer sinks it.
    def test_apply_shot_sinks_destroyer(self):

        # Create a state where I1 has already been hit.
        state = {
            "ships": self.state["ships"],
            "shots": ["I1"]
        }

        # Fire at I2, the destroyer's remaining cell.
        result = battleship_final.apply_shot(state, "I2")

        # The expected result identifies the ship that was sunk.
        self.assertEqual(result["result"], "sunk:destroyer")

        # I2 should be added to the list of shots.
        self.assertIn("I2", state["shots"])


    # Test that the program prevents shooting at the same cell twice.
    def test_cannot_fire_at_same_cell_twice(self):

        # Create a state where A1 has already been fired at.
        state = {
            "ships": self.state["ships"],
            "shots": ["A1"]
        }

        # with creates a context in which we expect an exception to occur.
        # assertRaises checks that the specified exception is raised.
        with self.assertRaises(ValueError):

            # Shooting A1 again should raise a ValueError.
            battleship_final.apply_shot(state, "A1")


    # Test that the fleet is defeated only after every ship has been sunk.
    def test_fleet_not_defeated_until_all_ships_are_sunk(self):

        # Create a state where every ship cell except I2 has been hit.
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

        # Fire at the final remaining destroyer cell.
        result = battleship_final.apply_shot(state, "I2")

        # The destroyer should now be completely sunk.
        self.assertEqual(result["result"], "sunk:destroyer")

        # Since all ships have now been sunk, fleet_defeated should be True.
        self.assertTrue(result["fleet_defeated"])


    # Test that the fleet is not defeated when one ship still has cells remaining.
    def test_fleet_not_defeated_when_one_ship_remains(self):

        # Create a state where every ship except the destroyer has been sunk.
        state = {
            "ships": self.state["ships"],
            "shots": [
                "A1", "A2", "A3", "A4", "A5",
                "C1", "C2", "C3", "C4",
                "E1", "E2", "E3",
                "G1", "G2", "G3"
            ]
        }

        # Fire at I1, which is the first cell of the destroyer.
        result = battleship_final.apply_shot(state, "I1")

        # The destroyer has not been completely hit yet, so the result is "hit".
        self.assertEqual(result["result"], "hit")

        # I2 is still unhit, so the entire fleet has not been defeated.
        self.assertFalse(result["fleet_defeated"])


    # Test that text describing a game state can be converted into a dictionary.
    def test_parse_state_with_all_ships(self):

        # Create a string representation of the game state.
        text = (

            # Define the carrier and its cells.
            "carrier:A1,A2,A3,A4,A5;"

            # Define the battleship and its cells.
            "battleship:C1,C2,C3,C4;"

            # Define the cruiser and its cells.
            "cruiser:E1,E2,E3;"

            # Define the submarine and its cells.
            "submarine:G1,G2,G3;"

            # Define the destroyer and its cells.
            # There is no semicolon here because it is the final ship entry.
            "destroyer:I1,I2"

            # The "|" separates the ship information from the fired shots.
            # A1 and B7 are the shots that have already been made.
            " | A1,B7"
        )

        # Pass the text to parse_state(), which should convert it into a dictionary.
        state = battleship_final.parse_state(text)

        # Check that the parsed ships match the expected ships.
        self.assertEqual(
            state["ships"],
            self.state["ships"]
        )

        # Check that the parsed shots match the expected shots.
        self.assertEqual(
            state["shots"],
            ["A1", "B7"]
        )


# This condition is True only when this Python file is run directly.
# It is False when this file is imported as a module.
if __name__ == "__main__":

    # Start unittest's test runner.
    # This discovers and runs the test methods in the file.
    unittest.main()
