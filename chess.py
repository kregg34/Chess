from graphics import *
import math
from abc import ABC, abstractmethod

WIN_SIZE = 600
win = GraphWin("Chess", WIN_SIZE, WIN_SIZE)
game_board = []
bottom_pieces = []
top_pieces = []

bottom_copy = []
top_copy = []
USE_COPIES = False

CASTLE_SELECTION_SQUARES_BOTTOM = [[0, 7], [2, 7], [6, 7], [7, 7]]
CASTLE_SELECTION_SQUARES_TOP = [[0, 0], [2, 0], [6, 0], [7, 0]]
BOTTOM_ROOK_LEFT_MAP = CASTLE_SELECTION_SQUARES_BOTTOM[0:2]
BOTTOM_ROOK_RIGHT_MAP = CASTLE_SELECTION_SQUARES_BOTTOM[2:4]
TOP_ROOK_LEFT_MAP = CASTLE_SELECTION_SQUARES_TOP[0:2]
TOP_ROOK_RIGHT_MAP = CASTLE_SELECTION_SQUARES_TOP[2:4]

bottom_to_move = False
FLIP_BOARD = True

HEIGHT = 8
WIDTH = 8
TILE_LENGTH = WIN_SIZE / 8


def main():
    init_menu()
    init_game_board()
    add_in_pieces()
    game_loop()
    win.close()


def init_menu():
    x_lower, x_upper = 200, 400
    button1_y_lower, button1_y_upper, button2_y_lower, button2_y_upper = 250, 350, 400, 500

    background = Rectangle(Point(0, 0), Point(WIN_SIZE, WIN_SIZE))
    background.setFill("black")
    button1 = Rectangle(Point(x_lower, button1_y_lower), Point(x_upper, button1_y_upper))
    button1.setFill("grey")
    button2 = Rectangle(Point(x_lower, button2_y_lower), Point(x_upper, button2_y_upper))
    button2.setFill("grey")
    welcome_text = Text(Point(300, 100), "Chess")
    welcome_text.setTextColor("red")
    welcome_text.setSize(30)
    desc_text = Text(Point(300, 150), "Please choose a side...")
    desc_text.setTextColor("white")
    desc_text.setSize(20)
    option_1_text = Text(Point(300, 300), "White")
    option_1_text.setSize(15)
    option_2_text = Text(Point(300, 450), "Black")
    option_2_text.setSize(15)

    background.draw(win)
    button1.draw(win)
    button2.draw(win)
    welcome_text.draw(win)
    desc_text.draw(win)
    option_1_text.draw(win)
    option_2_text.draw(win)

    global bottom_to_move, FLIP_BOARD
    while True:
        point = win.getMouse()
        if x_lower <= point.x <= x_upper and button1_y_lower <= point.y <= button1_y_upper:
            bottom_to_move = True
            FLIP_BOARD = False
            break
        elif x_lower <= point.x <= x_upper and button2_y_lower <= point.y <= button2_y_upper:
            bottom_to_move = False
            FLIP_BOARD = True
            break


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
    if FLIP_BOARD:
        bottom_color = "black"
        top_color = "white"
    else:
        bottom_color = "white"
        top_color = "black"

    bottom_pieces.append(King(4, 7, bottom_color, side="bottom"))
    bottom_pieces.append(Queen(3, 7, bottom_color, side="bottom"))
    bottom_pieces.append(Rook(0, 7, bottom_color, side="bottom"))
    bottom_pieces.append(Rook(7, 7, bottom_color, side="bottom"))
    bottom_pieces.append(Bishop(2, 7, bottom_color, side="bottom"))
    bottom_pieces.append(Bishop(5, 7, bottom_color, side="bottom"))
    bottom_pieces.append(Knight(1, 7, bottom_color, side="bottom"))
    bottom_pieces.append(Knight(6, 7, bottom_color, side="bottom"))
    top_pieces.append(King(4, 0, top_color, side="top"))
    top_pieces.append(Queen(3, 0, top_color, side="top"))
    top_pieces.append(Rook(0, 0, top_color, side="top"))
    top_pieces.append(Rook(7, 0, top_color, side="top"))
    top_pieces.append(Bishop(2, 0, top_color, side="top"))
    top_pieces.append(Bishop(5, 0, top_color, side="top"))
    top_pieces.append(Knight(1, 0, top_color, side="top"))
    top_pieces.append(Knight(6, 0, top_color, side="top"))
    for i in range(0, 8):
        bottom_pieces.append(Pawn(i, 6, bottom_color, side="bottom"))
        top_pieces.append(Pawn(i, 1, top_color, side="top"))


