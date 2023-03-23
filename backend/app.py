import json

from flask import Flask, jsonify, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

persons = [
  {
    "id": '1',
    "name": 'Luke Skywalker',
    "height": '172',
    "mass": '77',
    "hair_color": 'blond',
    "skin_color": 'fair',
    "eye_color": 'blue',
    "gender": 'male',
  },
  {
    "id": '2',
    "name": 'C-3PO',
    "height": '167',
    "mass": '75',
    "hair_color": 'n/a',
    "skin_color": 'gold',
    "eye_color": 'yellow',
    "gender": 'n/a',
  },
  {
    "id": '3',
    "name": 'R2-D2',
    "height": '96',
    "mass": '32',
    "hair_color": 'n/a',
    "skin_color": 'white, blue',
    "eye_color": 'red',
    "gender": 'n/a',
  },
  {
    "id": '4',
    "name": 'Darth Vader',
    "height": '202',
    "mass": '136',
    "hair_color": 'none',
    "skin_color": 'white',
    "eye_color": 'yellow',
    "gender": 'male',
  },
]


@app.route('/hello')
@cross_origin(supports_credentials=True)
def get_songs() -> Response:
    return jsonify(persons)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
