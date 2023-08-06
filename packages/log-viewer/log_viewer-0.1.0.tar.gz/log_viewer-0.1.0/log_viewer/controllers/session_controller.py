from flask import current_app, session

from log_viewer.controllers.exceptions import BadUserOrPasswordException


class SessionController:
    """
    Class to control the user's session.
    """
    def __init__(self):
        self._db_user = current_app.config['USER']
        self._db_psw = current_app.config['PASSWORD']
        self._session = session

    def is_login_needed(self):
        """
        Returns True if user or password are set, False otherwise.  
        :return bool:
        """
        return any([self._db_user is not None, self._db_psw is not None])

    def is_logged_in(self):
        """
        Returns True if user is logged in, False otherwise.
        :return bool:
        """
        return all(['username' in self._session, 'password' in self._session])

    def drop_session(self):
        """
        Drops user's and password's session.
        """
        self._session.pop('username', None)
        self._session.pop('password', None)

    def login_user(self, user, password):
        """
        Sets user's and password's session
        :param user: User to login.
        :param password: Password.
        :raise BadUserOrPasswordException: Bad user or password.
        """
        if (self._db_user is not None and self._db_user != user) or \
                (self._db_psw is not None and self._db_psw != password):
            raise BadUserOrPasswordException("Bad user or password.")
        else:
            self._session['username'] = user
            self._session['password'] = password
