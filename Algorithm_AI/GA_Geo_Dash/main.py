from utils import get_name, print_game_state
from geo_person import GeoPerson, modify_moves, GEO_MODIFY_BACK, STARTING_X, STARTING_Y

import random
import time

from typing import List

# Feel free to change this number or remove it. The number is chosen for ease of consistency

BOARD_VIEW = 100
FPS = .1
GEO_PEOPLE_COUNT = 10
NUMBER_OF_POTENTIAL_GENERATIONS = 100
SEED = 1
VIEW_GENERATION_EPOCH = 10

random.seed(SEED)

# Fun ascii characters can be found here
# https://www.sciencebuddies.org/science-fair-projects/references/ascii-table
BOARD = open("board.txt").read()
BOARD_BKG = BOARD.split("\n")


def game_loop(
    board: List[str],
    people_starting_pos: int,
    geo_people: List[GeoPerson],
    fps: float = 0.1,
    can_print_board: bool = False,
    generation: int = 0,
    previous_generation_best_score: int = 0,
) -> List[GeoPerson]:
    """The geo dash game

    Args:
        board (List[str]): a list of strings which helps show the y axis of the board.
            *NOTE* Game runs for the length of the bottom of the map
        people_starting_pos (int): This should ALWAYS be the STARTING_X value
        geo_people (List[GeoPerson]): All of the 'players' to compete in evolution
        fps (float, optional): Frames Per Second.
            Defaults to 0.1.
        can_print_board (bool, optional): Due to it taking 0->100+ itterations, you can turn this on and off to help pick up the speed.
            Defaults to False.
        generation (int, optional): A varible used for visual display only.
            Defaults to 0.
        previous_generation_best_score (int, optional): A varible used for visual display only.
            Defaults to 0.

    Returns:
        List[GeoPerson]: the modified Geo People from this game loop
    """

    # A for loop to itterate over the board. *NOTE* Game runs for the length of the bottom of the map
    for index in range(len(board[-1]) - people_starting_pos):
        # Sorting the Geo People to make sure that we always have an alive Geo Person to view
        geo_people = sorted(geo_people, key=lambda person: int(not person.is_alive))

        # Check if everyone died, and the game can end pre-maturely
        if not geo_people[0].is_alive:
            break

        # Printing the board in the terminal
        if can_print_board:
            print_game_state(
                board=board,
                start_index=index,
                screen_size=BOARD_VIEW,
                geo_people=geo_people,
                generation=generation,
                previous_generation_best_score=previous_generation_best_score,
            )

        # itterating over all of the Geo People and preforming their moves
        for person in geo_people:
            # Reducing Big O since we sorted above. When we reach this, we know all persons next are also dead
            if not person.is_alive:
                break

            # Checking if person is alive now and if not, to move to the next person
            person.check_if_is_alive(board, index)
            if not person.is_alive:
                person.score = index
                continue

            # Allowing for the person to move
            person.move(board, index)

        time.sleep(fps)

    return geo_people

def main():
    geo_people: List[GeoPerson] = [
        GeoPerson(
            moves=[
                random.randint(0, 1) for _ in range(len(BOARD_BKG[-1]) - STARTING_X)
            ],
            x_position=STARTING_X,
            y_position=STARTING_Y,
            name=get_name(),
        )
        for _ in range(GEO_PEOPLE_COUNT)
    ]

    # Defaulting a winner
    best_geo_person: GeoPerson = GeoPerson(
        [], x_position=STARTING_X, y_position=STARTING_Y, name="N/A"
    )

    for generation in range(NUMBER_OF_POTENTIAL_GENERATIONS):
        # Playing the Geo Dash game!
        geo_people = game_loop(
            board=BOARD_BKG,
            people_starting_pos=STARTING_X,
            geo_people=geo_people,
            fps=0 if bool(generation % VIEW_GENERATION_EPOCH) else FPS,
            generation=generation,
            can_print_board=not bool(generation % VIEW_GENERATION_EPOCH),
            previous_generation_best_score=best_geo_person.score,
        )

        # Grabbing the best preforming Geo Person
        best_geo_person = geo_people[0]

        # If the best Geo Person reached the end of the board, we can then exit the evolution because the model is fully trained
        if best_geo_person.score >= (len(BOARD_BKG[-1]) - STARTING_X - 1):
            break

        # Creating a new batch of Geo People inspired by the moves of the best preforming Geo Person
        geo_people = [
            GeoPerson(
                moves=modify_moves(list(best_geo_person.moves), best_geo_person.score - GEO_MODIFY_BACK),
                x_position=STARTING_X,
                y_position=STARTING_Y,
                name=get_name(),
            )
            for _ in range(GEO_PEOPLE_COUNT - 1)
        ]

        # Resetting the best Geo Person, and allowing them to compete again. This is because all of the offsprings could be worse
        best_geo_person.reset_geo(STARTING_X, STARTING_Y)
        geo_people.append(best_geo_person)

    # Restting the best Geo Person for one final run before the app closes!!!
    best_geo_person.reset_geo(STARTING_X, STARTING_Y)
    game_loop(
        board=BOARD_BKG,
        people_starting_pos=STARTING_X,
        geo_people=geo_people,
        generation=generation,
        can_print_board=True,
        fps=0.1,
    )

if __name__ == "__main__":
    main()