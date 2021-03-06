from flask import Blueprint, render_template, url_for, request, redirect, session

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/loginPage')
def loginPage():
    if session.get('email') == None:
        return render_template('loginPage.html')
    else:
        return redirect(url_for('routes.mainPage'))

@routes.route('/registerPage')
def registerPage():
    if session.get('email') == None:
        return render_template('registerPage.html')
    else:
        return redirect(url_for('routes.mainPage'))

@routes.route('/mainPage')
def mainPage():
    if session.get('email') != None:
        from models import getUser, getFriendsPropositions, getRequestsToShow
        user = getUser(session.get('email'))
        friendsPropositions = getFriendsPropositions(session.get('email'))
        friendsSentRequests = getRequestsToShow(session.get('email'), "sent")
        friendsPendingRequests = getRequestsToShow(session.get('email'), "pending")

        return render_template('mainPage.html', user = user, friends = user.friends, pending_friends_requests = friendsPendingRequests, sent_friends_requests = friendsSentRequests, friends_propositions = friendsPropositions)
    else:
        return redirect(url_for('routes.loginPage'))

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

@routes.route('/registerUser', methods=['POST', 'GET'])
def registerUser():
    if session.get('email') == None:
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']

            import re

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return render_template('registerPage.html', error="Given email doesnt contain required elements!")

            if (containsNumber(name) is True) or (containsNumber(surname) is True):
                return render_template('registerPage.html', error="Given name or surname has digits!")

            from models import registerNewUser
            if(registerNewUser(name,surname,email,password)):
               return redirect(url_for('routes.loginPage'))
            else:
                return render_template('registerPage.html', error="User with given email already exists!")
        else:
            return redirect(url_for('routes.registerPage'))
    else:
        return redirect(url_for('routes.mainPage'))

@routes.route('/checkCredentials', methods=['POST', 'GET'])
def checkCredentials():
    if session.get('email') == None:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            import re

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return redirect(url_for('routes.loginPage'))
            else:
                from models import checkCredentials
                if(checkCredentials(email, password)):
                    session['email'] = email
                    return redirect(url_for('routes.mainPage'))
                else:
                    return redirect(url_for('routes.loginPage'))
        else:
            return redirect(url_for('routes.loginPage'))
    else:
        return redirect(url_for('routes.mainPage'))

@routes.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('routes.loginPage'))

@routes.route('/addPost', methods=['POST', 'GET'])
def addPost():
    if session.get('email') != None:
        if request.method == 'POST':
            content = request.form['content']

            from models import addPost
            addPost(session.get('email'), content)
            return redirect(url_for('routes.mainPage'))
        else:
            return redirect(url_for('routes.mainPage'))
    else:
        return redirect(url_for('routes.loginPage'))

@routes.route('/deletePost/<id>', methods=['GET'])
def deletePost(id):
    if session.get('email') != None:
        from models import deletePost
        deletePost(id)
        return redirect(url_for('routes.mainPage'))
    else:
        return redirect(url_for('routes.mainPage'))

@routes.route('/sendFriendsRequest/<id>', methods=['GET'])
def sendFriendsRequest(id):
    if session.get('email') != None:
        from models import friendsRequestOperations
        friendsRequestOperations(session.get('email'), id, 'send')
        return redirect(url_for('routes.mainPage'))
    else:
        return redirect(url_for('routes.loginPage'))

@routes.route('/acceptFriendsRequest/<id>', methods=['GET'])
def acceptFriendsRequest(id):
    if session.get('email') != None:
        from models import friendsRequestOperations
        try:
            if friendsRequestOperations(session.get('email'), id, 'accept'):
                addFriend(session.get('email'), id)
                return redirect(url_for('routes.mainPage'))
        except TypeError:
            return redirect(url_for('routes.mainPage'))
        else:
            return redirect(url_for('routes.mainPage'))
    else:
        return redirect(url_for('routes.mainPage'))


@routes.route('/declineFriendsRequest/<id>', methods=['GET'])
def declineFriendsRequest(id):
    if session.get('email') != None:
        from models import friendsRequestOperations
        if friendsRequestOperations(session.get('email'), id, 'decline'):
            return redirect(url_for('routes.mainPage'))
        else:
            return redirect(url_for('routes.mainPage'))
    else:
        return redirect(url_for('routes.loginPage'))

@routes.route('/addFriend/<id>', methods=['GET'])
def addFriend(id):
    if session.get('email') != None:
        if request.method == 'GET':
            from models import addFriend
            addFriend(session.get('email'), id)
            return redirect(url_for('routes.mainPage'))
        else:
            return redirect(url_for('routes.mainPage'))
    else:
        return redirect(url_for('routes.loginPage'))

@routes.route('/deleteFriend/<id>', methods=['GET'])
def deleteFriend(id):
    if session.get('email') != None:
        if request.method == 'GET':
            from models import deleteFriend
            deleteFriend(session.get('email'), id)
            return redirect(url_for('routes.mainPage'))
        else:
            return redirect(url_for('routes.mainPage'))
    else:
        return redirect(url_for('routes.loginPage'))
