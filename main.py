from manim import *
from common.board import ChessBoard

class EvaluationFunction(Mobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = Square().set_fill(WHITE, opacity=1).round_corners(0.2)
        text = Text("f()").move_to(box.center()).set_fill(BLACK)

        self.add(box,text)

class MoveBoard(Scene):
    def construct(self):
        board = ChessBoard()

        evFunc = EvaluationFunction()
        self.play(FadeIn(evFunc))

        # First draw it

        board.shift(LEFT*4)
        board.scale(0.7)
        self.play(FadeIn(board, scale=0.5), run_time=1)

        #Transform to Eval
        self.play(Transform(board, Text("+4").move_to(RIGHT*4)),runtime=4)

        self.wait()
