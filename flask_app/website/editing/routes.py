from flask import flash, g, redirect, render_template

from .forms import ServerForm
from .models import Server


def configure_editsite_routes(app, server_form):
    @app.route("/create_server", methods=["GET", "POST"])
    def create_server():
        server = (
            Server.get_server()
        )  # Получаем сервер (или создаем новый, если его нет)
        form = ServerForm()

        if form.validate_on_submit():
            # Обновляем сервер с новыми данными из формы
            server.update_server(
                server_name=form.server_name.data,
                server_description=form.server_description.data,
                server_background=form.server_background.data,
                color_scheme=form.color_scheme.data,
            )
            server.set_content_html(form.content_html.data)
            server.save()  # Сохраняем изменения в базе данных
            flash("Сервер успешно обновлён!", "success")
            return redirect("/")

        # Заполняем форму текущими данными сервера для отображения
        form.content_html.data = server.content_html
        form.server_name.data = server.server_name
        form.server_description.data = server.server_description
        form.server_background.data = server.server_background
        form.color_scheme.data = server.color_scheme

        server = Server.get_server()
        return render_template(
            "server/create_server.html",
            form=form,
            server=server,
            user=g.current_user,
        )

    @app.route("/server")
    def server_dashboard():
        return render_template(
            "server/server_page.html",
            user=g.current_user,
        )
