from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
         return "<p>Hello HBNB!</p>"

@app.route('/hbnb', strict_slashes=False)
def only_hbnb():
         return "<p>HBNB</p>"

@app.route('/c/<text>', strict_slashes=False)
def show_tex(text):
         spaced_text = text.replace("_", " ")
         return f"<p>C { spaced_text }</p>"

@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def show_pytext(text='is_cool'):
        if text:
                spaced_text = text.replace("_", " ")
                return f"<p>Python { spaced_text }</p>"

@app.route('/number/<int:n>', strict_slashes=False)
def show_num(n):
	if type(n) is int:
		return f"<p>{ n } is a number</p>"

app.run(host="0.0.0.0", port="5000")
