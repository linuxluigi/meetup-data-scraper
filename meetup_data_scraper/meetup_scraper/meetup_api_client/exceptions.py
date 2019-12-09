class HttpNoSuccess(Exception):
    """
    Called when the server sends not 200, 404 or 410.
    """


class HttpNotFoundError(Exception):
    """
    Called when the server sends a 404 error.
    """


class HttpNotAccessibleError(Exception):
    """
    Called when the server sends a 410 error.
    """


class HttpNoXRateLimitHeader(Exception):
    """
    Called when a response has no X-RateLimit header
    """
