import re
import smtplib
import dns.resolver
import datetime
from tkinter import *
from flask import Flask
from flask import Flask, render_template, redirect, request, Response, session, send_file, jsonify
from data import db_session
from data.user import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.user import User
import secrets
from flask import session
from flask import jsonify
tk=Tk()
width = tk.winfo_screenwidth()
app = Flask(__name__)
app.config['SECRET_KEY'] = "mishadimamax200620072008"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)
oauth = OAuth(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", current_user=current_user)

@app.route('/mark_done', methods=['POST'])
@login_required
def mark_done():
    data = request.get_json()
    route_id = data.get("route_id")
    db_sess = db_session.create_session()
    user = User()
    
    print(f"Пользователь {current_user.email} прошел маршрут {route_id}")

    

    return jsonify({"message": "OK"}), 200

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/cultural_routes')
def cultural_routes():
    return render_template("cultural_routes.html")



@app.route('/cul_1')
def cul_1():
    return render_template("cul_1.html")
    




@app.route('/cul_2')
def cul_2():
    return render_template("cul_2.html")

@app.route('/cul_3')
def cul_3():
    return render_template("cul_3.html")

@app.route('/cul_4')
def cul_4():
    return render_template("cul_4.html")

@app.route('/cul_5')
def cul_5():
    return render_template("cul_5.html")

@app.route('/cul_6')
def cul_6():
    return render_template("cul_6.html")

@app.route('/gastronom')
def gastronom():
    return render_template("gastronom.html")

@app.route('/gas_1')
def gas_1():
    return render_template("gas_1.html")

@app.route('/gas_2')
def gas_2():
    return render_template("gas_2.html")

@app.route('/gas_3')
def gas_3():
    return render_template("gas_3.html")

@app.route('/gas_4')
def gas_4():
    return render_template("gas_4.html")

@app.route('/gas_5')
def gas_5():
    return render_template("gas_5.html")

@app.route('/gas_6')
def gas_6():
    return render_template("gas_6.html")

@app.route('/geog_obj')
def geog_obj():
    return render_template("geog_obj.html")

@app.route('/user_login')
def user_login():
    return render_template("user_login.html")

@app.route('/user_reg')
def user_reg():
    return render_template("user_reg.html")


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None
    
google = oauth.register(
    name='google',
    client_id="376838788269-k120re8lp9bjv3dv31i6s9d0ekpkh5tq.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',  
    client_kwargs={'scope': 'openid email profile', 'nonce': 'random_nonce_value'}
)

login_manager = LoginManager()
login_manager.init_app(app)

def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/login/google")
def login_google():
    nonce = secrets.token_urlsafe(16)  
    session["nonce"] = nonce  
    return google.authorize_redirect(
    url_for("auth_callback", _external=True),
    nonce=nonce  
    )


@app.route("/login/callback")
def auth_callback():
    token = google.authorize_access_token()
    if not token:
        return "Ошибка авторизации", 400

    try:
        nonce = session.pop("nonce", None)  
        if not nonce:
            return "Ошибка: nonce отсутствует", 400

        user_info = google.parse_id_token(token, nonce=nonce)  
    except Exception as e:
        return f"Ошибка обработки токена: {str(e)}", 400

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == user_info["email"]).first()

    if not user:
        user = User(
            name=user_info.get("name", "Без имени"),
            email=user_info["email"]
        )
        db_sess.add(user)
        db_sess.commit()

    login_user(user, remember=True)
    return redirect("/private_office")

@app.route('/reg_form', methods=["POST"])
def reg_form():
    form = request.form
    email = form.get('emailInput')
    password = form.get("passwordInput")
    name = form.get("nameInput")
    surname = form.get("surnameInput")
    phone_num = form.get("phone_num")
    db_sess = db_session.create_session()
    user = User()
    if not is_valid_email(email):
        return render_template("user_reg.html", error="Неверный формат email")
    existing_user = db_sess.query(User).filter(User.email == email).first()
    if existing_user:
        db_sess.close()
        return render_template("user_reg.html", error="Этот email уже зарегистрирован")
    user.name = name
    user.surname = surname
    user.email = email
    user.phone_num = phone_num
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return redirect('/user_login')


@app.route('/private_office')
def private_office():
    name = current_user.name
    surname = current_user.surname
    email = current_user.email
    phone_num = current_user.phone_num
    return render_template("private_office.html")

@app.before_request
def make_session_permanent():
    session.permanent = False



@app.route('/login', methods=["POST", "GET"])
def login():
    form = request.form
    if request.method=="POST":
        if form.get('rememberMe'):
            remember_me =form.get("rememberMe") == 'on'  
        else:
            remember_me = 'False'
        print(remember_me)
    email = form.get('emailInput')
    password = form.get("passwordInput")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        login_user(user, remember=remember_me)
        return redirect("/private_office")
    else:
        db_sess.close()
        print("Неверный email или пароль.", "error")
        return redirect(url_for('user_login'))
    

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
    app.run(debug=True, host='0.0.0.0', port=5000,)


if __name__ == "__main__":
    main()
    
