# Store all possible column letters on the board. [Eliah]
COLUMNS = "ABCDEFGHIJ"

# Store all possible row numbers on the board.
ROWS = range(1, 11)

# Create every possible cell, such as A1, A2, B1, B2, etc.
BOARD_CELLS = [f"{column}{row}" for column in COLUMNS for row in ROWS]

# Store each ship and its required size.
FLEET = {
    "carrier": 5,       # Carrier takes 5 cells.
    "battleship": 4,    # Battleship takes 4 cells.
    "cruiser": 3,       # Cruiser takes 3 cells.
    "submarine": 3,     # Submarine takes 3 cells.
    "destroyer": 2,     # Destroyer takes 2 cells.
}


# Convert the text version of a game state into a dictionary. [Eliah]
def parse_state(text):

    # Split the text into the ship information and shot information.
    

    # Create an empty dictionary to store the ships.
    

    # Go through each ship in the ship section.
    

        # Split the ship name from the cells it occupies.
        

        # Remove extra spaces and store the ship's cells.
        

    # Remove extra spaces and turn the shots into a list.
    

    # Return the complete game state.
    


# Find all cells where the player can legally shoot.[Hafsa and Lawerence]
def generate_legal_shots(state):

    #I have created an  empty list for legal shots.
        legal_shots = []

    

    # Check every cell on the board.
    

        # Only add the cell if it has not already been shot.
        

            # Add the cell to the legal shots list.
            

    # Return all cells that can still be shot.
    


# Apply a shot to the current game state.[Hannah and Muhammad]
def apply_shot(state,cell):

    # Add the new shot to the list of previous shots.
    

    # Check every ship on the board.
    

        # Check whether the shot hit this ship.
        

            # Remove the shot cell from the ship.
            

            # If no cells remain, the ship has been sunk.
            

                # Tell the game that the ship was sunk.
                

            # Tell the game that the ship was hit.
            

    # If the shot did not hit any ship, it was a miss.
    