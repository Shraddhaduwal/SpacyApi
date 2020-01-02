from flask import Flask, send_file
from flask_restful import Api

from resources.spacy_resources import Data, AllData
from data_visualization import visualize

# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init Api
api = Api(app)


@app.before_first_request  # It is required to create a table first because db does not create one for us
def create_tables():
    db.create_all()


@app.route('/plot/<string:csv_filename>')  # For plotting the data
def plotting(csv_filename):
    try:
        bytes_obj = visualize(csv_filename)

        return send_file(bytes_obj,
                         attachment_filename='plot.png',
                         mimetype='image/png')
    except Exception:
        return {'message': f'{csv_filename} is empty'}


api.add_resource(Data, '/data/<string:text_id>')
api.add_resource(AllData, '/alldata')
# /data refers to root class that is Data and /data/<string:text_id> refers to the text we send from postman


# Run the server
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(debug=True)
