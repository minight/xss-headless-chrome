from flask import render_template, request, redirect, current_app, Flask, flash, url_for, session
import hashlib
import time
from multiprocessing import Process
from flaskr.app import db
from . import app
from . import forms
from . import horseman
from .models import User

@app.route("/profile", methods=["GET", "POST"])
def profile():
    cur_user = None
    print("\n".join("%s: %s" % (k, v) for k, v in request.cookies.items()))
    if request.cookies.get("flag", "") == current_app.config.get("FLAG"):
        cur_user = User.query.filter_by(username="admin").first()

    if not cur_user:
        if not session.get("user"):
            flash("Please log in")
            return redirect(url_for("app.profile"))
        cur_user = User.query.filter_by(username=session['user']).first()

    if request.method == "POST":
        description = request.form.get("description", "")
        cur_user.description = description
        db.session.add(cur_user)
        db.session.commit()
        print("User: %s description updated to: %s" % (cur_user.username, cur_user.description))
        flash("Profile updated")
    return render_template("profile.html", user = cur_user)


@app.route("/logout")
def logout():
    session['user'] = None
    session.clear()
    return redirect(url_for("app.login"))

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        url = request.form.get("url", "")
        p = Process(
            target=horseman.xss_get,
            args=(url, current_app.config.get("HOST"), "flag", current_app.config.get("FLAG"),))
        p.start()
        flash("Your URL is being visited")
    return render_template("contact.html")


@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get("user"):
        flash("you are already logged in")
        return(redirect(url_for("app.profile")))


    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")


        if not username or not password:
            flash("Please have enter both a username and password")
            return render_template("register.html")

        cur_user = User.query.filter_by(username = username, password = password).first()
        if not cur_user:
            flash("Invalid username and password")
            return render_template("login.html")

        session['user'] = cur_user.username
        flash("Login successful")
        return redirect(url_for("app.profile"))

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("user"):
        flash("you are already logged in")
        return(redirect(url_for("app.profile")))

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please have both a username and password")
            return render_template("register.html")

        # check existence of username
        check_user = User.query.filter_by(username = username).all()
        if check_user:
            flash("Username already registered")
            return render_template("register.html")

        new_user = User(username=username, password=password, role='peasant')
        db.session.add(new_user)
        db.session.commit()

        flash("New user registered")
        return redirect(url_for("app.login"))

    return render_template("register.html")

