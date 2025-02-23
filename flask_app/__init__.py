from flask import Flask
from .config import Config
app = Flask(__name__)
app.config.from_object(Config)


from .models import db, User, Topic, Post
db.init_app(app)

from .forms import TopicForm, PostForm
from .forum import (
    delete_topic,
    edit_topic,
    create_topic,
    create_post,
    reply_post,
    edit_post,
    delete_post,
    view_topic,
    technical_forums,
    categories,
    threads,
    profile,
    search,
    admin,
    index,
)
from .caching import add_cache_headers, static_files
"""
from .oauth import (
    login_page,
    logout,
    oauth2_authorize,
    oauth2_callback
)"""
from .errors import (
    close_connection,
    bad_gateway,
    bad_request,
    forbidden,
    gateway_timeout,
    gone,
    handle_exception,
    im_a_teapot,
    internal_server_error,
    method_not_allowed,
    not_acceptable,
    not_implemented,
    page_not_found,
    request_timeout,
    service_unavailable,
    too_many_requests,
    unauthorized,
)