from flask import Blueprint, render_template, url_for, request

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/loginPage')
def loginPage():
    return render_template('loginPage.html')

@routes.route('/registerPage')
def registerPage():
    return render_template('registerPage.html')

@routes.route('/mainPage')
def mainPage():
    return render_template('mainPage.html')

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

@routes.route('/registerUser', methods=['POST', 'GET'])
def registerUser():
    from models import registerNewUser

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        import re

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('registerPage.html', error="Given email doesnt contain required element!")

        if (containsNumber(name) is True) or (containsNumber(surname) is True):
            return render_template('registerPage.html', error="Given name or surname has digits!")

        if(registerNewUser(name,surname,email,password)):
           return render_template(url_for('routes.loginPage'))
        else:
            return render_template('registerPage.html', error="User with given email already exists!")