from manim import *

from enum import Enum
from .board import SquareIndex

class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

LETTER_TO_TYPE_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "n": PieceType.KNIGHT,
    "b": PieceType.BISHOP,
    "r": PieceType.ROOK,
    "q": PieceType.QUEEN,
    "k": PieceType.KING
}

TYPE_TO_NAME_MAP: dict[PieceType, str] = {
    PieceType.PAWN: "pawn",
    PieceType.KNIGHT: "knight",
    PieceType.BISHOP: "bishop",
    PieceType.ROOK: "rook",
    PieceType.QUEEN: "queen",
    PieceType.KING: "king"
}

class PieceColor(Enum):
    LIGHT = 0
    DARK = 1

COLOR_TO_LETTER_MAP: dict[PieceColor, str] = {
    PieceColor.LIGHT: "l",
    PieceColor.DARK: "d"
}

def get_piece_mobject(piece_type: PieceType, piece_color: PieceColor) -> SVGMobject:
    piece_name = TYPE_TO_NAME_MAP[piece_type]
    piece_color_string = COLOR_TO_LETTER_MAP[piece_color]
    svg_path = f"images/{piece_name}_{piece_color_string}t"

    mobj = SVGMobject(svg_path)

    # Force correct base colors
    if piece_color == PieceColor.DARK:
        # All dark pieces should be solid black with white highlights on top
        for sub in mobj.submobjects:
            sub.set_fill(color=BLACK, opacity=1)
            if sub.get_stroke_color() == WHITE:
                sub.set_z_index(2)  # ensure highlight is above the fill
            else:
                sub.set_stroke(color=BLACK, opacity=1)
                sub.set_z_index(1)
    else:
        for sub in mobj.submobjects:
            sub.set_fill(color=WHITE, opacity=1)
            if sub.get_stroke_color() == BLACK:
                sub.set_z_index(2)
            else:
                sub.set_stroke(color=WHITE, opacity=1)
                sub.set_z_index(1)

    mobj.suspend_updating()
    return mobj


def get_piece_list_from_fen(fen: str) -> list[tuple[SquareIndex, PieceType, PieceColor]]:
    rank: int = 8
    file: int = 1 # 1 is the A file
    FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
    index: int = 0
    result: list[tuple[SquareIndex, PieceType, PieceColor]] = []
    while index < len(fen):
        char: str = fen[index]
        if char.isalpha():
            piece_color: PieceColor = PieceColor.LIGHT if char.upper() == char else PieceColor.DARK
            piece_type: PieceType = LETTER_TO_TYPE_MAP[char.lower()]
            result.append(((FILE_NAMES[file - 1], rank), piece_type, piece_color))
            file += 1
        elif char == "/":
            file = 1
            rank -= 1
        elif char == " ":
            # Space is between position and other info (castle rights, etc.)
            break
        else:
            file += int(char)
        index += 1
        if rank < 1:
            break
    return result
