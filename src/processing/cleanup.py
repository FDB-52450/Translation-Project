# Este archivo tendra como objetivo limpiar el texto obtenido por el OCR, lo que incluye:
# - Eliminar resultados de baja confianza
# - Eliminar caracteres no deseados (como saltos de línea, tabulaciones, etc.)
# - Normalizar tipos np (numpy) a tipos nativos de Python (como convertir np.int64 a int, np.float64 a float, etc.)
# - Convertir el texto a un formato más limpio y estructurado para facilitar su posterior procesamiento por el modelo de lenguaje.

import re
from math import atan2, degrees, hypot

from src.models.detection import OCRPage
from src.models.processing import NormalizedLine

from config import ONOMATOPOEIA_FILTERING

KNOWN_ONOMATOPOEIA = {
	"ah", "aha", "aah", "ahh", "ahhh", "eh", "oh", "ooh", "oooh", "uh",
	"huh", "hmm", "hmmm", "psst", "shh", "bang", "boom", "crash", "pow",
	"zap", "wham", "thud", "clang", "clink", "buzz", "hiss", "splash", "whoosh",
	"swish", "whiz", "zoom", "vroom", "swoosh", "tick", "tock", "ping", "ding",
	"dong", "beep", "boop", "meow", "woof", "moo", "baa", "purr", "mrr",
	"oof", "ugh", "ew", "ow", "ouch", "yay", "yikes", "brr", "phew", "fizz"
}

def convert_page_to_normalized_lines(page: OCRPage) -> list[NormalizedLine]:
	normalized_lines = []

	for line in page.lines:
		top_left, top_right, bottom_right, bottom_left = line.bbox

		center_x = sum(point[0] for point in line.bbox) / len(line.bbox)
		center_y = sum(point[1] for point in line.bbox) / len(line.bbox)
		
		width = hypot(top_right[0] - top_left[0], top_right[1] - top_left[1])
		height = hypot(bottom_left[0] - top_left[0], bottom_left[1] - top_left[1])
		
		rotation = degrees(atan2(top_right[1] - top_left[1], top_right[0] - top_left[0]))

		normalized_lines.append(
			NormalizedLine(
				text = line.text,
				center_x = float(center_x),
				center_y = float(center_y),
				width = float(width),
				height = float(height),
				rotation = float(rotation),
				confidence = round(line.confidence, 2),
			)
		)

	return normalized_lines

def is_onomatopoeia(text: str):
	cleaned = text.strip().lower()
	cleaned = cleaned.replace('!', '')
	
	if re.search(r"(.)\1\1", cleaned):
		return True

	if cleaned in KNOWN_ONOMATOPOEIA:
		return True

	if cleaned.isupper() and " " not in cleaned:
		return True
		
	return False


def clean_lines(lines: list[NormalizedLine]) -> list[NormalizedLine]:
	filtered = [line for line in lines if line.confidence >= 0.75]

	if ONOMATOPOEIA_FILTERING:
		filtered = [line for line in filtered if not is_onomatopoeia(line.text)]

	return filtered
