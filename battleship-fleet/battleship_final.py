# Store all possible column letters on the board.
COLUMNS = "ABCDEFGHIJ" # This stores A-J as a string of 10 letters

# Store all possible row numbers on the board.
ROWS = range(1, 11) # This stores 1-10 as a numbers in a range (integers)

# Create every possible cell, such as A1, A2, B1, B2, etc.
BOARD_CELLS = [ #This is the start of list syntax
    f"{column}{row}" # This f-string puts the column and row together (A1,A2,A3...)
    for column in COLUMNS # This for-loop iterates through the string, separating the letters (column=A)
    for row in ROWS # This for_loop iterates through the range, separating the numbers (row=1)
] # This is the end of list syntax

# Store each ship and its required size.
FLEET = { # This is the start of dictionary syntax
    "carrier": 5, # This is a key-value pair in which "carrier" is the key and 5 is the value
    "battleship": 4, # This is a key-value pair in which "battleship" is the key and 4 is the value
    "cruiser": 3, # This is a key-value pair in which "cruiser" is the key and 3 is the value
    "submarine": 3, # This is a key-value pair in which "submarine" is the key and 3 is the value
    "destroyer": 2, # This is a key-value pair in which "destroyer" is the key and 2 is the value
} # This is the end of dictionary syntax

# Convert a cell such as "A1" into a column and row.
def cell_position(cell): # This is a function that will return coordinants as a tuple 

    # Get the column letter.
    column = cell[0] # This takes the first character of the coordinants for the string

    # Get the row number.
    row = int(cell[1:]) # This syntax takes the very last character from the string and makes it a number

    # Return the position.
    return column, row # This creates the tuple using the comma and saves the result to the programme

# Check whether all cells belonging to a ship form one straight horizontal or vertical line
def validate_ship_position(cells): # This function checks that the ships are placed linear on the grid

    # Convert every cell into a column and row
    positions = [ # This is the start of list syntax
        cell_position(cell) # This changes a list of strings(ex."A1") into list of tuples("A",1)
        for cell in cells # This for-loop iterates through every cell(coordinant) in the cells(ship) 
    ]# This is the end of list syntax

    # Get all columns and rows.
    columns = [position[0] for position in positions] # This variable collects the first element in every tuple in our list
    rows = [position[1] for position in positions] # This variable collects the second element in every tuple in our list

    # Check whether the ship is horizontal.
    if len(set(rows)) == 1: # This if-statement removes repeats, then checks that the length of the list is 1
        
        # Get the row shared by all cells.
        row = rows[0] # This extracts the first integer from the rows list 

        # Convert column letters into their numeric positions.
        column_numbers = [ # This is the start of list syntax
            COLUMNS.index(column) # The index function calls for the "column" position in the "COLUMN" sequence 
            for column in columns # This for-loop uses the above code to create a list of column index numbers
        ] # This is the end of list syntax

        # Sort the columns.
        column_numbers.sort() # The sort function arranges the number from smallest to largest

        # Check that the columns are consecutive.
        expected = list( # This is the start of list syntax
            range( # This range creates a sequence of column numbers
                column_numbers[0],  # This is the first number in out range because it is the smallest number in the sequence
                column_numbers[0] + len(cells) # This range ends by adding the length of the sequence to the smallest number 
            )
        ) # This is the end of list syntax

        return column_numbers == expected # This return function saves whether or not the 2 lists are identical

    # Check whether the ship is vertical.
    if len(set(columns)) == 1: # This if-statement removes repeats, then checks that the length of the list is 1

        # Sort the row numbers.
        rows.sort() # The sort function arranges the number from smallest to largest

        # Check that the rows are consecutive.
        expected = list( # This is the start of list syntax
            range( # This range creates a sequence of row numbers
                rows[0], # This is the first number in out range because it is the smallest number in the sequence
                rows[0] + len(cells) # This range ends by adding the length of the sequence to the smallest number 
            )
        ) # This is the end of list syntax

        return rows == expected # This return function saves whether or not the 2 lists are identical

    # The ship is neither horizontal nor vertical.
    return False # This returns to the sender that the position is invalid

