from flask import Flask, jsonify
from noticias import buscar

app = Flask(__name__)

@app.route("/")
def mensaje():
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)
