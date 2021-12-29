from main import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)

class Friends(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend1id = db.Column(db.Integer, nullable=False)
    friend2id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)

class FriendsRequest(db.Model):
    __tablename__ = 'friends_requests'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend1id = db.Column(db.Integer, nullable=False)
    friend2id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)

def addNewUser(name, surname, email, password):
    newUser = Users(name, surname, email, password)
    db.session.add(newUser)
    db.session.commit()