# Validate the complete game state.
def validate_state(state): # This function checks that the game state is legal

    # Make sure the state has the expected keys.
    if "ships" not in state or "shots" not in state: # This ensures state dictionary contains keys - "ships " and "shots"
        raise ValueError("State must contain ships and shots.") 
        # If one of the keys are missing, raise ValueError with this string

    ships = state["ships"] # This variable gets the state value stored in "ships"
    shots = state["shots"]# This variable gets the state value stored in "shots"

    # Make sure ships is a dictionary.
    if not isinstance(ships, dict): # This if-statement checks if the ship object type is a dictionary.
        raise ValueError("Ships must be stored in a dictionary.") 
        # If ships is not a dictionary, raise ValueError with this string

    # Make sure shots is a list.
    if not isinstance(shots, list): # This if-statement checks if the shots object type is a list.
        raise ValueError("Shots must be stored in a list.") 
        # If shots is not a list, raise ValueError with this string

    # Check that every required ship exists.
    if set(ships.keys()) != set(FLEET.keys()): # This if-statement checks that the game state ships match the fleet ships
        raise ValueError("State must contain exactly the required ships.") 
        # If there is a ship missing in the fleet, raise ValueError with this string

    # Keep track of every cell occupied by a ship.
    occupied_cells = set() # This set will hold the cells occupied by ships

    # Validate every ship.
    for ship, cells in ships.items(): # This for-loop separates the ships and 

        # Get the required size of this ship.
        required_size = FLEET[ship]

        # Check the number of cells.
        if len(cells) != required_size:
            raise ValueError(f"{ship} must occupy {required_size} cells.") 
            # If the ship isn't the correct length, raise ValueError with this string

        # Check for duplicate cells within the ship.
        if len(set(cells)) != len(cells):
            raise ValueError(f"{ship} contains duplicate cells.")
            # If any of the same cells are selected for a ship , raise ValueError with this string

        # Check that every ship cell exists on the board.
        for cell in cells:
            if cell not in BOARD_CELLS:
                raise ValueError(f"Invalid ship cell: {cell}.") 
                # If the cell chosen doesn't exist on the board, raise ValueError with this string

            # Check for overlap with another ship.
            if cell in occupied_cells:
                raise ValueError(f"Ships cannot overlap at {cell}.") 
                # If a ship overlaps with another ship, raise ValueError with this string

            occupied_cells.add(cell)

        # Check that the ship is straight and contiguous.
        if not validate_ship_position(cells):
            raise ValueError(f"{ship} must occupy consecutive horizontal or vertical cells.") 
            # If ship coordinants aren't horizontal or vertical, raise ValueError with this string

    # Check for duplicate shots.
    if len(set(shots)) != len(shots):
        raise ValueError("Shots cannot contain duplicates.")
        # If a shot is made more than once, raise ValueError with this string

    # Check that every shot is a valid board cell.
    for shot in shots:
        if shot not in BOARD_CELLS:
            raise ValueError(f"Invalid shot cell: {shot}.")
            # If shot doesn't exist on the board, raise ValueError with this string

    # The state is valid.
    return True

# Convert the text version of a game state into a dictionary.
def parse_state(text):

    # Split the text into the ship information and shot information.
    ships_str, shots_str = text.split("|")

    # Create an empty dictionary to store the ships.
    ships = {}

    # Go through each ship in the ship section.
    for ship in ships_str.strip().split(";"):

        # Skip empty ship entries.
        if not ship.strip():
            continue

        # Split the ship name from the cells it occupies.
        name, cells = ship.split(":")

        # Remove extra spaces and store the ship's cells.
        ships[name.strip()] = [
            cell.strip()
            for cell in cells.split(",")
            if cell.strip()
        ]

    # Remove extra spaces and turn the shots into a list.
    shots = [
        shot.strip()
        for shot in shots_str.strip().split(",")
        if shot.strip()
    ]

    # Return the complete game state.
    return {
        "ships": ships,
        "shots": shots
    }


# Find all cells where the player can legally shoot.[Hafsa and Lawerence]
def generate_legal_shots(state):
    legal_shots = [] #I have created an  empty list for legal shots.

    for cell in BOARD_CELLS:# Now check every cell on the board
        
        if cell not in state["shots"]: # Only add the cell if it has not already been shot.
            legal_shots.append(cell) # Add the cell to the legal shots list.
            

    # Return all cells that can still be shot.
    return legal_shots


