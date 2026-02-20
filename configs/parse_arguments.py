import argparse

def parse_arguments():
    """Parse command-line arguments for configuration overrides."""
    parser = argparse.ArgumentParser(description="Flask app with Redis support.")
    parser.add_argument("--server_address", type=str, help="URL of the server.")
    parser.add_argument("--secret_key", type=str, help="Secret key for Flask app.")
    parser.add_argument("--redis_host", type=str, help="Redis server host.")
    parser.add_argument("--redis_port", type=int, help="Redis server port.")
    parser.add_argument("--redis_db", type=int, help="Redis database number.")
    parser.add_argument("--host", type=str, help="Server host.")
    parser.add_argument("--port", type=int, help="Server port.")
    parser.add_argument(
        "--mail_username",
        type=str,
        help="Mail username, which will send emails to users (my_email@example.com).",
    )
    parser.add_argument(
        "--mail_password", type=str, help="Mail password or app-specific password."
    )

    return parser.parse_args()