from manim import *

from common.board import ChessBoard, SquareIndex, RANKS, FILES
from common.piece import get_piece_list_from_fen, get_piece_mobject, PieceType

def read_file_to_string(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()

class PieceSquareTableMobject(Mobject):
    """
    The Mobject for visualizing a piece square table. Please not that only
    values between -50 and 50 are supported
    """
    square_size: float
    squares_dict: dict[SquareIndex, Square]
    data: dict[SquareIndex, int]

    def __init__(self, psqt: str, **kwargs):
        super().__init__(**kwargs)
        squares = VGroup()

        board_size = 6
        square_size = board_size / 8

        self.square_size = square_size
        self.squares_dict = {}
        self.data = self.parse_psqt(psqt)

        for rank_index, rank in enumerate(RANKS):
            for file_index, file in enumerate(FILES):
                color = BLUE_D
                opacity = ((self.data[file, rank] / 100) + 0.5) * 0.75 + 0.25
                sq = Square(side_length=square_size)
                sq.set_fill(color, opacity).set_stroke(BLACK, width=0.5)

                x = (file_index - 3.5) * square_size
                y = (rank_index - 3.5) * square_size
                sq.move_to([x, y, 0])

                squares.add(sq)
                self.squares_dict[(file, rank)] = sq

                value = str(self.data[file, rank] / 100)
                if not value.startswith("-"):
                    value = f"+{value}"
                value = Text(value)
                value.move_to(sq.get_center())
                value.scale(0.35)
                sq.add(value)
        self.add(squares)

    def parse_psqt(self, string: str, invert: bool = False) -> dict[SquareIndex, int]:
        ranks = RANKS if invert else reversed(RANKS)
        files = FILES
        psqt = {}
        lines = string.splitlines()
        for (line, rank) in zip(lines, ranks):
            values = line.split(",")
            for (value, file) in zip(values, files):
                psqt[(file, rank)] = int(value)
        return psqt


class PieceSquareTable(Scene):
    board: ChessBoard
    psqt: PieceSquareTableMobject
    piece_map: dict[SquareIndex, SVGMobject]


    def construct(self):
        self.piece_map = {}

        self.next_section("place pieces and highlight knights")
        self.board = ChessBoard()

        self.play(FadeIn(self.board))
        animations = self.place_pieces("r1b1k2r/3p1pbp/1pp2qpn/p7/2Q1P3/P1NBB3/1PP2PPP/R4RK")
        self.play(LaggedStart(animations, lag_ratio=0.05))
        
        self.play(self.board.highlight_square(("c", 3), GREEN), self.board.highlight_square(("h", 6), RED))
        # self.wait(10) # uncomment for final render

        HIGHLIGHT_SQUARES_GREEN = [("a", 2), ("a", 4), ("b", 1), ("b", 5), ("d", 1), ("d", 5), ("e", 2)]
        self.play(LaggedStart([self.board.highlight_square(square, GREEN) for square in HIGHLIGHT_SQUARES_GREEN], lag_ratio=0.15))
        # self.wait(3) # uncomment for final render
        HIGHLIGHT_SQUARES_RED = [("g", 8), ("g", 4), ("f", 5)]
        self.play(LaggedStart([self.board.highlight_square(square, RED) for square in HIGHLIGHT_SQUARES_RED], lag_ratio=0.15))
        

        self.next_section("setup piece square table")
        hide_pieces = [FadeOut(self.piece_map[key]) for key in self.piece_map if key != ("c", 3)]
        hide_highlights = self.board.unhighlight_all()
        self.play(LaggedStart(hide_pieces, lag_ratio=0.05), LaggedStart(hide_highlights, lag_ratio=0.05))

        self.psqt = PieceSquareTableMobject(read_file_to_string("psqt/knight.txt"))
        self.play(Transform(self.board, self.psqt))
        self.wait()

    def place_pieces(self, fen: str) -> list[Animation]:
        piece_list: list[tuple[SquareIndex, PieceType, PieceColor]] = (
            get_piece_list_from_fen(fen)
        )
        piece_list: list[tuple[SVGMobject, SquareIndex]] = [
            (get_piece_mobject(piece_type, piece_color), index, piece_type)
            for (index, piece_type, piece_color) in piece_list
        ]

        def setup_piece_mobject(
            mobject: SVGMobject, piece_type: PieceType, square: SquareIndex
        ) -> SVGMobject:
            scale = 0.70 if piece_type == PieceType.PAWN else 0.75
            self.piece_map[square] = mobject.set_height(self.board.square_size * scale).move_to(
                self.board.get_square_position(square)
            )
            return self.piece_map[square]

        piece_list: list[Mobject] = [
            setup_piece_mobject(mobject, piece_type, square)
            for (mobject, square, piece_type) in piece_list
        ]
        animations = [FadeIn(piece, scale=0.5) for piece in piece_list]
        return animations
