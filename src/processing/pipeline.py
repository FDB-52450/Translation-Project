from src.models.detection import OCRPage
from src.models.processing import Page, NormalizedLine

from src.processing.cleanup import convert_page_to_normalized_lines, clean_lines
from src.processing.structure import group_lines_into_blocks, group_blocks_into_text_blocks

def process_page(page: OCRPage) -> Page:
    normalized_lines: list[NormalizedLine] = convert_page_to_normalized_lines(page)
    clean_normalized_lines: list[NormalizedLine] = clean_lines(normalized_lines)

    line_blocks = group_lines_into_blocks(clean_normalized_lines)
    text_blocks = group_blocks_into_text_blocks(line_blocks)

    return Page(page.id, text_blocks)


def process_pages(pages: list[OCRPage]) -> list[Page]:
    processed_pages: list[Page] = []

    for page in pages:
        processed_page = process_page(page)
        processed_pages.append(processed_page)

    return processed_pages