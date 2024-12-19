from peewee import Model, ForeignKeyField ,CharField, IntegerField
from .db import db


class Index(Model):
    menuName = CharField()
    sumPrice = IntegerField()

    class Meta:
        database = db