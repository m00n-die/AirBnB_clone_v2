from flask import Flask
"""A flas application"""


app = Flask(__name__)
"""Flask application instance"""
app.url_map.strict_slashes = False


@app.route("/")
def hello_hbnb():
    return "<p>Hello HBNB!</p>"


@app.route("/hbnb", strict_slashes=False)
def only_hbnb():
    return "<p>HBNB</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