def game_loop():
    while True:
        next_move()

        if in_check(get_king(get_own_pieces()), get_enemy_pieces()):
            if in_checkmate():
                ending_text("checkmate")
                win.getMouse()
                break
        elif not has_valid_moves():
            ending_text("stalemate")
            win.getMouse()
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

    if not castling(selected_piece, selected_x, selected_y):
        if not valid_move_selection(potential_moves, selected_x, selected_y):
            return
        elif king_is_safe(selected_piece, selected_x, selected_y):
            selected_piece.move_piece(game_board[selected_x][selected_y])
            change_turn()


def castling(selected_piece, selected_x, selected_y):
    if is_a_king(selected_piece) and selected_castle_square(selected_x, selected_y):
        if not in_check(selected_piece, get_enemy_pieces()) and not selected_piece.check_if_moved():
            rook_to_move, rook_pos, king_pos, squares_to_check = get_rook(selected_x, selected_y)
            if rook_to_move.check_if_moved():
                return False
            for square in squares_to_check:
                if attacked(square) or blocked_by_piece(square[0], square[1], get_enemy_pieces()) \
                        or blocked_by_piece(square[0], square[1], get_own_pieces()):
                    return False
            selected_piece.move_piece(GameSquare(king_pos[0], king_pos[1]))
            rook_to_move.move_piece(GameSquare(rook_pos[0], rook_pos[1]))
            change_turn()
            return True


def attacked(square):
    for attacking_piece in get_enemy_pieces():
        for move in attacking_piece.get_potential_moves():
            if move[0] == square[0] and move[1] == square[1]:
                return True
    return False


def get_rook(selected_x, selected_y):
    for piece in get_own_pieces():
        if isinstance(piece, Rook):
            if bottom_to_move:
                for pos in BOTTOM_ROOK_LEFT_MAP:
                    if selected_x == pos[0] and selected_y == pos[1] and piece.x == 0 and piece.y == 7:
                        return piece, [3, 7], [2, 7], [[2, 7], [3, 7]]
                for pos in BOTTOM_ROOK_RIGHT_MAP:
                    if selected_x == pos[0] and selected_y == pos[1] and piece.x == 7 and piece.y == 7:
                        return piece, [5, 7], [6, 7], [[5, 7], [6, 7]]
            else:
                for pos in TOP_ROOK_LEFT_MAP:
                    if selected_x == pos[0] and selected_y == pos[1] and piece.x == 0 and piece.y == 0:
                        return piece, [3, 0], [2, 0], [[2, 0], [3, 0]]
                for pos in TOP_ROOK_RIGHT_MAP:
                    if selected_x == pos[0] and selected_y == pos[1] and piece.x == 7 and piece.y == 0:
                        return piece, [5, 0], [6, 0], [[5, 0], [6, 0]]


def selected_castle_square(selected_x, selected_y):
    if bottom_to_move:
        sqs = CASTLE_SELECTION_SQUARES_BOTTOM
    else:
        sqs = CASTLE_SELECTION_SQUARES_TOP
    for square in sqs:
        if square[0] == selected_x and square[1] == selected_y:
            return True
    return False


def is_a_king(selected_piece):
    if isinstance(selected_piece, King):
        return True
    else:
        return False


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
    global bottom_copy, top_copy, USE_COPIES
    bottom_copy, top_copy = get_piece_copies(selected_piece, move_x, move_y)
    own_king = None

    if bottom_to_move:
        for p in bottom_copy:
            if isinstance(p, King):
                own_king = p
                break
        enemy_pieces = top_copy
    else:
        for p in top_copy:
            if isinstance(p, King):
                own_king = p
                break
        enemy_pieces = bottom_copy

    USE_COPIES = True
    if in_check(own_king, enemy_pieces):
        USE_COPIES = False
        return False
    else:
        USE_COPIES = False
        return True


