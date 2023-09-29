"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.app_context().push()

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def users():
    """Homepage Redirect"""
    return redirect("/users")


@app.route("/users")
def users_index():
    """Page with info on users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)


@app.route("/users/new", methods=["GET"])
def users_new_form():
    """Form to create user"""
    return render_template("users/new.html")


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle Form Submission"""
    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"] or None,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def users_show(user_id):
    """Page with info on a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)


@app.route("/users/<int:user_id>/edit")
def users_edit(user_id):
    """Edit User Information"""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_update(user_id):
    """Update User"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    """Delete User"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def post_new_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("posts/new.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def post_new(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user,
        tags=tags,
    )

    db.session.add(new_post)
    db.session.commit()
    flash("Post has been Added")

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def posts_show(post_id):
    """Show Post"""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def posts_edit(post_id):
    """Edit Post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("posts/edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def posts_update(post_id):
    """Update Post"""
    post = Post.query.get_or_404(post_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash("Post Updated")

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def posts_delete(post_id):
    """Delete Post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Deleted Post")

    return redirect(f"/users/{post.user_id}")


@app.route("/tags")
def tags_index():
    """Show Tags"""
    tags = Tag.query.all()
    return render_template("tags/index.html", tags=tags)


@app.route("/tags/new")
def tags_new_form():
    """Add New Tag"""
    return render_template("tags/new.html")


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Submit Tag"""
    new_tag = Tag(name=request.form["name"])
    db.session.add(new_tag)
    db.session.commit()
    flash("Tag Has Been Created")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tags_show(tag_id):
    """Show Page with Info on Tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/show.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def tags_edit_form(tag_id):
    """Edit Tag Form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/edit.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def tags_edit(tag_id):
    """Edit Tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash("Tag Edited")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_delete(tag_id):
    """Delete A Tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash("Tag Deleted")

    return redirect("/tags")
