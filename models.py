from main import db
from passlib.hash import sha256_crypt

friends = db.Table('friends',
                db.Column('user1_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('user2_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('created_at', db.TIMESTAMP, server_default=db.func.now(), nullable=False)
)

friends_requests = db.Table('friends_requests',
                db.Column('user1_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('user2_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('sent_by', db.String),
                db.Column('created_at', db.TIMESTAMP, server_default=db.func.now(), nullable=False)
)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), nullable=False)
    friends_requests = db.relationship('Users',
                             secondary=friends_requests,
                             primaryjoin=(friends_requests.c.user1_id == id),
                             secondaryjoin=(friends_requests.c.user2_id == id),
                             lazy='dynamic')
    friends = db.relationship('Users',
                              secondary=friends,
                              primaryjoin=(friends.c.user1_id == id),
                              secondaryjoin=(friends.c.user2_id == id),
                              lazy='dynamic')
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

def getUserId(email):
    user = Users.query.filter_by(email=email).first()
    return user.id

def getUser(email):
    user = Users.query.filter_by(email = email).first()
    return user

def addPost(email, content):
    loggedUser = Users.query.filter_by(email = email).first()
    newPost = Posts(content = content, user = loggedUser)
    db.session.add(newPost)
    db.session.commit()

def friendsRequestOperations(email, id, typeOfOperation):
    loggedUser = Users.query.filter_by(email=email).first()
    userOperationIsExecutedOn = Users.query.get(id)

    if typeOfOperation == "send":
        if loggedUser is None or userOperationIsExecutedOn is None:
            return False
        else:
            if db.session.query(friends.c.user1_id, friends.c.user2_id).filter_by(user1_id=loggedUser.id,
                                                                                  user2_id=userOperationIsExecutedOn .id).first() is None:
                if db.session.query(friends_requests.c.user1_id, friends_requests.c.user2_id).filter_by(
                        user1_id=loggedUser.id, user2_id=userOperationIsExecutedOn .id).first() is None:
                    loggedUserRow = friends_requests.insert().values(user1_id=loggedUser.id, user2_id=userOperationIsExecutedOn .id,
                                                                     sent_by=email)
                    userRequestedRow = friends_requests.insert().values(user1_id=userOperationIsExecutedOn .id,
                                                                        user2_id=loggedUser.id, sent_by=email)

                    db.session.execute(loggedUserRow)
                    db.session.execute(userRequestedRow)
                    db.session.commit()
                    return True
                else:
                    return False
            else:
                return False
    elif typeOfOperation == "accept":
        if db.session.query(friends.c.user1_id, friends.c.user2_id).filter_by(user1_id=loggedUser.id,
                                                                              user2_id=userOperationIsExecutedOn .id).first() is None:
            if db.session.query(friends_requests.c.user1_id, friends_requests.c.user2_id).filter_by(
                    user1_id=loggedUser.id, user2_id=userOperationIsExecutedOn .id).first() is not None:
                addFriend(email, id)
                db.session.query(friends_requests).filter_by(user1_id=loggedUser.id, user2_id=userOperationIsExecutedOn .id).delete()
                db.session.query(friends_requests).filter_by(user1_id=userOperationIsExecutedOn .id, user2_id=loggedUser.id).delete()

                db.session.commit()
                return True
            else:
                return False
        else:
            return False
    elif typeOfOperation == "decline":
        if db.session.query(friends.c.user1_id, friends.c.user2_id).filter_by(user1_id=loggedUser.id,
                                                                              user2_id=userOperationIsExecutedOn .id).first() is None:
            if db.session.query(friends_requests.c.user1_id, friends_requests.c.user2_id).filter_by(
                    user1_id=loggedUser.id, user2_id=userOperationIsExecutedOn .id).first() is not None:
                db.session.query(friends_requests).filter_by(user1_id=loggedUser.id, user2_id=userOperationIsExecutedOn.id).delete()
                db.session.query(friends_requests).filter_by(user1_id=userOperationIsExecutedOn .id, user2_id=loggedUser.id).delete()
                db.session.commit()
                return True
            else:
                return False
        else:
            return False
    else:
        return None

def addFriend(email, id):
    loggedUser = Users.query.filter_by(email = email).first()
    userToBeAdded = Users.query.get(id)

    loggedUser.friends.append(userToBeAdded)
    userToBeAdded.friends.append(loggedUser)

    db.session.commit()

def deleteFriend(email, id):
    loggedUser = Users.query.filter_by(email = email).first()
    userToBeAdded = Users.query.get(id)

    loggedUser.friends.remove(userToBeAdded)
    userToBeAdded.friends.remove(loggedUser)

    db.session.commit()

def getFriendsPropositions(email):
    loggedUser = Users.query.filter_by(email=email).first()

    idsList = []

    users = db.session.query(Users).filter(Users.id != loggedUser.id).all()

    for i in range(len(users)):
        idsList.append(users[i].id)

    import random
    random.shuffle(idsList)
    userObjectsList = []

    for i in range(len(idsList)):
        if db.session.query(friends_requests).filter((friends_requests.c.user1_id == loggedUser.id) & (friends_requests.c.user2_id == idsList[i])).first() is None:
            if db.session.query(friends).filter((friends.c.user1_id == loggedUser.id) & (friends.c.user2_id == idsList[i])).first() is None:
                userObjectsList.append(Users.query.filter_by(id=idsList[i]).first())
            else:
                continue

    return userObjectsList

def getRequestsToShow(email, type):
    if type == "sent":
        query = db.session.query(friends_requests.c.user2_id).filter(
            (friends_requests.c.sent_by != email) & (friends_requests.c.user1_id == getUserId(email))).all()

        db.session.commit()

        idsList = []

        for i in range(len(query)):
            idsList.append(query[i].user2_id)

        userObjectsList = []

        for i in range(len(idsList)):
            userObjectsList.append(Users.query.filter_by(id=idsList[i]).first())

        return userObjectsList
    elif type == "pending":
        query = db.session.query(friends_requests.c.user2_id).filter((friends_requests.c.sent_by==email)&(friends_requests.c.user1_id==getUserId(email))).all()
        db.session.commit()

        idsList = []

        for i in range(len(query)):
            idsList.append(query[i].user2_id)

        userObjectsList = []

        for i in range(len(idsList)):
            userObjectsList.append(Users.query.filter_by(id=idsList[i]).first())

        return userObjectsList
    else:
        return None