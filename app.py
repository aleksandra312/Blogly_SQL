"""Blogly application."""

from flask import Flask, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Homepage redirects to list of users."""
    return redirect("/users")


@app.route("/users")
def list_users():
    """List users and show add form."""
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("user_list.html", users=users)


@app.route("/users/new")
def show_add_form():
    """Show an add form for users."""
    return render_template("user_new.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds a new user and redirects back to /users."""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("users/<int:user_id>")
def show_user(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.route("users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)


@app.route("users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edits a user, redirects to the /users page."""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route("users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect("/users")






