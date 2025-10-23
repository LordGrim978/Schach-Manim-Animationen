from manim import *
from common.board import ChessBoard, SquareIndex
from common.piece import PieceType, PieceColor, get_piece_mobject
from common import piece

class MaterialCounter(Mobject):
    counter: Text
    tracker: ValueTracker

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = Square().set_fill(WHITE, opacity=1).round_corners(0.2).shift(RIGHT * 4)
        self.tracker = ValueTracker(0)
        self.counter = always_redraw(lambda: Text(str(self.tracker.get_value())).move_to(box.center()).set_fill(BLACK))

        self.add(box, self.counter)

class CountMaterial(Scene):
    board: ChessBoard
    material_counter: MaterialCounter
    scale_factor: float = 0.75
    all_pieces_group: VGroup = VGroup()

    def construct(self):
        self.board = ChessBoard()
        self.board.scale(self.scale_factor)
        self.board.shift(LEFT * 4)

        self.material_counter = MaterialCounter()

        self.play(FadeIn(self.board), FadeIn(self.material_counter))
        self.place_many_pieces(piece.get_piece_list_from_fen("1kq4r/3P4/3p4/8/2b5/2p5/2N5/R2QR1K1 b - - 0 1"))
        self.wait(1)
        self.count_pieces()
        self.wait(1)
    
    def get_placed_piece_mobject(self, square: SquareIndex, piece_type: PieceType, piece_color: PieceColor):
        def get_piece_value(piece_type: PieceType, piece_color: PieceColor):
            PIECE_TYPE_TO_VALUE_MAP = {
                PieceType.KING: 0,
                PieceType.PAWN: 1,
                PieceType.KNIGHT: 3,
                PieceType.BISHOP: 3,
                PieceType.ROOK: 5,
                PieceType.QUEEN: 9,
            }
            value = PIECE_TYPE_TO_VALUE_MAP[piece_type]
            return value if piece_color == PieceColor.LIGHT else -value
        piece = get_piece_mobject(piece_type, piece_color)
        piece._value = get_piece_value(piece_type, piece_color)
        piece.set_height(self.board.square_size * 0.8 * self.scale_factor)
        piece.move_to(self.board.get_square_position(square))
        self.all_pieces_group.add(piece)
        return piece
    
    def place_many_pieces(self, piece_list: list[tuple[SquareIndex, PieceType, PieceColor]]):
        animations = [FadeIn(self.get_placed_piece_mobject(square, piece_type, piece_color))
            for (square, piece_type, piece_color) in piece_list]
        self.play(LaggedStart(*animations))
    
    def count_pieces(self):
        def generate_animation(piece):
            target = self.material_counter.get_left()
            piece._counted = False

            def update_func(mob, alpha):
                mob.move_to(mob.get_center() + alpha * (target - mob.get_center()))
                opacity = 1 - min(alpha * 1.25, 1)
                mob.set_opacity(opacity)

                if alpha > 0.5 and not getattr(mob, "_counted", False):
                    mob._counted = True
                    self.material_counter.tracker.set_value(
                        self.material_counter.tracker.get_value() + piece._value
                    )


            return UpdateFromAlphaFunc(piece, update_func, run_time=1)
        
        animations = [generate_animation(piece) for piece in self.all_pieces_group]
        self.play(LaggedStart(*animations, lag_ratio=0.5))
