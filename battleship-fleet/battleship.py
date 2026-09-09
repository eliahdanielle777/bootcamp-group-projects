COLUMNS = "ABCDEFGHIJ"
ROWS = range(1, 11)

BOARD_CELLS = [f"{column}{row}" for column in COLUMNS for row in ROWS]

FLEET = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2,
}

muhammad = [1,2,3]
hannah = "testing"
eliah=[1,2,3]
google = "fun"

def parse_state(text):
    ships_str, shots_str = [part.strip() for part in text.split("|")]

    ships = {}
    for entry in ships_str.split(";"):
        name, cells = entry.split(":")
        ships[name.strip()] = [cell.strip() for cell in cells.split(",")]

    shots = [cell.strip() for cell in shots_str.split(",") if cell.strip()]

    return ...


def generate_legal_shots(state):
    raise NotImplementedError("This function is not implemented yet.")


def apply_shot(state, cell):
    raise NotImplementedError("This function is not implemented yet.")
