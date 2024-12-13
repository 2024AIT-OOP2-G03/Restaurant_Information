from peewee import Model, ForeignKeyField
from .db import db
from .customer import Customer
from .food import Food
from .drink import Drink

class Reservation(Model):
    customer = ForeignKeyField(Customer, backref='reservations')
    food = ForeignKeyField(Food, backref='reservations')
    drink = ForeignKeyField(Drink, backref='reservations')

    class Meta:
        database = db