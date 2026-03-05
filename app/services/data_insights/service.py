"""
Data Insights service: matching, gaps, coverage, export.
"""
import os
from datetime import datetime
from .extractor import extract_cv_skills
from .canonicalizer import canonicalize_skill
INFERENCE_MAP = {
    "sqlalchemy": ["sql"],
    "flask": ["python", "api integration"],
    "backend python sql": ["python", "sql"],
    "api": ["api integration"],
    "rest api": ["api integration"],
}
from .market_loader import load_market_skills


def build_insights(root_path, profile, include_education=False):
    market_skills, market_sources, market_categories, synonym_map, datasets = load_market_skills(
        root_path, profile=profile
    )

    market_vocab = set(market_skills.keys()) | set(synonym_map.keys())
    cv_data = extract_cv_skills(
        profile,
        include_education=include_education,
        market_vocab=market_vocab,
        market_categories=market_categories
    )
    raw_cv_skills = cv_data["raw_cv_skills"]
    normalized_cv_skills = cv_data["normalized_cv_skills"]
    cv_skill_sources = cv_data["cv_skill_sources"]

    for skill in list(normalized_cv_skills):
        inferred = INFERENCE_MAP.get(skill, [])
        for inferred_skill in inferred:
            if inferred_skill not in normalized_cv_skills:
                normalized_cv_skills.append(inferred_skill)
            cv_skill_sources.setdefault(inferred_skill, [])
            if f"inferred_from_{skill}" not in cv_skill_sources[inferred_skill]:
                cv_skill_sources[inferred_skill].append(f"inferred_from_{skill}")

    normalized_cv_skills = sorted(set(normalized_cv_skills))

    canonical_cv_skills = []
    canonical_map = {}
    for skill in normalized_cv_skills:
        canonical = canonicalize_skill(skill, synonym_map)
        if canonical:
            canonical_map[skill] = canonical
            canonical_cv_skills.append(canonical)

    canonical_cv_skills = sorted(set(canonical_cv_skills))

    coverage = {}
    for skill in sorted(set(list(market_skills.keys()) + list(normalized_cv_skills))):
        in_cv = skill in normalized_cv_skills
        in_market = skill in market_skills
        coverage[skill] = {
            "present_in_cv": in_cv,
            "present_in_market": in_market,
            "datasets": sorted(market_sources.get(skill, []))
        }

    latest_dataset = None
    if datasets:
        latest_mtime = max(os.path.getmtime(path) for path in datasets)
        latest_dataset = datetime.utcfromtimestamp(latest_mtime).isoformat() + 'Z'

    return {
        "skills": {
            "raw_cv_skills": raw_cv_skills,
            "filtered_raw_skills": cv_data.get("filtered_raw_skills", []),
            "normalized_cv_skills": normalized_cv_skills,
            "canonical_cv_skills": canonical_cv_skills,
            "skill_sources": cv_skill_sources,
            "skill_types": cv_data.get("cv_skill_types", {})
        },
        "coverage": coverage,
        "datasets": {
            "files": sorted(os.path.basename(path) for path in datasets),
            "last_updated_utc": latest_dataset
        }
    }
