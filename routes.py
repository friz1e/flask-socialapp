from flask import Blueprint, render_template

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