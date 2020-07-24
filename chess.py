from graphics import *
import math
from abc import ABC, abstractmethod

WIN_SIZE = 600
win = GraphWin("Chess", WIN_SIZE, WIN_SIZE)
game_board = []
white_pieces = []
black_pieces = []

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
                    obj.setup_square(True)
                else:
                    obj.setup_square(False)
            else:
                if j % 2 == 0:
                    obj.setup_square(False)
                else:
                    obj.setup_square(True)

            obj.init_drawing()
        game_board.append(x)


def add_in_pieces():
    for i in range(0, 8):
        white_pieces.append(Pawn(i, 6, "white"))
        black_pieces.append(Pawn(i, 1, "black"))

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


def game_loop():
    while no_check_mate():
        next_move()


def next_move():
    global white_to_move

    point = win.getMouse()
    selected_x, selected_y = find_selected_tile(point)
    selected_piece = get_piece_on_tile(selected_x, selected_y, white_to_move)

    while True:
        if selected_piece is None:
            point = win.getMouse()
            selected_x, selected_y = find_selected_tile(point)
            selected_piece = get_piece_on_tile(selected_x, selected_y, white_to_move)
            continue
        else:
            # valid piece selection
            print("You selected a: " + selected_piece.get_name())

            pot_moves = selected_piece.get_potential_moves()
            print(pot_moves)

            move_point = win.getMouse()
            selected_x, selected_y = find_selected_tile(move_point)
            print(str(selected_x) + ", " + str(selected_y))

            for pot_move in pot_moves:
                if selected_x == pot_move[0] and selected_y == pot_move[1]:
                    selected_piece.move_piece(game_board[selected_x][selected_y])
                    change_turn()
                    break
        break


def change_turn():
    global white_to_move
    white_to_move = not white_to_move


def find_selected_tile(point):
    x_pixel, y_pixel = point.x, point.y
    x_sq = math.floor(x_pixel / TILE_LENGTH)
    y_sq = math.floor(y_pixel / TILE_LENGTH)
    return x_sq, y_sq


def get_piece_on_tile(selected_x, selected_y, is_whites_turn):
    if is_whites_turn:
        pieces_to_check = white_pieces
    else:
        pieces_to_check = black_pieces

    for piece in pieces_to_check:
        if piece.x == selected_x and piece.y == selected_y:
            return piece
    return None


def no_check_mate():
    return True


def blocked_by_own(x, y, color):
    if color == "white":
        for piece in white_pieces:
            if piece.x == x and piece.y == y:
                return True
    else:
        for piece in black_pieces:
            if piece.x == x and piece.y == y:
                return True
    return False


def get_north_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for y in range(y_start - 1, y_start - max_distance - 1, -1):
        if y < 0 or blocked_by_own(x_start, y, color):
            break
        moves.append([x_start, y])
    return moves


def get_south_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for y in range(y_start + 1, y_start + max_distance + 1):
        if y > 7 or blocked_by_own(x_start, y, color):
            break
        moves.append([x_start, y])
    return moves


def get_east_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for x in range(x_start + 1, x_start + max_distance + 1):
        if x > 7 or blocked_by_own(x, y_start, color):
            break
        moves.append([x, y_start])
    return moves


def get_west_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for x in range(x_start - 1, x_start - max_distance - 1, -1):
        if x < 0 or blocked_by_own(x, y_start, color):
            break
        moves.append([x, y_start])
    return moves


def get_northeast_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for x, y in zip(range(x_start + 1, x_start + max_distance + 1), range(y_start - 1, y_start - max_distance - 1, -1)):
        if x > 7 or y < 0 or blocked_by_own(x, y, color):
            break
        moves.append([x, y])
    return moves


def get_northwest_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for x, y in zip(range(x_start - 1, x_start - max_distance - 1, -1),
                    range(y_start - 1, y_start - max_distance - 1, -1)):
        if x < 0 or y < 0 or blocked_by_own(x, y, color):
            break
        moves.append([x, y])
    return moves


def get_southeast_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for x, y in zip(range(x_start + 1, x_start + max_distance + 1), range(y_start + 1, y_start + max_distance + 1)):
        if x > 7 or y > 7 or blocked_by_own(x, y, color):
            break
        moves.append([x, y])
    return moves


def get_southwest_moves(x_start, y_start, color, max_distance=7):
    moves = []
    for x, y in zip(range(x_start - 1, x_start - max_distance - 1, -1), range(y_start + 1, y_start + max_distance + 1)):
        if x < 0 or y > 7 or blocked_by_own(x, y, color):
            break
        moves.append([x, y])
    return moves


def get_knight_moves(x_start, y_start, color):
    moves = [[x_start + 1, y_start + 2],
             [x_start + 1, y_start - 2],
             [x_start - 1, y_start + 2],
             [x_start - 1, y_start - 2],
             [x_start + 2, y_start + 1],
             [x_start + 2, y_start - 1],
             [x_start - 2, y_start + 1],
             [x_start - 2, y_start - 1]]

    for mov in moves.copy():
        if blocked_by_own(mov[0], mov[1], color):
            moves.remove(mov)
    return moves


