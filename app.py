from flask import Flask, render_template
from models import initialize_database
from models import Customer
from routes import blueprints
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
    return render_template('index.html', total_num_people=total_num_people)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
