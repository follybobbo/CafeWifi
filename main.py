from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def say_hello():

    return "Hello Boy"





if __name__ == "__main__":
    app.run(debug=True)
