from graphics import *
import math
from abc import ABC, abstractmethod

# TODO: pawn promotions, en passant, castling, menu, AI
# For en passant, create a fake piece when a pawn moves two squares. Delete after one turn!

WIN_SIZE = 600
win = GraphWin("Chess", WIN_SIZE, WIN_SIZE)
game_board = []
white_pieces = []
black_pieces = []

white_copy = []
black_copy = []
USE_COPIES = False

white_to_move = True

HEIGHT = 8
WIDTH = 8
TILE_LENGTH = WIN_SIZE / 8


def main():
    init_game_board()
    add_in_pieces()
    game_loop()
    win.close()


def init_game_board():
    for i in range(0, HEIGHT):
        x = []
        for j in range(0, WIDTH):
            obj = GameSquare(i, j)
            x.append(obj)
            if i % 2 == 0:
                if j % 2 == 0:
                    obj.set_color("white")
                    obj.color_square()
                else:
                    obj.set_color("dark")
                    obj.color_square()
            else:
                if j % 2 == 0:
                    obj.set_color("dark")
                    obj.color_square()
                else:
                    obj.set_color("white")
                    obj.color_square()

            obj.init_drawing()
        game_board.append(x)


def add_in_pieces():
    white_pieces.append(King(4, 7, "white"))
    white_pieces.append(Queen(3, 7, "white"))
    white_pieces.append(Rook(0, 7, "white"))
    white_pieces.append(Rook(7, 7, "white"))
    white_pieces.append(Bishop(2, 7, "white"))
    white_pieces.append(Bishop(5, 7, "white"))
    white_pieces.append(Knight(1, 7, "white"))
    white_pieces.append(Knight(6, 7, "white"))
    black_pieces.append(King(4, 0, "black"))
    black_pieces.append(Queen(3, 0, "black"))
    black_pieces.append(Rook(0, 0, "black"))
    black_pieces.append(Rook(7, 0, "black"))
    black_pieces.append(Bishop(2, 0, "black"))
    black_pieces.append(Bishop(5, 0, "black"))
    black_pieces.append(Knight(1, 0, "black"))
    black_pieces.append(Knight(6, 0, "black"))
    for i in range(0, 8):
        white_pieces.append(Pawn(i, 6, "white"))
        black_pieces.append(Pawn(i, 1, "black"))


def game_loop():
    while True:
        next_move()

        if in_check(get_king(get_own_pieces()), get_enemy_pieces()):
            if in_checkmate():
                ending_text("checkmate")
                clicked_point = win.getMouse()
                break
        elif not has_valid_moves():
            ending_text("stalemate")
            clicked_point = win.getMouse()
            break


def ending_text(reason):
    rec = Rectangle(Point(125, 250), Point(475, 350))
    rec.setFill("black")
    rec.draw(win)

    if reason == "checkmate":
        text = "Checkmate!"
    else:
        text = "Stalemate!"

    txt = Text(Point(300, 300), text)
    txt.setSize(25)
    txt.setTextColor("green")
    txt.draw(win)


def next_move():
    selected_piece = get_selected_piece()
    potential_moves = selected_piece.get_potential_moves()

    if potential_moves is None:
        return

    clicked_point = win.getMouse()
    selected_x, selected_y = find_selected_tile(clicked_point)
    game_board[selected_piece.x][selected_piece.y].color_square()

    if not valid_move_selection(potential_moves, selected_x, selected_y):
        return
    elif king_is_safe(selected_piece, selected_x, selected_y):
        selected_piece.move_piece(game_board[selected_x][selected_y])
        change_turn()
    else:
        print("Invalid Move! (puts king in check)")
        return


def in_checkmate():
    if in_check(get_king(get_own_pieces()), get_enemy_pieces()):
        if not has_valid_moves():
            return True
    return False


