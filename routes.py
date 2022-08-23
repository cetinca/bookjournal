import datetime
import functools
import uuid
from dataclasses import asdict

from flask import Blueprint, render_template, session, redirect, url_for, request, make_response, current_app
from passlib.hash import pbkdf2_sha256

from forms import LoginForm, RegisterForm, AddBook, AddPages
from models import User

pages = Blueprint("books", __name__, template_folder="templates", static_folder="static")


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if not session.get("email"):
            return redirect(url_for("books.login"))
        return route(*args, **kwargs)

    return route_wrapper


def date_list(date=None):
    selected_date = datetime.datetime.strptime(date, "%d/%m/%Y") if date else datetime.date.today()
    dates = [(selected_date + datetime.timedelta(day)).strftime("%d/%m/%Y") for day in range(-3, 4)]
    return dates


@pages.route("/", methods=["GET", "POST"])
@login_required
def index():
    email, date = session.get("email"), request.args.get("date")
    user_data = current_app.db.user.find_one({"email": email})
    books = user_data["books"]
    pages_ = user_data["pages"]
    dates = date_list(date)
    daily_pages = dict()
    for date in dates:
        for item in pages_:
            if item["date"] == date:
                daily_pages[date] = item["page"]
    return render_template("index.html", title="Home page", books=books, dates=dates, daily_pages=daily_pages)


@pages.route("/add-book", methods=["GET", "POST"])
@login_required
def add_book():
    form = AddBook()
    email, is_valid, book, date = session.get("email"), form.validate_on_submit(), form.book.data, form.date.data
    if is_valid:
        date = datetime.datetime.strftime(date, "%d/%m/%Y")
        current_app.db.user.update_one({"email": email}, {"$push": {"books": {"book": book, "date": date}}})
        return redirect(url_for("books.index"))
    return render_template("add_book.html", title="Add book", form=form)


@pages.route("/add-pages", methods=["GET", "POST"])
@login_required
def add_pages():
    form = AddPages()
    email, is_valid, page, date = session.get("email"), form.validate_on_submit(), form.page.data, form.date.data
    if is_valid:
        date = datetime.datetime.strftime(date, "%d/%m/%Y")
        current_app.db.user.update_one({"email": email}, {"$push": {"pages": {"page": page, "date": date}}})
        return redirect(url_for("books.index"))
    return render_template("add_page.html", title="Add page", form=form)


@pages.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    is_valid, email, password = form.validate_on_submit(), form.email.data, form.password.data
    if is_valid:
        user_data = current_app.db.user.find_one({"email": email})

        if user_data and pbkdf2_sha256.verify(password, user_data["password"]):
            session["email"] = email
            return redirect(url_for("books.index"))
        return make_response("Wrong username or password", 403)
    return render_template("login.html", title="Login form", form=form)


@pages.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    is_valid, email, password = form.validate_on_submit(), form.email.data, form.password.data
    if is_valid:
        user_data = current_app.db.user.find_one({"email": email})
        if user_data:
            return make_response("User already exists.", 401)
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )

        current_app.db.user.insert_one(asdict(user))
        return redirect(url_for("books.login"))
    return render_template("register.html", title="Register form", form=form)


@pages.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("books.login"))
