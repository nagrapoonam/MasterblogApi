#import for rendering HTML templates in a Flask application
from flask import Flask, render_template

#Initializing a Flask application instance
app = Flask(__name__)

#route for handling HTTP GET requests to the root URL ("/") of the Flask application
@app.route('/', methods=['GET'])
def home():
    """ function renders the "index.html" template and returns the rendered HTML as a response."""
    return render_template("index.html")

#runs the Flask application when the Python script is executed directly,
# starting the server on host="0.0.0.0" and port=5002 with debug mode enabled.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
