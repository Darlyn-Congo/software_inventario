from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal, InvalidOperation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'  # Replace with a secure key in production

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=False, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(128), nullable=True)
    unit = db.Column(db.String(64), nullable=True)
    quantity = db.Column(db.Float, nullable=False)
    unit_value = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Item {self.code} - {self.description}>'


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/assign', methods=['GET', 'POST'])
def assign():
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        unit = request.form.get('unit', '').strip()
        quantity_raw = request.form.get('quantity', '0')
        unit_value_raw = request.form.get('unit_value', '0')

        # Basic validation
        if not code or not description:
            flash('Código y Descripción son campos obligatorios', 'danger')
            return redirect(url_for('assign'))

        try:
            quantity = float(quantity_raw)
            unit_value = float(unit_value_raw)
        except ValueError:
            flash('Cantidad y Valor Unitario deben ser números válidos', 'danger')
            return redirect(url_for('assign'))

        total_value = quantity * unit_value

        item = Item(code=code, description=description, category=category, unit=unit,
                    quantity=quantity, unit_value=unit_value, total_value=total_value)
        db.session.add(item)
        db.session.commit()

        flash('Artículo asignado con éxito', 'success')
        return redirect(url_for('tracking'))

    # GET
    return render_template('assign.html')


@app.route('/tracking')
def tracking():
    items = Item.query.order_by(Item.assigned_at.desc()).all()
    return render_template('tracking.html', items=items)


@app.route('/item/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Artículo eliminado', 'success')
    return redirect(url_for('tracking'))


@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.code = request.form.get('code', item.code)
        item.description = request.form.get('description', item.description)
        item.category = request.form.get('category', item.category)
        item.unit = request.form.get('unit', item.unit)
        try:
            item.quantity = float(request.form.get('quantity', item.quantity))
            item.unit_value = float(request.form.get('unit_value', item.unit_value))
        except ValueError:
            flash('Cantidad y Valor Unitario deben ser números válidos', 'danger')
            return redirect(url_for('edit_item', item_id=item_id))
        item.total_value = item.quantity * item.unit_value
        db.session.commit()
        flash('Artículo actualizado', 'success')
        return redirect(url_for('tracking'))
    return render_template('edit_item.html', item=item)


if __name__ == '__main__':
    app.run(debug=True)
