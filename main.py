from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/add")
def add_place():

    return render_template("add.html")

@app.route("/city")
def show_venue():

    return render_template("show-venue.html")




if __name__ == "__main__":
    app.run(debug=True)
