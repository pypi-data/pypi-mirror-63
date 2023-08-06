class HTMLGenerator:
    """
    Static class to generate HTML.
    """
    @staticmethod
    def generate_login(action):
        """
        Returns an HTML login form.
        :param str action: Action to perform after submitting.
        :return str: Login.
        """
        return '''  
            <form method=post autocomplete=o action=/{}>
                <p>USERNAME  <input id=user-text-field type=text name=username autocomplete=username/>
                <p>PASSWORD <input id=password-text-field type=password name=password autocomplete=password/>
                <p><input type=submit value=Login>
            </form>
        '''.format(action)

    @staticmethod
    def generate_logout(action):
        """
        Returns an HTML logout form.
        :param str action: Action to perform after submitting.
        :return str: Logout.
        """
        return """
            <form method=post action=/{}>
                <input type="submit" name="log out" value="Logout">
            </form>
        """.format(action)

    @staticmethod
    def generate_accordion(summary, main):
        """
        Returns an HTML native accordion.
        :param str summary: Accordion's summary.
        :param str main: Accordion's main body.
        :return str: Accordion.
        """
        return """
        <details>
                <summary>{}</summary>
                <main>{}</main>
        </details>
        """.format(summary, main)

    @staticmethod
    def generate_line(line):
        """
        Returns an an HTML line.
        :param str line: Line to be converted.
        :return str: Line.
        """
        return "<br>{}".format(line)
