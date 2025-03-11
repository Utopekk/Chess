import pygame as pg
import sys

pg.init()

WIDTH = HEGIHT = 800
SQ_SIZE = WIDTH // 8

screen = pg.display.set_mode((WIDTH, HEGIHT))
pg.display.set_caption("Chess")

board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
         ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

turn = 'w'
selected_pos = None


def draw_board():
    for r in range(8):
        for c in range(8):
            color = "WHITE" if (r+c) % 2 == 0 else "GREY"
            pg.draw.rect(screen, color, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if is_in_check(turn):
                pg.draw.rect(screen, (255, 0, 0), (find_king(turn)[1]*SQ_SIZE, find_king(turn)[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if selected_pos:
        pg.draw.rect(screen, (0, 255, 0), (selected_pos[0]*SQ_SIZE, selected_pos[1]*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces():
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                piece_image = pg.image.load(f"images/{piece}.png")
                piece_image = pg.transform.scale(piece_image, (SQ_SIZE, SQ_SIZE))
                screen.blit(piece_image, (c * SQ_SIZE, r * SQ_SIZE))


def move_piece(start_row, start_col, end_row, end_col):
    global turn, selected_pos
    piece = board[start_row][start_col]
    board[start_row][start_col] = "--"
    board[end_row][end_col] = piece
    if is_in_check(turn):
        board[start_row][start_col] = piece
        board[end_row][end_col] = "--"
        print("Move puts king in check!")
        return False
    selected_pos = None
    turn = 'b' if turn == 'w' else 'w'
    print("moved")
    return True


def find_king(turn):
    for r in range(8):
        for c in range(8):
            if board[r][c] == f"{turn}K":
                return r, c
    return None


def is_in_check(turn):
    king_pos = find_king(turn)
    opponent = 'b' if turn == 'w' else 'w'
    for r in range(8):
        for c in range(8):
            if board[r][c][0] == opponent:
                piece = board[r][c][1]
                if piece == "P":
                    if Pawn_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                        return True
                elif piece == "R":
                    if Rook_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                        return True
                elif piece == "B":
                    if Bishops_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                        return True
                elif piece == "Q":
                    if Queen_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                        return True
                elif piece == "N":
                    if Knight_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                        return True
                elif piece == "K":
                    if King_moves(r, c, king_pos[0], king_pos[1], opponent, check=True):
                        return True
    return False


def Pawn_moves(start_row, start_col, end_row, end_col, turn, check=False):
    if board[end_row][end_col] == "--" and start_col == end_col:
        if turn == 'w':
            if abs(start_row-end_row) == 1 or (abs(start_row-end_row) == 2 and start_row == 6):
                if not check:
                    move_piece(start_row, start_col, end_row, end_col)
                return True
        if turn == 'b':
            if abs(start_row-end_row) == 1 or (abs(start_row-end_row) == 2 and start_row == 1):
                if not check:
                    move_piece(start_row, start_col, end_row, end_col)
                return True
    if board[end_row][end_col] != "--":
        if turn == 'w' and abs(start_row-end_row) == 1 and abs(start_col-end_col) == 1:
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
        if turn == 'b' and abs(start_row-end_row) == 1 and abs(start_col-end_col) == 1:
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
    return False


def Rook_moves(start_row, start_col, end_row, end_col, turn, check=False):
    if start_col == end_col:  # Moving vertically
        step = 1 if end_row > start_row else -1
        for r in range(start_row + step, end_row, step):
            if board[r][start_col] != "--":
                return False
    elif start_row == end_row:  # Moving horizontally
        step = 1 if end_col > start_col else -1
        for c in range(start_col + step, end_col, step):
            if board[start_row][c] != "--":
                return False
    if (board[end_row][end_col] == "--" or board[end_row][end_col][0] != turn) and (start_row == end_row or start_col == end_col):
        if not check:
            move_piece(start_row, start_col, end_row, end_col)
        return True
    return False


def Bishops_moves(start_row, start_col, end_row, end_col, turn, check=False):
    if abs(start_row - end_row) == abs(start_col - end_col):  # Moving diagonally
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        for r, c in zip(range(start_row + row_step, end_row, row_step), range(start_col + col_step, end_col, col_step)):
            if board[r][c] != "--":
                return False
        if board[end_row][end_col] == "--" or board[end_row][end_col][0] != turn:
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
    return False


def Queen_moves(start_row, start_col, end_row, end_col, turn, check=False):
    if Rook_moves(start_row, start_col, end_row, end_col, turn, check) or Bishops_moves(start_row, start_col, end_row, end_col, turn, check):
        return True
    return False


def Knight_moves(start_row, start_col, end_row, end_col, turn, check=False):
    if board[end_row][end_col][0] != turn:
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
    return False


def King_moves(start_row, start_col, end_row, end_col, turn, check=False):
    if board[end_row][end_col][0] != turn:
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
    return False


def handle_click(pos):
    global selected_pos, turn
    col, row = pos
    col = col // SQ_SIZE
    row = row // SQ_SIZE
    print("click", board[row][col])
    print("selected pos", selected_pos)
    if selected_pos == (col, row):
        selected_pos = None
        return
    if selected_pos is None and board[row][col] != "--":
        selected_pos = (col, row)
    if selected_pos is not None and board[selected_pos[1]][selected_pos[0]][0] == turn:
        if board[selected_pos[1]][selected_pos[0]][1] == "P":
            Pawn_moves(selected_pos[1], selected_pos[0], row, col, turn)
            return
        if board[selected_pos[1]][selected_pos[0]][1] == "R":
            Rook_moves(selected_pos[1], selected_pos[0], row, col, turn)
            return
        if board[selected_pos[1]][selected_pos[0]][1] == "B":
            Bishops_moves(selected_pos[1], selected_pos[0], row, col, turn)
            return
        if board[selected_pos[1]][selected_pos[0]][1] == "Q":
            Queen_moves(selected_pos[1], selected_pos[0], row, col, turn)
            return
        if board[selected_pos[1]][selected_pos[0]][1] == "N":
            Knight_moves(selected_pos[1], selected_pos[0], row, col,turn)
            return
        if board[selected_pos[1]][selected_pos[0]][1] == "K":
            King_moves(selected_pos[1], selected_pos[0], row, col,turn)
            return


def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                handle_click(pg.mouse.get_pos())
        draw_board()
        draw_pieces()
        pg.display.flip()


if __name__ == "__main__":
    main()