class GameSquare:

    def __init__(self, square_x, square_y):
        self.square_x = square_x
        self.square_y = square_y
        self.rectangle = Rectangle(Point(square_x * TILE_LENGTH, square_y * TILE_LENGTH),
                                   Point((square_x + 1) * TILE_LENGTH, (square_y + 1) * TILE_LENGTH))

    def setup_square(self, color_is_white):
        if color_is_white:
            self.rectangle.setOutline(color_rgb(141, 108, 65))
            self.rectangle.setFill(color_rgb(141, 108, 65))
        else:
            self.rectangle.setOutline(color_rgb(255, 255, 255))
            self.rectangle.setFill(color_rgb(255, 255, 255))

    def init_drawing(self):
        self.rectangle.draw(win)

    def find_midpoint(self):
        return Point(self.square_x * TILE_LENGTH + (TILE_LENGTH / 2), self.square_y * TILE_LENGTH + (TILE_LENGTH / 2))


# Abstract class
class Piece(ABC):

    def __init__(self, start_x, start_y, color):
        self.x = start_x
        self.y = start_y
        self.color = color

    # TODO: Remove this later, its just for convenience
    def get_name(self):
        if isinstance(self, Pawn):
            return "Pawn"
        elif isinstance(self, Knight):
            return "Knight"
        elif isinstance(self, Rook):
            return "Rook"
        elif isinstance(self, Bishop):
            return "Bishop"
        elif isinstance(self, Queen):
            return "Queen"
        elif isinstance(self, King):
            return "King"

    def move_piece(self, square_to_move_to):
        if isinstance(self, (Pawn, King, Queen, Rook, Knight, Bishop)):
            self.img.undraw()
            # I created this method myself in graphics.py to make things easier
            self.img.change_anchor_point(square_to_move_to.find_midpoint())
            self.img.draw(win)
            self.x, self.y = square_to_move_to.square_x, square_to_move_to.square_y

        if isinstance(self, (Pawn, King, Rook)):
            self.has_moved()

    @abstractmethod
    def get_potential_moves(self):
        pass


class Pawn(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)
        self.moved = False

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_b.png")
        self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []

        if self.color == "white":
            if self.moved:
                potential_moves.extend(get_north_moves(self.x, self.y, 1))
            else:
                potential_moves.extend(get_north_moves(self.x, self.y, 2))
        else:
            if self.moved:
                potential_moves.extend(get_south_moves(self.x, self.y, 1))
            else:
                potential_moves.extend(get_south_moves(self.x, self.y, 2))

        return potential_moves

    def has_moved(self):
        self.moved = True

    def check_if_moved(self):
        return self.moved


class King(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)
        self.moved = False

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/king_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/king_b.png")
        self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_north_moves(self.x, self.y, self.color, 1))
        potential_moves.extend(get_south_moves(self.x, self.y, self.color, 1))
        potential_moves.extend(get_west_moves(self.x, self.y, self.color, 1))
        potential_moves.extend(get_east_moves(self.x, self.y, self.color, 1))
        potential_moves.extend(get_northeast_moves(self.x, self.y, self.color, 1))
        potential_moves.extend(get_northwest_moves(self.x, self.y, self.color, 1))
        potential_moves.extend(get_southeast_moves(self.x, self.y, self.color, 1))
        potential_moves.extend(get_southwest_moves(self.x, self.y, self.color, 1))
        return potential_moves

    def has_moved(self):
        self.moved = True

    def check_if_moved(self):
        return self.moved


class Queen(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/queen_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/queen_b.png")
        self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_north_moves(self.x, self.y, self.color))
        potential_moves.extend(get_south_moves(self.x, self.y, self.color))
        potential_moves.extend(get_west_moves(self.x, self.y, self.color))
        potential_moves.extend(get_east_moves(self.x, self.y, self.color))
        potential_moves.extend(get_northeast_moves(self.x, self.y, self.color))
        potential_moves.extend(get_northwest_moves(self.x, self.y, self.color))
        potential_moves.extend(get_southeast_moves(self.x, self.y, self.color))
        potential_moves.extend(get_southwest_moves(self.x, self.y, self.color))
        return potential_moves


class Rook(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)
        self.moved = False

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/rook_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/rook_b.png")
        self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_north_moves(self.x, self.y, self.color))
        potential_moves.extend(get_south_moves(self.x, self.y, self.color))
        potential_moves.extend(get_west_moves(self.x, self.y, self.color))
        potential_moves.extend(get_east_moves(self.x, self.y, self.color))
        return potential_moves

    def has_moved(self):
        self.moved = True

    def check_if_moved(self):
        return self.moved


class Bishop(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/bishop_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/bishop_b.png")
        self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_northeast_moves(self.x, self.y, self.color))
        potential_moves.extend(get_northwest_moves(self.x, self.y, self.color))
        potential_moves.extend(get_southeast_moves(self.x, self.y, self.color))
        potential_moves.extend(get_southwest_moves(self.x, self.y, self.color))
        return potential_moves


class Knight(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_b.png")
        self.img.draw(win)

    def get_potential_moves(self):
        potential_moves = []
        potential_moves.extend(get_knight_moves(self.x, self.y, self.color))
        return potential_moves


main()
