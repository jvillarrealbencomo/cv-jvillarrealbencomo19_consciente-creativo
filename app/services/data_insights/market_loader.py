"""
Market data loader for Data Insights. market_loader.py: load market skills and related metadata from CSV files.
"""
import csv
import os
from collections import defaultdict
from .normalizer import normalize_skill


def _data_insights_dir(root_path):
    return os.path.abspath(os.path.join(root_path, '..', 'data_insights'))


def load_market_skills(root_path, profile=None):
    data_dir = _data_insights_dir(root_path)
    market_skills = {}
    skill_sources = defaultdict(set)
    skill_categories = defaultdict(set)
    synonym_map = {}
    datasets = []

    if not os.path.isdir(data_dir):
        return market_skills, skill_sources, skill_categories, synonym_map, datasets

    for filename in os.listdir(data_dir):
        if not filename.endswith('.csv'):
            continue
        filepath = os.path.join(data_dir, filename)
        datasets.append(filepath)
        with open(filepath, encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                role = (row.get('role') or '').strip().lower().replace('-', '_').replace(' ', '_')
                if profile and role and role != profile:
                    continue

                normalized = normalize_skill(row.get('skill', ''))
                if not normalized:
                    continue

                canonical = row.get('synonyms')
                if canonical:
                    for synonym in canonical.split('|'):
                        normalized_syn = normalize_skill(synonym)
                        if normalized_syn:
                            synonym_map[normalized_syn] = normalized

                skill_sources[normalized].add(row.get('source') or os.path.splitext(filename)[0])
                category = row.get('category')
                if category:
                    skill_categories[normalized].add(category)
                market_skills[normalized] = row

    return market_skills, skill_sources, skill_categories, synonym_map, datasets
