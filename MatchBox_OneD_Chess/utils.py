from typing import List, Tuple

from chessBoard import Board, MAX_GAME_LENGTH, WHITE_TEAM_ID, BLACK_TEAM_ID


def get_moves(board: Board, team_id: int) -> List[dict]:
    """A function to find all of the possible moves for a team (used to train the AI)

    Args:
        board (Board): the chess board
        team_id (int): which team we need to collect the moves of

    Returns:
        List[dict]: schema
            [
                {
                    "start" : int,
                    "end"   : int
                },
                ...
            ]
    """
    # init moves
    moves = []
    # itterating over the board and looking for the team_id given
    for piece_index, piece in enumerate(board.board.copy()):
        if piece.team_id != team_id:
            continue
        # checking all of the tiles of the board and seeing if a tile contains a valid move
        piece_move_list = [
            move_index
            for move_index in range(len(board.board))
            if board.validate_move(start=piece_index, end=move_index)
        ]
        # looking for which tiles have the valid move and adding them to the list
        for move in piece_move_list:
            moves.append({"start": piece_index, "end": move})

    return moves


def _train_game_loop(white_moves: dict, black_moves: dict) -> Tuple[dict, dict, int]:
    """A function to itterate over the potential moves and remove moves which cause for the AI to loose

    Args:
        white_moves (List[dict]): list of avaible moves and their states. Schema
            {
                BoardState1 : [
                    {
                        "start" : int,
                        "end"   : int
                    },
                    ...
                ],
                BoardState2 : [
                    {
                        "start" : int,
                        "end"   : int
                    },
                    ...
                ],
                ...
            }

        black_moves (List[dict]): list of avaible moves and their states. Schema
            {
                BoardState1 : [
                    {
                        "start" : int,
                        "end"   : int
                    },
                    ...
                ],
                BoardState2 : [
                    {
                        "start" : int,
                        "end"   : int
                    },
                    ...
                ],
                ...
            }

    Returns:
        Tuple[dict,dict,int]:
            white_moves dict: updated white moves
            black_moves dict: updated black moves
            winner int: -1, WHITE_TEAM_ID, BLACK_TEAM_ID
    """
    # Initalization
    board = Board()
    winner = -1
    turn_team_id = WHITE_TEAM_ID
    board_states = []
    moves = []

    team_move_hashmap = {WHITE_TEAM_ID: white_moves, BLACK_TEAM_ID: black_moves}

    # playing the game for a fixed length, this is because some games may end in a king v king draw
    for _ in range(MAX_GAME_LENGTH):
        # Getting opposite team
        next_turn_team_id = (
            BLACK_TEAM_ID if turn_team_id == WHITE_TEAM_ID else WHITE_TEAM_ID
        )
        # Adding new board state to the list of states (new size = 3)
        board_states.append(board.get_string_board())

        # If this is a new game state, then we want to find the moves for this game state
        if not (board_states[-1] in team_move_hashmap[turn_team_id]):
            team_move_hashmap[turn_team_id][board_states[-1]] = get_moves(
                board=board, team_id=turn_team_id
            )

        # Grabbing a new move
        moves.append(team_move_hashmap[turn_team_id][board_states[-1]][0])

        # moving the board
        board.move_pieces(start=moves[-1]["start"], end=moves[-1]["end"])

        # if the move resulted in the opponent reaching the end of their tree. The team needs to remove that move
        move_lead_to_end_path = (
            board.get_string_board() in team_move_hashmap[next_turn_team_id]
        ) and not (team_move_hashmap[next_turn_team_id][board.get_string_board()])
        move_lead_to_check_mate = not (
            get_moves(board=board, team_id=next_turn_team_id)
        ) and (board._detect_king_is_checked(team_id=next_turn_team_id))
        move_lead_to_stale_mate = not (
            get_moves(board=board, team_id=next_turn_team_id)
        ) and not (board._detect_king_is_checked(team_id=next_turn_team_id))

        # if we have a check mate or a end of node (future moves of this branch lead to check mate) we want to remove the move that lead to this from the previous player
        if move_lead_to_check_mate or move_lead_to_end_path:
            team_move_hashmap[next_turn_team_id][board_states[-2]].remove(moves[-2])
            winner = turn_team_id
            break

        # if the move lead to a stale mate, we conside that a win for the black team, and want to remove this path from the white team
        if move_lead_to_stale_mate:
            if turn_team_id == WHITE_TEAM_ID:
                white_moves[board_states[-1]].remove(moves[-1])
            elif turn_team_id == BLACK_TEAM_ID:
                white_moves[board_states[-2]].remove(moves[-2])

            winner = BLACK_TEAM_ID
            break

        # circular gamestate. Since this is graph theory, we want to make sure to remove any recusrive edges
        if (board.get_string_board() in board_states) and (
            turn_team_id == WHITE_TEAM_ID
        ):
            white_moves[board_states[-1]].remove(moves[-1])
            winner = BLACK_TEAM_ID
            break

        # next persons turn
        turn_team_id = next_turn_team_id

    # if the game timed out, we want to punish the white moves and make them do better
    if winner == -1:
        white_moves[board_states[-2]].remove(moves[-2])

    return white_moves, black_moves, winner


def train() -> dict:
    """A function to build out the solution to the OneD chess puzzle

    Returns:
        dict: white_moves. list of avaible moves and their states. Schema
            {
                BoardState1 : [
                    {
                        "start" : int,
                        "end"   : int
                    },
                    ...
                ],
                BoardState2 : [
                    {
                        "start" : int,
                        "end"   : int
                    },
                    ...
                ],
                ...
            }
    """
    white_moves = {}
    black_moves = {}

    # if you don't see "fully trained" printed, please increase the range. 200 should work unless you touched something you werent supposed to touch
    for _ in range(200):
        white_moves, black_moves, _ = _train_game_loop(
            white_moves=white_moves, black_moves=black_moves
        )

        # A lil bit of cheating, but we know that 11_12_13_00_00_23_22_21 is the first move for white, and that 11_00_13_12_00_23_22_21 is the first move for black when white plays optimally.
        # This just helps reduce the training to not be 200, as well as lets us know when the puzzle is solved for white
        if not black_moves.get("11_00_13_12_00_23_22_21", "NA") or not white_moves.get("11_12_13_00_00_23_22_21", "NA"):
            print("fully trained")
            break

    return white_moves
