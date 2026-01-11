#!/usr/bin/env python3
"""
Quick script to view all Work Experience and Advanced Training records
Shows all fields and visibility settings
"""
from app import create_app, db
from app.models import WorkExperience, AdvancedTraining
from datetime import datetime

def print_table(data, title):
    """Simple table printer without tabulate"""
    if not data:
        print(f"No {title} records found.")
        return
    
    print(f"\n{title}:")
    print("-" * 150)
    
    # Get headers
    headers = list(data[0].keys())
    col_widths = {h: max(len(str(h)), max(len(str(row[h])) for row in data)) for h in headers}
    
    # Print header
    header_row = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
    print(header_row)
    print("-" * len(header_row))
    
    # Print rows
    for row in data:
        row_vals = [str(row[h]) for h in headers]
        row_str = " | ".join(f"{v:<{col_widths[h]}}" for h, v in zip(headers, row_vals))
        print(row_str)

app = create_app()

with app.app_context():
    print("=" * 150)
    print("WORK EXPERIENCE & ADVANCED TRAINING RECORDS VIEW")
    print("=" * 150)
    
    work_records = WorkExperience.query.all()
    if work_records:
        work_data = []
        for w in work_records:
            work_data.append({
                'ID': w.id,
                'Active': w.active,
                'Company': w.company[:20],
                'Job Title': w.job_title[:20],
                'Location': w.location or '-',
                'Start': w.start_date.strftime('%Y-%m-%d') if w.start_date else '',
                'End': w.end_date.strftime('%Y-%m-%d') if w.end_date else ('Current' if w.is_current else ''),
                'QA-Ana': w.visible_qa_analyst,
                'QA-Eng': w.visible_qa_engineer,
                'Data-Sci': w.visible_data_scientist,
                'Summary': w.show_responsibilities_summary,
                'Detailed': w.show_responsibilities_detailed,
                'Achieve': w.show_achievements,
                'Order': w.display_order
            })
        print_table(work_data, "WORK EXPERIENCE RECORDS")
    else:
        print("No work experience records found.")
    
    print("\n" + "=" * 150)
    
    training_records = AdvancedTraining.query.all()
    if training_records:
        training_data = []
        for t in training_records:
            training_data.append({
                'ID': t.id,
                'Active': t.active,
                'Type': t.type,
                'Name': t.name[:30],
                'Provider': t.provider[:20],
                'Completion': t.completion_date.strftime('%Y-%m-%d') if t.completion_date else '',
                'Expires': t.expiration_date.strftime('%Y-%m-%d') if t.expiration_date else '',
                'Cred-ID': t.credential_id[:15] if t.credential_id else '-',
                'Image': 'YES' if t.image_filename else 'NO',
                'QA-Ana': t.visible_qa_analyst,
                'QA-Eng': t.visible_qa_engineer,
                'Data-Sci': t.visible_data_scientist,
                'Order': t.display_order
            })
        print_table(training_data, "ADVANCED TRAINING RECORDS")
    
    print("\n" + "=" * 120)
    print("VISIBILITY LEGEND")
    print("=" * 120)
    print("""
QA Analyst:      Visible in QA Analyst profile (one_page optimization applies)
QA Engineer:     Visible in QA Engineer profile (one_page optimization applies)
Data Scientist:  Visible in Data Scientist profile (one_page optimization applies)

Work Experience Visibility Details:
  - Show Summary:     One-line job description (minimal visibility)
  - Show Detailed:    Full detailed responsibilities
  - Show Achievements: Key achievements/results

When exporting:
  - "Export PDF" (one_page: false) → Shows ALL content regardless of visibility flags
  - "One-Page PDF" (one_page: true)  → Trims content based on visibility flags to fit ~1 page
  
To make records appear in full export but NOT in one-page:
  1. Mark as "visible" for your profile (QA Analyst/Engineer/Data Scientist)
  2. They will appear in both "Export PDF" and "One-Page PDF"
  3. One-Page PDF will trim them first if space is needed
    """)
    
    print("\n" + "=" * 120)
    print("SUMMARY")
    print("=" * 120)
    print(f"Work Experience Records: {len(work_records)} (Active: {len([w for w in work_records if w.active])})")
    print(f"Advanced Training Records: {len(training_records)} (Active: {len([t for t in training_records if t.active])})")
