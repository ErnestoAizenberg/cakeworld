# flask_app/routes/auth.py
from flask import Blueprint, redirect, render_template, request, session, url_for

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def init_auth_routes(app, auth_controller):
    @auth_bp.route("/")
    @auth_bp.route("/entry")
    def entry():
        """Render the main authentication page (login/signup)"""
        mode = request.args.get("mode", "login")
        error = request.args.get("error")
        return render_template(
            "auth/entry.html",
            mode=mode,
            error=error,
            username=request.args.get("username", ""),
            email=request.args.get("email", ""),
        )

    @auth_bp.route("/login", methods=["POST"])
    def login():
        """Handle login form submission"""
        try:
            user = auth_controller.login(
                request.form.get("email"),
                request.form.get("password"),
            )
            session["user_id"] = user.id
            session["user_email"] = user.email

            auth_controller.send_welcome_notification(
                user=user,
                message="Вы вошли в акаунт",
                type="info",
            )

            return redirect(url_for("index_dash"))
        except Exception as e:
            return redirect(
                url_for(
                    "auth.entry",
                    mode="login",
                    email=request.form.get("email"),
                    error=str(e),
                )
            )

    @auth_bp.route("/register", methods=["POST"])
    def register():
        """Handle registration form submission"""
        try:
            user = auth_controller.register(
                request.form.get("username"),
                request.form.get("email"),
                request.form.get("password"),
                request.form.get("confirm_password"),
            )
            notif = {"user": user, "message": "-_-", "type": "info"}
            # auth_controller.send_welcome_notification(**notif)

            return redirect(
                url_for(
                    "auth.verify_pending",
                    email=user.email,
                )
            )
        except Exception as e:
            print(str(e))
            return redirect(
                url_for(
                    "auth.entry",
                    mode="signup",
                    username=request.form.get("username"),
                    email=request.form.get("email"),
                    error=str(e),
                )
            )

    @auth_bp.route("/verify/<token>")
    def verify_email(token):
        """Handle email verification link"""
        try:
            auth_controller.verify_email(token)
            return redirect(url_for("auth.verified_success"))
        except Exception as e:
            return redirect(url_for("auth.verify_error", error=str(e)))

    @auth_bp.route("/verify/success")
    def verified_success():
        """Show verification success page"""
        return render_template("auth/verify_success.html")

    @auth_bp.route("/verify/error")
    def verify_error():
        """Show verification error page"""
        error = request.args.get("error", "Verification failed")
        return render_template("auth/verify_error.html", error=error)

    @auth_bp.route("/verify/pending")
    def verify_pending():
        """Show verification pending page"""
        email = request.args.get("email", "")
        return render_template("auth/verify_pending.html", email=email)

    @auth_bp.route("/resend-verification", methods=["GET", "POST"])
    def resend_verification():
        """Handle resend verification email"""
        if request.method == "GET":
            return render_template("auth/resend_verification.html")

        try:
            auth_controller.resend_verification(request.form.get("email"))
            return redirect(
                url_for("auth.verify_pending", email=request.form.get("email"))
            )
        except Exception as e:
            return render_template(
                "auth/resend_verification.html",
                error=str(e),
                email=request.form.get("email"),
            )

    @auth_bp.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        """Handle password reset request"""
        if request.method == "GET":
            return render_template("auth/forgot_password.html")

        try:
            auth_controller.request_password_reset(request.form.get("email"))
            return render_template(
                "auth/reset_email_sent.html", email=request.form.get("email")
            )
        except Exception as e:
            return render_template(
                "auth/forgot_password.html",
                error=str(e),
                email=request.form.get("email"),
            )

    @auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
    def reset_password(token):
        """Handle password reset form"""
        if request.method == "GET":
            return render_template("auth/reset_password.html", token=token)

        try:
            auth_controller.reset_password(
                token,
                request.form.get("new_password"),
                request.form.get("confirm_password"),
            )
            return redirect(url_for("auth.password_reset_success"))
        except Exception as e:
            return render_template(
                "auth/reset_password.html", token=token, error=str(e)
            )

    @auth_bp.route("/logout")
    def logout():
        """Handle user logout"""
        session.pop("user_id")
        return redirect(url_for("index_dash"))

    app.register_blueprint(auth_bp)
