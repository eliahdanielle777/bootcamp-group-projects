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

    # Call the all_ships_sunk() function and give it our current game state.
    # The function will return either True or False.
    if all_ships_sunk(state):

        # This runs if all_ships_sunk() returned True.
        # It means every ship in the fleet has been destroyed.
        print("Fleet defeated! Game over!")

    # Stop the game because the player has won.
        break


    else:

        # This runs if all_ships_sunk() returned False.
        # It means at least one ship cell has not been hit yet.
        print("Fleet undefeated. The game continues!")
