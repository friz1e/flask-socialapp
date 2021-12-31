from main import db
from passlib.hash import sha256_crypt

friends = db.Table('friends',
                db.Column('user1_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('user2_id', db.Integer, db.ForeignKey('users.id'))
)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)
    friends = db.relationship('Users',
                              secondary=friends,
                              primaryjoin = (friends.c.user1_id == id),
                              secondaryjoin = (friends.c.user2_id == id),
                              lazy='dynamic',)
    posts = db.relationship('Posts', backref="user")

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

def checkCredentials(email, password):
    if db.session.query(db.exists().where(Users.email == email)).scalar():
        passwordDatabase = db.session.query(Users.password).where(Users.email == email).scalar()
        if(sha256_crypt.verify(password, passwordDatabase)):
            return True
        else:
            return False
    else:
        return False

def registerNewUser(name, surname, email, password):
    if db.session.query(db.exists().where(Users.email == email)).scalar():
        return False
    else:
        passwordHash = sha256_crypt.encrypt(password)

        newUser = Users(name, surname, email, passwordHash)
        db.session.add(newUser)
        db.session.commit()
        return True

def addPost(email, content):
    loggedUser = Users.query.filter_by(email = email).first()
    newPost = Posts(content = content, user = loggedUser)
    db.session.add(newPost)
    db.session.commit()

def addFriend(email, id):
    loggedUser = Users.query.filter_by(email = email).first()
    userToBeAdded = Users.query.get(id).first()

    loggedUser.friends.append(userToBeAdded)
    userToBeAdded.friends.append(loggedUser)