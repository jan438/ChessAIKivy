import ai
from move import Move

class Piece():

    WHITE = "W"
    BLACK = "B"

    def __init__(self, x, y, color, piece_type, value, id):
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = piece_type
        self.value = value
        self.id = id

    def get_possible_diagonal_moves(self, boardai):
        moves = []

        for i in range(1, 8):
            if (not boardai.in_bounds(self.x+i, self.y+i)):
                break

            piece = boardai.get_piece(self.x+i, self.y+i)
            moves.append(self.get_move(boardai, self.x+i, self.y+i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not boardai.in_bounds(self.x+i, self.y-i)):
                break

            piece = boardai.get_piece(self.x+i, self.y-i)
            moves.append(self.get_move(boardai, self.x+i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not boardai.in_bounds(self.x-i, self.y-i)):
                break

            piece = boardai.get_piece(self.x-i, self.y-i)
            moves.append(self.get_move(boardai, self.x-i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not boardai.in_bounds(self.x-i, self.y+i)):
                break

            piece = boardai.get_piece(self.x-i, self.y+i)
            moves.append(self.get_move(boardai, self.x-i, self.y+i))
            if (piece != 0):
                break

        return self.remove_null_from_list(moves)

    def get_possible_horizontal_moves(self, boardai):
        moves = []

        for i in range(1, 8 - self.x):
            piece = boardai.get_piece(self.x + i, self.y)
            moves.append(self.get_move(boardai, self.x+i, self.y))

            if (piece != 0):
                break

        for i in range(1, self.x + 1):
            piece = boardai.get_piece(self.x - i, self.y)
            moves.append(self.get_move(boardai, self.x-i, self.y))
            if (piece != 0):
                break

        for i in range(1, 8 - self.y):
            piece = boardai.get_piece(self.x, self.y + i)
            moves.append(self.get_move(boardai, self.x, self.y+i))
            if (piece != 0):
                break

        for i in range(1, self.y + 1):
            piece = boardai.get_piece(self.x, self.y - i)
            moves.append(self.get_move(boardai, self.x, self.y-i))
            if (piece != 0):
                break

        return self.remove_null_from_list(moves)

    def get_move(self, boardai, xto, yto):
        move = 0
        if (boardai.in_bounds(xto, yto)):
            piece = boardai.get_piece(xto, yto)
            if (piece != 0):
                if (piece.color != self.color):
                    move = Move(self.x, self.y, xto, yto)
            else:
                move = Move(self.x, self.y, xto, yto)
        return move

    def remove_null_from_list(self, l):
        return [move for move in l if move != 0]

    def to_string(self):
        return self.color + self.piece_type + " "

class Rook(Piece):

    PIECE_TYPE = "R"
    VALUE = 500

    def __init__(self, x, y, color, id):
        super(Rook, self).__init__(x, y, color, Rook.PIECE_TYPE, Rook.VALUE, id)

    def get_possible_moves(self, boardai):
        return self.get_possible_horizontal_moves(boardai)

    def clone(self):
        return Rook(self.x, self.y, self.color, id)


class Knight(Piece):

    PIECE_TYPE = "N"
    VALUE = 320

    def __init__(self, x, y, color, id):
        super(Knight, self).__init__(x, y, color, Knight.PIECE_TYPE, Knight.VALUE, id)

    def get_possible_moves(self, boardai):
        moves = []
        moves.append(self.get_move(boardai, self.x+2, self.y+1))
        moves.append(self.get_move(boardai, self.x-1, self.y+2))
        moves.append(self.get_move(boardai, self.x-2, self.y+1))
        moves.append(self.get_move(boardai, self.x+1, self.y-2))
        moves.append(self.get_move(boardai, self.x+2, self.y-1))
        moves.append(self.get_move(boardai, self.x+1, self.y+2))
        moves.append(self.get_move(boardai, self.x-2, self.y-1))
        moves.append(self.get_move(boardai, self.x-1, self.y-2))
        return self.remove_null_from_list(moves)

    def clone(self):
        return Knight(self.x, self.y, self.color, id)


class Bishop(Piece):

    PIECE_TYPE = "B"
    VALUE = 330

    def __init__(self, x, y, color, id):
        super(Bishop, self).__init__(x, y, color, Bishop.PIECE_TYPE, Bishop.VALUE, id)

    def get_possible_moves(self, boardai):
        return self.get_possible_diagonal_moves(boardai)

    def clone(self):
        return Bishop(self.x, self.y, self.color, id)


class Queen(Piece):

    PIECE_TYPE = "Q"
    VALUE = 900

    def __init__(self, x, y, color, id):
        super(Queen, self).__init__(x, y, color, Queen.PIECE_TYPE, Queen.VALUE, id)

    def get_possible_moves(self, boardai):
        diagonal = self.get_possible_diagonal_moves(boardai)
        horizontal = self.get_possible_horizontal_moves(boardai)
        return horizontal + diagonal

    def clone(self):
        return Queen(self.x, self.y, self.color, id)


class King(Piece):

    PIECE_TYPE = "K"
    VALUE = 20000

    def __init__(self, x, y, color, id):
        super(King, self).__init__(x, y, color, King.PIECE_TYPE, King.VALUE, id)

    def get_possible_moves(self, boardai):
        moves = []
        moves.append(self.get_move(boardai, self.x+1, self.y))
        moves.append(self.get_move(boardai, self.x+1, self.y+1))
        moves.append(self.get_move(boardai, self.x, self.y+1))
        moves.append(self.get_move(boardai, self.x-1, self.y+1))
        moves.append(self.get_move(boardai, self.x-1, self.y))
        moves.append(self.get_move(boardai, self.x-1, self.y-1))
        moves.append(self.get_move(boardai, self.x, self.y-1))
        moves.append(self.get_move(boardai, self.x+1, self.y-1))
        moves.append(self.get_castle_kingside_move(boardai))
        moves.append(self.get_castle_queenside_move(boardai))
        return self.remove_null_from_list(moves)

    def get_castle_kingside_move(self, boardai):
        piece_in_corner = boardai.get_piece(self.x+3, self.y)
        if (piece_in_corner == 0 or piece_in_corner.piece_type != Rook.PIECE_TYPE):
            return 0
        if (piece_in_corner.color != self.color):
            return 0
        if (self.color == Piece.WHITE and boardai.white_king_moved):
            return 0
        if (self.color == Piece.BLACK and boardai.black_king_moved):
            return 0
        if (boardai.get_piece(self.x+1, self.y) != 0 or boardai.get_piece(self.x+2, self.y) != 0):
            return 0
        return Move(self.x, self.y, self.x+2, self.y)

    def get_castle_queenside_move(self, boardai):
        piece_in_corner = boardai.get_piece(self.x-4, self.y)
        if (piece_in_corner == 0 or piece_in_corner.piece_type != Rook.PIECE_TYPE):
            return 0
        if (piece_in_corner.color != self.color):
            return 0
        if (self.color == Piece.WHITE and boardai.white_king_moved):
            return 0
        if (self.color == Piece.BLACK and boardai.black_king_moved):
            return 0
        if (boardai.get_piece(self.x-1, self.y) != 0 or boardai.get_piece(self.x-2, self.y) != 0 or boardai.get_piece(self.x-3, self.y) != 0):
            return 0
        return Move(self.x, self.y, self.x-2, self.y)


    def clone(self):
        return King(self.x, self.y, self.color, id)


class Pawn(Piece):

    PIECE_TYPE = "P"
    VALUE = 100

    def __init__(self, x, y, color, id):
        super(Pawn, self).__init__(x, y, color, Pawn.PIECE_TYPE, Pawn.VALUE, id)

    def is_starting_position(self):
        if (self.color == Piece.BLACK):
            return self.y == 1
        else:
            return self.y == 8 - 2

    def get_possible_moves(self, boardai):
        moves = []

        # Direction the pawn can move in.
        direction = -1
        if (self.color == Piece.BLACK):
            direction = 1

        # The general 1 step forward move.
        if (boardai.get_piece(self.x, self.y+direction) == 0):
            moves.append(self.get_move(boardai, self.x, self.y + direction))

        # The Pawn can take 2 steps as the first move.
        if (self.is_starting_position() and boardai.get_piece(self.x, self.y+ direction) == 0 and boardai.get_piece(self.x, self.y + direction*2) == 0):
            moves.append(self.get_move(boardai, self.x, self.y + direction * 2))

        # Eating pieces.
        piece = boardai.get_piece(self.x + 1, self.y + direction)
        if (piece != 0):
            moves.append(self.get_move(boardai, self.x + 1, self.y + direction))

        piece = boardai.get_piece(self.x - 1, self.y + direction)
        if (piece != 0):
            moves.append(self.get_move(boardai, self.x - 1, self.y + direction))

        return self.remove_null_from_list(moves)

    def clone(self):
        return Pawn(self.x, self.y, self.color, id)
