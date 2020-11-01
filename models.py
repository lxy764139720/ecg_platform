from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(20), nullable=False)

    __tablename__ = 'user'

    def __repr__(self):
        return "<User> id:" + str(self.id) + "username:" + self.username + \
               "phone:" + self.phone + "password:" + self.password