def get_piece_copies(selected_piece, move_x, move_y):
    bottom_pieces_cp, top_pieces_cp = [], []

    add_piece_copies(selected_piece, move_x, move_y, bottom_pieces, bottom_pieces_cp, "white")
    add_piece_copies(selected_piece, move_x, move_y, top_pieces, top_pieces_cp, "black")

    # Delete a captured piece from the list
    if bottom_to_move:
        for p1 in top_pieces_cp.copy():
            if p1.x == move_x and p1.y == move_y:
                top_pieces_cp.remove(p1)
    else:
        for p2 in bottom_pieces_cp.copy():
            if p2.x == move_x and p2.y == move_y:
                bottom_pieces_cp.remove(p2)

    return bottom_pieces_cp, top_pieces_cp


def add_piece_copies(selected_piece, move_x, move_y, pieces_to_copy, copy_list, color):
    for piece in pieces_to_copy:
        x, y = piece.x, piece.y
        if piece is selected_piece:
            x, y = move_x, move_y

        if isinstance(piece, Pawn):
            copy_list.append(Pawn(x, y, color, piece.side, False))
        elif isinstance(piece, Queen):
            copy_list.append(Queen(x, y, color, piece.side, False))
        elif isinstance(piece, Knight):
            copy_list.append(Knight(x, y, color, piece.side, False))
        elif isinstance(piece, Bishop):
            copy_list.append(Bishop(x, y, color, piece.side, False))
        elif isinstance(piece, Rook):
            copy_list.append(Rook(x, y, color, piece.side, False))
        elif isinstance(piece, King):
            copy_list.append(King(x, y, color, piece.side, False))


def get_selected_piece():
    selected_piece = None
    selected_x, selected_y = -1, -1
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
    global bottom_to_move
    bottom_to_move = not bottom_to_move


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
        if bottom_to_move:
            return bottom_copy
        else:
            return top_copy
    else:
        if bottom_to_move:
            return bottom_pieces
        else:
            return top_pieces


def get_enemy_pieces():
    if USE_COPIES:
        if bottom_to_move:
            return top_copy
        else:
            return bottom_copy
    else:
        if bottom_to_move:
            return top_pieces
        else:
            return bottom_pieces


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

    def __init__(self, start_x, start_y, color, side):
        self.x = start_x
        self.y = start_y
        self.color = color
        self.side = side

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

        if isinstance(self, Pawn):
            if self.y == 0 or self.y == 7:
                Piece.promotion(self)

        Piece.piece_capture(square_to_move_to)

    @staticmethod
    def promotion(promoted_pawn):
        for piece in get_own_pieces().copy():
            if piece is promoted_pawn:
                get_own_pieces().append(Queen(promoted_pawn.x, promoted_pawn.y,
                                              promoted_pawn.color, promoted_pawn.side))
                promoted_pawn.img.undraw()
                get_own_pieces().remove(promoted_pawn)

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

    def __init__(self, start_x, start_y, color, side, draw_flag=True):
        super().__init__(start_x, start_y, color, side)
        self.moved = False

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []

        if self.side == "bottom":
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

    def __init__(self, start_x, start_y, color, side, draw_flag=True):
        super().__init__(start_x, start_y, color, side)
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

    def __init__(self, start_x, start_y, color, side, draw_flag=True):
        super().__init__(start_x, start_y, color, side)

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

    def __init__(self, start_x, start_y, color, side, draw_flag=True):
        super().__init__(start_x, start_y, color, side)
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

    def __init__(self, start_x, start_y, color, side, draw_flag=True):
        super().__init__(start_x, start_y, color, side)

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

    def __init__(self, start_x, start_y, color, side, draw_flag=True):
        super().__init__(start_x, start_y, color, side)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_b.png")
        if draw_flag:
            self.img.draw(win)

    def get_potential_moves(self):
        return get_knight_moves(self.x, self.y)


if __name__ == "__main__":
    main()
