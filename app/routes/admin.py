"""
Admin Routes
Version 2025 - Administrative interface
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from markupsafe import Markup
from datetime import datetime
from app import db


from app.models import Person, WorkExperience, TechnicalTool, Education, Certification, Course, Language, ITProduct, AdvancedTraining

bp = Blueprint('admin', __name__, url_prefix='/admin')
@bp.route('/database/consulta')
def database_consulta():
    tables = [
        ('Person', Person),
        ('WorkExperience', WorkExperience),
        ('TechnicalTool', TechnicalTool),
        ('Education', Education),
        ('AdvancedTraining', AdvancedTraining),
        ('Language', Language),
        ('ITProduct', ITProduct)
    ]
    html = ['<h2>Database Table Records</h2>']
    for name, model in tables:
        records = model.query.all()
        html.append(f'<h3>{name}</h3>')
        if not records:
            html.append('<p><em>No records found.</em></p>')
        else:
            html.append('<table border="1" cellpadding="4" style="border-collapse:collapse;">')
            # Table header
            html.append('<tr>' + ''.join(f'<th>{col}</th>' for col in records[0].to_dict().keys()) + '</tr>')
            # Table rows
            for rec in records:
                html.append('<tr>' + ''.join(f'<td>{Markup.escape(str(val))}</td>' for val in rec.to_dict().values()) + '</tr>')
            html.append('</table>')
    return Markup(''.join(html))


@bp.route('/')
def index():
    """Admin dashboard"""
    stats = {
        'people': Person.query.count(),
        'experiences': WorkExperience.query.count(),
        'tools': TechnicalTool.query.count(),
        'education': Education.query.count(),
        'advanced_training': AdvancedTraining.query.count(),
        'languages': Language.query.count(),
        'products': ITProduct.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats, generated_at=datetime.utcnow())


@bp.route('/data')
def data():
    """Data management page"""
    return render_template('admin/data.html')


@bp.route('/settings')
def settings():
    """Settings page"""
    return render_template('admin/settings.html')


# Hidden: update WorkExperience dates via query params
# Usage:
#   /admin/database/update/experience-dates?id=1&start=2025-04-14&end=2025-11-13
@bp.route('/database/update/experience-dates')
def update_experience_dates():
    exp_id = request.args.get('id', type=int)
    start_raw = request.args.get('start')  # YYYY-MM-DD
    end_raw = request.args.get('end')      # YYYY-MM-DD

    if not exp_id:
        return Markup('<p><strong>Error:</strong> missing id. Example: ?id=1&start=2025-04-14&end=2025-11-13</p>'), 400

    exp = db.session.get(WorkExperience, exp_id)
    if not exp:
        return Markup(f'<p><strong>Error:</strong> WorkExperience id {exp_id} not found.</p>'), 404

    from datetime import datetime
    old_start = exp.start_date
    old_end = exp.end_date

    # Parse dates if provided
    try:
        if start_raw is not None:
            exp.start_date = datetime.strptime(start_raw, '%Y-%m-%d').date() if start_raw else None
        if end_raw is not None:
            exp.end_date = datetime.strptime(end_raw, '%Y-%m-%d').date() if end_raw else None
        db.session.commit()
    except ValueError:
        return Markup('<p><strong>Error:</strong> invalid date format. Use YYYY-MM-DD.</p>'), 400

    html = f"""
    <h3>WorkExperience #{exp.id} dates updated</h3>
    <table border="1" cellpadding="6" style="border-collapse:collapse;">
      <tr><th></th><th>Start</th><th>End</th></tr>
      <tr><td>Before</td><td>{old_start}</td><td>{old_end}</td></tr>
      <tr><td>After</td><td>{exp.start_date}</td><td>{exp.end_date}</td></tr>
    </table>
    <p><a href="/admin/database/consulta">Back to database view</a></p>
    """
    return Markup(html)

# Hidden: bulk fix TechnicalTool names from descriptions
# Usage:
#   /admin/database/update/tool-fix-names?ids=2,3,4,5
@bp.route('/database/update/tool-fix-names')
def update_tool_fix_names():
    ids_param = request.args.get('ids', '')
    try:
        ids = [int(x.strip()) for x in ids_param.split(',') if x.strip()]
    except ValueError:
        return Markup('<p><strong>Error:</strong> invalid ids list. Use comma-separated integers like ids=2,3,4,5</p>'), 400

    if not ids:
        return Markup('<p><strong>Error:</strong> missing ids. Example: ?ids=2,3,4,5</p>'), 400

    updated = []
    errors = []

    for tid in ids:
        tool = db.session.get(TechnicalTool, tid)
        if not tool:
            errors.append(f'TechnicalTool id {tid} not found')
            continue
        old_name = tool.name
        new_name = (getattr(tool, 'description', None) or '').strip()
        tool.name = new_name
        updated.append((tid, old_name, new_name))

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return Markup(f"<p><strong>Error:</strong> Failed to commit changes: {Markup.escape(str(e))}</p>"), 500

    html = ["<h3>TechnicalTool names updated from descriptions</h3>"]
    if updated:
        html.append('<table border="1" cellpadding="6" style="border-collapse:collapse;">')
        html.append('<tr><th>ID</th><th>Old Name</th><th>New Name</th></tr>')
        for rid, before, after in updated:
            html.append(f'<tr><td>{rid}</td><td>{Markup.escape(str(before))}</td><td>{Markup.escape(str(after))}</td></tr>')
        html.append('</table>')
    else:
        html.append('<p>No tools updated.</p>')

    if errors:
        html.append('<h4>Warnings</h4><ul>')
        for err in errors:
            html.append(f'<li>{Markup.escape(err)}</li>')
        html.append('</ul>')

    html.append('<p><a href="/admin/database/consulta">Back to database view</a></p>')
    return Markup(''.join(html))


# Hidden: update Education display_order
# Usage:
#   /admin/database/update/education-order?id=1&order=3
@bp.route('/database/update/education-order')
def update_education_order():
    edu_id = request.args.get('id', type=int)
    new_order = request.args.get('order', type=int)

    if not edu_id or new_order is None:
        return Markup('<p><strong>Error:</strong> missing id or order. Example: ?id=1&order=3</p>'), 400

    edu = db.session.get(Education, edu_id)
    if not edu:
        return Markup(f'<p><strong>Error:</strong> Education id {edu_id} not found.</p>'), 404

    old_order = edu.display_order
    edu.display_order = new_order
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return Markup(f'<p><strong>Error:</strong> {Markup.escape(str(e))}</p>'), 500

    html = f"""
    <h3>Education #{edu.id} display_order updated</h3>
    <table border="1" cellpadding="6" style="border-collapse:collapse;">
      <tr><th>Field</th><th>Before</th><th>After</th></tr>
      <tr><td>display_order</td><td>{old_order}</td><td>{edu.display_order}</td></tr>
      <tr><td>degree</td><td colspan="2">{Markup.escape(edu.degree)}</td></tr>
      <tr><td>institution</td><td colspan="2">{Markup.escape(edu.institution)}</td></tr>
    </table>
    <p><a href="/admin/database/consulta">Back to database view</a></p>
    """
    return Markup(html)


# Hidden: batch update WorkExperience
# a) Set location="Chile" for records 1, 3, and 5
# b) Move record 2 to end by setting its display_order to 999
# Usage:
#   /admin/database/update/experience-batch
@bp.route('/database/update/experience-batch')
def update_experience_batch():
    updated = []
    errors = []

    # a) Update locations for ids 1, 3, 5
    for exp_id in [1, 3, 5]:
        exp = db.session.get(WorkExperience, exp_id)
        if not exp:
            errors.append(f"WorkExperience id {exp_id} not found")
            continue
        old_loc = exp.location
        exp.location = 'Chile'
        updated.append((exp_id, 'location', old_loc, exp.location))

    # b) Move record 2 to the end (set display_order=999 so it appears last in its block)
    exp2 = db.session.get(WorkExperience, 2)
    if not exp2:
        errors.append("WorkExperience id 2 not found")
    else:
        old_order = exp2.display_order
        exp2.display_order = 999
        updated.append((2, 'display_order', old_order, exp2.display_order))

    # Commit changes
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return Markup(f"<p><strong>Error:</strong> Failed to commit changes: {Markup.escape(str(e))}</p>"), 500

    # Render summary
    html = ["<h3>WorkExperience batch update completed</h3>"]
    if updated:
        html.append('<h4>Updated Fields</h4>')
        html.append('<table border="1" cellpadding="6" style="border-collapse:collapse;">')
        html.append('<tr><th>Record ID</th><th>Field</th><th>Before</th><th>After</th></tr>')
        for rid, field, before, after in updated:
            html.append(f'<tr><td>{rid}</td><td>{field}</td><td>{Markup.escape(str(before))}</td><td>{Markup.escape(str(after))}</td></tr>')
        html.append('</table>')
    else:
        html.append('<p>No fields updated.</p>')

    if errors:
        html.append('<h4>Warnings</h4>')
        html.append('<ul>')
        for err in errors:
            html.append(f'<li>{Markup.escape(err)}</li>')
        html.append('</ul>')

    html.append('<p><a href="/admin/database/consulta">Back to database view</a></p>')
    return Markup(''.join(html))


# Hidden: preview WorkExperience in sorted order (as it appears in PDF/profile)
# Usage:
#   /admin/database/preview/experience-order
@bp.route('/database/preview/experience-order')
def preview_experience_order():
    from datetime import datetime
    
    # Apply same sorting logic as profiles.py
    block_priority = {"2021-2025": 0, "2015-2020": 1, "1985-2009": 2}
    
    experiences = WorkExperience.query.filter_by(active=True).all()
    
    def exp_sort_key(exp):
        block_idx = block_priority.get((exp.time_block or '').strip(), 999)
        disp = exp.display_order if isinstance(getattr(exp, 'display_order', None), int) else 0
        end = exp.end_date or datetime.max.date()
        start = exp.start_date or datetime.min.date()
        return (block_idx, disp, -int(end.strftime('%Y%m%d')), -int(start.strftime('%Y%m%d')))
    
    experiences_sorted = sorted(experiences, key=exp_sort_key)
    
    html = ['<h2>WorkExperience - Sorted Order (as in PDF)</h2>']
    html.append('<table border="1" cellpadding="6" style="border-collapse:collapse;">')
    html.append('<tr><th>Display Position</th><th>ID</th><th>Company</th><th>Time Block</th><th>Display Order</th><th>Start</th><th>End</th></tr>')
    
    for position, exp in enumerate(experiences_sorted, start=1):
        html.append(f'<tr>')
        html.append(f'<td><strong>{position}</strong></td>')
        html.append(f'<td>{exp.id}</td>')
        html.append(f'<td>{Markup.escape(exp.company)}</td>')
        html.append(f'<td>{Markup.escape(exp.time_block or "")}</td>')
        html.append(f'<td>{exp.display_order}</td>')
        html.append(f'<td>{exp.start_date}</td>')
        html.append(f'<td>{exp.end_date or "Present"}</td>')
        html.append(f'</tr>')
    
    html.append('</table>')
    html.append('<p><a href="/admin/database/consulta">Back to database view</a></p>')
    
    return Markup(''.join(html))


# Hidden: physically reorder WorkExperience table to match logical order
# Deletes and recreates records in sorted order so id matches display position
# Usage:
#   /admin/database/reorder/experience-physical
@bp.route('/database/reorder/experience-physical')
def reorder_experience_physical():
    from datetime import datetime
    
    # Apply same sorting logic as profiles.py
    block_priority = {"2021-2025": 0, "2015-2020": 1, "1985-2009": 2}
    
    experiences = WorkExperience.query.all()
    
    def exp_sort_key(exp):
        block_idx = block_priority.get((exp.time_block or '').strip(), 999)
        disp = exp.display_order if isinstance(getattr(exp, 'display_order', None), int) else 0
        end = exp.end_date or datetime.max.date()
        start = exp.start_date or datetime.min.date()
        return (block_idx, disp, -int(end.strftime('%Y%m%d')), -int(start.strftime('%Y%m%d')))
    
    experiences_sorted = sorted(experiences, key=exp_sort_key)
    
    # Save all data
    saved_data = []
    for exp in experiences_sorted:
        data = {
            'job_title': exp.job_title,
            'company': exp.company,
            'location': exp.location,
            'start_date': exp.start_date,
            'end_date': exp.end_date,
            'is_current': exp.is_current,
            'time_block': exp.time_block,
            'responsibilities_summary': exp.responsibilities_summary,
            'show_responsibilities_summary': exp.show_responsibilities_summary,
            'responsibilities_detailed': exp.responsibilities_detailed,
            'show_responsibilities_detailed': exp.show_responsibilities_detailed,
            'achievements': exp.achievements,
            'show_achievements': exp.show_achievements,
            'technologies': exp.technologies,
            'display_order': exp.display_order,
            'active': exp.active,
            'is_historical': exp.is_historical,
            'visible_qa_analyst': exp.visible_qa_analyst,
            'visible_qa_engineer': exp.visible_qa_engineer,
            'visible_data_scientist': exp.visible_data_scientist,
            'created_at': exp.created_at,
            'updated_at': exp.updated_at
        }
        saved_data.append(data)
    
    try:
        # Delete all records
        WorkExperience.query.delete()
        db.session.commit()
        
        # Reset autoincrement (only if sqlite_sequence table exists)
        try:
            db.session.execute(db.text("DELETE FROM sqlite_sequence WHERE name='work_experience';"))
            db.session.commit()
        except Exception:
            # sqlite_sequence might not exist, that's fine
            pass
        
        # Re-insert in correct order
        for data in saved_data:
            new_exp = WorkExperience()
            new_exp.job_title = data['job_title']
            new_exp.company = data['company']
            new_exp.location = data['location']
            new_exp.start_date = data['start_date']
            new_exp.end_date = data['end_date']
            new_exp.is_current = data['is_current']
            new_exp.time_block = data['time_block']
            new_exp.responsibilities_summary = data['responsibilities_summary']
            new_exp.show_responsibilities_summary = data['show_responsibilities_summary']
            new_exp.responsibilities_detailed = data['responsibilities_detailed']
            new_exp.show_responsibilities_detailed = data['show_responsibilities_detailed']
            new_exp.achievements = data['achievements']
            new_exp.show_achievements = data['show_achievements']
            new_exp.technologies = data['technologies']
            new_exp.display_order = data['display_order']
            new_exp.active = data['active']
            new_exp.is_historical = data['is_historical']
            new_exp.visible_qa_analyst = data['visible_qa_analyst']
            new_exp.visible_qa_engineer = data['visible_qa_engineer']
            new_exp.visible_data_scientist = data['visible_data_scientist']
            new_exp.created_at = data['created_at']
            new_exp.updated_at = data['updated_at']
            db.session.add(new_exp)
        
        db.session.commit()
        
        html = ['<h2>WorkExperience table physically reordered</h2>']
        html.append('<p>✓ Records deleted and recreated in sorted order.</p>')
        html.append('<p>Physical ID order now matches logical display order.</p>')
        html.append('<p><a href="/admin/database/consulta">View updated table</a></p>')
        html.append('<p><a href="/admin/database/preview/experience-order">Preview sorted order</a></p>')
        
        return Markup(''.join(html))
        
    except Exception as e:
        db.session.rollback()
        return Markup(f'<p><strong>Error:</strong> {Markup.escape(str(e))}</p><p><a href="/admin/database/consulta">Back</a></p>'), 500


# Hidden: restore WorkExperience data after failed reorder
# Usage:
#   /admin/database/restore/experience-data
@bp.route('/database/restore/experience-data')
def restore_experience_data():
    from datetime import date, datetime
    
    # Data from your original table
    records = [
        {
            'company': 'Apiux-Cliente: Superintendencia de educación',
            'job_title': 'QA Analyst',
            'location': 'Chile',
            'start_date': date(2025, 4, 14),
            'end_date': date(2025, 11, 13),
            'time_block': '2021-2025',
            'responsibilities_summary': 'Hoja de Trabajo Normativo\nHoja de Trabajo Recursos\nCaptura de Rendición de Cuentas\nFiscalización\nSife\nTramitación de Documentos',
            'achievements': 'Data dictionary construction in 6 systems with little or no information in 5 months',
            'display_order': 0,
        },
        {
            'company': 'Akzio Consultores. Client: Banco de Chile',
            'job_title': 'QA Analyst',
            'location': 'Chile',
            'start_date': date(2022, 11, 21),
            'end_date': date(2024, 7, 11),
            'time_block': '2021-2025',
            'responsibilities_summary': 'Requirements analysis, design, and execution of manual and automated tests, including functional, technical, regression, integration, smoke, and interface validation tests. Manual code inspection and inspection using SonarQube. Documentation of test and defect management in Jira and Confluence',
            'achievements': 'SEFE System upgrade and microservice development and implementation of decision models for large enterprises and corporations. 20% reduction in test execution time through process optimization',
            'display_order': 0,
        },
        {
            'company': 'Practia Global',
            'job_title': 'Freelance Consultant and Developer',
            'location': 'Chile',
            'start_date': date(2020, 11, 1),
            'end_date': date(2020, 12, 31),
            'time_block': '2015-2020',
            'responsibilities_summary': 'Integrated university indicators into software for an Argentine University',
            'achievements': 'BackEnd Python-SQL',
            'display_order': 0,
        },
        {
            'company': 'Diseños Susan',
            'job_title': 'Freelance Consultant and Developer',
            'location': 'Chile',
            'start_date': date(2020, 3, 1),
            'end_date': date(2020, 8, 31),
            'time_block': '2015-2020',
            'responsibilities_summary': 'Online Store',
            'achievements': '(Python/SQLAlchemy)',
            'display_order': 0,
        },
        {
            'company': 'ULA',
            'job_title': 'Freelance Consultant and Developer',
            'location': 'Ve',
            'start_date': date(2019, 1, 2),
            'end_date': date(2019, 6, 30),
            'time_block': '2015-2020',
            'responsibilities_summary': 'Hindmarsh-Rose Neuronal Modeling. Application in human brain study',
            'achievements': '(C++)',
            'display_order': 0,
        },
        {
            'company': 'Sílice Boquerón',
            'job_title': 'Freelance Consultant and Developer',
            'location': 'Ve',
            'start_date': date(2015, 2, 15),
            'end_date': date(2018, 12, 30),
            'time_block': '2015-2020',
            'responsibilities_summary': 'Sales + Inventory System',
            'achievements': 'Visual Basic',
            'display_order': 0,
        },
        {
            'company': 'Universidad Politécnica del estado Trujillo',
            'job_title': 'Full Professor and Researcher (Retired in Venezuela)',
            'location': 'Ve',
            'start_date': date(1985, 4, 1),
            'end_date': date(2009, 12, 31),
            'time_block': '1985-2009',
            'responsibilities_summary': 'Designed programming curriculum (Basic to C++), leading the creation of the Computer Science program, with a focus on code quality and development best practices, which consolidated algorithmic foundations and mentorship skills',
            'achievements': 'SEFE System upgrade and microservice development and implementation of decision models for large enterprises and corporations. 20% reduction in test execution time through process optimization.',
            'display_order': 0,
        }
    ]
    
    try:
        # Clear any existing records
        WorkExperience.query.delete()
        db.session.commit()
        
        # Insert records in sorted order
        for rec in records:
            exp = WorkExperience()
            exp.company = rec['company']
            exp.job_title = rec['job_title']
            exp.location = rec['location']
            exp.start_date = rec['start_date']
            exp.end_date = rec['end_date']
            exp.time_block = rec['time_block']
            exp.responsibilities_summary = rec['responsibilities_summary']
            exp.achievements = rec['achievements']
            exp.display_order = rec['display_order']
            exp.is_current = False
            exp.show_responsibilities_summary = True
            exp.show_responsibilities_detailed = False
            exp.show_achievements = True
            exp.active = True
            exp.is_historical = False
            exp.visible_qa_analyst = True
            exp.visible_qa_engineer = True
            exp.visible_data_scientist = True
            db.session.add(exp)
        
        db.session.commit()
        
        return Markup('''
            <h2>WorkExperience Data Restored</h2>
            <p>✓ 7 records restored in correct physical order</p>
            <p><a href="/admin/database/consulta">View restored table</a></p>
        ''')
        
    except Exception as e:
        db.session.rollback()
        return Markup(f'<p><strong>Error:</strong> {Markup.escape(str(e))}</p>'), 500


# Hidden: update TechnicalTool display_order
# Usage:
#   /admin/database/update/tool-order?id=1&order=2
@bp.route('/database/update/tool-order')
def update_tool_order():
    tool_id = request.args.get('id', type=int)
    new_order = request.args.get('order', type=int)

    if not tool_id or new_order is None:
        return Markup('<p><strong>Error:</strong> missing id or order. Example: ?id=1&order=2</p>'), 400

    tool = db.session.get(TechnicalTool, tool_id)
    if not tool:
        return Markup(f'<p><strong>Error:</strong> TechnicalTool id {tool_id} not found.</p>'), 404

    old_order = tool.display_order
    tool.display_order = new_order
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return Markup(f'<p><strong>Error:</strong> {Markup.escape(str(e))}</p>'), 500

    html = f"""
    <h3>TechnicalTool #{tool.id} display_order updated</h3>
    <table border="1" cellpadding="6" style="border-collapse:collapse;">
      <tr><th>Field</th><th>Before</th><th>After</th></tr>
      <tr><td>display_order</td><td>{old_order}</td><td>{tool.display_order}</td></tr>
      <tr><td>name</td><td colspan="2">{Markup.escape(tool.name)}</td></tr>
      <tr><td>subcategory_qa_analyst</td><td colspan="2">{Markup.escape(tool.subcategory_qa_analyst or '')}</td></tr>
    </table>
    <p><a href="/admin/database/consulta">Back to database view</a></p>
    """
    return Markup(html)


@bp.route('/update/advanced-training', methods=['GET'])
def update_advanced_training():
    """Hidden admin route to update AdvancedTraining records"""
    html = ['<h2>Update AdvancedTraining Records</h2>']
    
    # Update record 1: "Postdoctorate in Administrative Sciences" - set duration_hours to 96
    record1 = AdvancedTraining.query.filter_by(name="Postdoctorate in Administrative Sciences").first()
    if record1:
        old_duration = record1.duration_hours
        record1.duration_hours = 96
        db.session.commit()
        html.append(f"""
        <h3>Record 1 Updated: {Markup.escape(record1.name)}</h3>
        <table border="1" cellpadding="6" style="border-collapse:collapse;">
          <tr><th>Field</th><th>Before</th><th>After</th></tr>
          <tr><td>duration_hours</td><td>{old_duration}</td><td>{record1.duration_hours}</td></tr>
        </table>
        """)
    else:
        html.append('<p style="color: red;">Record 1 not found (name: "Postdoctorate in Administrative Sciences")</p>')
    
    # Update record 2: "English B1" - set duration_hours to 210 and description to empty
    record2 = AdvancedTraining.query.filter_by(name="English B1").first()
    if record2:
        old_duration = record2.duration_hours
        old_description = record2.description
        record2.duration_hours = 210
        record2.description = None  # or empty string
        db.session.commit()
        html.append(f"""
        <h3>Record 2 Updated: {Markup.escape(record2.name)}</h3>
        <table border="1" cellpadding="6" style="border-collapse:collapse;">
          <tr><th>Field</th><th>Before</th><th>After</th></tr>
          <tr><td>duration_hours</td><td>{old_duration}</td><td>{record2.duration_hours}</td></tr>
          <tr><td>description</td><td>{Markup.escape(old_description or '(empty)')}</td><td>{Markup.escape(record2.description or '(empty)')}</td></tr>
        </table>
        """)
    else:
        html.append('<p style="color: red;">Record 2 not found (name: "English B1")</p>')
    
    html.append('<p><a href="/admin/database/consulta">Back to database view</a></p>')
    return Markup(''.join(html))
