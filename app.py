from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/finestSelfDev"
mongo = PyMongo(app)



@app.route('/')
def base_redirect():
    return redirect(url_for('aspirations_render'))


@app.route('/aspirations', methods=['GET'])
def aspirations_render():
    main_data = list(mongo.db.aspirations.find({}))  * 20 or []



    return render_template('base.jinja2', page="aspirations", main_data=main_data)


@app.route('/actions', methods=['GET'])
def actions_render():
    return render_template('base.jinja2', page="actions")


if __name__ == "__main__":
    app.run(debug=True)
