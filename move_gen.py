from manim import *

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = list(range(1, 9))


class ChessBoard(Mobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        board_size = 6
        square_size = board_size / 8
        self.square_size = square_size
        self.squares_dict = {}

        squares = VGroup()
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


def knight_moves_from(square):
    file, rank = square
    file_idx = FILES.index(file)
    deltas = [(2, 1), (2, -1), (-2, 1), (-2, -1),
              (1, 2), (1, -2), (-1, 2), (-1, -2)]
    moves = []
    for dx, dy in deltas:
        f_idx = file_idx + dx
        r = rank + dy
        if 0 <= f_idx < 8 and 1 <= r <= 8:
            moves.append((FILES[f_idx], r))
    return moves


class KnightMovesScroll(Scene):
    def construct(self):
        # --- Setup chessboard
        board = ChessBoard()
        board.to_edge(LEFT, buff=1.2)
        self.add(board)

        # --- Knight position
        current_square = ("d", 4)
        knight = SVGMobject("knight.svg")
        knight.set_height(board.square_size * 0.8)
        knight.move_to(board.squares_dict[current_square].get_center())
        self.add(knight)

        # --- Build list of all knight move strings
        all_squares = [(f, r) for f in FILES for r in RANKS]
        move_lines = []
        for sq in all_squares:
            moves = knight_moves_from(sq)
            move_text = f"{sq[0]}{sq[1]} → " + ", ".join(f"{f}{r}" for f, r in moves)
            move_lines.append(move_text)

        # --- Add text lines and scroll window setup
        text_items = VGroup(*[
            Text(line, font_size=20, font="Consolas")
            for line in move_lines
        ])
        text_items.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        text_items.to_edge(RIGHT, buff=1.2)

        # --- Start the visible area from a1
        a1_index = all_squares.index(("a", 1))
        a1_text = text_items[a1_index]
        # Shift so that a1 appears near the top visible region
        text_items.shift(DOWN * (a1_text.get_center()[1] + 3))

        self.add(text_items)

        # --- Add black overlay boxes (fade masks)
        fade_width = 6.1  # slightly wider than text
        fade_height = 5.7

        top_fade = Rectangle(
            width=fade_width,
            height=fade_height,
            fill_color=BLACK,
            fill_opacity=1.0,
            stroke_width=0,
        )
        bottom_fade = top_fade.copy()

        # Position relative to visible area
        fade_center_x = text_items.get_center()[0]
        top_fade.move_to([fade_center_x, 3.5, 0])
        bottom_fade.move_to([fade_center_x, -3.5, 0])

        # Ensure fades are above everything
        top_fade.z_index = 50
        bottom_fade.z_index = 50
        text_items.z_index = 10

        self.add(top_fade, bottom_fade)  # add them last so they overlay

        # --- Compute scroll offset for smooth stop on knight’s square
        target_index = all_squares.index(current_square)
        target_text = text_items[target_index]
        offset = -target_text.get_center()[1]  # scroll upward until target centered

        # --- Animate continuous scrolling like iOS wheel
        self.play(
            text_items.animate.shift(UP * offset).set_rate_func(rate_functions.ease_in_out_cubic),
            run_time=4
        )



        # --- Highlight target line
        highlight_rect = SurroundingRectangle(target_text, color=YELLOW, buff=0.1)
        self.play(Create(highlight_rect))

        # --- Highlight knight’s moves on the board
        highlights = VGroup()
        for move in knight_moves_from(current_square):
            sq = board.squares_dict.get(move)
            if sq:
                h = Square(side_length=board.square_size)
                h.move_to(sq.get_center())
                h.set_fill(RED, opacity=0.4).set_stroke(width=0)
                highlights.add(h)
        self.play(FadeIn(highlights))
        self.wait(2)
