from flask import Blueprint, render_template, request, redirect, url_for
from models.food import Food

# Blueprintの作成
food_bp = Blueprint('food', __name__, url_prefix='/foods')

@food_bp.route('/')
def list():
    # データ取得
    foods = Food.select()
    return render_template('food_list.html', title='フードメニュー', items=foods)

@food_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        Food.create(name=name, price=price)
        return redirect(url_for('food.list'))
    
    return render_template('food_add.html')


@food_bp.route('/edit/<int:food_id>', methods=['GET', 'POST'])
def edit(food_id):
    food = Food.get_or_none(Food.id == food_id)
    if not food:
        return redirect(url_for('food.list'))

    if request.method == 'POST':
        food.name = request.form['name']
        food.price = request.form['price']
        food.save()
        return redirect(url_for('food.list'))

    return render_template('food_edit.html', food=food)
