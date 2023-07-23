from flask import Flask
"""A flas application"""


app = Flask(__name__)
"""Flask application instance"""
app.url_map.strict_slashes = False


@app.route("/")
def hello_hbnb():
    return "<p>Hello HBNB!</p>"

@app.route("/hbnb")
def only_hbnb():
	return "<p>HBNB</p>"


@app.route('/c/<text>')
def show_tex(text):
	spaced_text = text.replace("_", " ")
	return f"<p>C { spaced_text }</p>"


@app.route('/python')
@app.route('/python/<text>')
def show_pytext(text='is_cool'):
	if text:
		spaced_text = text.replace("_", " ")
		return f"<p>Python { spaced_text }</p>"


if __name__ == '__main__':
	app.run(host="0.0.0.0", port="5000")
