from dataclasses import dataclass

@dataclass
class TranslationContext:
    char_name_list: list[str] | None 
    additional_context: str | None
