"""
Database Initialization and Seed Data Script
Run this to create tables and populate with sample data
"""
import sys
import os
from datetime import date, datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import (PersonalData, Education, WorkExperience, ITProduct,
                        Certification, Course, Language, SupportTool)


def init_database():
    """Initialize database and create all tables"""
    app = create_app('development')
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")
        
        # Check if data already exists
        if PersonalData.query.first():
            print("⚠ Database already contains data. Skipping seed data.")
            return
        
        print("\nSeeding database with sample data...")
        seed_data()
        print("✓ Seed data added successfully")


def seed_data():
    """Populate database with sample data"""
    
    # Personal Data
    personal = PersonalData(
        full_name="Juan Villarreal Bencomo",
        professional_title="QA Engineer | Data Analyst | Software Developer",
        email="jvillarreal@example.com",
        phone="+1 (555) 123-4567",
        location="Caracas, Venezuela",
        summary="Experienced QA professional with strong background in test automation, data analysis, and software development. Proven track record in implementing quality assurance processes and delivering high-quality software solutions.",
        summary_short="QA Engineer with 8+ years of experience in test automation, data analysis, and agile methodologies.",
        url_personal="https://jvillarreal.dev",
        url_github="https://github.com/jvillarrealbencomo",
        url_linkedin="https://linkedin.com/in/jvillarrealbencomo",
        show_link="all",
        active=True,
        visible_in_summary=True
    )
    db.session.add(personal)
    
    # Education
    education1 = Education(
        degree="Bachelor's Degree in Computer Science",
        institution="Universidad Central de Venezuela",
        location="Caracas, Venezuela",
        start_date=date(2010, 9, 1),
        end_date=date(2015, 7, 15),
        description="Focus on software engineering, algorithms, and data structures",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=8,
        relevance_qa_engineer=9,
        relevance_data_scientist=9,
        display_order=1
    )
    
    education2 = Education(
        degree="Master's in Data Science",
        institution="Online University",
        location="Online",
        start_date=date(2020, 1, 1),
        end_date=date(2022, 6, 30),
        description="Advanced studies in machine learning, statistics, and big data analytics",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=5,
        relevance_qa_engineer=6,
        relevance_data_scientist=10,
        display_order=2
    )
    
    db.session.add_all([education1, education2])
    
    # Work Experience
    work1 = WorkExperience(
        job_title="Senior QA Engineer",
        company="Tech Solutions Inc.",
        location="Remote",
        start_date=date(2020, 3, 1),
        is_current=True,
        description="Lead QA initiatives for enterprise applications",
        functions="Design and execute test plans, implement automation frameworks, mentor junior QA engineers, collaborate with development teams in agile sprints",
        highlighted_aspect="Reduced testing time by 60% through comprehensive test automation using Selenium and Python",
        show_detail="both",
        technologies="Python, Selenium, pytest, Jenkins, Git, Jira, SQL",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=9,
        relevance_qa_engineer=10,
        relevance_data_scientist=6,
        display_order=1
    )
    
    work2 = WorkExperience(
        job_title="QA Analyst",
        company="Software Corp",
        location="Caracas, Venezuela",
        start_date=date(2017, 6, 1),
        end_date=date(2020, 2, 28),
        description="Quality assurance for web and mobile applications",
        functions="Manual and automated testing, bug tracking, requirements analysis, test case documentation",
        highlighted_aspect="Improved bug detection rate by 45% through systematic test coverage analysis",
        show_detail="aspect",
        technologies="Selenium, Java, TestNG, Postman, MySQL",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=10,
        relevance_qa_engineer=8,
        relevance_data_scientist=4,
        display_order=2
    )
    
    work3 = WorkExperience(
        job_title="Junior Developer",
        company="StartupXYZ",
        location="Caracas, Venezuela",
        start_date=date(2015, 8, 1),
        end_date=date(2017, 5, 31),
        description="Full-stack development for startup projects",
        functions="Develop features using Python/Flask, database design, API integration, code reviews",
        highlighted_aspect="Built REST API serving 10k+ daily requests with 99.9% uptime",
        show_detail="functions",
        technologies="Python, Flask, PostgreSQL, JavaScript, HTML/CSS",
        active=True,
        visible_in_summary=False,
        relevance_qa_analyst=5,
        relevance_qa_engineer=7,
        relevance_data_scientist=7,
        display_order=3
    )
    
    db.session.add_all([work1, work2, work3])
    
    # IT Products
    product1 = ITProduct(
        name="Test Automation Framework",
        description="Custom Python-based test automation framework for web applications",
        role="Lead Developer",
        technologies="Python, Selenium, pytest, Docker, CI/CD",
        start_date=date(2021, 1, 1),
        end_date=date(2021, 6, 30),
        project_url="https://github.com/jvillarrealbencomo/test-framework",
        github_url="https://github.com/jvillarrealbencomo/test-framework",
        impact_description="Adopted by 5 teams, reducing test execution time by 70%",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=8,
        relevance_qa_engineer=10,
        relevance_data_scientist=5,
        display_order=1
    )
    
    product2 = ITProduct(
        name="Data Quality Dashboard",
        description="Real-time dashboard for monitoring data quality metrics",
        role="Full Stack Developer",
        technologies="Python, Flask, PostgreSQL, Chart.js, Docker",
        start_date=date(2022, 3, 1),
        is_current=True,
        project_url="https://github.com/jvillarrealbencomo/dq-dashboard",
        github_url="https://github.com/jvillarrealbencomo/dq-dashboard",
        impact_description="Monitors 50+ data pipelines, detecting anomalies in real-time",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=6,
        relevance_qa_engineer=7,
        relevance_data_scientist=10,
        display_order=2
    )
    
    db.session.add_all([product1, product2])
    
    # Certifications
    cert1 = Certification(
        name="ISTQB Certified Tester Foundation Level",
        issuing_organization="ISTQB",
        issue_date=date(2018, 5, 15),
        credential_id="ISTQB-12345",
        comment="Fundamental certification for QA professionals covering test design and execution",
        visible_comment=True,
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=10,
        relevance_qa_engineer=9,
        relevance_data_scientist=3,
        display_order=1
    )
    
    cert2 = Certification(
        name="AWS Certified Cloud Practitioner",
        issuing_organization="Amazon Web Services",
        issue_date=date(2021, 11, 20),
        expiration_date=date(2024, 11, 20),
        credential_url="https://aws.amazon.com/verification",
        comment="Validates cloud computing knowledge for modern DevOps practices",
        visible_comment=False,
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=6,
        relevance_qa_engineer=8,
        relevance_data_scientist=7,
        display_order=2
    )
    
    cert3 = Certification(
        name="Professional Scrum Master I",
        issuing_organization="Scrum.org",
        issue_date=date(2019, 3, 10),
        credential_url="https://scrum.org/certificates",
        comment="Demonstrates understanding of Scrum framework and agile principles",
        visible_comment=True,
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=8,
        relevance_qa_engineer=9,
        relevance_data_scientist=6,
        display_order=3
    )
    
    db.session.add_all([cert1, cert2, cert3])
    
    # Courses
    course1 = Course(
        name="Advanced Test Automation with Python",
        provider="Udemy",
        completion_date=date(2020, 7, 15),
        duration_hours=40,
        skills_acquired="Selenium WebDriver, pytest, Page Object Model, CI/CD integration",
        comment="Comprehensive course covering modern test automation practices",
        visible_comment=False,
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=9,
        relevance_qa_engineer=10,
        relevance_data_scientist=4,
        display_order=1
    )
    
    course2 = Course(
        name="Machine Learning A-Z",
        provider="Coursera",
        completion_date=date(2021, 12, 10),
        duration_hours=60,
        skills_acquired="Python, scikit-learn, TensorFlow, pandas, numpy, data preprocessing",
        comment="Foundational ML course with hands-on projects",
        visible_comment=True,
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=4,
        relevance_qa_engineer=5,
        relevance_data_scientist=10,
        display_order=2
    )
    
    course3 = Course(
        name="API Testing Masterclass",
        provider="Test Automation University",
        completion_date=date(2019, 9, 20),
        duration_hours=25,
        skills_acquired="REST APIs, Postman, Newman, API security testing, performance testing",
        comment="In-depth coverage of API testing strategies",
        visible_comment=False,
        active=True,
        visible_in_summary=False,
        relevance_qa_analyst=9,
        relevance_qa_engineer=9,
        relevance_data_scientist=5,
        display_order=3
    )
    
    db.session.add_all([course1, course2, course3])
    
    # Languages
    lang1 = Language(
        name="Spanish",
        level="Native",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=10,
        relevance_qa_engineer=10,
        relevance_data_scientist=10,
        display_order=1
    )
    
    lang2 = Language(
        name="English",
        level="C1 - Advanced",
        certification_name="TOEFL",
        certification_score="105/120",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=10,
        relevance_qa_engineer=10,
        relevance_data_scientist=10,
        display_order=2
    )
    
    lang3 = Language(
        name="Portuguese",
        level="B1 - Intermediate",
        active=True,
        visible_in_summary=True,
        relevance_qa_analyst=5,
        relevance_qa_engineer=5,
        relevance_data_scientist=5,
        display_order=3
    )
    
    db.session.add_all([lang1, lang2, lang3])
    
    # Support Tools / Technical Skills
    tools_data = [
        ("Programming Language", "Python", "Expert", 8),
        ("Programming Language", "SQL", "Advanced", 7),
        ("Programming Language", "JavaScript", "Intermediate", 4),
        ("Programming Language", "Java", "Intermediate", 3),
        ("Framework", "Selenium WebDriver", "Expert", 8),
        ("Framework", "pytest", "Expert", 7),
        ("Framework", "Flask", "Advanced", 6),
        ("Framework", "Django", "Intermediate", 3),
        ("Database", "PostgreSQL", "Advanced", 6),
        ("Database", "MySQL", "Advanced", 5),
        ("Database", "MongoDB", "Intermediate", 3),
        ("Tool", "Git", "Advanced", 8),
        ("Tool", "Docker", "Advanced", 5),
        ("Tool", "Jenkins", "Advanced", 4),
        ("Tool", "Jira", "Advanced", 7),
        ("Tool", "Postman", "Expert", 6),
        ("Methodology", "Agile/Scrum", "Expert", 7),
        ("Methodology", "Test-Driven Development", "Advanced", 5),
        ("Cloud", "AWS", "Intermediate", 3),
        ("Data Science", "pandas", "Advanced", 4),
        ("Data Science", "NumPy", "Advanced", 4),
        ("Data Science", "scikit-learn", "Intermediate", 2),
    ]
    
    for i, (category, name, level, years) in enumerate(tools_data, 1):
        tool = SupportTool(
            category=category,
            name=name,
            proficiency_level=level,
            years_experience=years,
            active=True,
            visible_in_summary=True,
            # Set relevance based on category
            relevance_qa_analyst=9 if category in ["Tool", "Framework", "Methodology"] else 6,
            relevance_qa_engineer=10 if category in ["Framework", "Tool", "Programming Language"] else 7,
            relevance_data_scientist=10 if category in ["Data Science", "Programming Language"] else 5,
            display_order=i
        )
        db.session.add(tool)
    
    # Commit all changes
    db.session.commit()
    print("\n✓ Sample data created:")
    print(f"  - Personal Data: 1 record")
    print(f"  - Education: 2 records")
    print(f"  - Work Experience: 3 records")
    print(f"  - IT Products: 2 records")
    print(f"  - Certifications: 3 records")
    print(f"  - Courses: 3 records")
    print(f"  - Languages: 3 records")
    print(f"  - Technical Skills: {len(tools_data)} records")


if __name__ == '__main__':
    init_database()
