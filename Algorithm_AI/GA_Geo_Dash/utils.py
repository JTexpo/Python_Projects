from geo_person import GeoPerson, PLAYER_TOKEN

import random
from typing import List

# List of first names
FIRST_NAMES = [
    "John", "Jane", "Michael", "Emily", "William", "Olivia", "James", "Sophia",
    "Benjamin", "Emma", "Jacob", "Isabella", "Ethan", "Mia", "Alexander", "Ava",
    "Daniel", "Charlotte", "Matthew", "Amelia", "Joseph", "Harper", "David", "Evelyn",
    "Andrew", "Abigail", "Samuel", "Elizabeth", "Gabriel", "Sofia", "Henry", "Victoria",
    "Christopher", "Grace", "Anthony", "Chloe", "Jackson", "Camila", "Elijah", "Penelope",
    "Joshua", "Luna", "Carter", "Layla", "Nathan", "Zoey", "Dylan", "Mila", "Luke", "Avery",
    "Isaac", "Ella", "Liam", "Scarlett", "Owen", "Aria", "Caleb", "Lily", "Ryan", "Hannah",
    "Wyatt", "Natalie", "Christian", "Lillian", "Sebastian", "Addison", "Jack", "Aubrey",
    "Julian", "Stella", "Levi", "Zoe", "Aaron", "Leah", "Jayden", "Nora", "Charles", "Hazel",
    "Adam", "Violet", "Thomas", "Aurora", "Connor", "Savannah", "Isaiah", "Audrey", "Jonathan",
    "Brooklyn", "Jeremiah", "Bella", "Eli", "Claire"
]

# List of last names
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
    "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis",
    "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez",
    "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker",
    "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers",
    "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Cooper", "Richardson",
    "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James",
    "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes",
    "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson",
    "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales",
    "Bryant", "Alexander"]


def get_name() -> str:
    """A cutesy function to make the Geo People have more engaging names than just 0 -> 100+

    Returns:
        str: A full name
    """
    return f"{FIRST_NAMES[random.randint(0,len(FIRST_NAMES)-1)]} {LAST_NAMES[random.randint(0,len(LAST_NAMES)-1)]}"

def print_game_state(
    board: List[str],
    start_index: int,
    screen_size: int,
    geo_people: List[GeoPerson],
    generation: int,
    previous_generation_best_score: int,
):
    """A function to print the board as well as generation stats

    Args:
        board (List[str]): a list of strings which helps show the y axis of the board.
            *NOTE* Game runs for the length of the bottom of the map
        start_index (int): Where to start displaying the board
        screen_size (int): Where to end displaying the board
        geo_people (List[GeoPerson]): All of the 'players' to compete in evolution
        generation (int, optional): A varible used for visual display only.
        previous_generation_best_score (int, optional): A varible used for visual display only.
    """

    # Making a copy of the board, because python is weird with lists and may update the reference
    display_board = board.copy()

    # Grabbing the Y axis that the first Geo Person is on
    board_row = list(display_board[geo_people[0].y])
    # Updating the X axis to display the Geo Person
    board_row[geo_people[0].x + start_index] = PLAYER_TOKEN
    # Joining together the list of strings into 1 string
    display_board[geo_people[0].y] = "".join(board_row)

    """
    *NOTE*
    some terminals may not work well with this code, please feel free to try out this instead...

    # IMPORT THIS AT THE TOP OF THE FILE
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    """
    # Clearing screen to make the game visually appealing when updating
    print("\033c", end="")

    # Printing the board
    _ = [ print(row[start_index : start_index + screen_size]) for row in display_board ] 

    # printing the generation stats
    print(
        f"""
AI Stats
{"-"*(screen_size)}
Generation Number        : {generation}
Previous Gen. Score      : {previous_generation_best_score}
Previous Gen. Completion : {round((float(previous_generation_best_score) / float(len(display_board[-1])))*100,2)}%

Active Geo Person        : {geo_people[0].name}
Active Geo Person Action : {"Jump" if geo_people[0].jump_index else "Run" } 

Remaining Alive          : {sum([1 if person.is_alive else 0 for person in geo_people])}/{(len(geo_people))}
Current Score            : {start_index}
"""
    )
