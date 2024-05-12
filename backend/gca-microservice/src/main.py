from flask import request, url_for
from flask_api import FlaskAPI

app = FlaskAPI(__name__)

@app.route("/get_answer", methods=["Post"])
def getAnswer():
    """
    Returns "Hello World!"
    """
    return {"hello": "world"}

if __name__ == "__main__":
    app.run(debug=True)