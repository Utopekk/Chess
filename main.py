import pygame as pg
import sys

pg.init()

WIDTH = HEGIHT = 800
SQ_SIZE = WIDTH // 8

screen = pg.display.set_mode((WIDTH, HEGIHT))
pg.display.set_caption("Chess")
pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",
         "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
         "--", "--", "--", "--", "--", "--", "--", "--",
         "--", "--", "--", "--", "--", "--", "--", "--",
         "--", "--", "--", "--", "--", "--", "--", "--",
         "--", "--", "--", "--", "--", "--", "--", "--",
         "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
         "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

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
    piece = board[start_row][start_col]
    board[start_row][start_col] = "--"
    board[end_row][end_col] = piece
    print("Moved")


def Pawn_moves(start_row, start_col, end_row, end_col):
    if board[end_row][end_col] == "--":
        move_piece(start_row, start_col, end_row, end_col)


def handle_click(pos):
    global selected_pos, turn
    col, row = pos
    col = col // SQ_SIZE
    row = row // SQ_SIZE

    if selected_pos is None and board[row][col] != "--":
        selected_pos = (col, row)
    if board[row][col] == "--" and selected_pos is not None:
        if board[selected_pos[1]][selected_pos[0]][1] == "P":
            Pawn_moves(selected_pos[1], selected_pos[0], row, col)



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
