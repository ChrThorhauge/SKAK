
import numpy as np


class Game_state():
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ])
        self.white_to_move = True
        self.move_log = []

        self.checkmate = False
        self.stalemate = False

        self.white_king_location = (7,4)
        self.black_king_location = (0,4)

        self.move_functions = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)


    def in_check(self):
        self.white_to_move = not self.white_to_move
        result = self.check_checker() ## this guy always flips turns
        self.white_to_move = not self.white_to_move
        return result


    def get_valid_moves(self):
        moves = [m for m in self.get_all_moves() if self.is_legal(m)]

        if len(moves) == 0:
            if self.in_check() == True:
                self.checkmate = True
            else:
                self.stalemate = True
        else:

            self.checkmate = False
            self.stalemate = False
        return moves
    

    def is_legal(self, move):
        self.make_move(move)
        in_check = self.check_checker()
        self.undo_move()
        return not in_check


    def check_checker(self):
        # This is called from is_legal and starts by making a move, we want the
        # same color side to check where the king can go. 
        self.white_to_move = not self.white_to_move

        ally_color = "w" if self.white_to_move else "b"
        enemy_color = "b" if self.white_to_move else "w"

        # Keep track of the kings
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        in_check = False

       
        #Let us check moves for minor pieces + king


        tests = [(self.get_rook_moves, "RQ"),
                 (self.get_bishop_moves, "BQ"),
                 (self.get_knight_moves, "N"),
                 (self.get_king_moves, "K")]
        
        for get_move_functions, attackers in tests:
            moves = []
            get_move_functions(king_row, king_col, moves)
            for m in moves:
                if m.piece_captured[0] == enemy_color and m.piece_captured[1] in attackers:
                    in_check = True


        #Check for pawns

        pawn_row = king_row -1 if self.white_to_move else king_row + 1
        if 0 < pawn_row < 7:
            for dc in (-1,1):
                pawn_col = king_col + dc
                if 0 <= pawn_col <= 7 and self.board[pawn_row][pawn_col] == enemy_color + "p":
                    in_check = True


        self.white_to_move = not self.white_to_move
        return in_check

        



    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):    
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)

        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:
            if self.board[r-1][c] == "--":
                moves.append(move((r,c),(r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(move((r,c),(r-2,c), self.board))
            if c-1 >= 0: #Capture to the left
                if self.board[r-1][c-1][0] == "b":
                    moves.append(move((r,c),(r-1,c-1), self.board))
            if c+1 <= 7: #Capture to the right
                if self.board[r-1][c+1][0] == "b":
                    moves.append(move((r,c),(r-1,c+1), self.board))

        if self.white_to_move == False:
            if self.board[r+1][c] == "--":
                moves.append(move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(move((r,c),(r+2,c), self.board))
            if c-1 >= 0: #Capture to the left (from white perspec)
                if self.board[r+1][c-1][0] == "w":
                    moves.append(move((r,c),(r+1,c-1), self.board))
            if c+1 <= 7: #Capture to the right (from white perspec)
                if self.board[r+1][c+1][0] == "w":
                    moves.append(move((r,c),(r+1,c+1), self.board))

    def get_rook_moves(self, r, c, moves):
        directions = ((-1,0),(1,0),(0,-1),(0,1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + i*d[0]
                end_col = c + i*d[1]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((r,c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break                  


          
    def get_knight_moves(self, r, c, moves):
        directions = ( (-2,-1), (-2,1), (-1,2), (-1,-2), (2,-1), (2,1), (1,2), (1,-2) )
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    moves.append(move((r,c), (end_row, end_col), self.board))
                elif end_piece[0] == enemy_color:
                    moves.append(move((r,c), (end_row, end_col), self.board))
                                  
                                


    def get_bishop_moves(self, r, c, moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + i*d[0]
                end_col = c + i*d[1]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((r,c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break                  


    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r,c,moves)
        self.get_bishop_moves(r,c,moves)

    
    
    
    def get_king_moves(self, r, c, moves):
        directions = ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    moves.append(move((r,c), (end_row, end_col), self.board))
                elif end_piece[0] == enemy_color:
                    moves.append(move((r,c), (end_row, end_col), self.board))
        


    

                    



class move():

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6":2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c":2, "d": 3, "e": 4,
                     "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}



    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, move):
            return self.move_id == other.move_id

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)