def has_valid_moves():
    has_valid_move = False
    for piece in get_own_pieces():
        for move in piece.get_potential_moves():
            if king_is_safe(piece, move[0], move[1]):
                has_valid_move = True
                break
    return has_valid_move


def in_check(own_king, attacking_pieces):
    # Changes the turn so get_potential_moves returns moves for the attacking (opposite) side
    change_turn()
    for piece in attacking_pieces:
        potential_moves = piece.get_potential_moves()
        for potential_move in potential_moves:
            if potential_move[0] == own_king.x and potential_move[1] == own_king.y:
                change_turn()
                return True
    change_turn()
    return False


def king_is_safe(selected_piece, move_x, move_y):
    global white_copy, black_copy
    white_copy, black_copy = get_piece_copies(selected_piece, move_x, move_y)

    if white_to_move:
        for p in white_copy:
            if isinstance(p, King):
                own_king = p
                break
        enemy_pieces = black_copy
    else:
        for p in black_copy:
            if isinstance(p, King):
                own_king = p
                break
        enemy_pieces = white_copy

    global USE_COPIES
    USE_COPIES = True
    if in_check(own_king, enemy_pieces):
        USE_COPIES = False
        return False
    else:
        USE_COPIES = False
        return True


# TODO: clean this up
def get_piece_copies(selected_piece, move_x, move_y):
    white_pieces_cp, black_pieces_cp = [], []
    for piece in white_pieces:
        x, y = piece.x, piece.y
        if piece is selected_piece:
            x, y = move_x, move_y

        if isinstance(piece, Pawn):
            white_pieces_cp.append(Pawn(x, y, "white", False))
        elif isinstance(piece, Queen):
            white_pieces_cp.append(Queen(x, y, "white", False))
        elif isinstance(piece, Knight):
            white_pieces_cp.append(Knight(x, y, "white", False))
        elif isinstance(piece, Bishop):
            white_pieces_cp.append(Bishop(x, y, "white", False))
        elif isinstance(piece, Rook):
            white_pieces_cp.append(Rook(x, y, "white", False))
        elif isinstance(piece, King):
            white_pieces_cp.append(King(x, y, "white", False))

    for piece2 in black_pieces:
        x, y = piece2.x, piece2.y
        if piece2 is selected_piece:
            x, y = move_x, move_y

        if isinstance(piece2, Pawn):
            black_pieces_cp.append(Pawn(x, y, "black", False))
        elif isinstance(piece2, Queen):
            black_pieces_cp.append(Queen(x, y, "black", False))
        elif isinstance(piece2, Knight):
            black_pieces_cp.append(Knight(x, y, "black", False))
        elif isinstance(piece2, Bishop):
            black_pieces_cp.append(Bishop(x, y, "black", False))
        elif isinstance(piece2, Rook):
            black_pieces_cp.append(Rook(x, y, "black", False))
        elif isinstance(piece2, King):
            black_pieces_cp.append(King(x, y, "black", False))

    # Delete a captured piece from the list
    if white_to_move:
        for p1 in black_pieces_cp.copy():
            if p1.x == move_x and p1.y == move_y:
                black_pieces_cp.remove(p1)
    else:
        for p2 in white_pieces_cp.copy():
            if p2.x == move_x and p2.y == move_y:
                white_pieces_cp.remove(p2)

    return white_pieces_cp, black_pieces_cp


def get_selected_piece():
    selected_piece = None
    while True:
        if selected_piece is None:
            point = win.getMouse()
            selected_x, selected_y = find_selected_tile(point)
            pieces_to_check = get_own_pieces()
            selected_piece = get_piece_on_tile(selected_x, selected_y, pieces_to_check)
        else:
            game_board[selected_x][selected_y].highlight_square()
            return selected_piece


def valid_move_selection(potential_moves, selected_x, selected_y):
    for potential_move in potential_moves:
        if selected_x == potential_move[0] and selected_y == potential_move[1]:
            return True
    return False


def get_king(pieces_to_check):
    for piece in pieces_to_check:
        if isinstance(piece, King):
            return piece


