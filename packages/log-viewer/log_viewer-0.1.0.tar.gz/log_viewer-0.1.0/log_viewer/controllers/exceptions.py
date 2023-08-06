class BadUserOrPasswordException(Exception):
    """
    Login exception.
    """
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors
