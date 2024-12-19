from peewee import SqliteDatabase
from .db import db
# from .order import Order
from .food import Food
from .drink import Drink
from .customer import Customer
from .reservation import Reservation
from .index import Index

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    # User,
    # Order,
    Food,
    Drink,
    Customer,
    Reservation,
    Index
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()