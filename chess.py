from graphics import *
import math

WIN_SIZE = 600
win = GraphWin("Chess", WIN_SIZE, WIN_SIZE)
game_board = []
white_pieces = []
black_pieces = []

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

    white_to_move = True
    while no_check_mate():

        if white_to_move:
            print("White to move!")
            point = win.getMouse()
            print("You clicked at: " + str(point))

            find_selected_piece(point)

            white_to_move = False
        else:
            print("Black to move!")
            point = win.getMouse()
            print("You clicked at: " + str(point))

            find_selected_piece(point)

            white_to_move = True


def find_selected_piece(point):
    x_pixel, y_pixel = point.x, point.y
    x_sq = math.floor(x_pixel / TILE_LENGTH)
    y_sq = math.floor(y_pixel / TILE_LENGTH)
    print("You selected square: " + str(x_sq) + ", " + str(y_sq))


def no_check_mate():
    return True


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


class Piece:

    def __init__(self, start_x, start_y, color):
        self.x = start_x
        self.y = start_y
        self.color = color


class Pawn(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/pawn_b.png")
        self.img.draw(win)


class King(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/king_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/king_b.png")
        self.img.draw(win)


class Queen(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/queen_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/queen_b.png")
        self.img.draw(win)


class Rook(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/rook_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/rook_b.png")
        self.img.draw(win)


class Bishop(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/bishop_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/bishop_b.png")
        self.img.draw(win)


class Knight(Piece):

    def __init__(self, start_x, start_y, color):
        super().__init__(start_x, start_y, color)

        if self.color == "white":
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_w.png")
        else:
            self.img = Image(game_board[start_x][start_y].find_midpoint(), "photos/knight_b.png")
        self.img.draw(win)


main()
