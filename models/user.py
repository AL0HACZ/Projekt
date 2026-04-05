from datetime import datetime

from . import db

user_groups = db.Table('user_groups',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
                       )

group_categories = db.Table('group_categories',
                            db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                            db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                            )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    about_me = db.Column(db.Text, default="")
    groups = db.relationship('Group', secondary=user_groups, backref='users')


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(256))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    categories = db.relationship('Category', secondary=group_categories, backref='admin_groups')
