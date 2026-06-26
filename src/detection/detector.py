# Este archivo tendra como objetivo detectar el texto presente en las imagenes, utilizando un modelo de OCR
# y devolviendo los resultados sin procesar

from pathlib import WindowsPath
from paddleocr import PaddleOCR

def detect_text(ocr: PaddleOCR, image_path: WindowsPath):
    raw_results = ocr.predict(str(image_path))
    
    return raw_results