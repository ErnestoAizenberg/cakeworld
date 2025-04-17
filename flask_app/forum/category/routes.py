from flask import (Flask, abort, flash, g, redirect, render_template, session,
                   url_for)


def configure_topic_category_routes(app, category_controller, CategoryForm):
    @app.route("/create_category", methods=["GET", "POST"])
    def create_category():
        form = CategoryForm()
        if form.validate_on_submit():
            new_name = form.name.data
            if category_controller.get_category_by_name(new_name):
                flash("Упс... Это имя уже занято!", "info")
                return render_template(
                    "forum/category/create_category.html",
                    form=form,
                    user=g.current_user,
                )

            category = category_controller.create_category(form)
            flash("Категория успешно создана!", "success")
            return redirect(url_for("create_category"))

        return render_template(
            "forum/category/create_category.html",
            form=form,
            user=g.current_user,
        )

    @app.route("/community_topics")
    def community_topics():
        community_category = category_controller.get_category_by_name("Community")
        print("[DEBUG] community_category", community_category)
        topics = category_controller.get_category_topics(community_category.id)
        print("[DEBUG] community_category.topics", topics)

        return render_template(
            "forum/category/community_topics.html",
            user=g.current_user,
            category=community_category,
            topics=topics,
        )

    @app.route("/server_topics")
    def server_categories():
        server_category = category_controller.get_category_by_name("Server")
        youtube_category = category_controller.get_category_by_name("Youtube")
        rules_category = category_controller.get_category_by_name("Rules")

        server_topics = category_controller.get_category_topics(server_category.id)
        youtube_topics = category_controller.get_category_topics(youtube_category.id)
        rules_topics = category_controller.get_category_topics(rules_category.id)

        return render_template(
            "forum/category/technical_forums.html",
            user=g.current_user,
            server_topics=server_topics,
            youtube_topics=youtube_topics,
            rule_topics=rules_topics,
        )
