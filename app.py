from flask import Flask, render_template, request, jsonify, session, url_for, g, redirect


from flask import Flask, render_template, request

import nltk
import numpy as np
import json
# import random
# from nltk.stem import WordNetLemmatizer
# from keras.models import Sequential, load_model


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='Chinmay_god', password='acromai'))

users.append(User(id=3, username='Carlos', password='somethingsimple'))

i = 0
app = Flask(__name__)
#
app.secret_key = "ninjahattori"
query = []
data1 = json.load(open("static/data/query.json"))
@app.get("/")
def index_get():
    return render_template('base.html')




#
#
@app.route("/add_questions", methods=["POST", "GET"])
def ask_expert():
    if request.method == "POST":
        # email = request.form["email"]
        main = request.form["query"]
        query.append(main)
    #
    return render_template("expert.html")


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('expert_homepage'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/expert_homepage', methods=["POST", "GET"])
def expert_homepage():
    if not g.user:
        return redirect(url_for('login'))
    data = query
    return render_template("index.html", data=data)


@app.route('/delete/<ques>')
def delete(ques):
    query.remove(ques)
    return redirect(url_for('expert_homepage'))


if __name__ == "__main__":
    app.run(debug=True)
