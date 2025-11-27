"""
PDF Generator Service
One-page PDF generation for different CV profiles
"""
import os
from datetime import datetime
from weasyprint import HTML, CSS
from flask import render_template
from config import config


class PDFGenerator:
    """Generate professional one-page PDF CVs"""
    
    def __init__(self):
        """Initialize PDF generator"""
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated_pdfs')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_profile_pdf(self, data, profile_title):
        """
        Generate a one-page PDF for a specific profile
        
        Args:
            data (dict): Profile data including personal_data, experience, etc.
            profile_title (str): Profile name (e.g., 'QA Analyst')
        
        Returns:
            str: Path to generated PDF
        """
        # Filter only items marked as visible_in_summary
        filtered_data = self._filter_for_summary(data)
        
        # Render HTML template
        html_content = render_template(
            'pdf/cv_template.html',
            profile_title=profile_title,
            **filtered_data,
            generation_date=datetime.now().strftime('%B %d, %Y')
        )
        
        # Generate PDF filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_profile = profile_title.replace(' ', '_').lower()
        pdf_filename = f'CV_{safe_profile}_{timestamp}.pdf'
        pdf_path = os.path.join(self.output_dir, pdf_filename)
        
        # CSS for one-page optimization
        css_content = self._get_pdf_css()
        
        # Generate PDF with WeasyPrint
        HTML(string=html_content).write_pdf(
            pdf_path,
            stylesheets=[CSS(string=css_content)]
        )
        
        return pdf_path
    
    def _filter_for_summary(self, data):
        """
        Filter data to include only items with visible_in_summary=True
        
        Args:
            data (dict): Full profile data
        
        Returns:
            dict: Filtered data
        """
        filtered = data.copy()
        
        # Filter lists
        if 'education' in filtered:
            filtered['education'] = [e for e in filtered['education'] if e.visible_in_summary]
        
        if 'experience' in filtered:
            filtered['experience'] = [e for e in filtered['experience'] if e.visible_in_summary]
        
        if 'products' in filtered:
            filtered['products'] = [p for p in filtered['products'] if p.visible_in_summary]
        
        if 'certifications' in filtered:
            filtered['certifications'] = [c for c in filtered['certifications'] if c.visible_in_summary]
        
        if 'courses' in filtered:
            filtered['courses'] = [c for c in filtered['courses'] if c.visible_in_summary]
        
        if 'languages' in filtered:
            filtered['languages'] = [l for l in filtered['languages'] if l.visible_in_summary]
        
        if 'tools_by_category' in filtered:
            filtered_tools = {}
            for category, tools in filtered['tools_by_category'].items():
                visible_tools = [t for t in tools if t.visible_in_summary]
                if visible_tools:
                    filtered_tools[category] = visible_tools
            filtered['tools_by_category'] = filtered_tools
        
        return filtered
    
    def _get_pdf_css(self):
        """
        Get CSS optimized for one-page PDF
        
        Returns:
            str: CSS content
        """
        return """
        @page {
            size: Letter;
            margin: 0.5in;
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 9pt;
            line-height: 1.3;
            color: #333;
        }
        
        h1 {
            font-size: 18pt;
            margin: 0 0 4pt 0;
            color: #2c3e50;
        }
        
        h2 {
            font-size: 11pt;
            margin: 6pt 0 3pt 0;
            padding-bottom: 2pt;
            border-bottom: 1px solid #3498db;
            color: #2c3e50;
        }
        
        h3 {
            font-size: 10pt;
            margin: 3pt 0 2pt 0;
            color: #34495e;
        }
        
        p {
            margin: 2pt 0;
        }
        
        ul {
            margin: 2pt 0;
            padding-left: 15pt;
        }
        
        li {
            margin: 1pt 0;
        }
        
        .header {
            text-align: center;
            margin-bottom: 8pt;
            padding-bottom: 6pt;
            border-bottom: 2px solid #3498db;
        }
        
        .contact-info {
            font-size: 8pt;
            color: #666;
        }
        
        .section {
            margin-bottom: 6pt;
        }
        
        .job-title, .degree-title {
            font-weight: bold;
            font-size: 9.5pt;
        }
        
        .company, .institution {
            font-style: italic;
            color: #666;
        }
        
        .date-range {
            font-size: 8pt;
            color: #999;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 4pt;
            font-size: 8pt;
        }
        
        .compact-list {
            margin: 2pt 0;
            font-size: 8.5pt;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        """
    
    def estimate_content_size(self, data):
        """
        Estimate if content will fit on one page
        
        Args:
            data (dict): Profile data
        
        Returns:
            dict: Estimation metrics
        """
        estimation = {
            'sections': 0,
            'total_items': 0,
            'estimated_lines': 0,
            'fits_one_page': False
        }
        
        # Count items
        estimation['total_items'] += len(data.get('education', []))
        estimation['total_items'] += len(data.get('experience', []))
        estimation['total_items'] += len(data.get('certifications', []))
        estimation['total_items'] += len(data.get('courses', []))
        
        # Rough line estimation (adjust based on testing)
        estimation['estimated_lines'] = estimation['total_items'] * 4  # Average 4 lines per item
        
        # One page ~= 55-60 lines with 9pt font
        estimation['fits_one_page'] = estimation['estimated_lines'] <= 55
        
        return estimation
