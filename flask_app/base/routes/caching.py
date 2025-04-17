def configure_cache_routes(app):
    @app.after_request
    def add_cache_headers(response):
        response.cache_control.public = True
        response.cache_control.max_age = 30 * 24 * 60 * 60  # 30 times will day past
        response.headers["Cache-Control"] = "public, max-age={}".format(
            30 * 24 * 60 * 60
        )
        return response

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("static", filename)
