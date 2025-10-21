from manim import *
from common.board import ChessBoard

class KnightMoves(Scene):
    def construct(self):
        board = ChessBoard()
        # Note that we have to scale everything on the board by the scale factor
        # too in order for it to be the correct size in relation to the size of
        # the board and not too large or small
        BOARD_SCALE = 0.8
        board.scale(BOARD_SCALE)
        self.play(FadeIn(board))

        # The SVG file for the knight should be at images/knight_lt.svg
        knight = SVGMobject("images/knight_lt")
        knight.set_height(board.square_size * 0.8 * BOARD_SCALE)
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
                highlight = Square(side_length=board.square_size * BOARD_SCALE)
                highlight.move_to(sq.get_center())
                highlight.set_stroke(YELLOW, width=4)
                highlight.set_fill(YELLOW, opacity=0.5)
                highlights.add(highlight)

        self.play(LaggedStartMap(FadeIn, highlights, lag_ratio=0.15))
        self.wait(2)
