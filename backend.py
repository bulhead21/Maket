import datetime
from tkinter import *
from flask import Flask
from flask import Flask, render_template, redirect, request, Response, session, send_file, jsonify
from data import db_session
from data.user import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
tk=Tk()
width = tk.winfo_screenwidth()
app = Flask(__name__)
app.config['SECRET_KEY'] = "mishadimamax200620072008"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", current_user=current_user)


@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/cultural_routes')
def cultural_routes():
    return render_template("cultural_routes.html")


@app.route('/historical_heritage')
def historical_heritage():
    return render_template("historical_heritage.html")


@app.route('/geog_obj')
def geog_obj():
    return render_template("geog_obj.html")


@app.route('/user_login')
def user_login():
    return render_template("user_login.html")


@app.route('/user_reg')
def user_reg():
    return render_template("user_reg.html")


@app.route('/reg_form', methods=["POST"])
def reg_form():
    form = request.form
    email = form.get('emailInput')
    password = form.get("passwordInput")
    name = form.get("nameInput")
    surname = form.get("surnameInput")
    db_sess = db_session.create_session()
    user = User()
    user.name = name
    user.surname = surname
    user.email = email
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return redirect('/user_login')


@app.route('/private_office')
def private_office():
    # name = current_user.name
    # surname = current_user.surname
    # phone_num = current_user.phone_num
    # email = current_user.email
    return render_template("private_office.html")


@app.route('/login', methods=["POST"])
def login():
    form = request.form
    email = form.get('emailInput')
    password = form.get("passwordInput")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        login_user(user, remember=True)
        return redirect("/private_office")

    return redirect('/user_login')

@app.route('/posibiletes')
def posibiletes( ):
    return render_template("posibiletes.html")

@app.route('/tour_operator')
def tour_operator( ):
    return render_template("tour_operator.html")

@app.route('/guide')
def guide( ):
    return render_template("guide.html")

@app.route('/favourite_routes')
def favourite_routes( ):
    return render_template("favourite_routes.html")

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
@app.route('/partners')
def partners( ):
    return render_template("partners.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

#
# @app.route('/info')
# def info():
#     return render_template("info.html")
#
#
# @app.route('/info')
# def info():
#     return render_template("info.html")


def main():
    db_session.global_init("databases/places.db")
    app.run(debug=True)


if __name__ == "__main__":
    main()
    

