# Store all possible column letters on the board.
COLUMNS = "ABCDEFGHIJ"
# COLUMNS is a variable.
# = assigns the string "ABCDEFGHIJ" to that variable.
# A string is written inside quotation marks.

# Store all possible row numbers on the board.
ROWS = range(1, 11)
# range(1, 11) creates numbers from 1 up to, but not including, 11.
# Therefore, it produces 1 through 10.


# Create every possible cell on the board.
BOARD_CELLS = [
    f"{column}{row}"
    for column in COLUMNS
    for row in ROWS
]
# [] creates a list.
# f"{column}{row}" is an f-string that combines the values of
# column and row, for example "A1".
# The first "for" goes through each letter in COLUMNS.
# The second "for" goes through each number in ROWS.
# The result is every possible combination, from A1 to J10.


# Store each ship and its required size.
FLEET = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
# {} creates a dictionary.
# Each entry has a key and a value separated by a colon.
# For example, "carrier": 5 means the key is "carrier"
# and its value is 5.


# Convert a cell such as "A1" into a column and row.
def cell_position(cell):
# def defines a function.
# cell_position is the function name.
# (cell) means the function accepts one parameter called cell.
# The colon : marks the beginning of the function body.

    column = cell[0]
    # [0] accesses the first character of the string.
    # For "A1", cell[0] is "A".

    row = int(cell[1:])
    # [1:] is slicing: it takes everything from index 1 onwards.
    # For "A1", this gives "1".
    # int() converts the string "1" into the integer 1.

    return column, row
    # return sends a value back from the function.
    # The comma creates a tuple containing column and row.


# Check whether all cells belonging to a ship form
# a straight horizontal or vertical line.
def validate_ship_position(cells):

    positions = [
        cell_position(cell)
        for cell in cells
    ]
    # [] creates a list.
    # cell_position(cell) calls the function for each cell.
    # for cell in cells loops through every cell.
    # This is called a list comprehension.

    columns = [position[0] for position in positions]
    # Creates a list containing the first item from each tuple.
    # position[0] gets the column.

    rows = [position[1] for position in positions]
    # Creates a list containing the second item from each tuple.
    # position[1] gets the row.

    if len(set(rows)) == 1:
    # if starts a conditional statement.
    # set(rows) removes duplicate row values.
    # len() counts how many values remain.
    # == checks whether two values are equal.
    # If there is only one unique row, the ship is horizontal.

        row = rows[0]
        # Gets the first row from the rows list.

        column_numbers = [
            COLUMNS.index(column)
            for column in columns
        ]
        # .index() finds the position of a letter in COLUMNS.
        # For example, COLUMNS.index("A") returns 0.
        # The list comprehension does this for every column.

        column_numbers.sort()
        # .sort() arranges the numbers from smallest to largest.

        expected = list(
            range(
                column_numbers[0],
                column_numbers[0] + len(cells)
            )
        )
        # column_numbers[0] gets the first column number.
        # len(cells) gets the number of cells in the ship.
        # range() creates the expected sequence of consecutive columns.
        # list() converts that range into a list.

        return column_numbers == expected
        # == compares the actual column numbers with the expected ones.
        # return sends True or False back to the caller.

    if len(set(columns)) == 1:
    # If all columns are the same, the ship is vertical.

        rows.sort()
        # Sort the row numbers from smallest to largest.

        expected = list(
            range(
                rows[0],
                rows[0] + len(cells)
            )
        )
        # Creates the expected sequence of consecutive row numbers.

        return rows == expected
        # Returns True if the rows are consecutive.

    return False
    # If the ship is neither horizontal nor vertical,
    # the function returns False.


