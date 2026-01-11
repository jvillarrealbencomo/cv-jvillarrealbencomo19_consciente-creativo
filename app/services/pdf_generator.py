"""
PDF Generator Service
Version 2025 - Generate professional one-page CVs with auto-trimming
"""
from io import BytesIO
from datetime import datetime
from copy import deepcopy
import os


class PDFGenerator:
    """
    Service for generating PDF CVs with WeasyPrint
    """
    
    @staticmethod
    def generate_cv_pdf(profile_data, profile_name, auto_optimize: bool = False):
        """
        Generate a PDF CV from profile data
        
        Args:
            profile_data: Dictionary with all CV data
            profile_name: Profile identifier (qa_analyst, qa_engineer, data_scientist)
            auto_optimize: When True, iteratively trims content/styles to fit one page
                          When False, shows all content in multi-page extended format
            
        Returns:
            bytes: PDF file content
        """
        print(f'>>> PDFGenerator.generate_cv_pdf called')
        print(f'>>> auto_optimize: {auto_optimize} (type: {type(auto_optimize)})')
        
        # Use the 2-column sidebar layout for both, but with/without trimming
        return PDFGenerator._generate_sidebar_pdf(profile_data, profile_name, auto_optimize)
    
    @staticmethod
    def _generate_sidebar_pdf(profile_data, profile_name, auto_optimize):
        """Generate 2-column sidebar PDF layout
        
        When auto_optimize=False: Shows all content across multiple pages
        When auto_optimize=True: Trims content to fit ~1 page
        """
        try:
            from weasyprint import HTML, CSS
            from flask import render_template_string
        except ImportError:
            return PDFGenerator._generate_placeholder_pdf(profile_data, profile_name)
        
        working_data = deepcopy(profile_data)
        style_state = {
            'font_pt': 10.0,
            'line_height': 1.4,
            'margin_in': 0.5,
            'section_margin': 15,
        }

        base_dir = os.getcwd()

        def render_and_measure(data, styles):
            html_content = (
                PDFGenerator._generate_split_export_html(data, profile_name)
                if not auto_optimize else
                PDFGenerator._generate_html(data, profile_name)
            )
            css = CSS(string=PDFGenerator._get_pdf_css(
                base_font_pt=styles['font_pt'],
                line_height=styles['line_height'],
                margin_in=styles['margin_in'],
                section_margin=styles['section_margin'],
            ))
            document = HTML(string=html_content, base_url=base_dir).render(stylesheets=[css])
            return document, html_content, css

        try:
            document, html_content, pdf_css = render_and_measure(working_data, style_state)
            page_count = len(document.pages)
            
            print(f'>>> Sidebar PDF: {page_count} pages initially', flush=True)

            # If NOT optimizing, return all content across multiple pages
            if not auto_optimize:
                print(f'>>> Returning full extended PDF with all records (pages={page_count})', flush=True)
                return document.write_pdf()
            
            # If already 1 page or less, no need to optimize
            if page_count <= 1:
                print(f'>>> Already 1 page, returning as-is', flush=True)
                return document.write_pdf()
            
            print(f'>>> Starting optimization to fit ~1 page...', flush=True)

            # Trimming strategy: progressively reduce low-priority content, then typography
            trim_steps = [
                ('hide_advanced_training', lambda d: d.update({'advanced_training': []})),
                ('hide_languages', lambda d: d.update({'languages': []})),
                ('reduce_experience_detail', PDFGenerator._trim_experience_detail),
                ('shorten_summary', PDFGenerator._trim_summary),
                ('compact_tools', PDFGenerator._trim_tools),
                ('reduce_education', PDFGenerator._trim_education),
                ('limit_experiences', PDFGenerator._trim_experience_count),
                ('shrink_font_9_5', lambda _: style_state.update({'font_pt': 9.5})),
                ('tighten_line_height', lambda _: style_state.update({'line_height': 1.35})),
                ('shrink_font_9_0', lambda _: style_state.update({'font_pt': 9.0})),
                ('tighten_sections', lambda _: style_state.update({'section_margin': 12})),
                ('reduce_margins', lambda _: style_state.update({'margin_in': 0.45})),
                ('reduce_margins_more', lambda _: style_state.update({'margin_in': 0.40})),
            ]

            for name, apply_step in trim_steps:
                apply_step(working_data) if 'font' not in name and 'line' not in name and 'section' not in name and 'margin' not in name else apply_step(working_data)
                document, html_content, pdf_css = render_and_measure(working_data, style_state)
                page_count = len(document.pages)
                if page_count <= 1:
                    return document.write_pdf()

            # If still too long, return best-effort last render
            return document.write_pdf()
        except Exception:
            # If optimization fails, fall back to a single render
            html_content = PDFGenerator._generate_html(profile_data, profile_name)
            pdf_css = CSS(string=PDFGenerator._get_pdf_css())
            return HTML(string=html_content, base_url=base_dir).write_pdf(stylesheets=[pdf_css])
    
    @staticmethod
    def _generate_html(profile_data, profile_name):
        """Generate HTML content for PDF - Single page template-based layout"""
        person = profile_data.get('person', {})
        contacts = profile_data.get('visible_contacts', {})

        header_image = ''
        if person.get('profile_image_url'):
            img_url = person.get('profile_image_url')
            if img_url.startswith('/static/'):
                rel_path = img_url.replace('/static/', '', 1)
                abs_path = os.path.join(os.getcwd(), 'app', 'static', rel_path)
                img_src = f"file:///{abs_path.replace(os.sep, '/')}"
            else:
                img_src = img_url
            
            header_image = f"""<img class="sidebar-avatar" src="{img_src}" alt="Profile photo">"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>CV - {person.get('first_name', '')} {person.get('last_name', '')}</title>
        </head>
        <body>
            <div class="cv-page">
                <div class="cv-row">
                    <div class="cv-left-column">
                        {header_image}
                        {PDFGenerator._render_technical_skills_compact(profile_data.get('technical_tools', {}), profile_name)}
                        {PDFGenerator._render_languages_compact(profile_data.get('languages', []))}
                        {PDFGenerator._render_education_compact(profile_data.get('education', []), include_images=False)}
                        {PDFGenerator._render_references_compact(person)}
                        {PDFGenerator._render_contact_compact(contacts)}
                    </div>
                    <div class="cv-right-column">
                        <div class="cv-header-block">
                            <h1 class="cv-name">{person.get('first_name', '')} {person.get('last_name', '')}</h1>
                            <div class="cv-title" style="color: #0d6efd;">{profile_data.get('title', '')}</div>
                            {PDFGenerator._render_summary_compact(profile_data.get('summary'))}
                        </div>
                        {PDFGenerator._render_work_experience_compact(profile_data.get('work_experience', []))}
                        {PDFGenerator._render_advanced_training_compact(profile_data.get('advanced_training', []), include_images=False)}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

    @staticmethod
    def _generate_split_export_html(profile_data, profile_name):
        """Generate HTML for export mode with fixed page order:
        Page 1: Hero + summary
        Page 2: Sidebar sections (skills, languages, education, references, contact)
        Page 3: Work experience
        Page 4: Advanced training & certifications
        """
        person = profile_data.get('person', {})
        contacts = profile_data.get('visible_contacts', {})

        header_image = ''
        if person.get('profile_image_url'):
            img_url = person.get('profile_image_url')
            if img_url.startswith('/static/'):
                rel_path = img_url.replace('/static/', '', 1)
                abs_path = os.path.join(os.getcwd(), 'app', 'static', rel_path)
                img_src = f"file:///{abs_path.replace(os.sep, '/')}"
            else:
                img_src = img_url
            header_image = f"""<img class="sidebar-avatar" src="{img_src}" alt="Profile photo" style="width: 120px; height: auto; margin: 0 auto 8px auto; display: block;">"""

        page1 = f"""
        <div class="cv-page">
            <div class="cv-header-block" style="margin-top: 12px; text-align: center;">
                {header_image}
                <h1 class="cv-name" style="margin-top: 0;">{person.get('first_name', '')} {person.get('last_name', '')}</h1>
                <div class="cv-title" style="color: #0d6efd; margin-bottom:8px;">{profile_data.get('title', '')}</div>
                {PDFGenerator._render_summary_compact(profile_data.get('summary'))}
            </div>
        </div>
        <div class="page-break"></div>
        """

        page2 = f"""
        <div class="cv-page">
            {PDFGenerator._render_technical_skills_compact(profile_data.get('technical_tools', {}), profile_name)}
            {PDFGenerator._render_languages_compact(profile_data.get('languages', []))}
            {PDFGenerator._render_education_compact(profile_data.get('education', []), include_images=True)}
            {PDFGenerator._render_references_compact(person)}
            {PDFGenerator._render_contact_compact(contacts)}
        </div>
        <div class="page-break"></div>
        """

        page3 = f"""
        <div class="cv-page">
            {PDFGenerator._render_work_experience_compact(profile_data.get('work_experience', []))}
        </div>
        <div class="page-break"></div>
        """

        page4 = f"""
        <div class="cv-page">
            {PDFGenerator._render_advanced_training_compact(profile_data.get('advanced_training', []), include_images=True)}
        </div>
        """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>CV - {person.get('first_name', '')} {person.get('last_name', '')}</title>
        </head>
        <body>
            {page1}
            {page2}
            {page3}
            {page4}
        </body>
        </html>
        """
        return html

    @staticmethod
    def _format_date_mmyyyy(date_str):
        """Format dates as Mon YYYY if possible"""
        if not date_str:
            return ''
        try:
            # date_str expected ISO YYYY-MM-DD
            parts = date_str.split('-')
            if len(parts) >= 2:
                year = parts[0]
                month = parts[1]
                months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                m_idx = int(month) - 1
                if 0 <= m_idx < 12:
                    return f"{months[m_idx]} {year}"
            return date_str
        except Exception:
            return date_str

    @staticmethod
    def _split_summary_with_list(summary: str):
        """Split summary into an intro sentence and bullet items if present.
        Looks for a ':' separator and dash-prefixed items.
        """
        if not summary:
            return summary, []

        intro = summary
        items = []

        if ':' in summary:
            intro_part, rest = summary.split(':', 1)
            intro = intro_part.strip() + ':'
            rest = rest.strip()
            if rest:
                # Split on dash markers
                for chunk in rest.split('-'):
                    item = chunk.strip()
                    if item:
                        items.append(item)

        return intro, items
    
    @staticmethod
    def _format_contacts(contacts):
        """Format contact information sorted by international priority"""
        parts = []
        
        # Priority order: Email, LinkedIn, GitHub, CV URL, Phone
        if contacts.get('email'):
            parts.append(f"✉ {contacts['email']}")
        if contacts.get('linkedin_url'):
            parts.append(f"LinkedIn: {contacts['linkedin_url']}")
        if contacts.get('github_url'):
            parts.append(f"GitHub: {contacts['github_url']}")
        if contacts.get('personal_url'):
            parts.append(f"🌐 {contacts['personal_url']}")
        if contacts.get('phone'):
            parts.append(f"☎ {contacts['phone']}")
        
        return ' | '.join(parts)

    @staticmethod
    def _render_references(person):
        """Render reference block if data is present"""
        name = person.get('reference_name') or ''
        company = person.get('reference_company') or ''
        phone = person.get('reference_phone') or ''

        if not any([name, company, phone]):
            return ''

        ref_parts = []
        if name:
            ref_parts.append(name)
        if company:
            ref_parts.append(company)
        if phone:
            ref_parts.append(f"Tel: {phone}")

        ref_text = ' • '.join(ref_parts)
        return f"<div class='cv-references'>Reference: {ref_text}</div>"
    
    @staticmethod
    def _render_summary(summary):
        """Render professional summary section"""
        if not summary:
            return ''
        return f"""
        <div class="cv-section">
            <h2 class="section-title">Professional Summary</h2>
            <p class="summary-text">{summary}</p>
        </div>
        """
    
    @staticmethod
    def _render_experiences(experiences):
        """Render work experience section"""
        if not experiences:
            return ''
        
        items_html = ''
        for exp in experiences:
            start_date = exp.get('start_date', '')
            end_date = exp.get('end_date', 'Present')
            
            content = ''
            if exp.get('show_responsibilities_summary') and exp.get('responsibilities_summary'):
                content += f"<p class='exp-content'>{exp['responsibilities_summary']}</p>"
            if exp.get('show_responsibilities_detailed') and exp.get('responsibilities_detailed'):
                content += f"<p class='exp-content'>{exp['responsibilities_detailed']}</p>"
            if exp.get('show_achievements') and exp.get('achievements'):
                content += f"<p class='exp-content'><strong>Key Achievements:</strong><br>{exp['achievements']}</p>"
            
            items_html += f"""
            <div class="exp-item">
                <div class="exp-header">
                    <div class="exp-left">
                        <div class="exp-title">{exp.get('job_title', '')}</div>
                        <div class="exp-company">{exp.get('company', '')}{' • ' + exp.get('location', '') if exp.get('location') else ''}</div>
                    </div>
                    <div class="exp-dates">{start_date} - {end_date}</div>
                </div>
                {content}
            </div>
            """
        
        return f"""
        <div class="cv-section">
            <h2 class="section-title">Work Experience</h2>
            {items_html}
        </div>
        """
    
    @staticmethod
    def _render_technical_skills_compact(tools_by_category, profile_name):
        """(*) Technical Tools - sorted by display_order, grouped by subcategory for profile"""
        if not tools_by_category:
            return ''
        
        categories_html = ''
        for category, tools in tools_by_category.items():
            tool_names = ', '.join([t.get('name', '') for t in tools])
            categories_html += f"""<div class="compact-skill"><strong>{category}</strong><br>{tool_names}</div>"""
        
        return f"""
        <div class="compact-section">
            <h4 class="compact-heading">TECHNICAL SKILLS</h4>
            {categories_html}
        </div>
        """
    
    @staticmethod
    def _render_education_compact(education_list, include_images=False):
        """(**) Education - degree, year_obtained, institution, country + credential image"""
        if not education_list:
            return ''
        
        items = ''
        for edu in sorted(education_list, key=lambda e: e.get('display_order', 999)):
            degree = edu.get('degree', '')
            year = edu.get('year_obtained', '')
            institution = edu.get('institution', '')
            country = edu.get('country', '')
            
            parts = [
                f"<strong style=\"color: #000;\">{degree}</strong>",
                year,
                institution,
                country,
            ]
            display = '. '.join([str(p) for p in parts if p])
            
            # Add credential image if available and requested
            image_html = ''
            if include_images:
                thumb = edu.get('image_thumbnail_url') or (
                    edu.get('image_url') if (edu.get('image_mime_type') or '').startswith('image/') else None
                )
                if thumb:
                    # Convert relative URLs to file:// URLs
                    if thumb.startswith('/'):
                        abs_path = os.path.join(os.getcwd(), 'app', thumb.lstrip('/'))
                        thumb = f"file:///{abs_path.replace(os.sep, '/')}"
                    image_html = f'<br><img src="{thumb}" alt="Credential" style="max-height: 100px; margin-top: 4px;">'
            
            items += f"""<div class="compact-item">{display}{image_html}</div>"""
        
        return f"""
        <div class="compact-section">
            <h4 class="compact-heading">EDUCATION</h4>
            {items}
        </div>
        """

    @staticmethod
    def _render_languages_compact(languages):
        """Render languages section before education with specified typography"""
        if not languages:
            return ''

        items = ''
        for lang in languages:
            name = lang.get('name', '')
            conv = lang.get('level_conversation', '')
            read = lang.get('level_reading', '')
            write = lang.get('level_writing', '')

            items += (
                f"<div class=\"compact-item language-item\" "
                f"style=\"font-family: Georgia, serif; font-size: 9pt; color: #000;\">"
                f"{name}. Conversational:{conv}. Reading:{read}. Writing:{write}"
                f"</div>"
            )

        return f"""
        <div class="compact-section">
            <h4 class="compact-heading">LANGUAGES</h4>
            {items}
        </div>
        """
    
    @staticmethod
    def _render_work_experience_compact(experiences):
        """(***) Work Experience - formatted by time_block"""
        if not experiences:
            return ''
        
        items_by_block = {}
        
        for exp in experiences:
            block = exp.get('time_block') or 'Other'  # Handle None/empty as 'Other'
            block = block.strip() if block else 'Other'  # Handle whitespace
            if block not in items_by_block:
                items_by_block[block] = []
            items_by_block[block].append(exp)
        
        # Include 'Other' at the end to catch records without time_block
        block_order = ['2021-2025', '2015-2020', '1985-2009', 'Other']
        html = '<div class="compact-section"><h4 class="compact-heading">WORK EXPERIENCE</h4>'
        
        is_first_overall = True
        
        for block in block_order:
            if block not in items_by_block:
                continue
            
            block_items = items_by_block[block]
            
            if block == '2021-2025':
                first_item = is_first_overall
                for exp in block_items:
                    job = exp.get('job_title', '')
                    start = PDFGenerator._format_date_mmyyyy(exp.get('start_date', ''))
                    end = PDFGenerator._format_date_mmyyyy(exp.get('end_date', ''))
                    company = exp.get('company', '')
                    summary = exp.get('responsibilities_summary', '')
                    achievements = exp.get('achievements', '')
                    
                    dates = f"({start} - {end})" if start else ""
                    relevant = f"<strong style='color: #000;'>Relevant: {achievements}</strong>" if achievements else ""

                    intro, bullet_items = PDFGenerator._split_summary_with_list(summary)
                    summary_html = f"<div style='text-align: justify;'>{intro}</div>" if intro else ''
                    if bullet_items:
                        bullets = ''.join(f"<li>{item}</li>" for item in bullet_items)
                        summary_html += f"<ul class='compact-bullets'>{bullets}</ul>"
                    
                    entry_class = "compact-item" if first_item else "compact-item work-entry"
                    html += f"""<div class="{entry_class}"><strong style="color: #0d6efd;">{job}</strong> {dates}<br><strong style="color: #000;">{company}</strong><br>{summary_html}"""
                    if relevant:
                        html += f""" {relevant}"""
                    html += """</div>"""
                    if first_item:
                        is_first_overall = False
                    first_item = False
            
            elif block == '2015-2020':
                first_item = is_first_overall
                for exp in block_items:
                    job = exp.get('job_title', '')
                    start = PDFGenerator._format_date_mmyyyy(exp.get('start_date', ''))
                    end = PDFGenerator._format_date_mmyyyy(exp.get('end_date', ''))
                    company = exp.get('company', '')
                    summary = exp.get('responsibilities_summary', '')
                    achievements = exp.get('achievements', '')
                    
                    dates_str = f"{start} - {end}" if start else ''
                    
                    combined = f"<strong style='color: #000;'>{company}</strong>. {summary}. {achievements}" if achievements else f"<strong style='color: #000;'>{company}</strong>. {summary}."
                    entry_class = "compact-item" if first_item else "compact-item work-entry"
                    html += f"""<div class="{entry_class}"><strong style="color: #0d6efd;">{job}</strong> ({dates_str})<br>{combined}</div>"""
                    if first_item:
                        is_first_overall = False
                    first_item = False
            
            elif block == '1985-2009' or block == 'Other':
                # Handle both historical block and records without time_block
                first_item = is_first_overall
                for exp in block_items:
                    job = exp.get('job_title', '')
                    start = PDFGenerator._format_date_mmyyyy(exp.get('start_date', ''))
                    end = PDFGenerator._format_date_mmyyyy(exp.get('end_date', ''))
                    company = exp.get('company', '')
                    summary = exp.get('responsibilities_summary', '')
                    
                    dates = f"({start} - {end})" if start else ""
                    
                    entry_class = "compact-item" if first_item else "compact-item work-entry"
                    html += f"""<div class="{entry_class}"><strong style="color: #0d6efd;">{job}</strong> {dates}<br><strong style="color: #000;">{company}</strong><br>{summary}</div>"""
                    if first_item:
                        is_first_overall = False
                    first_item = False
        
        html += '</div>'
        return html
    
    @staticmethod
    def _render_advanced_training_compact(training_items, include_images=False):
        """(****) Advanced Training - name, provider, year only + credential image"""
        if not training_items:
            return ''
        
        sorted_items = sorted(training_items, key=lambda x: x.get('display_order', 999))
        items_html = ''
        
        for item in sorted_items:
            # Coalesce None to empty strings and normalize placeholder values
            def norm(v):
                s = (v or '').strip()
                return '' if s.lower() in {'none', 'n/a', 'na', '-', '--'} else s

            name = norm(item.get('name'))
            provider = norm(item.get('provider'))
            year = norm(item.get('completion_date'))
            description = norm(item.get('description'))
            
            # Extract year only
            if year and isinstance(year, str) and '-' in year:
                year = year.split('-')[0]
            elif year and isinstance(year, str):
                year = year[:4]
            
            # Handle display name based on description field
            display_name = f"<strong style='color: #000;'>{name}{(' ' + description) if description else ''}</strong>" if name else ''
            
            # Build parts and filter empties to avoid stray commas/None
            parts = [display_name] if display_name else []
            if provider:
                parts.append(provider)
            if year:
                parts.append(year)
            line = ', '.join(parts)
            
            # Add credential image if available and requested
            image_html = ''
            if include_images:
                thumb = item.get('image_thumbnail_url') or (
                    item.get('image_url') if (item.get('image_mime_type') or '').startswith('image/') else None
                )
                if thumb:
                    # Convert relative URLs to file:// URLs
                    if thumb.startswith('/'):
                        abs_path = os.path.join(os.getcwd(), 'app', thumb.lstrip('/'))
                        thumb = f"file:///{abs_path.replace(os.sep, '/')}"
                    image_html = f'<br><img src="{thumb}" alt="Credential" style="max-height: 100px; margin-top: 4px;">'
            
            items_html += f"""<div class="compact-item">{line}{image_html}</div>"""
        
        return f"""
        <div class="compact-section">
            <h4 class="compact-heading">ADVANCED TRAINING & CERTIFICATIONS</h4>
            {items_html}
        </div>
        """
    
    @staticmethod
    def _render_references_compact(person):
        """Render references in compact format for left column"""
        name = person.get('reference_name') or ''
        company = person.get('reference_company') or ''
        phone = person.get('reference_phone') or ''

        if not any([name, company, phone]):
            return ''

        # Build line 1: Name. Company
        line1 = ''
        if name:
            line1 += name
        if company:
            line1 += ('. ' if line1 else '') + company
        
        # Line 2: Phone
        items = line1
        if phone:
            items += f"<br>{phone}"

        return f"""
        <div class="compact-section">
            <h4 class="compact-heading">REFERENCES</h4>
            <div class="compact-item">{items}</div>
        </div>
        """
    
    @staticmethod
    def _render_contact_compact(contacts):
        """Render contacts in compact format for left column, sorted by international priority"""
        if not contacts:
            return ''
        
        items = ''
        # Priority order: Email, LinkedIn, GitHub, CV URL, Phone
        if contacts.get('email'):
            items += f"""<div class="compact-item">{contacts['email']}</div>"""
        if contacts.get('linkedin_url'):
            items += f"""<div class="compact-item" style="font-size: 8pt; line-height:1.2; word-break: break-all;">{contacts['linkedin_url']}</div>"""
        if contacts.get('github_url'):
            items += f"""<div class="compact-item" style="font-size: 8pt; line-height:1.2; word-break: break-all;">{contacts['github_url']}</div>"""
        if contacts.get('personal_url'):
            items += f"""<div class="compact-item">{contacts['personal_url']}</div>"""
        if contacts.get('phone'):
            items += f"""<div class="compact-item">{contacts['phone']}</div>"""
        
        return f"""
        <div class="compact-section">
            <h4 class="compact-heading">CONTACT</h4>
            {items}
        </div>
        """
    
    @staticmethod
    def _render_summary_compact(summary):
        """Render summary in compact format"""
        if not summary:
            return ''
        return f"""<div class="compact-summary">{summary}</div>"""
    
    @staticmethod
    def _render_tools_sidebar(tools_by_category):
        """Render technical tools section for sidebar"""
        if not tools_by_category:
            return ''
        
        categories_html = ''
        for category, tools in tools_by_category.items():
            tool_names = ', '.join([t.get('name', '') for t in tools])
            categories_html += f"""
            <div class="sidebar-skill-group">
                <strong class="sidebar-skill-category">{category}</strong>
                <div class="sidebar-skill-items">{tool_names}</div>
            </div>
            """
        
        return f"""
        <div class="sidebar-section">
            <h3 class="sidebar-section-title">Technical Skills</h3>
            {categories_html}
        </div>
        """
    
    @staticmethod
    def _render_tools(tools_by_category):
        """Render technical tools section (full-width, for non-sidebar layouts)"""
        if not tools_by_category:
            return ''
        
        categories_html = ''
        for category, tools in tools_by_category.items():
            tool_names = ', '.join([t.get('name', '') for t in tools])
            categories_html += f"""
            <div class="tools-category">
                <strong>{category}:</strong> {tool_names}
            </div>
            """
        
        return f"""
        <div class="cv-section">
            <h2 class="section-title">Technical Skills</h2>
            {categories_html}
        </div>
        """
    
    @staticmethod
    def _render_education(education_list):
        """Render education section"""
        if not education_list:
            return ''
        
        items_html = ''
        for edu in education_list:
            items_html += f"""
            <div class="edu-item">
                <div class="edu-header">
                    <div class="edu-left">
                        <div class="edu-degree">{edu.get('degree', '')}</div>
                        <div class="edu-institution">{edu.get('institution', '')}{' • ' + edu.get('country', '') if edu.get('country') else ''}</div>
                    </div>
                    <div class="edu-year">{edu.get('year_obtained', '') or edu.get('end_year', '')}</div>
                </div>
            </div>
            """
        
        return f"""
        <div class="cv-section">
            <h2 class="section-title">Education</h2>
            {items_html}
        </div>
        """
    
    @staticmethod
    def _render_advanced_training(training_items):
        """Render advanced training & certifications section (unified courses and certifications)"""
        if not training_items:
            return ''
        
        items_html = ''
        for item in training_items:
            completion_year = ''
            if item.get('completion_date'):
                try:
                    completion_year = datetime.fromisoformat(item['completion_date'].replace('Z', '+00:00')).year
                except:
                    pass
            
            # Format based on type
            item_type = item.get('type', 'Course')
            def norm(v):
                s = (v or '').strip()
                return '' if s.lower() in {'none', 'n/a', 'na', '-', '--'} else s
            provider = norm(item.get('provider'))
            name = norm(item.get('name'))
            description = norm(item.get('description'))
            
            # Build line avoiding 'None' and stray separators
            provider_part = f" - {provider}" if provider else ""
            year_part = f" ({completion_year})" if completion_year else ""
            description_part = f"<br><span style=\"font-size: 0.9em; color: #666;\">{description}</span>" if description else ""

            items_html += f"""
            <div class="training-item">
                <strong>{name}</strong>{provider_part}{year_part}
                {description_part}
            </div>
            """
        
        return f"""
        <div class="cv-section">
            <h2 class="section-title">Advanced Training & Certifications</h2>
            {items_html}
        </div>
        """
    
    @staticmethod
    def _render_languages(languages):
        """Render languages section"""
        if not languages:
            return ''
        
        items_html = ''
        for lang in languages:
            levels = []
            if lang.get('level_conversation'):
                levels.append(f"Speaking: {lang['level_conversation']}")
            if lang.get('level_reading'):
                levels.append(f"Reading: {lang['level_reading']}")
            if lang.get('level_writing'):
                levels.append(f"Writing: {lang['level_writing']}")
            
            items_html += f"""
            <div class="lang-item">
                <strong>{lang.get('name', '')}</strong>: {' • '.join(levels)}
            </div>
            """
        
        return f"""
        <div class="cv-section">
            <h2 class="section-title">Languages</h2>
            {items_html}
        </div>
        """
    
    @staticmethod
    def _get_pdf_css(base_font_pt: float = 9.0, line_height: float = 1.2, margin_in: float = 0.4, section_margin: int = 8):
        """Get CSS for single-page template layout"""
        template = """
        @page {{
            size: letter;
            margin: {margin_in}in;
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {base_font_pt}pt;
            line-height: {line_height};
            color: #000;
            margin: 0;
            padding: 0;
        }}
        
        .cv-page {{
            max-width: 100%;
        }}
        
        .cv-row {{
            position: relative;
            width: 100%;
            min-height: 100%;
            clear: both;
        }}
        
        .cv-left-column {{
            position: absolute;
            left: 0;
            top: 90px;
            width: 35%;
            padding: 8px 10px 6px 0;
            font-size: {font_left}pt;
            box-sizing: border-box;
        }}
        
        .cv-right-column {{
            margin-left: 35%;
            width: 65%;
            padding: 4px 0 6px 6px;
            font-size: {font_right}pt;
            box-sizing: border-box;
            min-height: 100%;
        }}

        /* Cap inline images (e.g., education/certifications thumbnails) */
        .cv-page img {{
            max-height: 100px;
            height: auto;
        }}

        .page-break {{
            page-break-after: always;
        }}
        
        .sidebar-avatar {{
            width: 80%;
            height: auto;
            margin: 0 auto 8px auto;
            display: block;
        }}
        
        .compact-section {{
            margin-bottom: 8px;
            page-break-inside: avoid;
        }}
        
        .compact-heading {{
            font-size: 10pt;
            font-weight: bold;
            border-bottom: 1px solid #000;
            padding-bottom: 2px;
            margin: 0 0 4px 0;
            color: #0d6efd;
        }}
        
        .compact-item {{
            font-size: {item_size}pt;
            margin-bottom: 3px;
            line-height: 1.15;
        }}

        .compact-bullets {{
            margin: 4px 0 0 14px;
            padding: 0;
        }}
        .compact-bullets li {{
            margin-bottom: 2px;
        }}

        .work-entry {{
            margin-top: 10px;
        }}
        
        .compact-skill {{
            font-size: {item_size}pt;
            margin-bottom: 2px;
        }}
        
        .compact-summary {{
            font-size: {summary_size}pt;
            line-height: 1.3;
            margin: 0 auto 8px auto;
            text-align: justify;
        }}
        
        .cv-header-block {{
            text-align: center;
            margin-bottom: 8px;
        }}

        .cv-name {{
            font-size: {name_size}pt;
            font-weight: bold;
            margin: 0 0 2px 0;
            color: #0d6efd;
            line-height: 1.05;
        }}
        
        .cv-title {{
            font-size: {title_size}pt;
            color: #333;
            margin: 0 0 4px 0;
            font-weight: 600;
            line-height: 1.05;
        }}
        
        strong {{
            font-weight: 700;
        }}
        """

        return template.format(
            margin_in=margin_in,
            base_font_pt=base_font_pt,
            line_height=line_height,
            font_left=round(base_font_pt * 0.9, 1),
            font_right=round(base_font_pt, 1),
            heading_size=round(base_font_pt * 1.1, 1),
            item_size=round(base_font_pt * 0.85, 1),
            summary_size=round(base_font_pt, 1),
            name_size=round(base_font_pt * 3.2, 1),
            title_size=round(base_font_pt * 2.2, 1),
        )

    # --------- Trimming helpers ---------
    @staticmethod
    def _trim_experience_detail(data: dict):
        """Reduce verbosity of experience: hide detailed responsibilities and achievements."""
        experiences = data.get('work_experience') or []
        for exp in experiences:
            if 'show_responsibilities_detailed' in exp:
                exp['show_responsibilities_detailed'] = False
            if 'show_achievements' in exp:
                exp['show_achievements'] = False
        return data

    @staticmethod
    def _trim_experience_count(data: dict, keep: int = 3):
        """Keep only the first N experiences, preserving existing sort order."""
        exps = data.get('work_experience') or []
        data['work_experience'] = exps[:keep]
        return data

    @staticmethod
    def _trim_summary(data: dict, max_chars: int = 350):
        """Shorten summary text to a reasonable character limit preserving words."""
        summary = data.get('summary')
        if not summary:
            return data
        if len(summary) <= max_chars:
            return data
        trimmed = summary[:max_chars].rsplit(' ', 1)[0] + '…'
        data['summary'] = trimmed
        return data

    @staticmethod
    def _trim_tools(data: dict, max_categories: int = 5, max_tools_per_cat: int = 6):
        """Limit number of tool categories and tools per category."""
        tools = data.get('technical_tools') or {}
        limited = {}
        for i, (cat, items) in enumerate(tools.items()):
            if i >= max_categories:
                break
            limited[cat] = items[:max_tools_per_cat]
        data['technical_tools'] = limited
        return data

    @staticmethod
    def _trim_education(data: dict, keep: int = 2):
        """Keep only the most recent education entries."""
        items = data.get('education') or []
        def sort_key(e):
            return e.get('year_obtained') or e.get('end_year') or 0
        items_sorted = sorted(items, key=sort_key, reverse=True)
        data['education'] = items_sorted[:keep]
        return data
    
    @staticmethod
    def _generate_placeholder_pdf(profile_data, profile_name):
        """Generate a simple placeholder PDF when WeasyPrint is not available"""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        person = profile_data.get('person', {})
        name = f"{person.get('first_name', '')} {person.get('last_name', '')}"
        
        c.setFont("Helvetica-Bold", 24)
        c.drawString(72, 720, name)
        
        c.setFont("Helvetica", 14)
        c.drawString(72, 695, profile_data.get('title', 'Professional'))
        
        c.setFont("Helvetica", 10)
        y = 670
        c.drawString(72, y, "This is a placeholder PDF.")
        y -= 20
        c.drawString(72, y, "Install WeasyPrint for full PDF generation:")
        y -= 15
        c.drawString(72, y, "pip install weasyprint")
        
        c.showPage()
        c.save()
        
        buffer.seek(0)
        return buffer.getvalue()
