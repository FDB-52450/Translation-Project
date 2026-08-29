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
class OCRPage:
    id: int
    lines: list[OCRLine]