from app import create_app
from app.routes.profiles import get_profile_data_dict

app = create_app()
ctx = app.app_context()
ctx.push()

data = get_profile_data_dict(1, 'qa_engineer', include_inactive=True)
print('Export PDF Work Experience Records:')
print(f'Total: {len(data["work_experience"])}')
print()
for i, exp in enumerate(data['work_experience'], 1):
    print(f'{i}. ID {exp["id"]}: {exp["company"][:50]}')
