from config import *
import chessboard
import json
from alive_progress import alive_bar
from copy import deepcopy


def summarize():
    games = get_csv()
    
    summary = []
    print(f"Processing {len(games)} games:")
    with alive_bar(len(games)) as bar:
        for g in games:
            r_diff = abs(g[9] - g[11])
            b = chessboard.Game(g[12])

            summary.append([r_diff, b.check_game()])
            
            bar()
    return summary


def analize(summary):
    turn = ['white', 'black']
    
    templates = {
        "captures": {
            'white': {
                'pawn': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'rook': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'bishop': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'knight': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'queen': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'king': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                }
            },
            'black': {
                'pawn': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'rook': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'bishop': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'knight': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'queen': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                },
                'king': {
                    'pawn': 0,
                    'rook': 0,
                    'bishop': 0,
                    'knight': 0,
                    'queen': 0
                }
            }
        },
        "checks": {
            'white': {
                'pawn': 0,
                'rook': 0,
                'bishop': 0,
                'knight': 0,
                'queen': 0,
                'king': 0
            },
            'black': {
                'pawn': 0,
                'rook': 0,
                'bishop': 0,
                'knight': 0,
                'queen': 0,
                'king': 0
            }
        },
        "check_squares": {
            "white": {},
            "black": {}
        },
        "check_origins": {
            "white": {},
            "black": {}
        },
        "promotion": {
            'white': {
                'rook': 0,
                'bishop': 0,
                'knight': 0,
                'queen': 0
            },
            'black': {
                'rook': 0,
                'bishop': 0,
                'knight': 0,
                'queen': 0
            }
        },
        "move_counts": {
            'white': {},
            'black': {}
        },
        "piece_move_count": {
            'white': {
                'pawn': {},
                'rook': {},
                'bishop': {},
                'knight': {},
                'queen': {},
                'king': {}
            },
            'black': {
                'pawn': {},
                'rook': {},
                'bishop': {},
                'knight': {},
                'queen': {},
                'king': {}
            }
        },
        "promotion_squares": {
            "white": {},
            "black": {}
        }
    }
    
    captures = {}
    checks = {}
    check_squares = {}
    check_origins = {}
    promotion = {}
    move_counts = {}
    piece_move_count = {}
    promotion_squares = {}

    print()
    print('Analizing Data:')
    with alive_bar(len(summary)) as bar:
        for s in summary:
            r_diff, s = s

            for move, details in enumerate(s):
                player = turn[move%2]

                move = details["move"]
                square = details['square']
                captured = PIECES[details["captured"]]
                moved_piece = PIECES[details["moved_piece"]]
                is_promotion = details["is_promotion"]
                promote_to = PIECES[details["promote_to"]]
                is_check = details["is_check"]
                attackers = details["attackers"]


                # Moves
                # -- Add diff
                if r_diff not in move_counts.keys():
                    move_counts[r_diff] = deepcopy(templates['move_counts'])
                # --
                if square not in move_counts[r_diff][player].keys():
                    move_counts[r_diff][player][square] = 1
                else:
                    move_counts[r_diff][player][square] += 1

                # -- Add diff
                if r_diff not in piece_move_count.keys():
                    piece_move_count[r_diff] = deepcopy(templates['piece_move_count'])
                # --
                if square not in piece_move_count[r_diff][player][moved_piece].keys():
                    piece_move_count[r_diff][player][moved_piece][square] = 1
                else:
                    piece_move_count[r_diff][player][moved_piece][square] += 1

                # Captures
                if captured is not None:
                    # -- Add diff
                    if r_diff not in captures.keys():
                        captures[r_diff] = deepcopy(templates['captures'])
                    # --
                    captures[r_diff][player][moved_piece][captured] += 1

                # Checks
                #  is_check = False if wasn't check
                #  otherwise is the position of the king in check
                if is_check:
                    # Checks
                    # -- Add diff
                    if r_diff not in checks.keys():
                        checks[r_diff] = deepcopy(templates['captures'])
                    # --
                    checks[r_diff][player][moved_piece] += 1

                    # Check Squares
                    # Add diff
                    if r_diff not in check_squares.keys():
                        check_squares[r_diff] = deepcopy(templates['check_squares'])
                    # --
                    if is_check not in check_squares[r_diff][player].keys():
                        check_squares[r_diff][player][is_check] = {moved_piece:{square:1}}
                    else:
                        if moved_piece not in check_squares[r_diff][player][is_check].keys():
                            check_squares[r_diff][player][is_check][moved_piece] = {square:1}
                        else:
                            if square not in check_squares[r_diff][player][is_check][moved_piece]:
                                check_squares[r_diff][player][is_check][moved_piece][square] = 1
                            else:
                                check_squares[r_diff][player][is_check][moved_piece][square] += 1

                    # TODO |
                    #      V

                    # Check Origin
                    # player, king_place, check_from, square_from, count
                    # -- Add King
                    if is_check not in check_origins[player].keys():
                        check_origins[player][is_check] = {}
                    # -- For each Attacker
                    for a in attackers:
                        # -- Get info
                        attacker_piece, attacker_square = a
                        # -- Fix attacker
                        attacker_piece = PIECES[attacker_piece]
                        # -- Add attacker
                        if attacker_piece not in check_origins[player][is_check].keys():
                            check_origins[player][is_check][attacker_piece] = {}
                        # -- Add attacker pos
                        if attacker_square not in check_origins[player][is_check][attacker_piece].keys():
                            check_origins[player][is_check][attacker_piece][attacker_square] = 0
                        # -- Finally Actually count it
                        check_origins[player][is_check][attacker_piece][attacker_square] += 1

                # Promotions
                if is_promotion:
                    promotion[player][promote_to] += 1
                    if promote_to not in promotion_squares[player].keys():
                        promotion_squares[player][promote_to] = {square: 1}
                    else:
                        if square not in promotion_squares[player][promote_to].keys():
                            promotion_squares[player][promote_to][square] = 1
                        else:
                            promotion_squares[player][promote_to][square] += 1
            bar()

    return {
        "move_count": move_counts,
        "piece_move_count": piece_move_count,
        "checks": checks,
        "check_squares": check_squares,
        "check_origins": check_origins,
        "captures": captures,
        "promotions": promotion,
        "promotion_squares": promotion_squares
    }


def save_info(data):
    with open(DATA_NAME, "w+") as file:
        file.write("data = " + str(data))
    
    with open(READABLE_DATA, 'w+', encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4))

    print()
    print(f"Saved to {DATA_NAME} and {READABLE_DATA}.")
    return

def run():
    save_info(analize(summarize()))
    return


if __name__ == "__main__":
    run()