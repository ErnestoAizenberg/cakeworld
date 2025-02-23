from werkzeug.exceptions import HTTPException
from flask import render_template, jsonify, request
from flask_app import app

@app.errorhandler(400)
def bad_request(e):
    """
    400 Bad Request:  Клиент отправил некорректный запрос (например, неправильный формат данных, неверные параметры).
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 400
    return render_template('error_400.html'), 400


@app.errorhandler(401)
def unauthorized(e):
    """
    401 Unauthorized:  Необходима аутентификация (например, пользователь не предоставил учетные данные или они неверны).
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 401
    return render_template('error_401.html'), 401


@app.errorhandler(403)
def forbidden(e):
    """
    403 Forbidden: Доступ к ресурсу запрещен (например, у пользователя нет прав доступа).
    """
    return render_template('error_403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.best_match(['application/json', 'text/html']) == 'application/json':
        return jsonify(error=str(e)), 404
    return render_template('error_404.html'), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """
    405 Method Not Allowed:  Запрошенный метод (GET, POST, PUT и т.д.) не разрешен для данного ресурса.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 405
    return render_template('error_405.html'), 405


@app.errorhandler(406)
def not_acceptable(e):
    """
    406 Not Acceptable:  Сервер не может предоставить контент в соответствии с заголовками Accept, отправленными клиентом.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 406
    return render_template('error_406.html'), 406


@app.errorhandler(408)
def request_timeout(e):
    """
    408 Request Timeout: Время ожидания запроса истекло.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 408
    return render_template('error_408.html'), 408


@app.errorhandler(410)
def gone(e):
    """
    410 Gone:  Запрошенный ресурс больше не доступен и не будет доступен снова.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 410
    return render_template('error_410.html'), 410


@app.errorhandler(418)
def im_a_teapot(e):
    """
    418 I'm a teapot:  Этот код ошибки часто используется в шутку.  Изначально был определен как часть RFC 2324,
    который был шуточным протоколом для управления чайниками.  Некоторые сервисы используют его для обозначения
    того, что клиент пытается выполнить невозможную операцию.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 418
    return render_template('error_418.html'), 418


@app.errorhandler(429)
def too_many_requests(e):
    """
    429 Too Many Requests:  Клиент отправил слишком много запросов за определенный период времени (ограничение скорости).
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 429
    return render_template('error_429.html'), 429

@app.errorhandler(500)
def internal_server_error(e):
    """
    500 Internal Server Error: Общая ошибка сервера (непредвиденная ошибка, которая не подпадает ни под одну другую категорию).
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 500
    return render_template('error_500.html'), 500


@app.errorhandler(501)
def not_implemented(e):
    """
    501 Not Implemented:  Сервер не поддерживает функциональность, необходимую для выполнения запроса.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 501
    return render_template('error_501.html'), 501


@app.errorhandler(502)
def bad_gateway(e):
    """
    502 Bad Gateway:  Сервер, действующий как шлюз или прокси, получил недействительный ответ от вышестоящего сервера.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 502
    return render_template('error_502.html'), 502


@app.errorhandler(503)
def service_unavailable(e):
    """
    503 Service Unavailable:  Сервер временно недоступен (например, из-за перегрузки или обслуживания).
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 503
    return render_template('error_503.html'), 503


@app.errorhandler(504)
def gateway_timeout(e):
    """
    504 Gateway Timeout:  Сервер, действующий как шлюз или прокси, не получил ответа от вышестоящего сервера вовремя.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), 504
    return render_template('error_504.html'), 504

# Обработка общих исключений
@app.errorhandler(HTTPException)
def handle_exception(e):
    """
    Обрабатывает все исключения, которые являются подклассами HTTPException (т.е. ошибки, которые Flask может сгенерировать).
    Это позволяет более гибко обрабатывать ошибки, не требуя явного определения обработчика для каждой из них.
    """
    if request.accept_mimetypes.accept_json:
        return jsonify(error=str(e)), e.code
    return render_template('error.html', error=e), e.code  # Используйте общий шаблон для исключений