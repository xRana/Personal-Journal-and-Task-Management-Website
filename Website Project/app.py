import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///diary.db")

############ what it is for?
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

today = date.today()

@app.route("/")
@login_required
def index():
    if request.method == "POST":
         x = db.execute("SELECT * FROM diarys WHERE id = ? AND date = ?",session["user_id"], today)
         return render_template("write.html", text=x)
    else:
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)

        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(user) != 0:
            return apology("username alraday has been taken", 400)

        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",request.form.get("username"), hash)

        x = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = x[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/write", methods=["GET", "POST"])
@login_required
def write():
    if request.method == "POST":
        today = date.today()
        if not request.form.get("write"):
            return apology("provied text", 400)
        else:
            db.execute("UPDATE diarys SET diary = ? WHERE id = ? AND date = ?",request.form.get("write"), session["user_id"], today)
            return redirect("/")

    else:
        today = date.today()
        x = db.execute("SELECT * FROM diarys WHERE id = ? AND date = ?",session["user_id"], today)
        if len(x) != 0:
            return render_template("write.html", text=x)
        else:
            db.execute("INSERT INTO diarys (id, date, diary) VALUES (?, ?, ?)",session["user_id"], today, " ")
            x = db.execute("SELECT * FROM diarys WHERE id = ? AND date = ?",session["user_id"], today)
            return render_template("write.html", text=x)

@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    if request.method == "POST":
        rows = db.execute("SELECT date FROM diarys WHERE id = ?", session["user_id"])
        i = 0
        while (i < len(rows)):
            rows[i] = rows[i]["date"]
            i = i + 1
        date = request.form.get("date")
        if not request.form.get("date"):
            return apology("provied a date", 400)
        elif date not in rows:
            return apology("nothing was written here", 400)
        else:
            x = db.execute("SELECT * FROM diarys WHERE id = ? AND date = ?", session["user_id"], date)
            return render_template("view.html", view=x)
    else:
        rows = db.execute("SELECT date FROM diarys WHERE id = ?", session["user_id"])
        i = 0
        min = rows[0]["date"]
        while (i < len(rows)):
            rows[i] = rows[i]["date"]
            if rows[i] < min:
                min = rows[i]
            i = i + 1
        return render_template("diary.html", today=today, min=min)

@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        if not request.form.get("todo"):
            return redirect(url_for("tasks"))
        else:
            new = request.form.get("todo")
            db.execute("INSERT INTO tasks (id, task, checked) VALUES (?, ?, ?)",session["user_id"], new, False)
            return redirect(url_for("tasks"))

    else:
        x = db.execute("SELECT task,checked FROM tasks WHERE id = ?",session["user_id"])
        return render_template("tasks.html", tasks=x)

@app.route("/delete1/<task>")
@login_required
def delete1(task):
    db.execute("DELETE FROM tasks WHERE id = ? AND task = ?",session["user_id"], task)
    return redirect(url_for("tasks"))

@app.route("/check/<task>")
@login_required
def check(task):
    x = db.execute("SELECT checked FROM tasks WHERE id = ? AND task = ?",session["user_id"], task)
    x = x[0]["checked"]
    print("yoo",x)
    db.execute("UPDATE tasks SET checked = ? WHERE id = ? AND task = ?",not x, session["user_id"], task)
    return redirect(url_for("tasks"))

