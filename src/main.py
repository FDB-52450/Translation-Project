from src.utils.image_utils import find_images

from src.processing.pipeline import process_page
from src.detection.pipeline import detect_page
from src.translation.translator import translate_page

def get_page_translation(image_path):
    print("DETECTING PAGE...")
    raw_page = detect_page(image_path)

    print("PROCESSING PAGE...")
    processed_page = process_page(raw_page)

    print("TRANSLATING PAGE...")

    return translate_page(processed_page, 'English', 'Spanish')

def main():
    image_paths = find_images('data/input')
    image_path = image_paths[2]

    translated_page = get_page_translation(image_path)

    for txtBlock in translated_page.text_blocks:
        print(f"OG TEXT: {txtBlock.original_text} - TL TEXT: {txtBlock.translated_text}")

if __name__ == '__main__':
    main()





