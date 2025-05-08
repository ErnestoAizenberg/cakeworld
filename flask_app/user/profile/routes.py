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

from flask_app.user.dtos import UserDTO
from flask_app.user.exceptions import UserNotFoundError


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
        if not viewer.id:
            return redirect("/auth/entry")
        owner_id = profile_url.split(".")[-1]
        if isinstance(owner_id, int):
            owner, status = controller.get_profile(owner_id)
            if owner is None:
                owner = UserDTO()
        else:
            owner = UserDTO()

        if request.method == "POST":
            if viewer and viewer.id == owner.id:
                file = request.files.get("avatar")
                if file:
                    avatar_path = controller.update_avatar(owner.id, file)
                    return redirect(url_for("profile", profile_url=profile_url))
                else:
                    flash("error", "error")
                    return redirect(url_for("profile", profile_url=profile_url))
            else:
                abort(403)
        try:
            post_amount = controller.count_user_posts(owner.id)
        except UserNotFoundError:
            post_amount = 0
        try:
            user_chats = (
                controller.get_user_chats(owner.id)
                if viewer and viewer.id == owner.id
                else None
            )
        except UserNotFoundError:
            user_chats = []

        return render_template(
            "profile/avatar.html",
            viewer=viewer,
            owner=owner,
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