def change_turn():
    global white_to_move
    white_to_move = not white_to_move


def find_selected_tile(point):
    x_pixel, y_pixel = point.x, point.y
    x_sq = math.floor(x_pixel / TILE_LENGTH)
    y_sq = math.floor(y_pixel / TILE_LENGTH)
    return x_sq, y_sq


def get_piece_on_tile(selected_x, selected_y, pieces_to_check):
    for piece in pieces_to_check:
        if piece.x == selected_x and piece.y == selected_y:
            return piece
    return None


def blocked_by_piece(x, y, pieces_to_check):
    for piece in pieces_to_check:
        if piece.x == x and piece.y == y:
            return True
    return False


def get_own_pieces():
    if USE_COPIES:
        if white_to_move:
            return white_copy
        else:
            return black_copy
    else:
        if white_to_move:
            return white_pieces
        else:
            return black_pieces


def get_enemy_pieces():
    if USE_COPIES:
        if white_to_move:
            return black_copy
        else:
            return white_copy
    else:
        if white_to_move:
            return black_pieces
        else:
            return white_pieces


def get_north_moves(x_start, y_start, max_distance=7):
    moves = []
    for y in range(y_start - 1, y_start - max_distance - 1, -1):
        if y < 0 or blocked_by_piece(x_start, y, get_own_pieces()):
            break
        moves.append([x_start, y])
        if blocked_by_piece(x_start, y, get_enemy_pieces()):
            break
    return moves


def get_south_moves(x_start, y_start, max_distance=7):
    moves = []
    for y in range(y_start + 1, y_start + max_distance + 1):
        if y > 7 or blocked_by_piece(x_start, y, get_own_pieces()):
            break
        moves.append([x_start, y])
        if blocked_by_piece(x_start, y, get_enemy_pieces()):
            break
    return moves


def get_east_moves(x_start, y_start, max_distance=7):
    moves = []
    for x in range(x_start + 1, x_start + max_distance + 1):
        if x > 7 or blocked_by_piece(x, y_start, get_own_pieces()):
            break
        moves.append([x, y_start])
        if blocked_by_piece(x, y_start, get_enemy_pieces()):
            break
    return moves


def get_west_moves(x_start, y_start, max_distance=7):
    moves = []
    for x in range(x_start - 1, x_start - max_distance - 1, -1):
        if x < 0 or blocked_by_piece(x, y_start, get_own_pieces()):
            break
        moves.append([x, y_start])
        if blocked_by_piece(x, y_start, get_enemy_pieces()):
            break
    return moves


def get_northeast_moves(x_start, y_start, max_distance=7):
    moves = []
    for x, y in zip(range(x_start + 1, x_start + max_distance + 1), range(y_start - 1, y_start - max_distance - 1, -1)):
        if x > 7 or y < 0 or blocked_by_piece(x, y, get_own_pieces()):
            break
        moves.append([x, y])
        if blocked_by_piece(x, y, get_enemy_pieces()):
            break
    return moves


def get_northwest_moves(x_start, y_start, max_distance=7):
    moves = []
    for x, y in zip(range(x_start - 1, x_start - max_distance - 1, -1),
                    range(y_start - 1, y_start - max_distance - 1, -1)):
        if x < 0 or y < 0 or blocked_by_piece(x, y, get_own_pieces()):
            break
        moves.append([x, y])
        if blocked_by_piece(x, y, get_enemy_pieces()):
            break
    return moves


def get_southeast_moves(x_start, y_start, max_distance=7):
    moves = []
    for x, y in zip(range(x_start + 1, x_start + max_distance + 1), range(y_start + 1, y_start + max_distance + 1)):
        if x > 7 or y > 7 or blocked_by_piece(x, y, get_own_pieces()):
            break
        moves.append([x, y])
        if blocked_by_piece(x, y, get_enemy_pieces()):
            break
    return moves


