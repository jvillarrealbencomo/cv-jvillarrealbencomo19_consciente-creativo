"""
Tokenizer utilities for CV skills extraction.
"""
import re

SEPARATORS = [",", "/", ";", "+", "&", "|"]


def tokenize(text):
    if not text:
        return []
    pattern = "|".join(re.escape(sep) for sep in SEPARATORS)
    parts = re.split(pattern, str(text))
    return [part.strip() for part in parts if part and part.strip()]
