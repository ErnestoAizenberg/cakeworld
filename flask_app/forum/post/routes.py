from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .controllers import PostController


def configure_post_routes(
    app: Flask,
    post_controller: PostController,
    PostForm: "FlaskForm",
    ReplyForm: "FlaskForm",
):
    @app.route("/view_post/<int:post_id>")
    def view_post(post_id: int):
        post = post_controller.view_post(post_id)
        if post is None:
            flash("Post not found.", "error")
            abort(404, "Post not found.")

        form = ReplyForm()
        reply_list = post_controller.get_all_replies(post_id)
        return render_template(
            "forum/post/thread.html",
            thread=post,
            user=g.current_user,
            form=form,
            reply_list=reply_list,
        )

    @app.route("/topic/<int:topic_id>/create_post", methods=["GET", "POST"])
    def create_post(topic_id: int):
        form = PostForm()

        if form.validate_on_submit():
            user_id = g.current_user.id
            post = post_controller.create_post(form, user_id, topic_id)

            if post:
                flash("Post created successfully.", "success")
                print("[DEBUG] post_id: ", post)
                return redirect(url_for("view_post", post_id=post.id))
            else:
                flash("Invalid form data.", "error")

        return render_template(
            "forum/post/create_thread.html", user=session.get("user"), form=form
        )

    @app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
    def edit_post(post_id: int):
        form = PostForm()

        if form.validate_on_submit():
            post = post_controller.edit_post(form, post_id)
            if post:
                flash("Post updated successfully.", "success")
                return redirect(url_for("view_topic", topic_id=post.topic_id))
            else:
                flash("Invalid form data or post not found.", "error")

        elif request.method == "GET":
            post = post_controller.view_post(post_id)
            if post:
                form.content.data = post.content

        return render_template(
            "forum/post/edit_post.html", form=form, user=g.current_user
        )

    @app.route("/post/<int:post_id>/reply", methods=["POST"])
    def reply_post(post_id: int):
        form = ReplyForm()

        if form.validate_on_submit():
            user_id = g.current_user.id
            reply = post_controller.reply_post(form, user_id, post_id)
            if reply:
                flash("Reply created successfully.", "success")
            else:
                flash("Invalid form data.", "error")
            return redirect(url_for("view_post", post_id=post_id))

        return redirect(url_for("view_post", post_id=post_id))

    @app.route("/post/<int:post_id>/delete", methods=["POST"])
    def delete_post(post_id: int):
        success = post_controller.delete_post(post_id)
        flash(
            "Post deleted successfully." if success else "Failed to delete post.",
            "success" if success else "error",
        )
        return redirect(url_for("index"))

    @app.route("/discussion-dashboard")
    def discussion():
        return render_template("discussion.html")
