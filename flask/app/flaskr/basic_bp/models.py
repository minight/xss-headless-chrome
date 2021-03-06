from flask import current_app
from ..app import db
import secrets

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.Text(), index=True)
    password = db.Column(db.Text(), index=True)
    role = db.Column(db.Text())
    description = db.Column(db.Text())

def populate():
    if User.query.filter_by(id=1).first():
        return

    user = User(username="admin", password=current_app.config.get("ADMIN_PASSWORD"), role="admin")
    db.session.add(user)
    db.session.commit()


