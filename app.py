from flask import Flask
from flask_restful import Api
from db import db

from resources.spacy_resources import Data, AllData
from models.spacy_models import DataModel

# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init Api
api = Api(app)


@app.before_first_request  # It is required to create a table first because db does not create one for us
def create_tables():
    db.create_all()


api.add_resource(Data, '/data/<string:text_id>')
api.add_resource(AllData, '/alldata')
# /data refers to root class that is Data and /data/<string:text_id> refers to the text we send from postman


# Run the server
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(debug=True)