# Validate the complete game state.
def validate_state(state):

    if "ships" not in state or "shots" not in state:
        raise ValueError("State must contain ships and shots.")
    # "ships" not in state checks whether the key is missing.
    # or means either condition can be True.
    # raise creates an exception.
    # ValueError indicates that the supplied value is invalid.

    ships = state["ships"]
    # [] accesses the value associated with the "ships" key.

    shots = state["shots"]
    # Gets the value associated with the "shots" key.

    if not isinstance(ships, dict):
        raise ValueError("Ships must be stored in a dictionary.")
    # isinstance() checks the data type of a value.
    # dict means dictionary.
    # not reverses the condition.
    # Therefore, this runs if ships is NOT a dictionary.

    if not isinstance(shots, list):
        raise ValueError("Shots must be stored in a list.")
    # Checks that shots is a list.

    if set(ships.keys()) != set(FLEET.keys()):
        raise ValueError("State must contain exactly the required ships.")
    # .keys() gets all dictionary keys.
    # set() allows the keys to be compared without considering order.
    # != means "not equal to".
    # This checks that the required ships match exactly.

    occupied_cells = set()
    # Creates an empty set.
    # The set will store cells already occupied by ships.

    for ship, cells in ships.items():
    # for loops through the dictionary.
    # .items() gives both the key and value.
    # ship receives the key.
    # cells receives the value.

        required_size = FLEET[ship]
        # Looks up the required size of the current ship.

        if len(cells) != required_size:
            raise ValueError(
                f"{ship} must occupy {required_size} cells."
            )
        # len() counts the ship's cells.
        # != checks whether the number is incorrect.
        # f-string inserts the values into the error message.

        if len(set(cells)) != len(cells):
            raise ValueError(f"{ship} contains duplicate cells.")
        # set(cells) removes duplicates.
        # If its length is different from the original length,
        # at least one cell was repeated.

        for cell in cells:
        # Loops through every cell belonging to the ship.

            if cell not in BOARD_CELLS:
                raise ValueError(f"Invalid ship cell: {cell}.")
            # Checks whether the cell exists on the board.
            # not in means the value is absent from the list.

            if cell in occupied_cells:
                raise ValueError(f"Ships cannot overlap at {cell}.")
            # Checks whether another ship already occupies the cell.

            occupied_cells.add(cell)
            # .add() puts the cell into the set.

        if not validate_ship_position(cells):
            raise ValueError(
                f"{ship} must occupy consecutive horizontal or vertical cells."
            )
        # Calls validate_ship_position().
        # not means the condition is True when the function returns False.


    if len(set(shots)) != len(shots):
        raise ValueError("Shots cannot contain duplicates.")
    # Checks that every shot is unique.

    for shot in shots:
        if shot not in BOARD_CELLS:
            raise ValueError(f"Invalid shot cell: {shot}.")
    # Checks every shot against the list of valid board cells.

    return True
    # If none of the validation checks failed,
    # the state is valid.


# Convert the text version of a game state into a dictionary.
def parse_state(text):

    ships_str, shots_str = text.split("|")
    # .split("|") divides the text wherever | appears.
    # The two resulting values are assigned to ships_str and shots_str.

    ships = {}
    # Creates an empty dictionary.

    for ship in ships_str.strip().split(";"):
        # .strip() removes spaces at the beginning and end.
        # .split(";") separates the different ships.
        # for processes each ship individually.

        if not ship.strip():
            continue
        # Checks whether the entry is empty.
        # continue skips the current loop iteration.

        name, cells = ship.split(":")
        # Splits the ship name from its cells.
        # The two results are assigned to name and cells.

        ships[name.strip()] = [
            cell.strip()
            for cell in cells.split(",")
            if cell.strip()
        ]
        # Creates a list of cells for the current ship.
        # [] creates the list.
        # .split(",") separates the cells.
        # .strip() removes unnecessary spaces.
        # if cell.strip() ignores empty entries.
        # The resulting list is stored in the dictionary.

    shots = [
        shot.strip()
        for shot in shots_str.strip().split(",")
        if shot.strip()
    ]
    # Creates a list containing all valid shot cells.

    state = {
        "ships": ships,
        "shots": shots
    }
    # Creates the complete game-state dictionary.

    validate_state(state)
    # Calls the validation function to make sure
    # the parsed state is legal.

    return state
    # Returns the completed state dictionary.


# Find all cells where the player can legally shoot.
def generate_legal_shots(state):

    legal_shots = []
    # Creates an empty list.

    for cell in BOARD_CELLS:
        # Checks every cell on the board.

        if cell not in state["shots"]:
            # Checks whether the cell has not already been shot.

            legal_shots.append(cell)
            # .append() adds the cell to the end of the list.

    return legal_shots
    # Returns all cells that are still available.


