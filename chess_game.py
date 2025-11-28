import pygame as pg
import sys
from tkinter import simpledialog, messagebox, Tk

pg.init()
WIDTH = HEIGHT = 800
SQ_SIZE = WIDTH // 8
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Chess")

# colors
WHITE = (240, 217, 181)
GREY = (181, 136, 99)
HIGHLIGHT = (0, 255, 0)
CHECK_HIGHLIGHT = (255, 0, 0)
MOVE_DOT = (128, 128, 128)

//
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
        self.selected_pos = None         # stored as (row, col)
        self.possible_moves = []         # list of (row, col)
        self.last_move = None            # for enpassant (start_row, start_col, end_row, end_col)
        self.king_moved = {'w': False, 'b': False}
        self.rook_moved = {'w': [False, False], 'b': [False, False]}  # [left rook, right rook]
        self.images = {}                 # cache for images
        self.load_images()

    def load_images(self):
        pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
        for p in pieces:
            try:
                img = pg.image.load(f"images/{p}.png")
                img = pg.transform.scale(img, (SQ_SIZE, SQ_SIZE))
                self.images[p] = img
            except Exception:
                self.images[p] = None

    def draw_board(self, screen, SQ_SIZE):
        in_check = self.is_in_check(self.turn)
        king_pos = self.find_king(self.turn)
        for r in range(8):
            for c in range(8):
                color = WHITE if (r + c) % 2 == 0 else GREY
                pg.draw.rect(screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # highlight king if in check
        if in_check and king_pos:
            kr, kc = king_pos
            pg.draw.rect(screen, CHECK_HIGHLIGHT, (kc * SQ_SIZE, kr * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # highlight selected square (if any)
        if self.selected_pos:
            sr, sc = self.selected_pos
            pg.draw.rect(screen, HIGHLIGHT, (sc * SQ_SIZE, sr * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            # draw possible moves
            if self.board[sr][sc][0] == self.turn:
                self.draw_possible_moves(screen, SQ_SIZE)

    def draw_pieces(self, screen, SQ_SIZE):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "--":
                    img = self.images.get(piece)
                    if img:
                        screen.blit(img, (c * SQ_SIZE, r * SQ_SIZE))
                    else:
                        # fallback: draw text if image missing
                        font = pg.font.SysFont(None, SQ_SIZE // 2)
                        text = font.render(piece, True, (0, 0, 0))
                        screen.blit(text, (c * SQ_SIZE + 8, r * SQ_SIZE + 8))

    def move_piece(self, start_row, start_col, end_row, end_col):
        """Perform a move on the real board (used when executing a chosen move)."""
        piece = self.board[start_row][start_col]
        if piece == "--":
            return False

        # apply move
        self.board[start_row][start_col] = "--"
        captured = self.board[end_row][end_col]
        self.board[end_row][end_col] = piece

        # If move leaves the player's king in check, undo and reject
        if self.is_in_check(self.turn):
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = captured
            print("Move puts king in check!")
            return False

        # update castling/rook/king moved flags
        if piece[1] == "K":
            self.king_moved[self.turn] = True
        if piece[1] == "R":
            if start_col == 0:
                self.rook_moved[self.turn][0] = True
            if start_col == 7:
                self.rook_moved[self.turn][1] = True

        # update last_move (for en passant)
        self.last_move = (start_row, start_col, end_row, end_col)

        # clear selection, switch turn
        self.selected_pos = None
        self.turn = 'b' if self.turn == 'w' else 'w'
        return True

    def draw_possible_moves(self, screen, SQ_SIZE):
        for move in self.possible_moves:
            mr, mc = move
            pg.draw.circle(screen, MOVE_DOT,
                           (mc * SQ_SIZE + SQ_SIZE // 2, mr * SQ_SIZE + SQ_SIZE // 2),
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

    def promotion(self, turn, end_row, end_col):
        options = ["Q", "R", "B", "N"]
        option = simpledialog.askstring("Promotion",
                                        "Choose promotion piece: Queen (Q), Rook (R), Bishop (B), Knight (N)")
        if option and option.upper() in options:
            self.board[end_row][end_col] = f"{turn}{option.upper()}"
        else:
            # default to queen if input invalid or cancelled
            self.board[end_row][end_col] = f"{turn}Q"

    def is_in_check(self, turn):
        """Return True if `turn` king is attacked by opponent."""
        king_pos = self.find_king(turn)
        if king_pos is None:
            return False
        kr, kc = king_pos
        opponent = 'b' if turn == 'w' else 'w'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != "--" and self.board[r][c][0] == opponent:
                    piece = self.board[r][c][1]
                    # use check=True so these functions don't perform side-effects
                    if piece == "P":
                        if self.Pawn_moves(r, c, kr, kc, opponent, check=True):
                            return True
                    elif piece == "R":
                        if self.Rook_moves(r, c, kr, kc, opponent, check=True):
                            return True
                    elif piece == "B":
                        if self.Bishops_moves(r, c, kr, kc, opponent, check=True):
                            return True
                    elif piece == "Q":
                        if self.Queen_moves(r, c, kr, kc, opponent, check=True):
                            return True
                    elif piece == "N":
                        if self.Knight_moves(r, c, kr, kc, opponent, check=True):
                            return True
                    elif piece == "K":
                        if self.King_moves(r, c, kr, kc, opponent, check=True):
                            return True
        return False

    def is_legal_move_after_simulation(self, start_row, start_col, end_row, end_col, turn):
        """
        Simulate the move on a temporary board.
        Return True only if the player's king is NOT in check afterwards.
        """
        board_copy = [row[:] for row in self.board]
        turn_copy = self.turn
        last_move_copy = self.last_move
        king_moved_copy = {k: v for k, v in self.king_moved.items()}
        rook_moved_copy = {k: v[:] for k, v in self.rook_moved.items()}

        # simulate
        moved_piece = self.board[start_row][start_col]
        captured = self.board[end_row][end_col]
        self.board[end_row][end_col] = moved_piece
        self.board[start_row][start_col] = "--"

        legal = not self.is_in_check(turn)

        # restore
        self.board = board_copy
        self.turn = turn_copy
        self.last_move = last_move_copy
        self.king_moved = king_moved_copy
        self.rook_moved = rook_moved_copy

        return legal

    def is_checkmate(self, turn):
        if not self.is_in_check(turn):
            return False
        # try every legal-looking move; if any results in not in_check, it's not checkmate
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != "--" and self.board[r][c][0] == turn:
                    piece = self.board[r][c][1]
                    for nr in range(8):
                        for nc in range(8):
                            if piece == "P" and self.Pawn_moves(r, c, nr, nc, turn, check=True):
                                if self.is_legal_move_after_simulation(r, c, nr, nc, turn):
                                    return False
                            elif piece == "R" and self.Rook_moves(r, c, nr, nc, turn, check=True):
                                if self.is_legal_move_after_simulation(r, c, nr, nc, turn):
                                    return False
                            elif piece == "B" and self.Bishops_moves(r, c, nr, nc, turn, check=True):
                                if self.is_legal_move_after_simulation(r, c, nr, nc, turn):
                                    return False
                            elif piece == "Q" and self.Queen_moves(r, c, nr, nc, turn, check=True):
                                if self.is_legal_move_after_simulation(r, c, nr, nc, turn):
                                    return False
                            elif piece == "N" and self.Knight_moves(r, c, nr, nc, turn, check=True):
                                if self.is_legal_move_after_simulation(r, c, nr, nc, turn):
                                    return False
                            elif piece == "K" and self.King_moves(r, c, nr, nc, turn, check=True):
                                if self.is_legal_move_after_simulation(r, c, nr, nc, turn):
                                    return False
        return True

    def Pawn_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        # Validate indices
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        piece = self.board[start_row][start_col]
        direction = -1 if turn == 'w' else 1

        # forward move
        if start_col == end_col and self.board[end_row][end_col] == "--":
            # one step
            if end_row - start_row == direction:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                    self.last_move = (start_row, start_col, end_row, end_col)
                    # promotion
                    if end_row == (0 if turn == 'w' else 7):
                        self.promotion(turn, end_row, end_col)
                return True
            # two steps from starting rank
            if end_row - start_row == 2 * direction and ((turn == 'w' and start_row == 6) or (turn == 'b' and start_row == 1)):
                middle = start_row + direction
                if self.board[middle][start_col] == "--":
                    if not check:
                        self.move_piece(start_row, start_col, end_row, end_col)
                        self.last_move = (start_row, start_col, end_row, end_col)
                    return True

        # captures
        if abs(start_col - end_col) == 1 and end_row - start_row == direction:
            # normal capture
            if self.board[end_row][end_col] != "--" and self.board[end_row][end_col][0] != turn:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                    if end_row == (0 if turn == 'w' else 7):
                        self.promotion(turn, end_row, end_col)
                return True
            # en passant
            if self.last_move:
                ls_r, ls_c, le_r, le_c = self.last_move
                # last move must have been a two-step pawn move by opponent landing adjacent
                if self.board[start_row][end_col] == f"{'b' if turn == 'w' else 'w'}P" \
                        and ls_r == (1 if turn == 'w' else 6) and le_r == (3 if turn == 'w' else 4) and le_c == end_col:
                    if end_row == start_row + direction:
                        if not check:
                            # remove captured pawn and move
                            self.board[start_row][start_col] = "--"
                            self.board[start_row][end_col] = "--"
                            self.board[end_row][end_col] = f"{turn}P"
                            self.last_move = (start_row, start_col, end_row, end_col)
                            self.change_turn()
                        return True
        return False

    def Rook_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        if not (start_row == end_row or start_col == end_col):
            return False
        # path clear?
        dr = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        dc = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        r, c = start_row + dr, start_col + dc
        while (r, c) != (end_row, end_col):
            if self.board[r][c] != "--":
                return False
            r += dr
            c += dc
        # destination friendly?
        if self.board[end_row][end_col] == "--" or self.board[end_row][end_col][0] != turn:
            if not check:
                self.move_piece(start_row, start_col, end_row, end_col)
            return True
        return False

    def Bishops_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        dr = 1 if end_row > start_row else -1
        dc = 1 if end_col > start_col else -1
        r, c = start_row + dr, start_col + dc
        while (r, c) != (end_row, end_col):
            if self.board[r][c] != "--":
                return False
            r += dr
            c += dc
        if self.board[end_row][end_col] == "--" or self.board[end_row][end_col][0] != turn:
            if not check:
                self.move_piece(start_row, start_col, end_row, end_col)
            return True
        return False

    def Queen_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        return self.Rook_moves(start_row, start_col, end_row, end_col, turn, check) or \
               self.Bishops_moves(start_row, start_col, end_row, end_col, turn, check)

    def Knight_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
            if self.board[end_row][end_col] == "--" or self.board[end_row][end_col][0] != turn:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                return True
        return False

    def King_moves(self, start_row, start_col, end_row, end_col, turn, check=False):
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # normal one-square move
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            if self.board[end_row][end_col] == "--" or self.board[end_row][end_col][0] != turn:
                if not check:
                    self.move_piece(start_row, start_col, end_row, end_col)
                return True

        # castling: only consider when actually performing the move (not during attack tests)
        if not check:
            row_for_castle = 7 if turn == 'w' else 0
            if start_row == row_for_castle and start_col == 4 and not self.king_moved[turn] and not self.is_in_check(turn):
                # kingside
                if end_row == row_for_castle and end_col == 6:
                    if (self.board[row_for_castle][5] == '--' and self.board[row_for_castle][6] == '--'
                            and self.board[row_for_castle][7] == f"{turn}R" and not self.rook_moved[turn][1]):
                        # also should ensure squares the king travels over are not attacked
                        # check squares 5 and 6 are safe
                        safe = True
                        for col_check in (5, 6):
                            # temporarily move king to that square and test
                            board_copy = [row[:] for row in self.board]
                            self.board[row_for_castle][4] = "--"
                            self.board[row_for_castle][col_check] = f"{turn}K"
                            if self.is_in_check(turn):
                                safe = False
                            self.board = board_copy
                            if not safe:
                                break
                        if safe:
                            # perform castling
                            self.board[row_for_castle][4] = "--"
                            self.board[row_for_castle][5] = f"{turn}R"
                            self.board[row_for_castle][6] = f"{turn}K"
                            self.board[row_for_castle][7] = "--"
                            self.change_turn()
                            return True
                # queenside
                if end_row == row_for_castle and end_col == 2:
                    if (self.board[row_for_castle][3] == '--' and self.board[row_for_castle][2] == '--'
                            and self.board[row_for_castle][1] == '--' and self.board[row_for_castle][0] == f"{turn}R"
                            and not self.rook_moved[turn][0]):
                        safe = True
                        for col_check in (3, 2):
                            board_copy = [row[:] for row in self.board]
                            self.board[row_for_castle][4] = "--"
                            self.board[row_for_castle][col_check] = f"{turn}K"
                            if self.is_in_check(turn):
                                safe = False
                            self.board = board_copy
                            if not safe:
                                break
                        if safe:
                            self.board[row_for_castle][0] = "--"
                            self.board[row_for_castle][1] = "--"
                            self.board[row_for_castle][2] = f"{turn}K"
                            self.board[row_for_castle][3] = f"{turn}R"
                            self.board[row_for_castle][4] = "--"
                            self.change_turn()
                            return True
        return False

    def handle_click(self, pos):
        # pos is (x,y) in pixels — convert to (row, col)
        x, y = pos
        col = x // SQ_SIZE
        row = y // SQ_SIZE

        # sanity bounds
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        # deselect if clicking the same square
        if self.selected_pos == (row, col):
            self.selected_pos = None
            self.possible_moves = []
            return

        # if nothing selected and clicked on a friendly piece -> select it and list legal moves
        if self.selected_pos is None and self.board[row][col] != "--" and self.board[row][col][0] == self.turn:
            self.selected_pos = (row, col)
            piece = self.board[row][col][1]
            self.possible_moves = []
            for r in range(8):
                for c in range(8):
                    ok = False
                    if piece == "P" and self.Pawn_moves(row, col, r, c, self.turn, check=True):
                        ok = True
                    elif piece == "R" and self.Rook_moves(row, col, r, c, self.turn, check=True):
                        ok = True
                    elif piece == "B" and self.Bishops_moves(row, col, r, c, self.turn, check=True):
                        ok = True
                    elif piece == "Q" and self.Queen_moves(row, col, r, c, self.turn, check=True):
                        ok = True
                    elif piece == "N" and self.Knight_moves(row, col, r, c, self.turn, check=True):
                        ok = True
                    elif piece == "K" and self.King_moves(row, col, r, c, self.turn, check=True):
                        ok = True

                    if ok and self.is_legal_move_after_simulation(row, col, r, c, self.turn):
                        self.possible_moves.append((r, c))
            return

        # if a source was selected and clicked somewhere else, attempt to move
        if self.selected_pos is not None:
            sr, sc = self.selected_pos
            tr, tc = row, col
            piece = self.board[sr][sc]
            if piece == "--":
                # should not happen, but just reset
                self.selected_pos = None
                self.possible_moves = []
                return

            ptype = piece[1]
            performed = False
            # call the specific move function without check so it executes the move (they call move_piece)
            if ptype == "P" and self.Pawn_moves(sr, sc, tr, tc, self.turn, check=False):
                performed = True
            elif ptype == "R" and self.Rook_moves(sr, sc, tr, tc, self.turn, check=False):
                performed = True
            elif ptype == "B" and self.Bishops_moves(sr, sc, tr, tc, self.turn, check=False):
                performed = True
            elif ptype == "Q" and self.Queen_moves(sr, sc, tr, tc, self.turn, check=False):
                performed = True
            elif ptype == "N" and self.Knight_moves(sr, sc, tr, tc, self.turn, check=False):
                performed = True
            elif ptype == "K" and self.King_moves(sr, sc, tr, tc, self.turn, check=False):
                performed = True

            # If move was attempted but move_piece rejected it as leaving king in check, performed will be False
            # For en-passant and castling we already performed changes inside Pawn_moves/King_moves,
            # but those functions call move_piece / change_turn as appropriate.

            # clear selection and possible moves regardless (successful move already cleared them)
            self.selected_pos = None
            self.possible_moves = []

    # Game move methods (Pawn_moves etc.) already implemented above

# Game loop
def main():
    game = ChessGame()
    root = Tk()
    root.withdraw()
    running = True
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game.handle_click(pg.mouse.get_pos())
                # checkmate check after a move (game.turn has been toggled by move_piece/change_turn if a move was made)
                if game.is_checkmate(game.turn):
                    game.draw_board(screen, SQ_SIZE)
                    game.draw_pieces(screen, SQ_SIZE)
                    pg.display.flip()
                    winner = "White" if game.turn == 'b' else "Black"
                    messagebox.showinfo("Checkmate", f"{winner} wins by checkmate!")
                    running = False

        game.draw_board(screen, SQ_SIZE)
        game.draw_pieces(screen, SQ_SIZE)
        pg.display.flip()


if __name__ == "__main__":
    main()
