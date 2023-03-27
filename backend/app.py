import json

from flask import Flask, jsonify, Response
from flask_cors import CORS, cross_origin

from .get_humanact import get_humanact
from .data_collect import get_windspeedgrid

app = Flask(__name__)
CORS(app, support_credentials=True)

data_munitions = get_humanact("munitions").to_crs("EPSG:4326")
data_platforms = get_humanact("platforms").to_crs("EPSG:4326")
data_windfarms = get_humanact("windfarmspoly").to_crs("EPSG:4326")


@app.route('/munitions')
@cross_origin(supports_credentials=True)
def get_munitions() -> Response:
    res = data_munitions
    return res.to_json()


@app.route('/platforms')
@cross_origin(supports_credentials=True)
def get_platforms() -> Response:
    res = data_platforms
    return res.to_json()


@app.route('/windfarms')
@cross_origin(supports_credentials=True)
def get_windfarms() -> Response:
    res = data_windfarms
    return res.to_json()


@app.route('/windspeed')
@cross_origin(supports_credentials=True)
def get_windspeed() -> Response:
    windspeed = get_windspeedgrid()[0]
    return windspeed


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
