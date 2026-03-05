"""
Canonicalizer for CV and market skills.
Synonyms are used only for canonicalization (not scoring).
"""
import re
from .normalizer import normalize_skill


def canonicalize_skill(value, synonym_map):
    normalized = normalize_skill(value)
    if not normalized:
        return None
    canonical = synonym_map.get(normalized, normalized)
    canonical = canonical.replace(" ", "_")
    canonical = re.sub(r"_+", "_", canonical)
    return canonical
