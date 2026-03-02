"""
Normalizer for CV skills.
"""
import re

NORMALIZATION_MAP = {
    "api": "api integration",
    "rest api": "api integration",
    "backend api": "api integration",
    "ci cd": "ci/cd",
    "ci_cd": "ci/cd",
    "sklearn": "scikit learn",
    "scikit-learn": "scikit learn",
}


def normalize_skill(value):
    if not value:
        return None
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9+#./ ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return None
    return NORMALIZATION_MAP.get(text, text)