# Apply a shot to the current game state.[Muhammad]
def apply_shot(state,cell):
    #Remove extra spaces from the cell name and accounts for lowercase letters.
    #check whether the cell is a valid board cell.
    cell = cell.strip().upper() 
    if cell not in BOARD_CELLS: 
        raise ValueError("invalid cell") 
    #check whether the cell has already been shot.
    elif cell in state["shots"]: 
        raise ValueError("cell has already been fired at.") 
        #add the new shot to the list of previous shots. 
    state["shots"].append(cell) 
        #check every ship on the board. 
    for ship,cells in state["ships"].items(): 
        #check whether the shot hit this ship. 
        if cell in cells: 
            #check whether every cell belonging to the ship has been shot. 
            ship_sunk = all(ship_cell in state["shots"] for ship_cell in cells) 
            #check whether the ship has been completely destroyed. 
            if ship_sunk: 
                #assume that the entire fleet has been defeated. 
                fleet_defeated = True 
                #check every ship in the fleet. 
                for ship_cells in state["ships"].values(): 
                    #check whether every cell of this ship has been shot. 
                    if not all(ship_cell in state["shots"] for ship_cell in ship_cells): 
                        #The fleet is not defeated if one ship remains. 
                        fleet_defeated = False 
                        #stop checking the remaining ships 
                        break 
                #The sunk result and fleet status. 
                return {"result":f"sunk:{ship}","fleet_defeated":fleet_defeated} 
            #a normal hit because the ship still has cells remaining 
            return {"result":"hit","fleet_defeated":False} 
    #return miss when the shot did not hit any ship. 
    return{"result":"miss","fleet_defeated":False}

# This function checks whether every ship in the player's fleet has been completely hit.[Hannah]
def all_ships_sunk(state):

    # state["ships"] contains all of the ships and the board cells they occupy.
    # .values() gives us only the list of cells for each ship.
    for ship_cells in state["ships"].values():

        # Go through every cell belonging to the current ship.
        # For example, a carrier might have A1, A2, A3, A4 and A5.
        for cell in ship_cells:

            # Check whether this particular ship cell has been shot at.
            # state["shots"] contains all the cells that the player has fired at.
            if cell not in state["shots"]:

                # If even ONE ship cell has not been shot,
                # then that ship has not been completely destroyed.
                # Therefore, the entire fleet cannot be defeated yet.
                return False

    # If we reach this point, we checked every cell of every ship
    # and every ship cell has been shot.
    # Therefore, the entire fleet has been defeated.
    return True


# This function converts the result from apply_shot() into a message that is easier for the player to understand.[Hannah]
def display_result(result):

    # Get the actual results from the dictionary.
    shot_result = result["result"]

    # Check if the result from apply_shot() was "hit".
    if shot_result == "hit":

        # Tell the player that their shot hit a ship.
        return "Hit!"

    # If the result was not "hit", check whether it was "miss".
    elif shot_result == "miss":

        # Tell the player that their shot missed all ships.
        return "Miss!"

    # If it was not a hit or miss, check whether a ship was sunk.
    # startswith("sunk:") checks whether the result begins with "sunk:".
    elif shot_result.startswith("sunk:"):

        # Split the result at the ":" character.
        # For example, "sunk:carrier" becomes ["sunk", "carrier"].
        # Get the name of the ship after "sunk:". 
        ship_name = shot_result.split(":")[1]

        # Create a message using the name of the ship that was sunk.
        # The f before the string allows us to insert ship_name.
        return f"Hit! You sank the {ship_name}!"

    # If the result was not hit, miss, or sunk,
    # then the result is not recognised.
    else:

        # Return a message explaining that the result was unknown.
        return "Unknown result."
    

# Create the starting game state.
# "ships" stores each ship and the cells it occupies.
# "shots" starts as an empty list because no shots have
def play_game():
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

    # Keep the game running until the player defeats the entire fleet.
    while True:

        # Find all the cells that have not been shot yet.
        legal_shots = generate_legal_shots(state)

        # Show the player which cells they can choose from.
        print("Legal shots:", legal_shots)

        # Ask the player which cell they want to shoot.
        cell = input("Enter a cell to shoot (for example A1): ")

        # Try to apply the player's shot.
        try:

            # Apply a shot to the game.
            result = apply_shot(state, cell)

        # If the player enters an invalid or repeated cell,
        # show the error message and ask them to try again.
        except ValueError as error:
            print(error)
            continue

        # Display the result of the shot.
        print(display_result(result))

        # Check whether all ships have been sunk.
        if all_ships_sunk(state):

            # The player has destroyed every ship.
            print("Fleet defeated! Game over!")

            # Stop the game.
            break

        else:

            # At least one ship remains.
            print("Fleet undefeated. The game continues!")


if __name__ == "__main__":
    play_game()
