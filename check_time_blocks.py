from app import create_app, db
from app.models.work_experience import WorkExperience

app = create_app()
ctx = app.app_context()
ctx.push()

exps = WorkExperience.query.order_by(WorkExperience.id).all()
print('Work Experience Time Blocks:')
print('=' * 60)

blocks = {}
for e in exps:
    block = e.time_block or 'None'
    if block not in blocks:
        blocks[block] = []
    blocks[block].append(e.id)

for block in sorted(blocks.keys()):
    ids = blocks[block]
    print(f'{block}: {len(ids)} records - IDs {ids}')

print('\nDetailed list:')
for e in exps:
    print(f"ID {e.id}: {e.company[:40]:40} | time_block=[{e.time_block}]")
