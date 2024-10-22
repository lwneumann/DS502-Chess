from config import *
import chess

class Game:
    def __init__(self, moves):
        self.board = chess.Board()
        self.moves = moves
        # To store details of each move
        self.move_details = []
        return

    def get_king(self, player):
        return self.board.king(player)

    def get_player(self):
        return self.board.turn

    def get_attackers(self, player=None):
        if player is None:
            player = self.get_player()

        attacker_list = []

        for square in self.board.attackers(chess.WHITE, self.get_king(player)):
            p = self.board.piece_at(square)
            if p.color != player:
                attacker_list.append([p.symbol().lower(), str(square)])
        return attacker_list

    def analyze_move(self, move, turn):
        if "-O" in move:
            # Move
            self.board.push_san(move)

            # Square
            if turn%2 == 0:
                # White
                if move.count('-') == 2:
                    # Queen Side - C1
                    square = 2
                else:
                    # King Side - G1
                    square = 6
            else:
                # Black
                if move.count('-') == 2:
                    # Queen Side - C8
                    square = 58
                else:
                    # King Side - G8
                    square = 62

            # Check
            attackers = []

            is_check = move[-1] == "+"
            if is_check:
                # Get NON active player
                is_check = self.get_king(not self.get_player())
                
                # Get attacks
                attackers = self.get_attackers()

            # Store details
            move_detail = {
                'move': move,
                'square': square,
                'captured': None,
                'moved_piece': "k",
                'is_promotion': None,
                'promote_to': None,
                'is_check': is_check,
                'attackers': attackers
            }
            self.move_details.append(move_detail)
            return

        square = move.replace('+', '')
        square = square.replace('#', '')
        if "=" in square:
            square = square[:-2]
        if len(square) > 2:
            square = square[-2:]
        square = chess.parse_square(square)

        # Get piece
        prior_piece = str(self.board.piece_at(square)).lower()
        
        # Move
        self.board.push_san(move)

        # Moved Piece
        moved_piece = str(self.board.piece_at(square)).lower()

        # Promotion
        is_promotion = "=" in move
        promote_to = None
        if is_promotion:
            if move[-1] in ("+", "#"):
                promote_to = move[-2].lower()
            else:
                promote_to = move[-1].lower()

        # Check
        is_check = move[-1] == "+"
        attackers = []
        if is_check:
            # Get NON active player
            is_check = self.get_king(not self.get_player())

            # Get attackers
            attackers = self.get_attackers()

        # Store details
        move_detail = {
            'move': move,
            'square': square,
            'captured': prior_piece,
            'moved_piece': moved_piece,
            'is_promotion': is_promotion,
            'promote_to': promote_to,
            'is_check': is_check,
            'attackers': attackers
        }
        self.move_details.append(move_detail)
        return

    def check_game(self):
        for turn, m in enumerate(self.moves):
            self.analyze_move(m, turn)
        return self.move_details


def play():
    b = Game([])
    print()
    m = ''

    while m != "exit":
        print(b.board)
        print()
        m = input("Move: ")
        if m == "checks":
            print()
        elif m == "attack":
            b.get_attackers()
        else:
            try:
                b.board.push_san(m)
            except:
                print('\nIllegal Move :(')
        print()
    return


if __name__ == "__main__":
    pass
    # play()