# Apply a shot to the current game state.
def apply_shot(state, cell):

    cell = cell.strip().upper()
    # .strip() removes extra spaces.
    # .upper() converts letters to uppercase.
    # This allows inputs such as " a1 " to become "A1".

    if cell not in BOARD_CELLS:
        raise ValueError("invalid cell")
    # Rejects cells that do not exist on the board.

    elif cell in state["shots"]:
        raise ValueError("cell has already been fired at.")
    # elif means "otherwise, if".
    # Checks whether the cell has already been shot.

    state["shots"].append(cell)
    # Adds the new shot to the shots list.

    for ship, cells in state["ships"].items():
        # Loops through every ship and its cells.

        if cell in cells:
            # Checks whether the shot hit this ship.

            ship_sunk = all(
                ship_cell in state["shots"]
                for ship_cell in cells
            )
            # all() returns True only if every condition is True.
            # This checks whether every cell of the ship has been hit.

            if ship_sunk:

                fleet_defeated = True
                # Initially assume every ship has been defeated.

                for ship_cells in state["ships"].values():
                    # .values() gives only the cells for each ship.

                    if not all(
                        ship_cell in state["shots"]
                        for ship_cell in ship_cells
                    ):
                        # Checks whether this ship still has unhit cells.

                        fleet_defeated = False
                        # The fleet cannot be defeated.

                        break
                        # Stops the loop because one unsunk ship is enough.

                return {
                    "result": f"sunk:{ship}",
                    "fleet_defeated": fleet_defeated
                }
                # Returns a dictionary describing the result.

            return {
                "result": "hit",
                "fleet_defeated": False
            }
            # The shot hit a ship, but the ship is not sunk.

    return {
        "result": "miss",
        "fleet_defeated": False
    }
    # If no ship contained the cell, the shot was a miss.


# Check whether every ship in the fleet has been completely hit.
def all_ships_sunk(state):

    for ship_cells in state["ships"].values():
        # Gets the cells belonging to each ship.

        for cell in ship_cells:
            # Checks every cell of the current ship.

            if cell not in state["shots"]:
                # If one ship cell has not been shot...

                return False
                # ...the fleet has not been defeated.

    return True
    # Every ship cell has been shot,
    # so the entire fleet is defeated.


# Convert a result into a player-friendly message.
def display_result(result):

    shot_result = result["result"]
    # Gets the result value from the dictionary.

    if shot_result == "hit":
        return "Hit!"
    # == checks whether the result is exactly "hit".

    elif shot_result == "miss":
        return "Miss!"
    # Checks whether the result is "miss".

    elif shot_result.startswith("sunk:"):
        # .startswith() checks whether the string begins with "sunk:".

        ship_name = shot_result.split(":")[1]
        # .split(":") separates "sunk" and the ship name.
        # [1] selects the second item.

        return f"Hit! You sank the {ship_name}!"
        # f-string inserts the ship name into the message.

    else:
        return "Unknown result."
    # else runs when none of the previous conditions were True.


# Run the main game loop.
def play_game(state):

    while True:
        # while repeats the code as long as its condition is True.
        # True is always True, so the loop continues until break.

        legal_shots = generate_legal_shots(state)
        # Calls the function that finds available cells.

        print("Legal shots:", legal_shots)
        # print() displays information in the console.

        cell = input("Enter a cell to shoot (for example A1): ")
        # input() asks the player for text.
        # The player's response is stored in cell.

        try:
            # try begins a section of code where an error may occur.

            result = apply_shot(state, cell)
            # Attempts to apply the player's shot.

        except ValueError as error:
            # except handles a ValueError raised by apply_shot().
            # The error object is stored in the variable error.

            print(error)
            # Displays the error message.

            continue
            # Restarts the while loop without executing the remaining code.

        print(display_result(result))
        # Converts the result into a readable message and displays it.

        if all_ships_sunk(state):
            # Checks whether every ship has been destroyed.

            print("Fleet defeated! Game over!")

            break
            # Stops the while loop.

        print("Fleet undefeated. The game continues!")
        # Runs if at least one ship remains.


# Create the starting game state.
state = {
    "ships": {
        "carrier": ["A1", "A2", "A3", "A4", "A5"],
        "battleship": ["C1", "C2", "C3", "C4"],
        "cruiser": ["E1", "E2", "E3"],
        "submarine": ["G1", "G2", "G3"],
        "destroyer": ["I1", "I2"]
    },
    "shots": []
}
# The outer {} creates the game-state dictionary.
# "ships" contains another dictionary of ships and their cells.
# "shots" contains a list of cells that have been fired at.


# Only start the game when this file is run directly.
if __name__ == "__main__":
    # __name__ is a special Python variable.
    # When this file is run directly, __name__ equals "__main__".
    # This prevents play_game() from running automatically
    # if the file is imported by another Python file.

    play_game(state)
    # Calls the game function using the starting state.

