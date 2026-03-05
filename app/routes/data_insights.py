"""
Data Insights API
Version 2026 - Public data cross-referencing for skills
"""
import csv
import io
import re
from datetime import datetime
from flask import Blueprint, jsonify, request, current_app, Response
from app.services.data_insights.service import build_insights
from app.models.app_metadata import get_app_metadata_value

bp = Blueprint('data_insights', __name__, url_prefix='/api/data_insights')


PROFILE_MAP = {
    'qa_analyst': 'qa_analyst',
    'qa-analyst': 'qa_analyst',
    'qa analyst': 'qa_analyst',
    'qa_engineer': 'qa_engineer',
    'qa-engineer': 'qa_engineer',
    'qa engineer': 'qa_engineer',
    'data_scientist': 'data_scientist',
    'data-scientist': 'data_scientist',
    'data scientist': 'data_scientist',
}


def _normalize_profile(profile_raw):
    if not profile_raw:
        return None
    key = profile_raw.strip().lower()
    key = key.replace('_', ' ').replace('-', ' ')
    key = re.sub(r'\s+', ' ', key)
    return PROFILE_MAP.get(key, PROFILE_MAP.get(profile_raw.strip().lower()))


@bp.route('/market-insights', methods=['GET'])
def market_insights():
    profile_raw = request.args.get('profile')
    profile = _normalize_profile(profile_raw)
    if not profile:
        return jsonify({'error': 'Invalid or missing profile'}), 400

    include_education = request.args.get('include_education', 'false').lower() in ('true', '1', 'yes')
    insights = build_insights(current_app.root_path, profile, include_education=include_education)
    
    # Add metadata from app_metadata table
    insights['meta'] = {
        'api_version': get_app_metadata_value('api_version', 'v2'),
        'release_year': get_app_metadata_value('release_year', '2026'),
        'generated_at': datetime.utcnow().isoformat(),
        'model': 'market_cross_reference_v1',
        'api_status': get_app_metadata_value('api_status', 'production')
    }
    
    return jsonify(insights), 200


@bp.route('/profile-readiness', methods=['GET'])
def profile_readiness():
    profile_raw = request.args.get('profile')
    profile = _normalize_profile(profile_raw)
    if not profile:
        return jsonify({'error': 'Invalid or missing profile'}), 400

    include_education = request.args.get('include_education', 'false').lower() in ('true', '1', 'yes')
    insights = build_insights(current_app.root_path, profile, include_education=include_education)

    coverage = insights.get('coverage', {})
    skill_types = insights.get('skills', {}).get('skill_types', {})
    market_skills = [
        skill for skill, data in coverage.items()
        if data.get('present_in_market') and skill_types.get(skill) != 'language'
    ]
    matched_skills = [
        skill for skill, data in coverage.items()
        if data.get('present_in_market') and data.get('present_in_cv') and skill_types.get(skill) != 'language'
    ]
    market_count = len(market_skills)
    matched_count = len(matched_skills)
    readiness = (matched_count / market_count) if market_count else 0.0

    return jsonify({
        'meta': {
            'api_version': get_app_metadata_value('api_version', 'v2'),
            'release_year': get_app_metadata_value('release_year', '2026'),
            'generated_at': datetime.utcnow().isoformat(),
            'model': 'market_cross_reference_v1',
            'api_status': get_app_metadata_value('api_status', 'production')
        },
        'profile': profile,
        'readiness_score': round(readiness * 100, 2),
        'method': 'matched_market_skills / total_market_skills',
        'counts': {
            'market_skill_count': market_count,
            'matched_skill_count': matched_count
        },
        'datasets': insights.get('datasets')
    }), 200


@bp.route('/market-insights/export', methods=['GET'])
def market_insights_export():
    profile_raw = request.args.get('profile')
    profile = _normalize_profile(profile_raw)
    if not profile:
        return jsonify({'error': 'Invalid or missing profile'}), 400

    include_education = request.args.get('include_education', 'false').lower() in ('true', '1', 'yes')
    insights = build_insights(current_app.root_path, profile, include_education=include_education)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['profile', 'skill', 'present_in_cv', 'present_in_market', 'datasets'])

    coverage = insights.get('coverage', {})
    for skill in sorted(coverage.keys()):
        data = coverage[skill]
        writer.writerow([
            profile,
            skill,
            'true' if data.get('present_in_cv') else 'false',
            'true' if data.get('present_in_market') else 'false',
            ';'.join(data.get('datasets', []))
        ])

    csv_data = output.getvalue()
    output.close()

    filename = f"market_insights_{profile}.csv"
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


@bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Comprehensive dashboard endpoint for Data Insights frontend
    Returns data for all 3 charts in a single response
    Fixed to Data Scientist profile
    """
    # Always use data_scientist profile (Evidence Hub requirement)
    profile = 'data_scientist'

    include_education = request.args.get('include_education', 'false').lower() in ('true', '1', 'yes')
    insights = build_insights(current_app.root_path, profile, include_education=include_education)

    coverage = insights.get('coverage', {})
    skill_types = insights.get('skills', {}).get('skill_types', {})
    
    # Filter out languages for readiness calculation
    market_skills = [
        skill for skill, data in coverage.items()
        if data.get('present_in_market') and skill_types.get(skill) != 'language'
    ]
    matched_skills = [
        skill for skill, data in coverage.items()
        if data.get('present_in_market') and data.get('present_in_cv') and skill_types.get(skill) != 'language'
    ]
    missing_skills = [
        skill for skill in market_skills if skill not in matched_skills
    ]
    
    market_count = len(market_skills)
    matched_count = len(matched_skills)
    missing_count = market_count - matched_count
    readiness = (matched_count / market_count) if market_count else 0.0

    # Chart 3: Dataset-level alignment (Kaggle vs O*NET)
    # Group skills by dataset
    kaggle_matched = []
    kaggle_missing = []
    onet_matched = []
    onet_missing = []
    
    for skill, data in coverage.items():
        # Skip languages
        if skill_types.get(skill) == 'language':
            continue
        
        datasets = data.get('datasets', [])
        is_in_cv = data.get('present_in_cv', False)
        is_in_market = data.get('present_in_market', False)
        
        if not is_in_market:
            continue
            
        # Check if skill is in Kaggle dataset (normalized tag)
        if 'kaggle' in datasets:
            if is_in_cv:
                kaggle_matched.append(skill)
            else:
                kaggle_missing.append(skill)
        
        # Check if skill is in O*NET dataset (normalized tag)
        if 'onet' in datasets:
            if is_in_cv:
                onet_matched.append(skill)
            else:
                onet_missing.append(skill)
    
    kaggle_total = len(kaggle_matched) + len(kaggle_missing)
    onet_total = len(onet_matched) + len(onet_missing)
    
    kaggle_alignment = (len(kaggle_matched) / kaggle_total * 100) if kaggle_total > 0 else 0
    onet_alignment = (len(onet_matched) / onet_total * 100) if onet_total > 0 else 0
    
    return jsonify({
        'meta': {
            'api_version': get_app_metadata_value('api_version', 'v2'),
            'release_year': get_app_metadata_value('release_year', '2026'),
            'generated_at': datetime.utcnow().isoformat(),
            'model': 'market_cross_reference_v1',
            'api_status': get_app_metadata_value('api_status', 'production')
        },
        'profile': profile,
        'chart1_profile_readiness': {
            'matched_skill_count': matched_count,
            'market_skill_count': market_count,
            'readiness_score': round(readiness * 100, 2),
            'matched_skills': sorted(matched_skills),
            'missing_skills': sorted(missing_skills),
            'all_market_skills': sorted(market_skills)
        },
        'chart2_coverage': {
            'market_demand': market_count,
            'present_in_cv': matched_count,
            'gap': missing_count,
            'market_demand_skills': sorted(market_skills),
            'present_in_cv_skills': sorted(matched_skills),
            'gap_skills': sorted(missing_skills)
        },
        'chart3_dataset_alignment': {
            'kaggle': {
                'total': kaggle_total,
                'matched': len(kaggle_matched),
                'missing': len(kaggle_missing),
                'matched_skills': sorted(kaggle_matched),
                'missing_skills': sorted(kaggle_missing),
                'alignment_percent': round(kaggle_alignment, 1)
            },
            'onet': {
                'total': onet_total,
                'matched': len(onet_matched),
                'missing': len(onet_missing),
                'matched_skills': sorted(onet_matched),
                'missing_skills': sorted(onet_missing),
                'alignment_percent': round(onet_alignment, 1)
            }
        },
        'datasets': insights.get('datasets'),
        'all_skills_detailed': {
            skill: {
                'present_in_cv': coverage[skill].get('present_in_cv'),
                'present_in_market': coverage[skill].get('present_in_market'),
                'datasets': coverage[skill].get('datasets'),
                'skill_type': skill_types.get(skill, 'unknown')
            }
            for skill in sorted(coverage.keys())
        }
    }), 200


@bp.route('/dashboard-debug', methods=['GET'])
def dashboard_debug():
    """
    Developer-only dashboard endpoint with detailed skill breakdowns
    Returns same data as /dashboard but includes actual skill lists for each metric
    Hidden from production UI - for debugging and development only
    """
    # Always use data_scientist profile (Evidence Hub requirement)
    profile = 'data_scientist'

    include_education = request.args.get('include_education', 'false').lower() in ('true', '1', 'yes')
    insights = build_insights(current_app.root_path, profile, include_education=include_education)

    coverage = insights.get('coverage', {})
    skill_types = insights.get('skills', {}).get('skill_types', {})
    
    # Filter out languages for readiness calculation
    market_skills = [
        skill for skill, data in coverage.items()
        if data.get('present_in_market') and skill_types.get(skill) != 'language'
    ]
    matched_skills = [
        skill for skill, data in coverage.items()
        if data.get('present_in_market') and data.get('present_in_cv') and skill_types.get(skill) != 'language'
    ]
    missing_skills = [
        skill for skill in market_skills if skill not in matched_skills
    ]
    
    market_count = len(market_skills)
    matched_count = len(matched_skills)
    missing_count = market_count - matched_count
    readiness = (matched_count / market_count) if market_count else 0.0

    # Chart 3: Dataset-level alignment (Kaggle vs O*NET)
    # Group skills by dataset
    kaggle_matched = []
    kaggle_missing = []
    onet_matched = []
    onet_missing = []
    
    for skill, data in coverage.items():
        # Skip languages
        if skill_types.get(skill) == 'language':
            continue
        
        datasets = data.get('datasets', [])
        is_in_cv = data.get('present_in_cv', False)
        is_in_market = data.get('present_in_market', False)
        
        if not is_in_market:
            continue
            
        # Check if skill is in Kaggle dataset (normalized tag)
        if 'kaggle' in datasets:
            if is_in_cv:
                kaggle_matched.append(skill)
            else:
                kaggle_missing.append(skill)
        
        # Check if skill is in O*NET dataset (normalized tag)
        if 'onet' in datasets:
            if is_in_cv:
                onet_matched.append(skill)
            else:
                onet_missing.append(skill)
    
    kaggle_total = len(kaggle_matched) + len(kaggle_missing)
    onet_total = len(onet_matched) + len(onet_missing)
    
    kaggle_alignment = (len(kaggle_matched) / kaggle_total * 100) if kaggle_total > 0 else 0
    onet_alignment = (len(onet_matched) / onet_total * 100) if onet_total > 0 else 0
    
    return jsonify({
        'meta': {
            'api_version': get_app_metadata_value('api_version', 'v2'),
            'release_year': get_app_metadata_value('release_year', '2026'),
            'generated_at': datetime.utcnow().isoformat(),
            'model': 'market_cross_reference_v1',
            'api_status': get_app_metadata_value('api_status', 'production'),
            'debug_mode': True
        },
        'profile': profile,
        'chart1_profile_readiness': {
            'matched_skill_count': matched_count,
            'market_skill_count': market_count,
            'readiness_score': round(readiness * 100, 2),
            'matched_skills': sorted(matched_skills),
            'missing_skills': sorted(missing_skills),
            'all_market_skills': sorted(market_skills)
        },
        'chart2_coverage': {
            'market_demand': market_count,
            'present_in_cv': matched_count,
            'gap': missing_count,
            'market_demand_skills': sorted(market_skills),
            'present_in_cv_skills': sorted(matched_skills),
            'gap_skills': sorted(missing_skills)
        },
        'chart3_dataset_alignment': {
            'kaggle': {
                'total': kaggle_total,
                'matched': len(kaggle_matched),
                'missing': len(kaggle_missing),
                'matched_skills': sorted(kaggle_matched),
                'missing_skills': sorted(kaggle_missing),
                'alignment_percent': round(kaggle_alignment, 1)
            },
            'onet': {
                'total': onet_total,
                'matched': len(onet_matched),
                'missing': len(onet_missing),
                'matched_skills': sorted(onet_matched),
                'missing_skills': sorted(onet_missing),
                'alignment_percent': round(onet_alignment, 1)
            }
        },
        'datasets': insights.get('datasets'),
        'all_skills_detailed': {
            skill: {
                'present_in_cv': coverage[skill].get('present_in_cv'),
                'present_in_market': coverage[skill].get('present_in_market'),
                'datasets': coverage[skill].get('datasets'),
                'skill_type': skill_types.get(skill, 'unknown')
            }
            for skill in sorted(coverage.keys())
        }
    }), 200
