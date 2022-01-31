from flask import Flask, render_template, request, jsonify, session, url_for, g, redirect
from flask import Flask, render_template, request
import json



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

data1 = json.load(open("static/data/query.json"))
@app.get("/")
def index_get():
    return render_template('base.html')




#
#
@app.route("/add_questions", methods=["POST", "GET"])
def ask_expert():
    if request.method == "POST":
        email = request.form["email"]
        query = request.form["query"]
        f = json.load(open("static/data/query.json", ))
        main = {
            email: {"query": query
                    }
        }
        f.update(main)
        json_object = json.dumps(f, indent=4)
        with open("static/data/query.json", "w") as outfile:
            outfile.write(json_object)
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
    query = json.load(open("static/data/query.json"))
    for i in query:
        data1.update({i:query[i]["query"]})
    data = data1
    return render_template("index.html", data=data)


@app.route('/delete/<gmail>')
def delete(gmail):
    data = json.load(open("static/data/query.json", ))
    data.pop(gmail)
    json_object = json.dumps(data, indent=4)
    with open("static/data/query.json", "w") as outfile:
        outfile.write(json_object)
    data1.pop(gmail)
    return redirect("/expert_homepage")


if __name__ == "__main__":
    app.run(debug=True)
