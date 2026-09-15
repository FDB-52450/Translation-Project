# Este archivo tendra como objetivo posicionar el texto obtenido por el LLM en la copia de la imagen original, 
# para que se vea como si fuera parte de la imagen original.

import cv2

from src.models.processing import TextBlock

## Estos metodos utilizan un metodo en base a detectar bbox de las burbujas que contienen el texto,
## dejo de utilizarse debido a falta de consistencia

'''def detect_bubble_bbox(image, text_block: TextBlock, padding = 30):
    """
    image: BGR numpy array
    text_block: TextBlock from src.models.processing
    padding: extra margin around the original text box

    Returns:
        (x, y, w, h) for the detected speech bubble.
        If detection fails, returns the original text box area.
    """

    # Convert TextBlock -> original text bbox
    x = text_block.center_x - text_block.width / 2
    y = text_block.center_y - text_block.height / 2
    w = text_block.width
    h = text_block.height

    original_box = (int(x), int(y), int(w), int(h))

    h_img, w_img = image.shape[:2]

    x0 = max(0, int(x) - padding)
    y0 = max(0, int(y) - padding)
    x1 = min(w_img, int(x) + int(w) + padding)
    y1 = min(h_img, int(y) + int(h) + padding)

    crop = image[y0:y1, x0:x1]

    if crop.size == 0:
        return original_box

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 1) Try contour detection around the text
    edges = cv2.Canny(blur, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        text_cx = (x1 - x0) / 2
        text_cy = (y1 - y0) / 2

        best_contour = None
        best_score = None

        for c in contours:
            area = cv2.contourArea(c)
            if area < 200:
                continue

            bx, by, bw, bh = cv2.boundingRect(c)
            cx = bx + bw / 2
            cy = by + bh / 2

            score = area - 0.5 * abs(cx - text_cx) - 0.5 * abs(cy - text_cy)

            if best_score is None or score > best_score:
                best_contour = c
                best_score = score

        if best_contour is not None:
            bx, by, bw, bh = cv2.boundingRect(best_contour)
            return (x0 + bx, y0 + by, bw, bh)

    # 2) Fallback: threshold-based detection
    _, mask = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        bubble = max(contours, key=cv2.contourArea)
        bx, by, bw, bh = cv2.boundingRect(bubble)

        return (x0 + bx, y0 + by, bw, bh)

    # 3) Final fallback: original text box
    return original_box


def render_translated_text(image, text_block: TextBlock, font_scale=1.0, color=(0, 0, 0), thickness=2):
    """
    Render the translated text inside the bubble area for a TextBlock.
    Uses the original text block geometry as the anchor for placement.
    """
    bubble_bbox = detect_bubble_bbox(image, text_block)
    x, y, w, h = map(int, bubble_bbox)

    translated = text_block.translated_text or text_block.original_text
    if not translated:
        return image

    # Keep text inside bubble bounds and use the original area as anchor
    text_x = int(text_block.center_x - text_block.width / 2)
    text_y = int(text_block.center_y - text_block.height / 2)
    text_x = max(x + 10, min(text_x, x + w - 10))
    text_y = max(y + 10, min(text_y, y + h - 10))

    # Compute a font scale that fits the text inside the bubble
    max_line_width = w - 20
    max_text_height = h - 20
    working_scale = max(0.4, font_scale)
    lines = [translated]

    while working_scale >= 0.35:
        wrapped = []
        current = ""
        for word in translated.split():
            candidate = f"{current} {word}".strip()
            candidate_w = cv2.getTextSize(candidate, cv2.FONT_HERSHEY_SIMPLEX, working_scale, thickness)[0][0]
            if candidate_w > max_line_width and current:
                wrapped.append(current)
                current = word
            else:
                current = candidate
        if current:
            wrapped.append(current)

        if not wrapped:
            break

        line_height = int(25 * working_scale)
        text_h_est = len(wrapped) * line_height
        widest = max(cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, working_scale, thickness)[0][0] for line in wrapped)

        if widest <= max_line_width and text_h_est <= max_text_height:
            lines = wrapped
            break

        working_scale -= 0.05

    if not lines:
        lines = [translated]

    for i, line in enumerate(lines):
        line_x = text_x
        line_y = text_y + i * int(25 * working_scale)
        cv2.putText(
            image,
            line,
            (line_x, line_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            working_scale,
            color,
            thickness,
            cv2.LINE_AA,
        )

    return image'''

'''def render_translated_text(image, text_block: TextBlock):
    max_width = text_block.width * 1.25
    max_height = text_block.height * 1.25

    cv2.putText(
        image,
        text_block.translated_text,
        (int(text_block.center_x), int(text_block.center_y)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        image,
        text_block.translated_text,
        (int(text_block.center_x), int(text_block.center_y)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 0, 0),
        1,
        cv2.LINE_AA
    )

    return image'''

import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_translated_text(
    image, text_block: TextBlock, font_path='fonts/AnimeAce2.ttf',
    max_font_size = 100, min_font_size = 10, padding = 10,
    fill = (0, 0, 0), stroke_width = 2, stroke_fill = (255, 255, 255),
):
    text = text_block.translated_text

    if text is None:
        print(text_block)

    # Convert OpenCV BGR -> Pillow RGB
    pil_image = Image.fromarray(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    )
    draw = ImageDraw.Draw(pil_image)

    max_width = text_block.width * 1.25 - 2 * padding
    max_height = text_block.height * 1.25 - 2 * padding

    # Try progressively smaller fonts
    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = ImageFont.truetype(font_path, font_size)

        # Word wrapping based on actual rendered width
        lines = []
        current_line = ""

        for word in text.split():
            candidate = (
                word
                if not current_line
                else current_line + " " + word
            )

            bbox = draw.textbbox(
                (0, 0),
                candidate,
                font=font,
                stroke_width=stroke_width,
            )

            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)

                # Handle words that are themselves too long
                current_line = word

        if current_line:
            lines.append(current_line)

        # Measure the entire block
        spacing = int(font_size * 0.15)

        bbox = draw.multiline_textbbox(
            (0, 0),
            "\n".join(lines),
            font=font,
            spacing=spacing,
            stroke_width=stroke_width,
        )

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width <= max_width and text_height <= max_height:
            break
    else:
        # Couldn't fit even at min_font_size
        font = ImageFont.truetype(font_path, min_font_size)
        spacing = int(min_font_size * 0.15)

    # Center the text block in the bounding box

    draw.multiline_text(
        (text_block.center_x, text_block.center_y),
        "\n".join(lines),
        font=font,
        fill=fill,
        anchor="mm",
        align="center",
        spacing=spacing,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )

    # Convert Pillow RGB -> OpenCV BGR
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)