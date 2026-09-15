import cv2
import numpy as np

from src.models.processing import LineBlock, TextBlock


def build_text_mask(image_shape, line_block: LineBlock):
    height, width = image_shape[:2]

    left = int(line_block.center_x - line_block.width / 2)
    top = int(line_block.center_y - line_block.height / 2)
    right = int(line_block.center_x + line_block.width / 2)
    bottom = int(line_block.center_y + line_block.height / 2)

    left = max(0, min(left, width - 1))
    top = max(0, min(top, height - 1))
    right = max(0, min(right, width))
    bottom = max(0, min(bottom, height))

    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.rectangle(mask, (left, top), (right, bottom), 255, thickness=-1)
    return mask


def clean_line_block(image, line_block: LineBlock):
    height, width = image.shape[:2]

    left = int(line_block.center_x - line_block.width / 2)
    top = int(line_block.center_y - line_block.height / 2)
    right = int(line_block.center_x + line_block.width / 2)
    bottom = int(line_block.center_y + line_block.height / 2)

    left = max(0, min(left, width - 1))
    top = max(0, min(top, height - 1))
    right = max(0, min(right, width))
    bottom = max(0, min(bottom, height))

    if right <= left or bottom <= top:
        return image

    cleaned = image.copy()
    cv2.rectangle(cleaned, (left, top), (right, bottom), (255, 255, 255), thickness=-1)
    return cleaned


def clean_old_text(image, text_block: TextBlock):
    cleaned = image.copy()

    for line_block in text_block.line_blocks:
        cleaned = clean_line_block(cleaned, line_block)

    return cleaned

## Estos metodos utilizar la bbox de la burbuja de texto para limpiar el texto,
## dejo de utilizarse debido a malos resultos cuando la burbuja de texto es circular

'''def build_text_mask_from_block(bubble_bbox, text_block: TextBlock):
    """
    Build a binary mask for the original text area inside the bubble.

    Parameters:
        bubble_bbox: (x, y, w, h) in image coordinates
        text_block: TextBlock instance

    Returns:
        mask: 2D uint8 mask where text pixels are 255
    """
    bx, by, bw, bh = map(int, bubble_bbox)

    left = int(text_block.center_x - text_block.width / 2)
    top = int(text_block.center_y - text_block.height / 2)
    right = int(text_block.center_x + text_block.width / 2)
    bottom = int(text_block.center_y + text_block.height / 2)

    mask = np.zeros((bh, bw), dtype=np.uint8)

    x1 = max(0, left - bx)
    y1 = max(0, top - by)
    x2 = min(bw, right - bx)
    y2 = min(bh, bottom - by)

    if x2 <= x1 or y2 <= y1:
        return mask

    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, thickness=-1)

    return mask


def clean_old_text_in_bubble(image, bubble_bbox, text_block: TextBlock | None = None, inpaint_radius=3):
    """
    Remove old text inside a bubble and reconstruct the underlying background.

    Parameters:
        image: BGR numpy array
        bubble_bbox: (x, y, w, h) of the bubble region
        text_block: TextBlock representing the original text area inside the bubble
        inpaint_radius: radius used by OpenCV inpaint

    Returns:
        cleaned_image: image with old text removed from the bubble area
    """
    x, y, w, h = map(int, bubble_bbox)

    if text_block is None:
        return image

    bubble_crop = image[y:y + h, x:x + w].copy()
    mask = build_text_mask_from_block((x, y, w, h), text_block)

    if cv2.countNonZero(mask) == 0:
        return image

    cleaned_crop = cv2.inpaint(bubble_crop, mask, inpaint_radius, cv2.INPAINT_TELEA)
    image[y:y + h, x:x + w] = cleaned_crop
    return image'''
