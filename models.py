from app import db, login_manager
from flask_login import UserMixin

# Association table for many-to-many relationship between users and groups
user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    groups = db.relationship('Group', secondary=user_group, backref=db.backref('members', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    prompts = db.relationship('Prompt', backref='group', lazy=True)

    def __repr__(self):
        return f'<Group {self.name}>'

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    responses = db.relationship('Response', backref='prompt', lazy=True)

    def __repr__(self):
        return f'<Prompt {self.content}>'

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Response {self.answer[:20]}...>'
