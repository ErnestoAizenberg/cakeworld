from unittest.mock import MagicMock

import pytest
from flask import session, url_for


@pytest.fixture
def app():
    from flask_app import create_app

    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


class TestAuthRoutes:
    """Test cases for authentication routes."""

    def test_entry_page_get(self, client):
        """Test entry page renders correctly."""
        response = client.get(url_for("auth.entry"))
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_login_success(self, client, mock_auth_controller):
        """Test successful login redirects to dashboard."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_auth_controller.login.return_value = mock_user

        response = client.post(
            url_for("auth.login"),
            data={"email": "test@example.com", "password": "password123"},
            follow_redirects=False,
        )

        assert response.status_code == 302
        assert url_for("dashboard.index") in response.location

    def test_login_failure(self, client, mock_auth_controller):
        """Test failed login shows error."""
        mock_auth_controller.login.side_effect = AuthException(
            "Invalid credentials", 401
        )

        response = client.post(
            url_for("auth.login"),
            data={"email": "test@example.com", "password": "wrong"},
            follow_redirects=True,
        )

        assert b"Invalid credentials" in response.data

    def test_register_success(self, client, mock_auth_controller):
        """Test successful registration redirects to verification page."""
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_auth_controller.register.return_value = mock_user

        response = client.post(
            url_for("auth.register"),
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=False,
        )

        assert response.status_code == 302
        assert url_for("auth.verify_pending") in response.location

    def test_verify_email_success(self, client, mock_auth_controller):
        """Test successful email verification redirects to success page."""
        mock_auth_controller.verify_email.return_value = True

        response = client.get(url_for("auth.verify_email", token="valid_token"))

        assert response.status_code == 302
        assert url_for("auth.verified_success") in response.location

    def test_password_reset_flow(self, client, mock_auth_controller):
        """Test complete password reset flow."""
        # Request reset
        mock_auth_controller.request_password_reset.return_value = True
        response = client.post(
            url_for("auth.forgot_password"), data={"email": "test@example.com"}
        )
        assert b"reset email sent" in response.data

        # Submit new password
        mock_auth_controller.reset_password.return_value = True
        response = client.post(
            url_for("auth.reset_password", token="valid_token"),
            data={
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
            follow_redirects=False,
        )
        assert url_for("auth.password_reset_success") in response.location

    def test_logout(self, client, mock_auth_controller):
        """Test logout clears session and redirects."""
        with client.session_transaction() as sess:
            sess["user_id"] = 1

        response = client.get(url_for("auth.logout"), follow_redirects=False)

        assert "user_id" not in session
        assert response.status_code == 302
        assert url_for("main.index") in response.location
