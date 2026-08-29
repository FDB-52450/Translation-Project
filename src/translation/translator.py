# Este archivo tendra como objetivo enviar el texto limpio y organizado a un modelo de lenguaje para su traducción.

from ollama import chat
from src.models.processing import Page, TextBlock
from src.models.translation import TranslationContext

MODEL = "gemma3:12b-it-qat"
SYSTEM_PROMPT = """
You are a professional translator.

Rules:
- Translate from the source language to the target language.
- Preserve the meaning, tone, and intent.
- Preserve formatting, line breaks, and paragraph structure.
- Do NOT summarize.
- Do NOT explain.
- Do NOT add notes.
- Do NOT translate proper names unless they normally have an established translation.
- Return ONLY the translated text.
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
    Translate every item from {src_lang} to {target_lang}.

    [CRITICAL CONTEXT FOR THIS TRANSLATION]
    {context_str}

    Return exactly one translated item for each input item.
    Do not number them.
    Separate each translation with <SEP>.

    Input:
    <SEP>
    """ + "<SEP>".join(blocks_str)

    response = chat(
        model = MODEL,
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        options = {"temperature": 0},
    )

    translations = response.message.content.split("<SEP>")

    for block, tl_str in zip(page.text_blocks, translations):
        block.translated_text = tl_str

    return page