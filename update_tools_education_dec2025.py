"""
Update TechnicalTool and Education records - December 2025
"""
from app import create_app, db
from app.models import TechnicalTool, Education

app = create_app()

with app.app_context():
    print("\n=== Updating TechnicalTool Records ===\n")
    
    # Update TechnicalTool record 1
    tool1 = db.session.get(TechnicalTool, 1)
    if tool1:
        old_name = tool1.name
        tool1.name = "JIRA, Xray, Jenkins, Confluence, Postman, SoapUI, Control-M, DataStage, Cyberark, SonarQube, Excel, GNU Make"
        print(f"Record 1:")
        print(f"  Before: {old_name}")
        print(f"  After:  {tool1.name}\n")
    else:
        print("❌ TechnicalTool record 1 not found\n")
    
    # Update TechnicalTool record 5
    tool5 = db.session.get(TechnicalTool, 5)
    if tool5:
        old_name = tool5.name
        tool5.name = "Python (Flask, Jupyter), Java, C++, PHP, Visual Basic"
        print(f"Record 5:")
        print(f"  Before: {old_name}")
        print(f"  After:  {tool5.name}\n")
    else:
        print("❌ TechnicalTool record 5 not found\n")
    
    print("\n=== Updating Education Records ===\n")
    
    # Update Education record 1
    edu1 = db.session.get(Education, 1)
    if edu1:
        old_institution = edu1.institution
        edu1.institution = "USM"
        print(f"Record 1:")
        print(f"  Before: {old_institution}")
        print(f"  After:  {edu1.institution}\n")
    else:
        print("❌ Education record 1 not found\n")
    
    # Update Education record 2
    edu2 = db.session.get(Education, 2)
    if edu2:
        old_institution = edu2.institution
        edu2.institution = "ULA"
        print(f"Record 2:")
        print(f"  Before: {old_institution}")
        print(f"  After:  {edu2.institution}\n")
    else:
        print("❌ Education record 2 not found\n")
    
    # Update Education record 3
    edu3 = db.session.get(Education, 3)
    if edu3:
        old_institution = edu3.institution
        edu3.institution = "UNERMB"
        print(f"Record 3:")
        print(f"  Before: {old_institution}")
        print(f"  After:  {edu3.institution}\n")
    else:
        print("❌ Education record 3 not found\n")
    
    # Commit all changes
    db.session.commit()
    print("✅ All records updated successfully!")
