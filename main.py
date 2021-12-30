from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes import routes

app = Flask(__name__)

app.register_blueprint(routes)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)