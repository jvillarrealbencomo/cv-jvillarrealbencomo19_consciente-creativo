"""
CV skills extractor.
"""
from collections import defaultdict
from app.models import TechnicalTool, Course, WorkExperience, AdvancedTraining, Education
from .tokenizer import tokenize
from .normalizer import normalize_skill
from .skill_filter import is_valid_skill, normalize_basic, classify_skill, expand_compound_tokens, build_known_terms


def _add_skill(raw_value, source, cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
               market_vocab, market_categories, skill_types, known_terms):
    raw = str(raw_value).strip() if raw_value is not None else ""
    if not raw:
        return
    raw_cv_skills.add(raw)
    for candidate in expand_compound_tokens(raw, known_terms):
        basic = normalize_basic(candidate)
        if not is_valid_skill(basic, market_vocab, market_categories):
            continue
        filtered_raw_skills.add(candidate)
        normalized = normalize_skill(candidate)
        if not normalized:
            continue
        cv_skills.add(normalized)
        cv_skill_sources[normalized].add(source)
        skill_type = classify_skill(normalized, market_vocab, market_categories)
        if skill_type:
            skill_types[normalized] = skill_type


def extract_cv_skills(profile, include_education=False, market_vocab=None, market_categories=None):
    cv_skills = set()
    cv_skill_sources = defaultdict(set)
    raw_cv_skills = set()
    filtered_raw_skills = set()
    market_vocab = market_vocab or set()
    market_categories = market_categories or {}
    skill_types = {}
    known_terms = build_known_terms(market_vocab)

    if profile == 'qa_analyst':
        tools = TechnicalTool.query.filter_by(active=True, usable_qa_analyst=True).all()
    elif profile == 'qa_engineer':
        tools = TechnicalTool.query.filter_by(active=True, usable_qa_engineer=True).all()
    elif profile == 'data_scientist':
        tools = TechnicalTool.query.filter_by(active=True, usable_data_scientist=True).all()
    else:
        tools = []

    for tool in tools:
        _add_skill(tool.name, "technical_tools", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
               market_vocab, market_categories, skill_types, known_terms)

    for course in Course.query.filter_by(active=True).all():
        for skill in course.get_skills_list():
            _add_skill(skill, "courses", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
                       market_vocab, market_categories, skill_types, known_terms)

    for exp in WorkExperience.query.filter_by(active=True).all():
        for tech in exp.get_technologies_list():
            _add_skill(tech, "work_experience", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
                       market_vocab, market_categories, skill_types, known_terms)
        for field in [exp.responsibilities_summary, exp.responsibilities_detailed, exp.achievements]:
            for token in tokenize(field):
                _add_skill(token, "work_experience", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
                           market_vocab, market_categories, skill_types, known_terms)

    for training in AdvancedTraining.query.filter_by(active=True).all():
        _add_skill(training.name, "advanced_training", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
               market_vocab, market_categories, skill_types, known_terms)
        for token in tokenize(training.description):
            _add_skill(token, "advanced_training", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
                       market_vocab, market_categories, skill_types, known_terms)

    if include_education:
        for education in Education.query.filter_by(active=True).all():
            _add_skill(education.degree, "education", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
                       market_vocab, market_categories, skill_types, known_terms)
            for token in tokenize(education.details):
                _add_skill(token, "education", cv_skills, cv_skill_sources, raw_cv_skills, filtered_raw_skills,
                           market_vocab, market_categories, skill_types, known_terms)

    return {
        "raw_cv_skills": sorted(raw_cv_skills),
        "filtered_raw_skills": sorted(filtered_raw_skills),
        "normalized_cv_skills": sorted(cv_skills),
        "cv_skill_sources": {k: sorted(v) for k, v in cv_skill_sources.items()},
        "cv_skill_types": skill_types
    }
