import piecesai
from move import Move
from pathlib import Path
import os
import sys
import platform
import sysconfig
import csv

class Boardai:

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspiecesai, white_king_moved, black_king_moved, human, alg):
        self.chesspiecesai = chesspiecesai
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved
        self.human = human
        self.alg = alg
        
    def listpieces(self):
        count = 0
        countwhite = 0
        countblack = 0
        for i in range (8):
            for j in range (8):
                if self.chesspiecesai[i][j] != 0:
                    count += 1
                    piece = self.chesspiecesai[i][j]
                    if piece.color == 'W':
                        countwhite += 1
                    if piece.color == 'B':
                        countblack += 1
                    print(count,"AI:",piece.piece_type,piece.color,piece.x,piece.y,piece.id)
        print("Count ","White:",countwhite,"Black::",countblack)     

    @classmethod
    def clone(cls, chessboardai):
        chesspiecesai = [[0 for x in range(Boardai.WIDTH)] for y in range(Boardai.HEIGHT)]
        for x in range(Boardai.WIDTH):
            for y in range(Boardai.HEIGHT):
                piece = chessboardai.chesspiecesai[x][y]
                if (piece != 0):
                    chesspiecesai[x][y] = piece.clone()
        return cls(chesspiecesai, chessboardai.white_king_moved, chessboardai.black_king_moved, chessboardai.human, chessboardai.alg)

    @classmethod
    def new(cls):
        chess_piecesai = [[0 for x in range(Boardai.WIDTH)] for y in range(Boardai.HEIGHT)]
        if sys.platform[0] == 'l':
            path = '/home/jan/git/ChessAIKivy'
        if sys.platform[0] == 'w':
            path = "C:/Users/janbo/OneDrive/Documents/GitHub/ChessAIKivy"
        try:
            os.chdir(path)
            #print("Current working directory: {0}".format(os.getcwd()))
            data_folder = Path("./CSV/")
            file_to_open = data_folder / "begin.csv"
            try:
                with open(file_to_open, 'r') as file:
                    csvreader = csv.reader(file)
                    for row in csvreader:
                        sid = row[1]
                        x = ord(row[2]) - 48
                        y = 7 - (ord(row[3]) - 48)
                        f = row[4]
                        if row[0] == 'C':
                            cls.human = sid
                            cls.alg = f
                        if row[0] == 'W':
                            if sid[0] == 'P':
                                chess_piecesai[x][y] = piecesai.Pawn(x, y, piecesai.Piece.WHITE, id="WhitePawn_"+sid[1])
                            if sid[0] == 'R':
                                chess_piecesai[x][y] = piecesai.Rook(x, y, piecesai.Piece.WHITE, id="WhiteRook_"+sid[1])
                            if sid[0] == 'N':
                                chess_piecesai[x][y] = piecesai.Knight(x, y, piecesai.Piece.WHITE, id="WhiteKnight_"+sid[1])
                            if sid[0] == 'B':
                                chess_piecesai[x][y] = piecesai.Bishop(x, y, piecesai.Piece.WHITE, id="WhiteBishop_"+sid[1])
                            if sid[0] == 'Q':
                                chess_piecesai[x][y] = piecesai.Queen(x, y, piecesai.Piece.WHITE, id="WhiteQueen")
                            if sid[0] == 'K':
                                chess_piecesai[x][y] = piecesai.King(x, y, piecesai.Piece.WHITE, id="WhiteKing")
                                cls.white_king_moved = f
                        if row[0] == 'B':
                            if sid[0] == 'P':
                                chess_piecesai[x][y] = piecesai.Pawn(x, y, piecesai.Piece.BLACK, id="BlackPawn_"+sid[1])
                            if sid[0] == 'R':
                                chess_piecesai[x][y] = piecesai.Rook(x, y, piecesai.Piece.BLACK, id="BlackRook_"+sid[1])
                            if sid[0] == 'N':
                                chess_piecesai[x][y] = piecesai.Knight(x, y, piecesai.Piece.BLACK, id="BlackKnight_"+sid[1])
                            if sid[0] == 'B':
                                chess_piecesai[x][y] = piecesai.Bishop(x, y, piecesai.Piece.BLACK, id="BlackBishop_"+sid[1])
                            if sid[0] == 'Q':
                                chess_piecesai[x][y] = piecesai.Queen(x, y, piecesai.Piece.BLACK, id="BlackQueen")
                            if sid[0] == 'K':
                                chess_piecesai[x][y] = piecesai.King(x, y, piecesai.Piece.BLACK, id="BlackKing")
                                cls.black_king_moved = f
                    file.close()
                    return cls(chess_piecesai, False, False, cls.human, cls.alg)
            except IOError: 
                print("Error: File does not appear to exist.")
            except Exception as err:
                print("Unexpected error",repr(err))
        except FileNotFoundError:
            print("Directory: {0} does not exist".format(path))
        except NotADirectoryError:
            print("{0} is not a directory".format(path))
        except PermissionError:
            print("You do not have permissions to change to {0}".format(path))
        # Create pawns.
        for x in range(Boardai.WIDTH):
            chess_piecesai[x][Boardai.HEIGHT-2] = piecesai.Pawn(x, Boardai.HEIGHT-2, piecesai.Piece.WHITE, id="WhitePawn_"+str(x))
            chess_piecesai[x][1] = piecesai.Pawn(x, 1, piecesai.Piece.BLACK, id="BlackPawn_"+str(x))

        # Create rooks.
        chess_piecesai[0][Boardai.HEIGHT-1] = piecesai.Rook(0, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteRook_0")
        chess_piecesai[Boardai.WIDTH-1][Boardai.HEIGHT-1] = piecesai.Rook(Boardai.WIDTH-1, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteRook_1")
        chess_piecesai[0][0] = piecesai.Rook(0, 0, piecesai.Piece.BLACK, id="BlackRook_0")
        chess_piecesai[Boardai.WIDTH-1][0] = piecesai.Rook(Boardai.WIDTH-1, 0, piecesai.Piece.BLACK, id="BlackRook_1")

        # Create Knights.
        chess_piecesai[1][Boardai.HEIGHT-1] = piecesai.Knight(1, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteKnight_0")
        chess_piecesai[Boardai.WIDTH-2][Boardai.HEIGHT-1] = piecesai.Knight(Boardai.WIDTH-2, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteKnight_1")
        chess_piecesai[1][0] = piecesai.Knight(1, 0, piecesai.Piece.BLACK, id="BlackKnight_0")
        chess_piecesai[Boardai.WIDTH-2][0] = piecesai.Knight(Boardai.WIDTH-2, 0, piecesai.Piece.BLACK, id="BlackKnight_1")

        # Create Bishops.
        chess_piecesai[2][Boardai.HEIGHT-1] = piecesai.Bishop(2, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteBishop_0")
        chess_piecesai[Boardai.WIDTH-3][Boardai.HEIGHT-1] = piecesai.Bishop(Boardai.WIDTH-3, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteBishop_1")
        chess_piecesai[2][0] = piecesai.Bishop(2, 0, piecesai.Piece.BLACK, id="BlackBishop_0")
        chess_piecesai[Boardai.WIDTH-3][0] = piecesai.Bishop(Boardai.WIDTH-3, 0, piecesai.Piece.BLACK, id="BlackBishop_1")

        # Create King & Queen.
        chess_piecesai[4][Boardai.HEIGHT-1] = piecesai.King(4, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteKing")
        chess_piecesai[3][Boardai.HEIGHT-1] = piecesai.Queen(3, Boardai.HEIGHT-1, piecesai.Piece.WHITE, id="WhiteQueen")
        chess_piecesai[4][0] = piecesai.King(4, 0, piecesai.Piece.BLACK, id="BlackKing")
        chess_piecesai[3][0] = piecesai.Queen(3, 0, piecesai.Piece.BLACK, id="BlackQueen")

        return cls(chess_piecesai, False, False, cls.human, cls.alg)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Boardai.WIDTH):
            for y in range(Boardai.HEIGHT):
                piece = self.chesspiecesai[x][y]
                if (piece != 0):
                    if (piece.color == color):
                        moves += piece.get_possible_moves(self)

        return moves

    def perform_move(self, move):
        piece = self.chesspiecesai[move.xfrom][move.yfrom]
        if piece == 0:
            return
        if (piece.piece_type == piecesai.Pawn.PIECE_TYPE) and (move.yfrom == 3 and move.yto == 2):
            if move.xto == move.xfrom - 1 or move.xto == move.xfrom + 1:
                self.chesspiecesai[move.xto][3] = 0
                self.chesspiecesai[move.xfrom][3] = 0
        self.move_piece(piece, move.xto, move.yto)
        
        if (piece.piece_type == piecesai.Pawn.PIECE_TYPE):
        
            # If a pawn reaches the end, upgrade it to a queen.
            if (piece.y == 0 or piece.y == Boardai.HEIGHT-1):
                if piece.color == piecesai.Piece.WHITE:
                    promoqueen = "WhiteQueen"
                else:
                    promoqueen = "BlackQueen"    
                self.chesspiecesai[piece.x][piece.y] = piecesai.Queen(piece.x, piece.y, piece.color, promoqueen)
                
        if (piece.piece_type == piecesai.King.PIECE_TYPE):
            # Mark the king as having moved.
            if (piece.color == piecesai.Piece.WHITE):
                self.white_king_moved = True
            else:
                self.black_king_moved = True
            
            # Check if king-side castling
            if (move.xto - move.xfrom == 2):
                rook = self.chesspiecesai[piece.x+1][piece.y]
                self.move_piece(rook, piece.x-1, piece.y)
            # Check if queen-side castling
            if (move.xto - move.xfrom == -2):
                rook = self.chesspiecesai[piece.x-2][piece.y]
                self.move_piece(rook, piece.x+1, piece.y)
                
    
    def move_piece(self, piece, xto, yto):
        self.chesspiecesai[piece.x][piece.y] = 0
        piece.x = xto
        piece.y = yto

        self.chesspiecesai[xto][yto] = piece


    # Returns if the given color is checked.
    def is_check(self, color):
        other_color = piecesai.Piece.WHITE
        if (color == piecesai.Piece.WHITE):
            other_color = piecesai.Piece.BLACK

        for move in self.get_possible_moves(other_color):
            copy = Boardai.clone(self)
            copy.perform_move(move)

            king_found = False
            for x in range(Boardai.WIDTH):
                for y in range(Boardai.HEIGHT):
                    piece = copy.chesspiecesai[x][y]
                    if (piece != 0):
                        if (piece.color == color and piece.piece_type == piecesai.King.PIECE_TYPE):
                            king_found = True

            if (not king_found):
                return True

        return False

    # Returns piece at given position or 0 if: No piece or out of bounds.
    def get_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0

        return self.chesspiecesai[x][y]

    def in_bounds(self, x, y):
        return (x >= 0 and y >= 0 and x < Boardai.WIDTH and y < Boardai.HEIGHT)

    def to_string(self):
        string =  "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for y in range(Boardai.HEIGHT):
            string += str(8 - y) + " | "
            for x in range(Boardai.WIDTH):
                piece = self.chesspiecesai[x][y]
                if (piece != 0):
                    string += piece.to_string()
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"
