"""
-------- CSV --------
Header:
0: id              -
1: rated           -
2: created_at      -
3: last_move_at    -
4: turns           -
5: victory_status  -
6: winner          -
7: increment_code  -
8: white_id        -
9: white_rating    -
10: black_id       -
11: black_rating   -
12: moves          -
13: opening_eco    -
14: opening_name   -
15: opening_ply    -

--- Chess Library ---
a1 - 0
b1 - 1
   |
h1 - 7
a2 - 8
   |
h8 - 63


------ Summary ------
move
captured
moved_piece
is_promotion
promote_to
is_check

----- Analysis -----
captures
checks
check_squares
check_origins
promotions
move_count
piece_move_count
promotion_squares

----- Questions -----
- Multiple or combine them somehow?
- Best way to do board
    geom_tile?
    geom_raster?
    something something bins?
- ^ How do best convert, row/col for x/y
    or just use current # somehow?
    index at 0 or 1?
    [row, col] or [col, row]
    (python is <- for indexing)



Group via difference in rating not based on actual rating?
also add some about rating groups too probably? maybe based on 

+-----------------------------+
|             |       |       |
|             |       |       |
|             |       +-------+
|             |               |
|             |               |
|             |               |
|             +---------------+
|                             |
|                             |
|                             |
|                             |
|                             |
+-----------------------------+


game_diff,player,piece,count <---
    Pre group or let R do the work
    is it convient to group in R
    (~20,000 data points)

Stakes of big idea if smalls takes
/\
|
cut for making bins

images in same pdf?
bullet point for readability?
"""

CSV_NAME = "games.csv"
DATA_NAME = "chess_data.txt"
READABLE_DATA = "data.txt"
CSV_STORAGE = "./UseableCSV/"

PIECES = {
    'p': 'pawn',
    'r': 'rook',
    'b': 'bishop',
    'n': 'knight',
    'q': 'queen',
    'k': 'king',
    'none': None,
    None: None
}

CSV_HEADERS = {
    "captures": "player,piece_moved,piece_taken,count",
    "checks": "player,piece,count",
    "check_squares": "player,square,moved_piece,moved_from,count",
    "check_origins": "player,king_pos,checker,check_square,count",
    "move_count": "player,square,count",
    "piece_move_count": "player,piece,square,count",
    "promotion_squares": "square,count",
    "promotions": "player,promote_to,count"
}
CSV_HEADER_PREFIX = ""

# ---- File Handeling ----

def get_csv():
    with open(CSV_NAME, "r") as file:
        text = file.read()
    game = [line.split(",") for line in text.split('\n')[1:-1]]
    
    for g in range(len(game)):
        game[g][12] = game[g][12].split(' ')
    return game


def square_to_move(move):
    """
    0 -> a1
    1 -> b1
    |
    7 -> h1
    8 -> a2
    |
    63 -> h8
    """
    left = (move % 8) + 97
    right = (move // 8) + 1
    return chr(left) + str(right)


def move_to_square(square):
    """
    a1 -> 1, 1
    b4 -> 2, 4
    """
    col = ord(square[0]) - 97 + 1  # index at 1 to match chess board
    row = int(square[1])
    return col, row
