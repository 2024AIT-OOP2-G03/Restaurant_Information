from flask import Blueprint, render_template, request, redirect, url_for
from models.reservation import Reservation
from models.food import Food
from models.drink import Drink
from models.customer import Customer

# Blueprintの作成
reservation_bp = Blueprint('reservation', __name__, url_prefix='/reservations')

@reservation_bp.route('/')
def list():
    # データ取得
    reservations = Reservation.select()
    return render_template('reservation_list.html', title='予約リスト', items=reservations)

#予約の追加
@reservation_bp.route('/add', methods=['GET', 'POST'])
def add():
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        # 必須項目を検証
        customer_id = request.form.get('customer_id')
        food_id = request.form.get('food_id')
        drink_id = request.form.get('drink_id')
        Reservation.create(customer=customer_id, food=food_id, drink=drink_id)
        return redirect(url_for('reservation.list'))
    
    customers = Customer.select()
    foods = Food.select()
    drinks = Drink.select()
    return render_template('reservation_add.html', customers=customers, foods=foods, drinks=drinks)

#予約の編集
@reservation_bp.route('/edit/<int:reservation_id>', methods=['GET', 'POST'])
def edit(reservation_id):
    reservation = Reservation.get_or_none(Reservation.id == reservation_id)
    if not reservation:
        return redirect(url_for('reservation.list'))

    if request.method == 'POST':
        reservation.customer_id = request.form['customer_id']
        reservation.food_id = request.form['food_id']
        reservation.drink_id = request.form['drink_id']
        reservation.save()
        return redirect(url_for('reservation.list'))

    customers = Customer.select()
    foods = Food.select()
    drinks = Drink.select()
    return render_template('reservation_edit.html', reservation=reservation, customers=customers, foods=foods, drinks=drinks)