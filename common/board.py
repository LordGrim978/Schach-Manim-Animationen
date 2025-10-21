from manim import *

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = list(range(1, 9))

class ChessBoard(Mobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        squares = VGroup()

        board_size = 6
        square_size = board_size / 8

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
        self.add(squares)
