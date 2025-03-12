import pygame as pg
import sys

pg.init()

WIDTH = HEIGHT = 800
SQ_SIZE = WIDTH // 8

screen = pg.display.set_mode((WIDTH, HEIGHT))
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
possible_moves = []
last_move = None  # For en passant
king_moved = {'w': False, 'b': False}
rook_moved = {'w': [False, False], 'b': [False, False]}  # [left rook, right rook]


def draw_board():
    for r in range(8):
        for c in range(8):
            color = "WHITE" if (r + c) % 2 == 0 else "GREY"
            pg.draw.rect(screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if is_in_check(turn):
                pg.draw.rect(screen, (255, 0, 0),
                             (find_king(turn)[1] * SQ_SIZE, find_king(turn)[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if selected_pos:
        pg.draw.rect(screen, (0, 255, 0), (selected_pos[0] * SQ_SIZE, selected_pos[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        if board[selected_pos[1]][selected_pos[0]][0] == turn:
            draw_possible_moves()


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
    if piece[1] == "K":
        king_moved[turn] = True
    if piece[1] == "R":
        if start_col == 0:
            rook_moved[turn][0] = True
        if start_col == 7:
            rook_moved[turn][1] = True
    selected_pos = None
    turn = 'b' if turn == 'w' else 'w'
    return True


def draw_possible_moves():
    for move in possible_moves:
        pg.draw.circle(screen, (128, 128, 128), (move[1] * SQ_SIZE + SQ_SIZE // 2, move[0] * SQ_SIZE + SQ_SIZE // 2),
                       SQ_SIZE // 6)


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
                    if Pawn_moves(r, c, king_pos[0], king_pos[1], check=True):
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
                    if King_moves(r, c, king_pos[0], king_pos[1], check=True):
                        return True
    return False


def is_checkmate(turn):
    if not is_in_check(turn):
        return False

    for r in range(8):
        for c in range(8):
            if board[r][c][0] == turn:
                piece = board[r][c][1]
                for row in range(8):
                    for col in range(8):
                        if piece == "P" and Pawn_moves(r, c, row, col, check=True):
                            if not is_in_check(turn):
                                return False
                        elif piece == "R" and Rook_moves(r, c, row, col, turn, check=True):
                            if not is_in_check(turn):
                                return False
                        elif piece == "B" and Bishops_moves(r, c, row, col, turn, check=True):
                            if not is_in_check(turn):
                                return False
                        elif piece == "Q" and Queen_moves(r, c, row, col, turn, check=True):
                            if not is_in_check(turn):
                                return False
                        elif piece == "N" and Knight_moves(r, c, row, col, turn, check=True):
                            if not is_in_check(turn):
                                return False
                        elif piece == "K" and King_moves(r, c, row, col, check=True):
                            if not is_in_check(turn):
                                return False
    return True


def Pawn_moves(start_row, start_col, end_row, end_col, check=False):
    global last_move, selected_pos, turn
    if board[end_row][end_col] == "--" and start_col == end_col:
        if turn == 'w':
            if start_row - end_row == 1 or (abs(start_row - end_row) == 2 and start_row == 6 and board[5][start_col] == "--"):
                if not check:
                    move_piece(start_row, start_col, end_row, end_col)
                    last_move = (start_row, start_col, end_row, end_col)
                return True
        if turn == 'b':
            if end_row - start_row == 1 or (abs(start_row - end_row) == 2 and start_row == 1 and board[2][start_col] == "--"):
                if not check:
                    move_piece(start_row, start_col, end_row, end_col)
                    last_move = (start_row, start_col, end_row, end_col)
                return True
    if board[end_row][end_col][0] != turn and board[end_row][end_col] != "--":
        if turn == 'w' and (start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
        if turn == 'b' and (start_row - end_row) == -1 and abs(start_col - end_col) == 1:
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
    if last_move:  # en passant
        last_start_row, last_start_col, last_end_row, last_end_col = last_move
        if abs(start_col - end_col) == 1 and end_row == start_row + (-1 if turn == 'w' else 1):
            if board[end_row][end_col] == "--" and board[start_row][end_col] == f"{'b' if turn == 'w' else 'w'}P":
                print("last start row", last_start_row)
                print("last start col", last_start_col)
                print("last end row", last_end_row)
                print("last end col", last_end_col)
                if last_start_row == (1 if turn == 'w' else 6) and last_end_row == (3 if turn == 'w' else 4) and last_end_col == end_col:
                    if not check:
                        board[start_row][start_col] = "--"
                        board[start_row][end_col] = "--"
                        board[end_row][end_col] = f"{turn}P"
                        last_move = (start_row, start_col, end_row, end_col)
                        selected_pos = None
                        turn = 'b' if turn == 'w' else 'w'
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
    if (board[end_row][end_col] == "--" or board[end_row][end_col][0] != turn) and (
            start_row == end_row or start_col == end_col):
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
    if Rook_moves(start_row, start_col, end_row, end_col, turn, check) or Bishops_moves(start_row, start_col, end_row,
                                                                                        end_col, turn, check):
        return True
    return False


def Knight_moves(start_row, start_col, end_row, end_col, turn, check=False):
    if board[end_row][end_col][0] != turn:
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (
                abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
    return False


def King_moves(start_row, start_col, end_row, end_col, check=False):
    global selected_pos, turn
    if board[end_row][end_col][0] != turn:
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            if not check:
                move_piece(start_row, start_col, end_row, end_col)
            return True
    # Castling
    if turn == 'w':
        i = 7
    else:
        i = 0
    if start_row == end_row and start_col == 4 and not king_moved[turn]:
        if end_col == 6 and board[i][5] == '--' and board[i][6] == '--' and board[i][7] == f"{turn}R" and not rook_moved[turn][1]:
            if not check:
                board[i][4] = "--"
                board[i][5] = f"{turn}R"
                board[i][6] = f"{turn}K"
                board[i][7] = "--"
                selected_pos = None
                turn = 'b' if turn == 'w' else 'w'
            return True
        if end_col == 2 and board[i][3] == '--' and board[i][2] == '--' and board[i][1] == "--" and board[i][0] == f"{turn}R" and not rook_moved[turn][0]:
            if not check:
                board[i][0] = "--"
                board[i][1] = "--"
                board[i][2] = f"{turn}K"
                board[i][3] = f"{turn}R"
                board[i][4] = "--"
                selected_pos = None
                turn = 'b' if turn == 'w' else 'w'
            return True
    return False


def handle_click(pos):
    global selected_pos, turn, possible_moves
    col, row = pos
    col = col // SQ_SIZE
    row = row // SQ_SIZE
    print("selected pos", selected_pos)
    if selected_pos == (col, row):
        selected_pos = None
        possible_moves = []
        return
    if selected_pos is None and board[row][col] != "--" and board[row][col][0] == turn:
        selected_pos = (col, row)
        piece = board[row][col][1]
        possible_moves = []
        for r in range(8):
            for c in range(8):
                if piece == "P" and Pawn_moves(row, col, r, c, check=True):
                    possible_moves.append((r, c))
                elif piece == "R" and Rook_moves(row, col, r, c, turn, check=True):
                    possible_moves.append((r, c))
                elif piece == "B" and Bishops_moves(row, col, r, c, turn, check=True):
                    possible_moves.append((r, c))
                elif piece == "Q" and Queen_moves(row, col, r, c, turn, check=True):
                    possible_moves.append((r, c))
                elif piece == "N" and Knight_moves(row, col, r, c, turn, check=True):
                    possible_moves.append((r, c))
                elif piece == "K" and King_moves(row, col, r, c, check=True):
                    possible_moves.append((r, c))
    if selected_pos is not None and board[selected_pos[1]][selected_pos[0]][0] == turn:
        if board[selected_pos[1]][selected_pos[0]][1] == "P":
            Pawn_moves(selected_pos[1], selected_pos[0], row, col)
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
            Knight_moves(selected_pos[1], selected_pos[0], row, col, turn)
            return
        if board[selected_pos[1]][selected_pos[0]][1] == "K":
            King_moves(selected_pos[1], selected_pos[0], row, col)
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
        if is_checkmate(turn):
            sys.exit("Checkmate")
        pg.display.flip()


if __name__ == "__main__":
    main()
