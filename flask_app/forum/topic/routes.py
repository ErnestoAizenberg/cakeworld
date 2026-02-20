from flask import Flask, Blueprint, flash, g, redirect, render_template, url_for

from flask_app.forum.post.forms import PostForm

from .controllers import TopicController
from .forms import TopicForm


def configure_topic_routes(
    app: Flask,
    topic_controller: TopicController,
):
    topic_bp = Blueprint("forum_topic", __name__, url_prefix="/topics")

    @topic_bp.route("/<string:url_name>")
    def view_topic(url_name):
        topic = topic_controller.get_topic_by_url_name(url_name)
        posts = topic_controller.get_posts_for_topic(topic.id)
        print("[DEBUG] posts: ", posts)
        return render_template(
            "forum/topic/view_topic.html",
            topic=topic,
            posts=posts,
            form=PostForm(),
        )

    @topic_bp.route("/create", methods=["GET", "POST"])
    def create_topic():
        form = TopicForm()
        form.category.choices = [(c.id, c.name) for c in g.categories]

        if form.validate_on_submit():
            topic = topic_controller.create_topic(form.data, g.current_user.id)
            flash("Тема успешно создана!", "success")
            return redirect(url_for("forum_topic.view_topic", url_name=topic.url_name))

        return render_template("forum/topic/create_topic.html", form=form)

    @topic_bp.route("/<int:topic_id>/edit", methods=["GET", "POST"])
    def edit_topic(topic_id):
        form = TopicForm()
        form.category.choices = [(c.id, c.name) for c in g.categories]
        topic = topic_controller.get_topic(topic_id)

        if form.validate_on_submit():
            updated_topic = topic_controller.update_topic(topic_id, form.data)
            flash("Тема успешно обновлена!", "success")
            return redirect(
                url_for("forum_topic.view_topic", url_name=updated_topic.url_name)
            )

        # Предустановка значений подсказки
        form.title.data = topic.title
        form.url_name.data = topic.url_name
        form.description.data = topic.description
        form.category.data = topic.category_id

        return render_template("forum/topic/edit_topic.html", form=form, topic=topic)

    @topic_bp.route("/<int:topic_id>/delete", methods=["POST"])
    def delete_topic(topic_id):
        topic_controller.delete_topic(topic_id)
        flash("Тема успешно удалена!", "success")
        return redirect(url_for("forum.index"))

    app.register_blueprint(topic_bp)
