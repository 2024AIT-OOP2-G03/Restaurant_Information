from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
#棒グラフ用
from models import Customer
from models.index import Index
from models.reservation import Reservation
from models.food import Food
from models.drink import Drink
from peewee import fn


app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def home():

    # グラフ用計算処理
    indexdata = list()
    # 累計客数の算出
    total_num_people = int(Customer.select(fn.SUM(Customer.numPeople)).scalar() or 0)
    #
    
    total_sum_price = sum([reservation.food.price + reservation.drink.price for reservation in Reservation.select()])
    if total_num_people > 0:
        average_price_per_person = total_sum_price / total_num_people
    else:
        average_price_per_person = 0
        
    #全ての予約の合計金額の表示 
    total_price_sum = sum(reservation.food.price + reservation.drink.price for reservation in Reservation)
    # データリストをhtmlに送って遷移
    return render_template('index.html', indexdata=indexdata, total_num_people= total_num_people,
                           average_price_per_person=average_price_per_person,total_price_sum=total_price_sum)

def list():
    # リスト初期化
    Index.delete().execute()
    # 各種データ取得
    reservations = Reservation.select()
    foods = Food.select()
    drinks = Drink.select()

    #データ整理
    #商品ごとの総額
    menu_totals = {}
    # foodデータ
    calculate_totals(reservations,foods, menu_totals)
    # drinkデータ
    calculate_totals(reservations,drinks, menu_totals)

    # menu_totalsをIndexテーブルに保存
    for menu_name, sum_price in menu_totals.items():
        Index.create(
            menuName=menu_name, 
            sumPrice=sum_price,
            )

    # JSON変換用に辞書形式でデータを返す
    return [
        {"menuName": index.menuName, "sumPrice": index.sumPrice}
        for index in Index.select()
    ]

def calculate_totals(reservations,items, menu_totals):
    # 商品登録
    for item in items:
        menu_totals[item.name] = 0
    
    # 売上計算
    for reservation in reservations:
        for item in items:
            #food
            if reservation.food.name == item.name:
                menu_totals[item.name] += item.price  # 売上加算
            #drink
            if reservation.drink.name == item.name:
                menu_totals[item.name] += item.price  # 売上加算

if __name__ == '__main__':
    app.run(port=8080, debug=True)
