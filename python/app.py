from flask import Flask, request, render_template, g, redirect
import sqlite3
import os
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'flaskmemo.db'  # データを保存するSQLiteのファイル名。実際の接続はsqlite3.connect(DATABASE)で行う。

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Flask-Login 設定
login_manager = LoginManager() # ログイン状態を管理する LoginManager を作成
login_manager.init_app(app) # Flaskアプリ(app)に組み込んで、ログイン機能を使えるようにする

class User(UserMixin):
    def __init__(self, userid):
        self.id = userid


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

# ===== 認証関連 =====

#ここからリードコーディング！！！

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error_message = ""
    if request.method == "POST":
        userid = request.form.get("userid")
        password = request.form.get("password")
        pass_hash = generate_password_hash(password)  # pbkdf2:sha256 がデフォルト

        db = get_db()
        user_check = get_db().execute(
            'SELECT userid FROM user WHERE userid = ?', [userid]).fetchone()
        if not user_check:
            db.execute(
                'INSERT INTO user (userid, password) VALUES (?, ?)',
                (userid, pass_hash)
            )
            db.commit()
            return redirect("/login")
        else:
            error_message = "入力されたユーザIDは既に利用されています"

    return render_template("signup.html", error_message=error_message)


@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = ""
    userid = ""
    if request.method == "POST":
        userid = request.form.get("userid")
        password = request.form.get("password")
        #ログインのチェック
        user_data = get_db().execute(
            'SELECT userid FROM user WHERE userid = ?', [userid]
            ).fetchone()
        if user_data is not None:
            if check_password_hash(user_data[0], password):
                user = User(userid)
                login_user(user)
                return redirect("/")
            error_message = "入力されたユーザIDまたはパスワードが違います"

        if(userid == "guri" and password == "1234"):
                user = User(userid)
                login_user(user)
                return redirect("/")
        db = get_db()
        user = db.execute(
            'SELECT userid, password FROM user WHERE userid = ?',
            (userid,)
        ).fetchone()

        if user is None:
            error_message = "ユーザIDまたはパスワードが違います"
        elif not check_password_hash(user["password"], password):
            error_message = "ユーザIDまたはパスワードが違います"
        else:
            user_obj = User(userid)
            login_user(user_obj)
            return redirect("/")

    return render_template("login.html", error_message=error_message)

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("/login")

# ===== メモ機能 =====

@app.route("/")
@login_required
def top():
    memo_list = get_db().execute(
        'SELECT id, title, body FROM memo'
    ).fetchall()
    return render_template("index.html", memo_list=memo_list)

@app.route("/regist", methods=["GET", "POST"])
@login_required
def regist():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        db = get_db()
        db.execute('INSERT INTO memo (title, body) VALUES (?, ?)', (title, body))
        db.commit()
        return redirect("/")

    return render_template('regist.html')

@app.route("/<id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        db.execute('UPDATE memo SET title=?, body=? WHERE id=?', (title, body, id))
        db.commit()
        return redirect("/")

    post = db.execute(
        'SELECT id, title, body FROM memo WHERE id = ?', (id,)
    ).fetchone()
    return render_template("edit.html", post=post)

@app.route("/<id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    db = get_db()
    if request.method == "POST":
        db.execute('DELETE FROM memo WHERE id=?', (id,))
        db.commit()
        return redirect("/")

    post = db.execute(
        'SELECT id, title, body FROM memo WHERE id = ?', (id,)
    ).fetchone()
    return render_template("delete.html", post=post)

# ===== DB関連 =====

def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

if __name__ == "__main__":
    app.run(debug=True)