def get_southwest_moves(x_start, y_start, max_distance=7):
    moves = []
    for x, y in zip(range(x_start - 1, x_start - max_distance - 1, -1), range(y_start + 1, y_start + max_distance + 1)):
        if x < 0 or y > 7 or blocked_by_piece(x, y, get_own_pieces()):
            break
        moves.append([x, y])
        if blocked_by_piece(x, y, get_enemy_pieces()):
            break
    return moves


def get_knight_moves(x_start, y_start):
    moves = [[x_start + 1, y_start + 2],
             [x_start + 1, y_start - 2],
             [x_start - 1, y_start + 2],
             [x_start - 1, y_start - 2],
             [x_start + 2, y_start + 1],
             [x_start + 2, y_start - 1],
             [x_start - 2, y_start + 1],
             [x_start - 2, y_start - 1]]

    for mov in moves.copy():
        if mov[0] > 7 or mov[0] < 0 or mov[1] > 7 or mov[1] < 0 or blocked_by_piece(mov[0], mov[1], get_own_pieces()):
            moves.remove(mov)

    return moves


# Classes -------------------------------------------------
class GameSquare:

    def __init__(self, square_x, square_y):
        self.square_x, self.square_y = square_x, square_y
        self.rectangle = Rectangle(Point(square_x * TILE_LENGTH, square_y * TILE_LENGTH),
                                   Point((square_x + 1) * TILE_LENGTH, (square_y + 1) * TILE_LENGTH))
        self.color = ""

    def set_color(self, color):
        self.color = color

    def color_square(self):
        if self.color == "white":
            self.rectangle.setOutline(color_rgb(141, 108, 65))
            self.rectangle.setFill(color_rgb(141, 108, 65))
        else:
            self.rectangle.setOutline(color_rgb(255, 255, 255))
            self.rectangle.setFill(color_rgb(255, 255, 255))

    def init_drawing(self):
        self.rectangle.draw(win)

    def find_midpoint(self):
        return Point(self.square_x * TILE_LENGTH + (TILE_LENGTH / 2), self.square_y * TILE_LENGTH + (TILE_LENGTH / 2))

    def highlight_square(self):
        self.rectangle.setOutline(color_rgb(235, 248, 1))
        self.rectangle.setFill(color_rgb(235, 248, 1))


class Piece(ABC):

    def __init__(self, start_x, start_y, color):
        self.x = start_x
        self.y = start_y
        self.color = color

    def update_xy(self, x, y):
        self.x, self.y = x, y

    def move_piece(self, square_to_move_to):
        if isinstance(self, (Pawn, King, Queen, Rook, Knight, Bishop)):
            self.x, self.y = square_to_move_to.square_x, square_to_move_to.square_y
            self.img.undraw()
            self.img.change_anchor_point(square_to_move_to.find_midpoint())
            self.img.draw(win)

        if isinstance(self, (Pawn, King, Rook)):
            self.has_moved()

        Piece.piece_capture(square_to_move_to)

    @staticmethod
    def piece_capture(square_to_move_to):
        enemy_pieces = get_enemy_pieces()

        for piece in enemy_pieces.copy():
            if square_to_move_to.square_x == piece.x and square_to_move_to.square_y == piece.y:
                piece.img.undraw()
                enemy_pieces.remove(piece)

    @abstractmethod
    def get_potential_moves(self):
        pass


