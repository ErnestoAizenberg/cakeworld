import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
from typing import Optional

from flask import current_app, render_template


class EmailService:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        sender: str,
        use_tls: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize EmailService with SMTP configuration.

        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            smtp_username: SMTP username
            smtp_password: SMTP password
            sender: Email address to send from
            use_tls: Whether to use TLS (default: True)
            logger: Optional logger instance
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.sender = sender
        self.use_tls = use_tls
        self.logger = logger or logging.getLogger(__name__)

    def _send_email(self, msg: MIMEMultipart) -> None:
        """
        Internal method to send email using SMTP.
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            self.logger.info(f"Email sent successfully to {msg['To']}")
        except Exception as e:
            self.logger.error(f"Failed to send email to {msg['To']}: {str(e)}")
            raise

    def send_async_email(self, app, msg: MIMEMultipart) -> None:
        """
        Send email asynchronously.

        Args:
            app: Flask application context
            msg: Email message to send
        """
        try:
            with app.app_context():
                self._send_email(msg)
        except Exception as e:
            self.logger.error(f"Async email failed: {str(e)}")
            raise

    def _create_message(
        self, subject: str, recipients: list[str], html_content: str
    ) -> MIMEMultipart:
        """
        Create MIME email message with HTML content.
        """
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = ", ".join(recipients)

        # Attach HTML content
        msg.attach(MIMEText(html_content, "html"))

        return msg

    def send_verification_email(
        self,
        verification_link: str,
        username: str,
        email: str,
        subject: Optional[str] = None,
    ) -> None:
        """
        Send email verification email.
        """
        html_content = render_template(
            "emails/verify_email.html",
            username=username,
            verification_link=verification_link,
        )

        subject = subject or "Verify Your Email"
        msg = self._create_message(subject, [email], html_content)

        self.logger.info(f"Sending verification email to {email}")
        Thread(
            target=self.send_async_email, args=(current_app._get_current_object(), msg)
        ).start()

    def send_password_reset_email(
        self,
        reset_link: str,
        email: str,
        username: str,
        subject: Optional[str] = None,
    ) -> None:
        """
        Send password reset email (alias for send_reset_password_email).
        """
        return self.send_reset_password_email(reset_link, email, username, subject)

    def send_reset_password_email(
        self,
        reset_link: str,
        email: str,
        username: str,
        subject: Optional[str] = None,
    ) -> None:
        """
        Send password reset email.
        """
        html_content = render_template(
            "emails/reset_password.html",
            username=username,
            reset_link=reset_link,
        )

        subject = subject or "Reset Your Password"
        msg = self._create_message(subject, [email], html_content)

        self.logger.info(f"Sending password reset email to {email}")
        Thread(
            target=self.send_async_email, args=(current_app._get_current_object(), msg)
        ).start()

    def send_welcome_email(
        self,
        username: str,
        email: str,
        subject: Optional[str] = None,
    ) -> None:
        """
        Send welcome email after registration.
        """
        html_content = render_template(
            "emails/welcome_email.html",
            username=username,
        )

        subject = subject or "Welcome to Our Platform!"
        msg = self._create_message(subject, [email], html_content)

        self.logger.info(f"Sending welcome email to {email}")
        Thread(
            target=self.send_async_email, args=(current_app._get_current_object(), msg)
        ).start()
