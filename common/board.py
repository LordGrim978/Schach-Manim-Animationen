from manim import *

from typing import TypeAlias

SquareIndex: TypeAlias = tuple[str, int]

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = list(range(1, 9))

class ChessBoard(Mobject):
    square_size: float
    squares_dict: dict[SquareIndex, Square]
    highlight_dict: dict[SquareIndex, Square]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        squares = VGroup()

        board_size = 6
        square_size = board_size / 8

        self.square_size = square_size
        self.squares_dict = {}
        self.highlight_dict = {}

        for rank_index, rank in enumerate(RANKS):
            for file_index, file in enumerate(FILES):
                is_light = (file_index + rank_index) % 2 == 1
                color = "#f0d9b5" if is_light else "#b58863"

                sq = Square(side_length=square_size)
                sq.set_fill(color, opacity=1).set_stroke(BLACK, width=0.5)

                x = (file_index - 3.5) * square_size
                y = (rank_index - 3.5) * square_size
                sq.move_to([x, y, 0])

                squares.add(sq)
                self.squares_dict[(file, rank)] = sq
        self.add(squares)
    
    def get_square_position(self, square_index: SquareIndex) -> Point:
        square = self.squares_dict.get(square_index)
        if not square:
            raise Exception(f"Attempted to select invalid square: `{square_index}`")
        return square.get_center()
    
    def highlight_square(self, square: SquareIndex, highlight_color: ManimColor, board_scale: float = 1.0) -> Animation:
        highlight = Square(side_length=self.square_size * board_scale)
        highlight.move_to(self.get_square_position(square))
        highlight.set_stroke(highlight_color, width=4)
        highlight.set_fill(highlight_color, opacity=0.25)
        self.highlight_dict[square] = highlight
        return FadeIn(highlight)
    
    def unhighlight_square(self, square: SquareIndex, board_scale: float = 1.0, do_not_delete: bool = False) -> Animation:
        highlight = self.highlight_dict.get(square)
        if not highlight:
            raise Exception(f"Unable to unhighlight square {square}: There was no highlight")
        if not do_not_delete:
            del self.highlight_dict[square]
        return FadeOut(highlight)
    
    def unhighlight_all(self, board_scale: float = 1.0) -> list[Animation]:
        animations = [self.unhighlight_square(square, board_scale, do_not_delete=True) for square in self.highlight_dict]
        self.highlight_dict = {}
        return animations
