"""Blogly application."""

from flask import Flask, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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
def show_edit_form_user(user_id):
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


@app.route("/users/<int:user_id>/posts/new")
def show_form_add_new_post(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("post_new.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods["POST"])
def add_post(user_id):
    """Add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)

    tag_ids = [int(input_tag_id) for input_tag_id in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title = request.form['title'],
        content = request.form['content']
        user = user,
        tags=tags
    )
    db.session.add(new_post)
    db.session.commit()

    flash(f"Successfully added a new Post '{new_post.title}'!")
    return redirect(f"users/{user_id}")


@app.route("/posts/<post_id>")
def show_post(post_id):
    """Show a post."""
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)


@app.route("posts/<int:post_id>/edit")
def show_edit_form_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post_edit.html', post=post, tags=tags)


@app.route("posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edits a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)

    tag_ids = [int(input_tag_id) for input_tag_id in request.form.getlist("tags")]
    
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.title = request.form['title'],
    user.content = request.form['content'],

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete s post."""
    post = Post.query.get_or_404(post_id)

    db.session.delete(user)
    db.session.commit()
    return redirect(f"users/{post.user_id}")


@app.route("/tags")
def list_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.order_by(Tag.name).all()

    return render_template("tag_list.html", tags=tags)


@app.route("/tags/<tag_id>")
def show_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)


@app.route("/tags/new")
def show_tag_add_form():
    """Shows a form to add a new tag."""
    return render_template("tag_new.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Process add form, adds tag, and redirect to tag list."""
    new_tag = Tag(
        name = request.form['name']
    )
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("tags/<int:tag_id>/edit")
def show_edit_form_tag(tag_id):
    """Show the edit page for a tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag=tag)


@app.route("tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edits a tag, redirects to the /tags page."""
    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['name'],

    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")


@app.route("tags/<int:tag_id>/delete")
def delete_tag(tag_id):
    """Delete the tag."""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")

