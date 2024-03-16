import boardai, piecesai, numpy

class Heuristics:

    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    @staticmethod
    def evaluate(boardai):
        material = Heuristics.get_material_score(boardai)

        pawns = Heuristics.get_piece_position_score(boardai, piecesai.Pawn.PIECE_TYPE, Heuristics.PAWN_TABLE)
        knights = Heuristics.get_piece_position_score(boardai, piecesai.Knight.PIECE_TYPE, Heuristics.KNIGHT_TABLE)
        bishops = Heuristics.get_piece_position_score(boardai, piecesai.Bishop.PIECE_TYPE, Heuristics.BISHOP_TABLE)
        rooks = Heuristics.get_piece_position_score(boardai, piecesai.Rook.PIECE_TYPE, Heuristics.ROOK_TABLE)
        queens = Heuristics.get_piece_position_score(boardai, piecesai.Queen.PIECE_TYPE, Heuristics.QUEEN_TABLE)

        return material + pawns + knights + bishops + rooks + queens
        
    @staticmethod    
    def get_piece_position_score(boardai, piece_type, table):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = boardai.chesspiecesai[x][y]
                if (piece != 0):
                    if (piece.piece_type == piece_type):
                        if (piece.color == piecesai.Piece.WHITE):
                            white += table[x][y]
                        else:
                            black += table[7 - x][y]

        return white - black

    @staticmethod
    def get_material_score(boardai):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = boardai.chesspiecesai[x][y]
                if (piece != 0):
                    if (piece.color == piecesai.Piece.WHITE):
                        white += piece.value
                    else:
                        black += piece.value

        return white - black
          
class AI:

    INFINITE = 10000000

    @staticmethod
    def get_ai_move(chessboardai, invalid_moves, aicolor, hmcolor, alg):
        best_move = 0
        best_score = AI.INFINITE
        for move in chessboardai.get_possible_moves(aicolor):
            if (AI.is_invalid_move(move, invalid_moves)):
                continue

            copy = boardai.Boardai.clone(chessboardai)
            copy.perform_move(move)

            if alg == 'A':
                score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True, aicolor, hmcolor)
            if alg == 'M':
                score = AI.minimax(copy, 2, True, aicolor, hmcolor)
         
            if (score < best_score):
                best_score = score
                best_move = move

        # Checkmate.
        if (best_move == 0):
            return 0

        copy = boardai.Boardai.clone(chessboardai)
        copy.perform_move(best_move)
        if (copy.is_check(aicolor)):
            invalid_moves.append(best_move)
            return AI.get_ai_move(chessboardai, invalid_moves, aicolor, hmcolor, alg)

        return best_move

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if (invalid_move.equals(move)):
                return True
        return False

    @staticmethod
    def minimax(chessboardai, depth, maximizing, aicolor, hmcolor):
        if (depth == 0):
            return Heuristics.evaluate(chessboardai)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in chessboardai.get_possible_moves(hmcolor):
                copy = boardai.Boardai.clone(chessboardai)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, False, aicolor, hmcolor)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in chessboardai.get_possible_moves(aicolor):
                copy = boardai.Boardai.clone(chessboardai)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, True, aicolor, hmcolor)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(chessboardai, depth, a, b, maximizing, aicolor, hmcolor):
        if (depth == 0):
            return Heuristics.evaluate(chessboardai)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in chessboardai.get_possible_moves(hmcolor):
                copy = boardai.Boardai.clone(chessboardai)
                copy.perform_move(move)

                best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False, aicolor, hmcolor))
                a = max(a, best_score)
                if (b <= a):
                    break
            return best_score
        else:
            best_score = AI.INFINITE
            for move in chessboardai.get_possible_moves(aicolor):
                copy = boardai.Boardai.clone(chessboardai)
                copy.perform_move(move)

                best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True, aicolor, hmcolor))
                b = min(b, best_score)
                if (b <= a):
                    break
            return best_score
