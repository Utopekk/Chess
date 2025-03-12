import pygame as pg
import sys

from main import change_turn

pg.init()
WIDTH = HEIGHT = 800
SQ_SIZE = WIDTH // 8
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Chess")


class ChessGame:
    def __init__(self):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.turn = 'w'
        self.selected_pos = None
        self.possible_moves = []
        self.last_move = None  # for en passant
        self.king_moved = {'w': False, 'b': False}
        self.rook_moved = {'w': [False, False], 'b': [False, False]}  # [left rook, right rook]

    def draw_board(self, screen, SQ_SIZE):
        for r in range(8):
            for c in range(8):
                color = "WHITE" if (r + c) % 2 == 0 else "GREY"
                pg.draw.rect(screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                if self.is_in_check(self.turn):
                    pg.draw.rect(screen, (255, 0, 0),
                                 (self.find_king(self.turn)[1] * SQ_SIZE, self.find_king(self.turn)[0] * SQ_SIZE,
                                  SQ_SIZE, SQ_SIZE))
        if self.selected_pos:
            pg.draw.rect(screen, (0, 255, 0),
                         (self.selected_pos[0] * SQ_SIZE, self.selected_pos[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if self.board[self.selected_pos[1]][self.selected_pos[0]][0] == self.turn:
                self.draw_possible_moves(screen, SQ_SIZE)

    def draw_pieces(self, screen, SQ_SIZE):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "--":
                    piece_image = pg.image.load(f"images/{piece}.png")
                    piece_image = pg.transform.scale(piece_image, (SQ_SIZE, SQ_SIZE))
                    screen.blit(piece_image, (c * SQ_SIZE, r * SQ_SIZE))

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = "--"
        self.board[end_row][end_col] = piece
        if self.is_in_check(self.turn):
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = "--"
            print("Move puts king in check!")
            return False
        if piece[1] == "K":
            self.king_moved[self.turn] = True
        if piece[1] == "R":
            if start_col == 0:
                self.rook_moved[self.turn][0] = True
            if start_col == 7:
                self.rook_moved[self.turn][1] = True
        self.selected_pos = None
        self.turn = 'b' if self.turn == 'w' else 'w'
        return True

    def draw_possible_moves(self, screen, SQ_SIZE):
        for move in self.possible_moves:
            pg.draw.circle(screen, (128, 128, 128),
                           (move[1] * SQ_SIZE + SQ_SIZE // 2, move[0] * SQ_SIZE + SQ_SIZE // 2),
                           SQ_SIZE // 6)

    def change_turn(self):
        self.selected_pos = None
        self.turn = 'b' if self.turn == 'w' else 'w'

    def find_king(self, turn):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == f"{turn}K":
                    return r, c
        return None

    def is_in_check(self, turn):
        king_pos = self.find_king(turn)
        opponent = 'b' if turn == 'w' else 'w'
        for r in range(8):
            for c in range(8):
                if self.board[r][c][0] == opponent:
                    piece = self.board[r][c][1]
                    if piece == "P":
                        if self.Pawn_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                            return True
                    elif piece == "R":
                        if self.Rook_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                            return True
                    elif piece == "B":
                        if self.Bishops_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                            return True
                    elif piece == "Q":
                        if self.Queen_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                            return True
                    elif piece == "N":
                        if self.Knight_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                            return True
                    elif piece == "K":
                        if self.King_moves(r, c, king_pos[0], king_pos[1], check=True):
                            return True
        return False

    def Pawn_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if self.board[end_row][end_col] == "--" and start_col == end_col:
            if turn == 'w':
                if start_row - end_row == 1 or (
                        abs(start_row - end_row) == 2 and start_row == 6 and self.board[5][start_col] == "--"):
                    if not check:
                        self.move_piece(start_row, start_col, end_row, end_col)
                        self.last_move = (start_row, start_col, end_row, end_col)
                    return True
            if turn == 'b':
                if end_row - start_row == 1 or (
                        abs(start_row - end_row) == 2 and start_row == 1 and self.board[2][start_col] == "--"):
                    if not check:
                        self.move_piece(start_row, start_col, end_row, end_col)
                        self.last_move = (start_row, start_col, end_row, end_col)
                    return True
        if self.board[end_row][end_col][0] != turn and self.board[end_row][end_col] != "--":
            if turn == 'w' and (start_row - end_row) == 1 and abs(start_col - end_col) == 1:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                return True
            if turn == 'b' and (start_row - end_row) == -1 and abs(start_col - end_col) == 1:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                return True
        if self.last_move:  # en passant
            last_start_row, last_start_col, last_end_row, last_end_col = self.last_move
            if abs(start_col - end_col) == 1 and end_row == start_row + (-1 if turn == 'w' else 1):
                if self.board[end_row][end_col] == "--" and self.board[start_row][
                    end_col] == f"{'b' if turn == 'w' else 'w'}P":
                    if last_start_row == (1 if turn == 'w' else 6) and last_end_row == (
                            3 if turn == 'w' else 4) and last_end_col == end_col:
                        if not check:
                            self.board[start_row][start_col] = "--"
                            self.board[start_row][end_col] = "--"
                            self.board[end_row][end_col] = f"{turn}P"
                            self.last_move = (start_row, start_col, end_row, end_col)
                            self.change_turn()
                        return True
        return False

    def Rook_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if start_col == end_col:  # Moving vertically
            step = 1 if end_row > start_row else -1
            for r in range(start_row + step, end_row, step):
                if self.board[r][start_col] != "--":
                    return False
        elif start_row == end_row:  # Moving horizontally
            step = 1 if end_col > start_col else -1
            for c in range(start_col + step, end_col, step):
                if self.board[start_row][c] != "--":
                    return False
        if (self.board[end_row][end_col] == "--" or self.board[end_row][end_col][0] != turn) and (
                start_row == end_row or start_col == end_col):
            if not check:
                self.move_piece(start_row, start_col, end_row, end_col)
            return True
        return False

    def Bishops_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if abs(start_row - end_row) == abs(start_col - end_col):  # Moving diagonally
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            for r, c in zip(range(start_row + row_step, end_row, row_step),
                            range(start_col + col_step, end_col, col_step)):
                if self.board[r][c] != "--":
                    return False
            if self.board[end_row][end_col] == "--" or self.board[end_row][end_col][0] != turn:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                return True
        return False

    def Queen_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if self.Rook_moves(start_row, start_col, end_row, end_col, turn, check) or self.Bishops_moves(start_row,
                                                                                                      start_col,
                                                                                                      end_row, end_col,
                                                                                                      turn, check):
            return True
        return False

    def Knight_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if self.board[end_row][end_col][0] != turn:
            if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (
                    abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                return True
        return False

    def King_moves(self, start_row, start_col, end_row, end_col, check=False):
        if self.board[end_row][end_col][0] != self.turn:
            if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                return True
        # Castling
        if self.turn == 'w':
            i = 7
        else:
            i = 0
        if start_row == end_row and start_col == 4 and not self.king_moved[self.turn]:
            if end_col == 6 and self.board[i][5] == '--' and self.board[i][6] == '--' and self.board[i][
                7] == f"{self.turn}R" and not \
                    self.rook_moved[self.turn][1]:
                if not check:
                    self.board[i][4] = "--"
                    self.board[i][5] = f"{self.turn}R"
                    self.board[i][6] = f"{self.turn}K"
                    self.board[i][7] = "--"
                    self.change_turn()
                return True
            if end_col == 2 and self.board[i][3] == '--' and self.board[i][2] == '--' and self.board[i][1] == "--" and \
                    self.board[i][
                        0] == f"{self.turn}R" and not self.rook_moved[self.turn][0]:
                if not check:
                    self.board[i][0] = "--"
                    self.board[i][1] = "--"
                    self.board[i][2] = f"{self.turn}K"
                    self.board[i][3] = f"{self.turn}R"
                    self.board[i][4] = "--"
                    self.change_turn()
                return True
        return False

    def handle_click(self, pos):
        col, row = pos
        col = col // SQ_SIZE
        row = row // SQ_SIZE
        if self.selected_pos == (col, row):
            self.selected_pos = None
            self.possible_moves = []
            return
        if self.selected_pos is None and self.board[row][col] != "--" and self.board[row][col][0] == self.turn:
            self.selected_pos = (col, row)
            piece = self.board[row][col][1]
            self.possible_moves = []
            for r in range(8):
                for c in range(8):
                    if piece == "P" and self.Pawn_moves(row, col, r, c, self.turn, check=True):
                        self.possible_moves.append((r, c))
                    elif piece == "R" and self.Rook_moves(row, col, r, c, self.turn, check=True):
                        self.possible_moves.append((r, c))
                    elif piece == "B" and self.Bishops_moves(row, col, r, c, self.turn, check=True):
                        self.possible_moves.append((r, c))
                    elif piece == "Q" and self.Queen_moves(row, col, r, c, self.turn, check=True):
                        self.possible_moves.append((r, c))
                    elif piece == "N" and self.Knight_moves(row, col, r, c, self.turn, check=True):
                        self.possible_moves.append((r, c))
                    elif piece == "K" and self.King_moves(row, col, r, c, check=True):
                        self.possible_moves.append((r, c))

        if self.selected_pos is not None and self.board[self.selected_pos[1]][self.selected_pos[0]][0] == self.turn:
            if self.board[self.selected_pos[1]][self.selected_pos[0]][1] == "P":
                self.Pawn_moves(self.selected_pos[1], self.selected_pos[0], row, col, self.turn)
                return
            if self.board[self.selected_pos[1]][self.selected_pos[0]][1] == "R":
                self.Rook_moves(self.selected_pos[1], self.selected_pos[0], row, col, self.turn)
                return
            if self.board[self.selected_pos[1]][self.selected_pos[0]][1] == "B":
                self.Bishops_moves(self.selected_pos[1], self.selected_pos[0], row, col, self.turn)
                return
            if self.board[self.selected_pos[1]][self.selected_pos[0]][1] == "Q":
                self.Queen_moves(self.selected_pos[1], self.selected_pos[0], row, col, self.turn)
                return
            if self.board[self.selected_pos[1]][self.selected_pos[0]][1] == "N":
                self.Knight_moves(self.selected_pos[1], self.selected_pos[0], row, col, self.turn)
                return
            if self.board[self.selected_pos[1]][self.selected_pos[0]][1] == "K":
                self.King_moves(self.selected_pos[1], self.selected_pos[0], row, col)


# Game loop
def main():
    game = ChessGame()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game.handle_click(pg.mouse.get_pos())
        game.draw_board(screen, SQ_SIZE)
        game.draw_pieces(screen, SQ_SIZE)
        pg.display.flip()


if __name__ == "__main__":
    main()