class Pawn(Piece):

    def __init__(self, start_x, start_y, color, draw_flag=True):
        super().__init__(start_x, start_y, color)
        self.moved = False

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        if self.color == "white":
            if not blocked_by_piece(self.x, self.y - 1, get_enemy_pieces()) \
                    and not blocked_by_piece(self.x, self.y - 2, get_enemy_pieces()) and not self.moved:
                potential_moves.extend(get_north_moves(self.x, self.y, 2))
            elif not blocked_by_piece(self.x, self.y - 1, get_enemy_pieces()):
                potential_moves.extend(get_north_moves(self.x, self.y, 1))

            if blocked_by_piece(self.x - 1, self.y - 1, get_enemy_pieces()):
                potential_moves.extend(get_northwest_moves(self.x, self.y, 1))
            if blocked_by_piece(self.x + 1, self.y - 1, get_enemy_pieces()):
                potential_moves.extend(get_northeast_moves(self.x, self.y, 1))
        else:
            if not blocked_by_piece(self.x, self.y + 1, get_enemy_pieces()) \
                    and not blocked_by_piece(self.x, self.y + 2, get_enemy_pieces()) and not self.moved:
                potential_moves.extend(get_south_moves(self.x, self.y, 2))
            elif not blocked_by_piece(self.x, self.y + 1, get_enemy_pieces()):
                potential_moves.extend(get_south_moves(self.x, self.y, 1))

            if blocked_by_piece(self.x - 1, self.y + 1, get_enemy_pieces()):
                potential_moves.extend(get_southwest_moves(self.x, self.y, 1))
            if blocked_by_piece(self.x + 1, self.y + 1, get_enemy_pieces()):
                potential_moves.extend(get_southeast_moves(self.x, self.y, 1))
        return potential_moves

    def has_moved(self):
        self.moved = True

    def check_if_moved(self):
        return self.moved


class King(Piece):

    def __init__(self, start_x, start_y, color, draw_flag=True):
        super().__init__(start_x, start_y, color)
        self.moved = False

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/king_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/king_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_north_moves(self.x, self.y, 1))
        potential_moves.extend(get_south_moves(self.x, self.y, 1))
        potential_moves.extend(get_west_moves(self.x, self.y, 1))
        potential_moves.extend(get_east_moves(self.x, self.y, 1))
        potential_moves.extend(get_northeast_moves(self.x, self.y, 1))
        potential_moves.extend(get_northwest_moves(self.x, self.y, 1))
        potential_moves.extend(get_southeast_moves(self.x, self.y, 1))
        potential_moves.extend(get_southwest_moves(self.x, self.y, 1))
        return potential_moves

    def has_moved(self):
        self.moved = True

    def check_if_moved(self):
        return self.moved


class Queen(Piece):

    def __init__(self, start_x, start_y, color, draw_flag=True):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/queen_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/queen_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_north_moves(self.x, self.y))
        potential_moves.extend(get_south_moves(self.x, self.y))
        potential_moves.extend(get_west_moves(self.x, self.y))
        potential_moves.extend(get_east_moves(self.x, self.y))
        potential_moves.extend(get_northeast_moves(self.x, self.y))
        potential_moves.extend(get_northwest_moves(self.x, self.y))
        potential_moves.extend(get_southeast_moves(self.x, self.y))
        potential_moves.extend(get_southwest_moves(self.x, self.y))
        return potential_moves


class Rook(Piece):

    def __init__(self, start_x, start_y, color, draw_flag=True):
        super().__init__(start_x, start_y, color)
        self.moved = False

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/rook_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/rook_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_north_moves(self.x, self.y))
        potential_moves.extend(get_south_moves(self.x, self.y))
        potential_moves.extend(get_west_moves(self.x, self.y))
        potential_moves.extend(get_east_moves(self.x, self.y))
        return potential_moves

    def has_moved(self):
        self.moved = True

    def check_if_moved(self):
        return self.moved


class Bishop(Piece):

    def __init__(self, start_x, start_y, color, draw_flag=True):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/bishop_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/bishop_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_northeast_moves(self.x, self.y))
        potential_moves.extend(get_northwest_moves(self.x, self.y))
        potential_moves.extend(get_southeast_moves(self.x, self.y))
        potential_moves.extend(get_southwest_moves(self.x, self.y))
        return potential_moves


class Knight(Piece):

    def __init__(self, start_x, start_y, color, draw_flag=True):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        return get_knight_moves(self.x, self.y)


main()
