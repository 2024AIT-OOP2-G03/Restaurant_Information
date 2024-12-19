from flask import Blueprint, render_template, request, redirect, url_for
from models.drink import Drink

# Blueprintの作成
drink_bp = Blueprint('drink', __name__, url_prefix='/drinks')


@drink_bp.route('/')
def list():
    # データ取得
    drinks = Drink.select()
    return render_template('drink_list.html', title='ドリンクメニュー', items=drinks)

@drink_bp.route('/add', methods=['GET', 'POST'])
def add():
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        Drink.create(name=name, price=price)
        return redirect(url_for('drink.list'))
    
    return render_template('drink_add.html')


@drink_bp.route('/edit/<int:drink_id>', methods=['GET', 'POST'])
def edit(drink_id):
    drink = Drink.get_or_none(Drink.id == drink_id)
    if not drink:
        return redirect(url_for('drink.list'))

    if request.method == 'POST':
        drink.name = request.form['name']
        drink.price = request.form['price']
        drink.save()
        return redirect(url_for('drink.list'))

    return render_template('drink_edit.html', drink=drink)
