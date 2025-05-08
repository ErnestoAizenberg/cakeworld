from flask import (
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


def configure_profile_routes(app, controller):
    @app.route("/edit_account", methods=["POST"])
    def edit_account():
        new_username = request.form.get("username")
        message, status = controller.edit_account(new_username)

        if status == 200:
            return redirect(url_for("entry", mode="login"))
        else:
            flash(message)
            return redirect(url_for("entry", mode="login"))

    @app.route("/profile/<string:profile_url>", methods=["GET", "POST"])
    def profile(profile_url):
        viewer = g.current_user

        owner, status = controller.get_profile(profile_url)
        print("[DEBUG] profile owner: ", owner, status)
        if status == 404:
            abort(404, "User not found")

        if request.method == "POST":
            if viewer and viewer.id == owner.id:
                file = request.files.get("avatar")
                if file:
                    avatar_path = controller.update_avatar(owner, file)
                    return redirect(url_for("profile", profile_url=profile_url))
                else:
                    flash("error", "error")
                    return redirect(url_for("profile", profile_url=profile_url))
            else:
                abort(403)

        post_amount = controller.count_user_posts(owner.id)
        user_chats = (
            controller.get_user_chats(owner.id)
            if viewer and viewer.id == owner.id
            else None
        )

        return render_template(
            "profile/avatar.html",
            viewer=viewer,
            owner=owner,
            user=owner,
            server=g.server_info,
            post_amount=post_amount,
            user_chats=user_chats,
        )

    @app.route("/user/description", methods=["GET", "PUT"])
    def handle_user_description():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        if request.method == "GET":
            description, status = controller.get_user_description(user_id)
            if status != 200:
                return jsonify({"error": description}), status
            return jsonify({"description": description}), 200

        elif request.method == "PUT":
            data = request.get_json()
            description = data.get("description", "")
            message, status = controller.update_user_description(user_id, description)
            if status != 200:
                return jsonify({"error": message}), status
            return jsonify({"message": message}), 200

    @app.route("/user/<int:user_id>/description", methods=["GET"])
    def get_public_user_description(user_id):
        description, status = controller.get_user_description(user_id)
        if status != 200:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"description": description}), 200
