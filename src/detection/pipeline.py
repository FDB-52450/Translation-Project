from src.models.detection import OCRPage

from src.detection.detector import detect_text
from src.detection.parser import parse_page
from src.detection.ocr import get_ocr

from paddleocr import PaddleOCR


def detect_page(image_path: str, ocr: PaddleOCR = None, id: int = 1) -> OCRPage:
    if not ocr:
        ocr = get_ocr()

    raw_results = detect_text(ocr, image_path)
    raw_lines = parse_page(raw_results)

    return OCRPage(id, raw_lines, image_path)


def detect_pages(images_path: list[str]) -> list[OCRPage]:
    ocr = get_ocr()
    raw_pages: list[OCRPage] = []

    for num, img_path in enumerate(images_path):
        raw_page = detect_page(img_path, ocr, num + 1)
        raw_pages.append(raw_page)

    return raw_pages