class HttpNotFoundError(Exception):
    """
    Called when the server sends a 404 error.
    """


class HttpNotAccessibleError(Exception):
    """
    Called when the server sends a 410 error.
    """
