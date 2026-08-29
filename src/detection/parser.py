# Este archivo transforma los datos de una sola pagina obtenidos por OCR
# en los modelos usados por el resto de la aplicacion.

from src.models.detection import OCRLine, OCRPage

def parse_page(raw_page) -> OCRPage:
    texts = raw_page.get("rec_texts", [])
    scores = raw_page.get("rec_scores", [])
    polygons = raw_page.get("rec_polys", [])

    lines = [
        OCRLine(
            text = text,
            bbox = polygon.tolist() if hasattr(polygon, "tolist") else polygon,
            confidence = float(score),
        ) 
        for text, score, polygon in zip(texts, scores, polygons)
    ]

    return OCRPage(1, lines = lines)