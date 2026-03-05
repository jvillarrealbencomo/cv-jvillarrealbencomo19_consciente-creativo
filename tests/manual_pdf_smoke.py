import os
from app.services.pdf_generator import PDFGenerator

profile_data = {
    'person': {
        'first_name': 'Javier',
        'last_name': 'Villarreal Bencomo'
    },
    'visible_contacts': {
        'email': 'javier@example.com',
        'phone': '+1 555 123 4567',
        'linkedin_url': 'https://linkedin.com/in/jvillarreal',
        'github_url': 'https://github.com/jvillarreal',
        'personal_url': 'https://javier.example.com'
    },
    'title': 'QA Engineer / Data Quality',
    'summary': 'Quality-focused engineer with experience in test automation, data validation, and building resilient QA processes across web and data platforms. Passionate about continuous improvement and reliable delivery.',
    'work_experience': [
        {
            'job_title': 'QA Engineer',
            'company': 'Tech Corp',
            'location': 'Remote',
            'start_date': '2023-01-01',
            'end_date': None,
            'responsibilities_summary': 'Built and maintained automated test suites for APIs and web UI.',
            'responsibilities_detailed': 'Designed robust test data strategies. Implemented CI/CD test gates. Collaborated with developers to shift-left testing. Reduced regression cycles by 40%.',
            'achievements': 'Introduced parallel test runs, improving feedback time by 60%.',
            'show_responsibilities_summary': True,
            'show_responsibilities_detailed': True,
            'show_achievements': True
        },
        {
            'job_title': 'QA Analyst',
            'company': 'DataCo',
            'location': 'Mexico',
            'start_date': '2021-01-01',
            'end_date': '2022-12-01',
            'responsibilities_summary': 'Led manual and exploratory testing for BI dashboards.',
            'responsibilities_detailed': 'Validated data quality across ETL pipelines. Coordinated UAT. Authored comprehensive test cases and checklists.',
            'achievements': 'Improved defect detection rate by 25% through risk-based testing.',
            'show_responsibilities_summary': True,
            'show_responsibilities_detailed': True,
            'show_achievements': True
        }
    ],
    'technical_tools': {
        'Automation': [{'name': 'Selenium'}, {'name': 'Playwright'}, {'name': 'pytest'}],
        'Data QA': [{'name': 'Great Expectations'}, {'name': 'DBT'}],
        'CI/CD': [{'name': 'GitHub Actions'}, {'name': 'Jenkins'}]
    },
    'education': [
        {'degree': 'B.Sc. Computer Science', 'institution': 'UNAM', 'country': 'MX', 'year_obtained': 2019},
        {'degree': 'Diploma in Data QA', 'institution': 'Online Institute', 'country': 'Remote', 'year_obtained': 2022}
    ],
    'certifications': [
        {'name': 'ISTQB CTFL', 'issuing_organization': 'ISTQB', 'issue_date': '2020-06-01'},
        {'name': 'AWS Cloud Practitioner', 'issuing_organization': 'AWS', 'issue_date': '2021-03-15'}
    ],
    'languages': [
        {'name': 'Spanish', 'level_conversation': 'Native', 'level_reading': 'Native', 'level_writing': 'Native'},
        {'name': 'English', 'level_conversation': 'Professional', 'level_reading': 'Professional', 'level_writing': 'Professional'}
    ]
}

if __name__ == '__main__':
    pdf_bytes = PDFGenerator.generate_cv_pdf(profile_data, 'qa_engineer', auto_optimize=True)
    out_dir = os.path.join('app', 'generated_pdfs')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'smoke_test.pdf')
    with open(out_path, 'wb') as f:
        f.write(pdf_bytes)
    print(f'Wrote: {out_path} ({len(pdf_bytes)} bytes)')
