# Este archivo tendra como objetivo enviar el texto limpio y organizado a un modelo de lenguaje para su traducción.

import json
from ollama import chat

from src.models.processing import Page, TextBlock
from src.models.translation import TranslationContext

MODEL = "gemma3:12b-it-qat"
SYSTEM_PROMPT = """
You are a professional translator.

Rules:
- Translate from the source language to the target language.
- Preserve the meaning, tone, and intent.
- Preserve line breaks INSIDE each input item.
- Do NOT summarize.
- Do NOT explain.
- Do NOT add notes.
- Do NOT translate proper names unless they normally have an established translation.
- Return exactly one translation for every input item.
- Preserve the exact order of the input items.
- Never merge two input items.
- Never omit an input item.
- Never add an item.
- Your response must be a JSON array of strings.
""".strip()


def translate_page(page: Page, src_lang: str, target_lang: str, context: TranslationContext = None) -> Page:
    blocks_str = [tb.original_text for tb in page.text_blocks]
    context_str = ''

    if context:
        context_sections = []

        if context.char_name_list:
            context_sections.append("- Specific Names & Terminology:\n  " + "\n  ".join(f"* {name}" for name in context.char_name_list))
        if context.additional_context:
            context_sections.append(f"- Additional Context:\n  {context.additional_context}")
        
        context_str = "\n".join(context_sections) if context_sections else "None"

    prompt = f"""
    Translate each input from {src_lang} to {target_lang}.

    [CRITICAL CONTEXT FOR THIS TRANSLATION]
    {context_str}

    There are exactly {len(blocks_str)} input items.
    You MUST return exactly {len(blocks_str)} translations.
    Return ONLY a JSON array of strings.

    For example:
    Input 1: "The mission was simple. Find"
    Input 2: "the device."

    Correct output:
    ["La misión era sencilla. Encuentra", "el dispositivo."]

    INCORRECT output:
    ["La misión era sencilla. Encuentra el dispositivo."]

    Inputs:
    """

    for i, block in enumerate(blocks_str):
        prompt += f"\nINPUT {i + 1}:\n{block}\n"

    response = chat(
        model = MODEL,
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        format={
            "type": "array",
            "items": {"type": "string"},
            "minItems": len(blocks_str),
            "maxItems": len(blocks_str)
        },
        options = {"temperature": 0},
    )

    translations = json.loads(response.message.content)

    for block, tl_str in zip(page.text_blocks, translations):
        block.translated_text = tl_str

    return page

def translate_pages(pages: list[Page], src_lang: str, target_lang: str, context: TranslationContext = None) -> list[Page]:
    tl_pages: list[Page] = []

    for page in pages:
        tl_page = translate_page(page, src_lang, target_lang, context)

        print(f"PAGE {page.id} TRANSLATED SUCCESFULLY")
        tl_pages.append(tl_page)

    return tl_pages