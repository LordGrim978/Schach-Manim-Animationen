from manim import *

from common.board import ChessBoard, SquareIndex
from common.piece import get_piece_list_from_fen, get_piece_mobject, PieceType


class PieceSquareTable(Scene):
    board: ChessBoard

    def construct(self):
        self.next_section("place pieces and highlight knights")
        self.board = ChessBoard()

        self.play(FadeIn(self.board))
        animations = self.place_pieces(
            "r1b1k2r/3p1pbp/1pp2qpn/p7/2Q1P3/P1NBB3/1PP2PPP/R4RK"
        )
        self.play(LaggedStart(animations, lag_ratio=0.05))
        
        self.play(self.board.highlight_square(("c", 3), GREEN), self.board.highlight_square(("h", 6), RED))
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
            return mobject.set_height(self.board.square_size * scale).move_to(
                self.board.get_square_position(square)
            )

        piece_list: list[Mobject] = [
            setup_piece_mobject(mobject, piece_type, square)
            for (mobject, square, piece_type) in piece_list
        ]
        animations = [FadeIn(piece, scale=0.5) for piece in piece_list]
        return animations
