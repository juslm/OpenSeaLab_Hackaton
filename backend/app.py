import json

from flask import Flask, jsonify, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

zones = [
    {
        "id": '1',
        "name": 'Zone 1 name',
        "area": '12345',
        "polygon": [[51.604185, 2.674773],
                    [51.241534, 2.652383],
                    [51.080872, 1.566426],
                    [51.306570, 1.570184],
                    [51.554536, 2.160120]]
    },
    {
        "id": '2',
        "name": 'Zone 2 name',
        "area": '12345',
        "polygon": [[52.923565, 4.237541],
                    [53.695897, 2.914547],
                    [53.731058, 4.764185]],
    },
    {
        "id": '3',
        "name": 'Zone 3 name',
        "area": '12345',
        "polygon": [[52.931184, 2.013089],
                    [52.891607, 2.686011],
                    [53.455049, 1.610033]]
    },
]


@app.route('/zones')
@cross_origin(supports_credentials=True)
def get_zones() -> Response:
    return jsonify(zones)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
