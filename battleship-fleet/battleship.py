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
        

    # Remove extra spaces and tdef display_result(result):urn the shots into a list.
    

    # Return the complete game state.
    


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
    #Remove extra spaces from the cell name 
    cell = cell.strip() #check whether the cell is a valid board cell 
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

    # Check if the result from apply_shot() was "hit".
    if result == "hit":

        # Tell the player that their shot hit a ship.
        return "Hit!"

    # If the result was not "hit", check whether it was "miss".
    elif result == "miss":

        # Tell the player that their shot missed all ships.
        return "Miss!"

    # If it was not a hit or miss, check whether a ship was sunk.
    # startswith("sunk:") checks whether the result begins with "sunk:".
    elif result.startswith("sunk:"):

        # Split the result at the ":" character.
        # For example, "sunk:carrier" becomes ["sunk", "carrier"].
        ship_name = result.split(":")[1]

        # Create a message using the name of the ship that was sunk.
        # The f before the string allows us to insert ship_name.
        return f"Hit! You sank the {ship_name}!"

    # If the result was not hit, miss, or sunk,
    # then something unexpected happened.
    else:

        # Return a message explaining that the result was unknown.
        return "Unknown result."


# Call the all_ships_sunk() function and give it our current game state.
# The function will return either True or False.
if all_ships_sunk(state):

    # This runs if all_ships_sunk() returned True.
    # It means every ship in the fleet has been destroyed.
    print("Fleet defeated! Game over!")

else:

    # This runs if all_ships_sunk() returned False.
    # It means at least one ship cell has not been hit yet.
    print("Fleet undefeated. The game continues!")
