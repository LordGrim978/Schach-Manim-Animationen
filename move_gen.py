from manim import *

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = list(range(1, 9))

class ChessBoard(Mobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        squares = VGroup()

        board_size = 6
        square_size = board_size / 8
        self.square_size = square_size

        self.squares_dict = {}

        for rank_index, rank in enumerate(reversed(RANKS)):
            for file_index, file in enumerate(FILES):
                is_light = (file_index + rank_index) % 2 == 0
                color = "#f0d9b5" if is_light else "#b58863"

                sq = Square(side_length=square_size)
                sq.set_fill(color, opacity=1).set_stroke(BLACK, width=0.5)

                x = (file_index - 3.5) * square_size
                y = (rank_index - 3.5) * square_size
                sq.move_to([x, y, 0])

                squares.add(sq)
                self.squares_dict[(file, rank)] = sq

        self.add(squares)

class KnightMoves(Scene):
    def construct(self):
        board = ChessBoard()
        board.scale(0.8)
        self.play(FadeIn(board))

        # Place knight in the center (d4)
        knight = SVGMobject("knight.png")  # needs a knight svg in working dir
        knight.set_height(board.square_size * 0.8)
        knight.move_to(board.squares_dict[("d", 4)].get_center())
        self.play(FadeIn(knight, scale=0.5))

        # Legal knight moves from d4
        knight_moves = [
            ("c", 6), ("e", 6),
            ("b", 5), ("f", 5),
            ("b", 3), ("f", 3),
            ("c", 2), ("e", 2),
        ]

        highlights = VGroup()
        for move in knight_moves:
            sq = board.squares_dict.get(move)
            if sq:
                highlight = Square(side_length=board.square_size)
                highlight.move_to(sq.get_center())
                highlight.set_stroke(YELLOW, width=4)
                highlight.set_fill(YELLOW, opacity=0.5)
                highlights.add(highlight)

        self.play(LaggedStartMap(FadeIn, highlights, lag_ratio=0.15))
        self.wait(2)
