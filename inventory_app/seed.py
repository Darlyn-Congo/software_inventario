from app import db, Item, app

# Añadir algunos artículos de ejemplo
items = [
    Item(code='A001', description='Mouse USB', category='Periféricos', unit='unidad', quantity=10, unit_value=15.0, total_value=150.0),
    Item(code='A002', description='Teclado mecánico', category='Periféricos', unit='unidad', quantity=5, unit_value=50.0, total_value=250.0),
    Item(code='A003', description='Monitor 24"', category='Monitores', unit='unidad', quantity=3, unit_value=120.0, total_value=360.0),
]

with app.app_context():
    # Ensure tables are created
    db.create_all()
    for it in items:
        db.session.add(it)
    try:
        db.session.commit()
        print('Seed data added.')
    except Exception as e:
        print('Error adding seed data:', e)
