import cv2
from pathlib import Path

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"}

def find_images(folder: str | Path) -> list[Path]:
    folder = Path(folder)

    image_paths = sorted(
        path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    return image_paths

def improve_image(imagePath):
    img = cv2.imread(imagePath)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    return img