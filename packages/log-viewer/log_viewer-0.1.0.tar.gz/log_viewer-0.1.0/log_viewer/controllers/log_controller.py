import logging
from pathlib import Path

import log_viewer.settings as st
from log_viewer.utils import HTMLGenerator


class LogController:
    """
    Log controller.
    """
    def __init__(self, file_paths):
        """
        :param [str] file_paths: Paths list to search logs files for.
        """
        self.file_paths = self._str_paths_to_paths(file_paths)
        self._html_generator = HTMLGenerator

    @staticmethod
    def _str_paths_to_paths(file_paths):
        """
        Splits the str paths returning a list of Paths instead.
        :param str file_paths: List to be split.
        :return [Path]: Sorted Paths.
        """
        log_paths = []
        for log_path in file_paths:
            for path in Path(log_path).rglob(st.LOG_SEARCH_REGEX):
                log_paths.append(path)

        return sorted(log_paths)

    def generate_logs_html(self):
        """
        Loops over the given paths, searching for log files and transform its into HTML.
        :return str: HTML logs within accordions.
        """
        html = ""
        for file_paths in self.file_paths:
            lines_html = ""
            try:
                with open(str(file_paths), "r") as fd:
                    for line in fd:
                        lines_html += self._html_generator.generate_line(line)
            except PermissionError as e:
                logging.warning("Error reading file path: {}, {}".format(file_paths, e))

            html += self._html_generator.generate_accordion(str(file_paths), lines_html)

        return html
