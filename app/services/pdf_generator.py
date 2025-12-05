"""
PDF Generator Service
Version 2025 - Generate professional one-page CVs with auto-trimming
"""
from io import BytesIO
from datetime import datetime
from copy import deepcopy


class PDFGenerator:
    """
    Service for generating PDF CVs with WeasyPrint
    """
    
    @staticmethod
    def generate_cv_pdf(profile_data, profile_name, auto_optimize: bool = True):
        """
        Generate a PDF CV from profile data
        
        Args:
            profile_data: Dictionary with all CV data
            profile_name: Profile identifier (qa_analyst, qa_engineer, data_scientist)
            auto_optimize: When True, iteratively trims content/styles to fit one page
            
        Returns:
            bytes: PDF file content
        """
        try:
            from weasyprint import HTML, CSS
            from flask import render_template_string
        except ImportError:
            # WeasyPrint not installed, return placeholder
            return PDFGenerator._generate_placeholder_pdf(profile_data, profile_name)
        
        # Attempt to render with auto-optimization to guarantee one-page output
        working_data = deepcopy(profile_data)
        style_state = {
            'font_pt': 10.0,
            'line_height': 1.4,
            'margin_in': 0.5,
            'section_margin': 15,
        }

        def render_and_measure(data, styles):
            html_content = PDFGenerator._generate_html(data, profile_name)
            css = CSS(string=PDFGenerator._get_pdf_css(
                base_font_pt=styles['font_pt'],
                line_height=styles['line_height'],
                margin_in=styles['margin_in'],
                section_margin=styles['section_margin'],
            ))
            document = HTML(string=html_content).render(stylesheets=[css])
            return document, html_content, css

        try:
            document, html_content, pdf_css = render_and_measure(working_data, style_state)
            page_count = len(document.pages)

            if not auto_optimize or page_count <= 1:
                return document.write_pdf()

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
            return HTML(string=html_content).write_pdf(stylesheets=[pdf_css])
    
    @staticmethod
    def _generate_html(profile_data, profile_name):
        """Generate HTML content for PDF"""
        person = profile_data.get('person', {})
        contacts = profile_data.get('visible_contacts', {})
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>CV - {person.get('first_name', '')} {person.get('last_name', '')}</title>
        </head>
        <body>
            <div class="cv-page">
                <!-- Header -->
                <div class="cv-header">
                    <h1 class="cv-name">{person.get('first_name', '')} {person.get('last_name', '')}</h1>
                    <div class="cv-title">{profile_data.get('title', '')}</div>
                    <div class="cv-contacts">
                        {PDFGenerator._format_contacts(contacts)}
                    </div>
                </div>
                
                <!-- Professional Summary -->
                {PDFGenerator._render_summary(profile_data.get('summary'))}
                
                <!-- Work Experience -->
                {PDFGenerator._render_experiences(profile_data.get('work_experience', []))}
                
                <!-- Technical Skills -->
                {PDFGenerator._render_tools(profile_data.get('technical_tools', {}))}
                
                <!-- Education -->
                {PDFGenerator._render_education(profile_data.get('education', []))}
                
                <!-- Advanced Training & Certifications -->
                {PDFGenerator._render_advanced_training(profile_data.get('advanced_training', []))}
                
                <!-- Languages -->
                {PDFGenerator._render_languages(profile_data.get('languages', []))}
            </div>
        </body>
        </html>
        """
        
        return html
    
    @staticmethod
    def _format_contacts(contacts):
        """Format contact information"""
        parts = []
        if contacts.get('email'):
            parts.append(f"✉ {contacts['email']}")
        if contacts.get('phone'):
            parts.append(f"☎ {contacts['phone']}")
        if contacts.get('linkedin_url'):
            parts.append(f"LinkedIn: {contacts['linkedin_url']}")
        if contacts.get('github_url'):
            parts.append(f"GitHub: {contacts['github_url']}")
        if contacts.get('personal_url'):
            parts.append(f"🌐 {contacts['personal_url']}")
        
        return ' | '.join(parts)
    
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
    def _render_tools(tools_by_category):
        """Render technical tools section"""
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
            provider = item.get('provider', '')
            name = item.get('name', '')
            description = item.get('description', '')
            
            items_html += f"""
            <div class="training-item">
                <strong>{name}</strong> - {provider} {f'({completion_year})' if completion_year else ''}
                {f'<br><span style="font-size: 0.9em; color: #666;">{description}</span>' if description else ''}
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
    def _get_pdf_css(base_font_pt: float = 10.0, line_height: float = 1.4, margin_in: float = 0.5, section_margin: int = 15):
        """Get CSS for PDF generation with tunable typography and spacing"""
        return f"""
        @page {{
            size: letter;
            margin: {margin_in}in;
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {base_font_pt}pt;
            line-height: {line_height};
            color: #212529;
        }}
        
        .cv-page {{
            max-width: 100%;
        }}
        
        .cv-header {{
            border-bottom: 3px solid #0d6efd;
            padding-bottom: 10px;
            margin-bottom: {section_margin}px;
        }}
        
        .cv-name {{
            font-size: {base_font_pt * 2.4:.1f}pt;
            font-weight: bold;
            margin: 0 0 5px 0;
            color: #212529;
        }}
        
        .cv-title {{
            font-size: {base_font_pt * 1.4:.1f}pt;
            color: #6c757d;
            margin: 0 0 8px 0;
        }}
        
        .cv-contacts {{
            font-size: {max(base_font_pt - 1, 8):.1f}pt;
            color: #495057;
        }}
        
        .cv-section {{
            margin-bottom: {section_margin}px;
            page-break-inside: avoid;
        }}
        
        .section-title {{
            font-size: {base_font_pt * 1.3:.1f}pt;
            font-weight: bold;
            color: #0d6efd;
            border-bottom: 2px solid #dee2e6;
            padding-bottom: 3px;
            margin-bottom: 10px;
        }}
        
        .summary-text {{
            margin: 0;
            text-align: justify;
        }}
        
        .exp-item, .edu-item {{
            margin-bottom: 12px;
            page-break-inside: avoid;
        }}
        
        .exp-header, .edu-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }}
        
        .exp-title, .edu-degree {{
            font-weight: bold;
            font-size: {base_font_pt * 1.1:.1f}pt;
        }}
        
        .exp-company, .edu-institution {{
            color: #6c757d;
            font-style: italic;
            font-size: {base_font_pt:.1f}pt;
        }}
        
        .exp-dates, .edu-year {{
            color: #6c757d;
            font-size: {max(base_font_pt - 1, 8):.1f}pt;
            white-space: nowrap;
        }}
        
        .exp-content {{
            margin: 5px 0;
            font-size: {max(base_font_pt - 0.5, 8):.1f}pt;
        }}
        
        .tools-category {{
            margin-bottom: 8px;
            font-size: {max(base_font_pt - 0.5, 8):.1f}pt;
        }}
        
        .cert-item, .lang-item {{
            margin-bottom: 6px;
            font-size: {max(base_font_pt - 0.5, 8):.1f}pt;
        }}
        
        strong {{
            font-weight: 600;
        }}
        """

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
