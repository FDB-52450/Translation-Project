import os
import time
import json

from src.utils.image_utils import find_images

from src.processing.pipeline import process_page, process_pages
from src.detection.pipeline import detect_page, detect_pages
from src.translation.translator import translate_page, translate_pages
from src.rendering.pipeline import render_page_text, render_pages_text

from src.models.processing import Page

def write_to_file(processed_pages: list[Page]):
    data = []

    for proc_page in processed_pages:
        blocks = []

        for num, block in enumerate(proc_page.text_blocks):
            blocks.append({
                'id': num + 1,
                'text': block.original_text.strip()
            })

        data.append({
            'id': proc_page.id,
            'blocks': blocks
        })

    with open("data/temp/output.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    
def get_page_translation(image_path):
    print("DETECTING PAGE...")
    raw_page = detect_page(image_path)

    print("PROCESSING PAGE...")
    processed_page = process_page(raw_page)

    print(f"PAGE: {processed_page.id}")

    for block in processed_page.text_blocks:
        print(f"BLOCK: {block.original_text} - X: {block.center_x} Y: {block.center_y} W: {block.width} H: {block.height}")

    print("TRANSLATING PAGE...")
    translated_page = translate_page(processed_page, 'English', 'Spanish')

    print("CREATING TRANSLATED IMAGE...")
    image_path = render_page_text(translated_page)

    print("IMAGE CREATED!")

def get_pages_translatinos(images_path):
    print("DETECTING PAGES...")

    start_time = time.time()
    raw_pages = detect_pages(images_path)

    os.system("cls")
    print(f"PAGES DETECTED SUCCESFULLY [TIME TAKEN: {round(time.time() - start_time, 3)} seconds]")
    print("-----------------------------")
    print("PROCESSING PAGES...")

    start_time = time.time()
    processed_pages = process_pages(raw_pages)
    write_to_file(processed_pages)

    os.system("cls")
    print(f"PAGES PROCESSED SUCCESFULLY [TIME TAKEN: {round(time.time() - start_time, 3)} seconds]")
    print("-----------------------------")
    print("PAGE CONTENTS WRITTEN TO FILE - SELECT WHICH BLOCKS YOU WISH TO SKIP [FORMAT: page.block]")

    blocks_to_remove = input("BLOCKS [PRESS ENTER TO SKIP]: ")

    if blocks_to_remove != '':
        blocks_to_remove = blocks_to_remove.split(',')
        removals = []

        for block_remove in blocks_to_remove:
            page, block = map(int, block_remove.strip().split('.'))
            removals.append((page, block))

        for page, block in sorted(removals, reverse=True):
            processed_pages[page - 1].text_blocks.pop(block - 1)

    print("TRANSLATING PAGES...")
    
    start_time = time.time()
    translated_pages = translate_pages(processed_pages, 'English', 'Spanish')

    os.system("cls")
    print(f"PAGES TRANSLATED SUCCESFULLY [TIME TAKEN: {round(time.time() - start_time, 3)} seconds]")
    print("-----------------------------")
    print("RENDERING PAGES...")

    start_time = time.time()
    tl_images_paths = render_pages_text(translated_pages)

    os.system("cls")
    print(f"PAGES RENDERED SUCCESFULLY [TIME TAKEN: {round(time.time() - start_time, 3)} seconds]")
    print("-----------------------------")
    print("PAGES SAVED AT: data/output ")
    


def main():
    image_paths = find_images('data/input')
    #image_path = image_paths[3]

    #get_page_translation(image_path)

    get_pages_translatinos(image_paths)



if __name__ == '__main__':
    main()





