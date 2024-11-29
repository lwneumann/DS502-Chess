from config import *
import chessboard
import json
from alive_progress import alive_bar
from copy import deepcopy


def summarize():
    games = get_csv()
    
    summary = []
    print()
    print(f"Processing {len(games)} games:")
    with alive_bar(len(games)) as bar:
        for g in games:
            w_rat = int(g[9])
            b_rat = int(g[11])
            r_diff = w_rat - b_rat
            b = chessboard.Game(g[12])
            winner = g[6]
            summary.append([w_rat, b_rat, r_diff, winner, b.castled, b.promotes, b.check_game()])
            
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
        },
        "castle": {
            "white": {"King": 0,
                      "Queen": 0},
            "black": {"King": 0,
                      "Queen": 0}
        }
    }
    
    captures = deepcopy(templates['captures'])
    checks = deepcopy(templates['checks'])
    check_squares = deepcopy(templates['check_squares'])
    check_origins = deepcopy(templates['check_origins'])
    promotion = deepcopy(templates['promotion'])
    move_counts = deepcopy(templates['move_counts'])
    piece_move_count = deepcopy(templates['piece_move_count'])
    promotion_squares = deepcopy(templates['promotion_squares'])
    castle_counts = deepcopy(templates['castle'])
    castle_winners = {
        "white": {
            "white": 0,
            "black": 0,
            "draw": 0
        },
        "black": {
            "white": 0,
            "black": 0,
            "draw": 0
        }
    }
    promotion_wins = {
        "white": {
            "white": 0,
            "black": 0
        },
        "black": {
            "white": 0,
            "black": 0
        },
        "draw": {
            "white": 0,
            "black": 0
        }
    }
    openings = {
        "white": {},
        "black": {},
        "draw": {}
    }
    promote_opening = {
        "white": {},
        "black": {}
    }
    winner = {
        "white": 0,
        "black": 0,
        "draw": 0
    }
    diff_winrate = {}
    avg_winrate = {}

    print()
    print('Analizing Data:')
    with alive_bar(len(summary)) as bar:
        for s in summary:
            w_rat, b_rat, r_diff, outcome, castled, proms, s = s

            # Average Winrates
            avg_rat = round((w_rat+b_rat)/2)
            if avg_rat not in avg_winrate:
                avg_winrate[avg_rat] = deepcopy(winner)
            avg_winrate[avg_rat][outcome] += 1

            # Winrate
            if r_diff not in diff_winrate:
                diff_winrate[r_diff] = deepcopy(winner)
            diff_winrate[r_diff][outcome] += 1

            # Castling
            if castled[0]:
                castle_winners['white'][outcome] += 1
            if castled[1]:
                castle_winners['black'][outcome] += 1

            # Promotions
            promotion_wins[outcome]["white"] += proms[0]
            promotion_wins[outcome]["black"] += proms[1]

            for move_num, details in enumerate(s):
                player = turn[move_num%2]

                move = details["move"]
                square = details['square']
                captured = PIECES[details["captured"]]
                moved_piece = PIECES[details["moved_piece"]]
                is_promotion = details["is_promotion"]
                promote_to = PIECES[details["promote_to"]]
                is_check = details["is_check"]
                attackers = details["attackers"]
                castle = details["castle"]

                # Openings
                if move_num == 0:
                    # Opening Moves
                    if move not in openings[outcome].keys():
                        openings[outcome][move] = 0
                    openings[outcome][move] += 1

                    # Promote Openings
                    if proms[0] > 0:
                        if move not in promote_opening["white"].keys():
                            promote_opening["white"][move] = 0
                        promote_opening["white"][move] += 1
                elif move_num == 1 and proms[1] > 0:
                    if move not in promote_opening["black"].keys():
                        promote_opening["black"][move] = 0
                    promote_opening["black"][move] += 1

                # Moves
                if square not in move_counts[player].keys():
                    move_counts[player][square] = 1
                else:
                    move_counts[player][square] += 1

                if square not in piece_move_count[player][moved_piece].keys():
                    piece_move_count[player][moved_piece][square] = 1
                else:
                    piece_move_count[player][moved_piece][square] += 1

                # Captures
                if captured is not None:
                    captures[player][moved_piece][captured] += 1

                # Checks
                #  is_check = False if wasn't check
                #  otherwise is the position of the king in check
                if is_check:
                    # Checks
                    checks[player][moved_piece] += 1

                    # Check Squares
                    if is_check not in check_squares[player].keys():
                        check_squares[player][is_check] = {moved_piece:{square:1}}
                    else:
                        if moved_piece not in check_squares[player][is_check].keys():
                            check_squares[player][is_check][moved_piece] = {square:1}
                        else:
                            if square not in check_squares[player][is_check][moved_piece]:
                                check_squares[player][is_check][moved_piece][square] = 1
                            else:
                                check_squares[player][is_check][moved_piece][square] += 1

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

                # Castle
                if castle == 'k':
                    castle_counts[player]["King"] += 1
                elif castle == 'q':
                    castle_counts[player]["Queen"] += 1
            bar()

    return {
        "move_count": move_counts,
        "piece_move_count": piece_move_count,
        "checks": checks,
        "check_squares": check_squares,
        "check_origins": check_origins,
        "captures": captures,
        "promotions": promotion,
        "promotion_squares": promotion_squares,
        "promotion_wins": promotion_wins,
        "castle_counts": castle_counts,
        "castle_winners": castle_winners,
        "openings": openings,
        "promote_opening": promote_opening,
        "rating_wins": diff_winrate,
        "average_wins": avg_winrate
        }


def save_info(data):
    with open(DATA_NAME, "w+") as file:
        file.write(str(data))
    
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