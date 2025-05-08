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


def configure_post_routes(app, post_controller, PostForm, ReplyForm):
    @app.route("/view_post/<int:post_id>")
    def view_post(post_id):
        post = post_controller.view_post(post_id)
        if not post:
            flash("Пост не найден.", "error")
            return redirect(url_for("index"))

        form = ReplyForm()
        reply_list = post_controller.get_posts_by_user(post.user_id)
        return render_template(
            "thread.html",
            thread=post,
            user=g.current_user,
            form=form,
            reply_list=reply_list,
        )

    @app.route("/topic/<int:topic_id>/create_post", methods=["GET", "POST"])
    def create_post(topic_id):
        form = PostForm()

        if form.validate_on_submit():
            success, message, post = post_controller.create_post(
                form, g.current_user.id, topic_id
            )
            flash(message, "success" if success else "error")
            return redirect(
                url_for("view_topic", url_name=post.topic.url_name)
                if success
                else url_for("create_post", topic_id=topic_id)
            )

        return render_template(
            "create_thread.html",
            user=session.get("user"),
            form=form,
        )

    @app.route("/post/<int:post_id>/reply", methods=["POST"])
    def reply_post(post_id):
        form = ReplyForm()

        if form.validate_on_submit():
            success, message, reply = post_controller.reply_post(
                form, g.current_usrer.id, post_id
            )
            flash(message, "success" if success else "error")
            return redirect(url_for("view_post", post_id=post_id))

        return redirect(url_for("view_post", post_id=post_id))

    @app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
    def edit_post(post_id):
        form = PostForm()

        if form.validate_on_submit():
            success, message, post = post_controller.edit_post(form, post_id)
            flash(message, "success" if success else "error")
            return redirect(
                url_for("view_topic", topic_id=post.user_id)
                if success
                else url_for("edit_post", post_id=post_id)
            )

        elif request.method == "GET":
            post = post_controller.view_post(post_id)
            if post:
                form.content.data = post.content

        return render_template("edit_post.html", form=form, user=g.current_user)

    @app.route("/post/<int:post_id>/delete", methods=["POST"])
    def delete_post(post_id):
        success, message = post_controller.delete_post(post_id)
        flash(message, "success" if success else "error")
        return redirect(url_for("index"))
