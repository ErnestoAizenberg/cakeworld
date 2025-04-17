# flask_app/user/auth/services/email_service.py
from threading import Thread

from flask import current_app, render_template, url_for
from flask_mail import Message


class EmailService:  # I CAN USE MY HTML SANITIZER HERE FOR SAKE OF SAFETY
    def __init__(self, mail):
        self.mail = mail

    def send_async_email(self, app, msg):
        """Асинхронная отправка email."""
        with app.app_context():
            self.mail.send(msg)

    def send_verification_email(self, user_dto):
        """Отправляет письмо для подтверждения email."""
        verification_link = url_for(
            "auth.verify_email", token=user_dto.verification_token, _external=True
        )
        html_content = render_template(
            "emails/verify_email.html",
            username=user_dto.username,
            verification_link=verification_link,
        )

        msg = Message(
            subject="Verify Your Email",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[user_dto.email],
        )
        msg.html = html_content

        # Асинхронная отправка
        Thread(
            target=self.send_async_email, args=(current_app._get_current_object(), msg)
        ).start()

    def send_password_reset_email(self, user_dto):
        return self.send_reset_password_email(user_dto)

    def send_reset_password_email(self, user_dto):
        """Отправляет письмо для сброса пароля."""
        reset_link = url_for(
            "auth.reset_password", token=user_dto.verification_token, _external=True
        )
        html_content = render_template(
            "emails/reset_password.html",
            username=user_dto.username,
            reset_link=reset_link,
        )

        msg = Message(
            subject="Reset Your Password",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[user_dto.email],
        )
        msg.html = html_content

        # Асинхронная отправка
        Thread(
            target=self.send_async_email, args=(current_app._get_current_object(), msg)
        ).start()

    def send_welcome_email(self, user_dto):
        """Отправляет приветственное письмо после регистрации."""
        html_content = render_template(
            "emails/welcome_email.html", username=user_dto.username
        )

        msg = Message(
            subject="Welcome to Our Platform!",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[user_dto.email],
        )
        msg.html = html_content

        # Асинхронная отправка
        Thread(
            target=self.send_async_email, args=(current_app._get_current_object(), msg)
        ).start()
