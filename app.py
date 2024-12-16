from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models import Customer
from models import Reservation
from peewee import fn

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    total_num_people = int(Customer.select(fn.SUM(Customer.numPeople)).scalar() or 0)
    total_sum_price = sum([reservation.food.price + reservation.drink.price for reservation in Reservation.select()])
    if total_num_people > 0:
        average_price_per_person = total_sum_price / total_num_people
    else:
        average_price_per_person = 0

    return render_template('index.html', total_num_people=total_num_people, average_price_per_person=average_price_per_person)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
