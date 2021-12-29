from main import db
from passlib.hash import sha256_crypt

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

class Friends(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend1id = db.Column(db.Integer, nullable=False)
    friend2id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)

    def __init__(self, friend1id, friend2id):
        self.friend1id = friend1id
        self.friend2id = friend2id

class FriendsRequest(db.Model):
    __tablename__ = 'friends_requests'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend1id = db.Column(db.Integer, nullable=False)
    friend2id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)

    def __init__(self, friend1id, friend2id):
        self.friend1id = friend1id
        self.friend2id = friend2id

#def checkCredentials(email, password):

def registerNewUser(name, surname, email, password):
    if db.session.query(db.exists().where(Users.email==email)).scalar():
        return False
    else:
        passwordHash = sha256_crypt.encrypt(password)

        newUser = Users(name, surname, email, passwordHash)
        db.session.add(newUser)
        db.session.commit()
        return True

