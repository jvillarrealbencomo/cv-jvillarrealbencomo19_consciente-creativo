from app import create_app, db
from app.models.advanced_training import AdvancedTraining

app = create_app()
app.app_context().push()

records = AdvancedTraining.query.filter_by(active=True).order_by(AdvancedTraining.id).all()
print('\nAdvanced Training Records:')
print('=' * 80)
for r in records:
    img_status = r.image_filename if r.image_filename else 'No image'
    print(f'ID {r.id}: "{r.name}"')
    print(f'  Type: {r.type}')
    print(f'  Image: {img_status}')
    if r.image_path:
        print(f'  Path: {r.image_path}')
    print()
