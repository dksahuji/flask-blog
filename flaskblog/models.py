from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import expression

#from __main__ import db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#each class is a table in db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True, passive_deletes=True)#passive_deletes=True
    #comments = db.relationship('Comment', backref='author', lazy=True, passive_deletes=True)
    posts = db.relationship('Post', backref='author', passive_deletes=True)
    comments = db.relationship('Comment', backref='author', passive_deletes=True)

    def get_reset_token(self, expires_sec=1800): # in seconds
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    abstract = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_original = db.Column(db.Text, nullable=False)
    type_select = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    tags_life = db.Column(db.Boolean, default=False, nullable=False)
    tags_inspiration = db.Column(db.Boolean, default=False, nullable=False)
    tags_philosophy = db.Column(db.Boolean, default=False, nullable=False)
    tags_personalfinance = db.Column(db.Boolean, default=False, nullable=False)
    tags_ml = db.Column(db.Boolean, default=False, nullable=False)
    tags_quotes = db.Column(db.Boolean, default=False, nullable=False)
    tags_technology = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    #comments = db.relationship('Comment', backref='post', passive_deletes=True)
    comments = db.relationship('Comment', backref='post', passive_deletes=True, order_by=Comment.__table__.columns.date_posted)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"




