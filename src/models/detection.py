from dataclasses import dataclass
from typing import List
import numpy as np

## CLASES DE DETECCION DE TEXTO

@dataclass
class OCRLine:
    text: str
    bbox: List[List[np.float32]]
    confidence: float

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
    lines: List[NormalizedLine]
    center_x: float
    center_y: float
    width: float
    height: float
    rotation: float
    confidence: float