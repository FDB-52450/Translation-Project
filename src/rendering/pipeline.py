from pathlib import Path
import cv2

from src.models.processing import Page

from src.rendering.cleaner import clean_old_text
from src.rendering.renderer import render_translated_text #, detect_bubble_bbox
from src.utils.image_utils import load_bgr_image


def render_page_text(page: Page):
    bgr_image = load_bgr_image(page.image_path)
    rendered = bgr_image.copy()

    for text_block in page.text_blocks:
        rendered = clean_old_text(rendered, text_block)
        rendered = render_translated_text(rendered, text_block)

    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"page_{page.id}.png"

    cv2.imwrite(str(output_path), rendered)

    return output_path


def render_pages_text(pages: list[Page]):
    output_paths = []

    for page in pages:
        output_paths.append(render_page_text(page))

    return output_paths