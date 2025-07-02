from flask import Flask, jsonify
import numpy as np
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api/graph_data')
def graph_data():
    x = np.linspace(0, 10, 100)
    data = {
        "x": x.tolist(),
        "y1": np.sin(x).tolist(),
        "y2": np.cos(x).tolist()
    }
    return jsonify(data)

@app.route('/api/3d_data')
def data_3d():
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = 10 * np.outer(np.cos(u), np.sin(v)).tolist()
    y = 10 * np.outer(np.sin(u), np.sin(v)).tolist()
    z = 10 * np.outer(np.ones_like(u), np.cos(v)).tolist()
    return jsonify({"x": x, "y": y, "z": z})

@app.route('/api/sine_wave')
def sine_wave():
    x = np.linspace(0, 10, 100)
    y = np.sin(x).tolist()
    return jsonify({"x": x.tolist(), "y": y})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
