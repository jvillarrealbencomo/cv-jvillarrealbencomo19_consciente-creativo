"""
Skill filter for CV raw text.
"""
import re

MAX_WORDS = 3
MIN_LENGTH = 2
DISALLOWED_CHARS = {".", "%", "(", ")", ":"}

NARRATIVE_VERBS = {
    "designed", "developed", "implemented", "producing", "managed", "built",
    "created", "led", "improved", "supported", "maintained", "executed",
    "delivered", "optimized", "analyzed", "documented", "coordinated",
    "integrated", "performed", "collaborated", "presented", "trained"
}

STOP_SKILLS = {
    "none", "n/a", "na", "other", "misc", "general", "various",
    "technical", "design", "integration", "analysis",
    "and", "to", "with", "including", "of",
    "system", "process", "metrics", "evidence", "dataset", "datasets",
    "sources", "synonyms", "normalization", "canonicalization", "extraction",
    "coverage", "gap", "comparison", "repositories", "outputs", "domain",
    "reproducible", "results", "tests", "testing"
}

CONNECTIVES = {"and", "to", "with", "including"}
STARTS_WITH = ("and ", "to ", "with ", "including ")

ALLOWED_SKILL_TYPES = {
    "technology", "framework", "language", "library", "methodology", "tool"
}

FORBIDDEN_SKILL_TYPES = {
    "process", "capability", "artifact", "concept", "system_feature",
    "output", "documentation", "meta"
}

TECHNOLOGIES = {
    "python", "sql", "sqlalchemy", "flask", "postman", "newman", "ci/cd",
    "api integration", "api"
}

FRAMEWORKS = {"selenium", "cucumber", "gherkin"}

LIBRARIES = {"pandas", "numpy", "scikit learn"}

METHODOLOGIES = {"machine learning", "feature engineering", "data visualization", "statistics"}

TOOLS = {"jira", "sonarqube", "git"}

LANGUAGES = {"english", "b1 english", "intermediate english"}

ALLOWED_PHRASES = METHODOLOGIES | {"api integration", "ci/cd", "scikit learn", "b1 english", "intermediate english"}

CATEGORY_TO_TYPE = {
    "programming": "technology",
    "databases": "technology",
    "devops": "technology",
    "engineering": "technology",
    "data processing": "library",
    "modeling": "methodology",
    "analytics": "methodology",
    "api testing": "tool",
    "test automation": "framework"
}


def normalize_basic(text: str) -> str:
    if not text:
        return ""
    value = str(text).strip().lower()
    value = value.replace("-", " ")
    value = re.sub(r"\s+", " ", value)
    return value


def classify_skill(text: str, market_vocab: set[str], market_categories: dict[str, set[str]]):
    if text in LANGUAGES:
        return "language"
    if text in FRAMEWORKS:
        return "framework"
    if text in LIBRARIES:
        return "library"
    if text in TECHNOLOGIES:
        return "technology"
    if text in METHODOLOGIES:
        return "methodology"
    if text in TOOLS:
        return "tool"
    if text in market_vocab:
        categories = market_categories.get(text, set())
        for category in categories:
            mapped = CATEGORY_TO_TYPE.get(category.lower())
            if mapped in ALLOWED_SKILL_TYPES:
                return mapped
    return None


def build_known_terms(market_vocab: set[str]):
    return set(market_vocab) | TECHNOLOGIES | FRAMEWORKS | LIBRARIES | METHODOLOGIES | TOOLS | LANGUAGES | ALLOWED_PHRASES


def expand_compound_tokens(text: str, known_vocab: set[str]):
    cleaned = normalize_basic(text)
    if not cleaned:
        return []
    cleaned = re.sub(r"[()\[\]{}]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned or cleaned in ALLOWED_PHRASES:
        return [cleaned] if cleaned else []
    if " " not in cleaned:
        return [cleaned]

    found = []
    for term in sorted(known_vocab, key=len, reverse=True):
        if " " in term and term in cleaned:
            found.append(term)

    words = cleaned.split()
    for word in words:
        if word in known_vocab:
            found.append(word)

    if found:
        return sorted(set(found))
    return [cleaned]


def is_valid_skill(text: str, market_vocab: set[str], market_categories: dict[str, set[str]]) -> bool:
    text = normalize_basic(text)
    if not text:
        return False
    if text in STOP_SKILLS:
        return False
    if text.startswith(STARTS_WITH):
        return False
    if any(word in CONNECTIVES for word in text.split()):
        return False
    if len(text.split()) > MAX_WORDS:
        return False
    if any(verb in text.split() for verb in NARRATIVE_VERBS):
        return False
    if any(char in text for char in DISALLOWED_CHARS):
        return False
    if len(text) < MIN_LENGTH:
        return False
    skill_type = classify_skill(text, market_vocab, market_categories)
    if not skill_type or skill_type in FORBIDDEN_SKILL_TYPES:
        return False
    return True
