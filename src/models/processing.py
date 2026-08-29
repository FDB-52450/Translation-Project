from statistics import median

from dataclasses import dataclass
from math import atan2, degrees, hypot

@dataclass
class NormalizedLine:
    text: str
    center_x: float
    center_y: float
    width: float
    height: float
    rotation: float
    confidence: float


@dataclass
class LineBlock:
    lines: list[NormalizedLine]

    @property
    def text(self) -> str:
        return " ".join(line.text for line in self.lines)

    @property
    def center_x(self) -> float:
        left = min(line.center_x - line.width / 2 for line in self.lines)
        right = max(line.center_x + line.width / 2 for line in self.lines)

        return (left + right) / 2

    @property
    def center_y(self) -> float:
        top = min(line.center_y - line.height / 2 for line in self.lines)
        bottom = max(line.center_y + line.height / 2 for line in self.lines)

        return (top + bottom) / 2

    @property
    def width(self) -> float:
        left = min(line.center_x - line.width / 2 for line in self.lines)
        right = max(line.center_x + line.width / 2 for line in self.lines)

        return right - left

    @property
    def height(self) -> float:
        top = min(line.center_y - line.height / 2 for line in self.lines)
        bottom = max(line.center_y + line.height / 2 for line in self.lines)

        return bottom - top


@dataclass
class TextBlock:
    line_blocks: list[LineBlock]
    translated_text: str | None = None

    @property
    def original_text(self) -> str:
        return " ".join(
            block.text for block in self.line_blocks
        )

    @property
    def center_x(self) -> float:
        left = min(block.center_x - block.width / 2 for block in self.line_blocks)
        right = max(block.center_x + block.width / 2 for block in self.line_blocks)

        return (left + right) / 2

    @property
    def center_y(self) -> float:
        top = min(block.center_y - block.height / 2 for block in self.line_blocks)
        bottom = max(block.center_y + block.height / 2 for block in self.line_blocks)

        return (top + bottom) / 2

    @property
    def width(self) -> float:
        left = min(block.center_x - block.width / 2 for block in self.line_blocks)
        right = max(block.center_x + block.width / 2 for block in self.line_blocks)

        return right - left

    @property
    def height(self) -> float:
        top = min(block.center_y - block.height / 2 for block in self.line_blocks)
        bottom = max(block.center_y + block.height / 2 for block in self.line_blocks)

        return bottom - top


@dataclass
class Page:
    id: int
    text_blocks: list[TextBlock]
