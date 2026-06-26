import os

from src.detection.detector import detect_text
from src.processing.cleanup import normalize_results
from src.utils.image_utils import find_images
from detection.ocr import get_ocr

def translate_image(ocr, image_path):
    raw_results = detect_text(ocr, image_path)
    normalized_results = normalize_results(raw_results)

    for page in normalized_results:
        texts = page.get("rec_texts", [])
        scores = page.get("rec_scores", [])
        polys = page.get("rec_polys", [])

        for j, (text, score, poly) in enumerate(zip(texts, scores, polys), start=1):
            print(f"Line {j}:")
            print(f"  Text : {text}")
            print(f"  Score: {score:.3f}")
            print(f"  Poly : {poly.tolist()}")
            print()

        print("--" * 40)


def translate_image_batch(ocr, image_paths):
    for image_path in image_paths:
        translate_image(ocr, image_path)


if __name__ == "__main__":
    ocr = get_ocr()
    image_paths = find_images('data/input')

    os.system("cls")

    if not image_paths or len(image_paths) == 0:
        print("No images found in the specified folder.")
        exit(1)
        
    mode = input("Select mode [1: Single Image, 2: Batch Processing]: ")

    os.system("cls")

    if mode == "2":
        translate_image_batch(ocr, image_paths)

    elif mode == "1":
        if len(image_paths) == 1:
            image_path = image_paths[1]

            translate_image(ocr, image_path)
        else:
            print("Multiple images found. Select one image to process:")

            x = 1

            for image_path in image_paths:
                print(f"Image {x}: {str(image_path).replace('data/input/', '')}")
                x += 1
            
            image_index = int(input("Enter the image number to process: ")) - 1

            os.system("cls")

            if 0 <= image_index < len(image_paths):
                selected_image_path = image_paths[image_index]
                
                translate_image(ocr, selected_image_path)
            else:
                print("Invalid image number selected.")
    else:
        print("Invalid mode selected. Please choose either 1 or 2.")
