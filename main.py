from manim import *

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = list(range(1, 9))

class EvaluationFunction(Mobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = Square().set_fill(WHITE, opacity=1).round_corners(0.2)
        text = Text("f()").move_to(box.center()).set_fill(BLACK)

        self.add(box,text)

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