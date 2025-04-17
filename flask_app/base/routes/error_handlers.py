from functools import partial

from flask import jsonify, render_template, request
from werkzeug.exceptions import HTTPException

error_template_mapping = {
    400: "error/error_400.html",
    401: "error/error_401.html",
    403: "error/error_403.html",
    404: "error/error_404.html",
    405: "error/error_405.html",
    406: "error/error_406.html",
    408: "error/error_408.html",
    410: "error/error_410.html",
    418: "error/error_418.html",
    429: "error/error_429.html",
    500: "error/error_500.html",
    501: "error/error_501.html",
    502: "error/error_502.html",
    503: "error/error_503.html",
    504: "error/error_504.html",
}


def handle_error(e, status_code):
    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
        return jsonify(error=str(e)), status_code
    template = error_template_mapping.get(status_code, "error.html")
    return render_template(template, error=e), status_code


def configure_exception_routes(app):
    for status_code in error_template_mapping.keys():
        app.errorhandler(status_code)(partial(handle_error, status_code=status_code))

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return handle_error(e, e.code)

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        return handle_error(e, 500)
