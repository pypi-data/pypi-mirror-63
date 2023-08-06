from functools import wraps

from flask import Blueprint, current_app, request, redirect, url_for, flash

from log_viewer.controllers.log_controller import LogController
from log_viewer.controllers.session_controller import SessionController, BadUserOrPasswordException
from log_viewer.utils import HTMLGenerator


logs_api_v1 = Blueprint('logs_api_v1', __name__)


def login_required(view):
    """
    Login required decorator.
    :param view: View to be decorated.
    :return: Decorated view.
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        sc = SessionController()
        if not sc.is_login_needed() or sc.is_logged_in():
            return view(**kwargs)
        else:
            flash("Please log in")
            return redirect(url_for('logs_api_v1.login'))

    return wrapped_view


@logs_api_v1.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login view.
    """
    sc = SessionController()
    if not sc.is_login_needed() or sc.is_logged_in():
        return redirect("/")

    login_failed = ""
    if request.method == 'POST' and sc.is_login_needed():
        user = request.form['username']
        psw = request.form['password']
        try:
            sc.login_user(user, psw)
            return redirect("/")
        except BadUserOrPasswordException:
            login_failed = "BAD USER OR PASSWORD"

    return HTMLGenerator.generate_login('login') + HTMLGenerator.generate_line(login_failed)


@logs_api_v1.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Session logout view.
    """
    sc = SessionController()
    if not any([sc.is_login_needed(), sc.is_logged_in()]):
        return redirect("/")

    SessionController().drop_session()
    return redirect(url_for('logs_api_v1.login'))


@logs_api_v1.route('/', methods=['GET'])
@logs_api_v1.route('/logs', methods=['GET'])
@login_required
def logs():
    """
    Logs view.
    """
    html = ""
    if SessionController().is_login_needed():
        html = HTMLGenerator.generate_logout('logout')
    str_paths = current_app.config['LOG_PATHS']
    controller = LogController(str_paths)
    html += controller.generate_logs_html()

    return html
