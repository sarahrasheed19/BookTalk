from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import settings

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = settings.PSQL_URI
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
