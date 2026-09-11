- Does the parse_state function return enough information to generate legal shots and apply one?
    Yes, parse_state function returns a validated dictionary containing the ships and the cells they occupy and a validated list containing every cell that has already been fired at

- Is it easy to check whether a cell has already been fired at, and which ship (if any) it belongs to?
    Yes, the shots list makes it easy the check whether a shot has been fired already
    Yes, the ship dictionary make it easy to see where the hit cell is located

- Can every member of the team explain the difference between a "hit" and a "sunk" ship, and how sinking every ship ends the game?
    A hit means the player has fired correctly at ship but at least one cell remain in the ship
    A sunk ship means the player has hit all cells in a ship.
    The all_ships_sunk function checks every ship If the sip has been completely hit

- Does the apply_shot function cleanly reject a shot at a cell that's already been fired at?
    Yes, the function checks this before adding the shot. Invalid shots are rejected

- What was your approach to teamwork?
    We met as a team and decided the process and flow of information. We created pseudocode. We designated function group memeber. Then we came together and worked out any remaining issues.
- What improvements remain?
    Save the game
    Menu
    Instructions and rules how to play
    Friendlier and more discriptive error codes

