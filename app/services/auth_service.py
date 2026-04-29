import logging
from functools import wraps

logger = logging.getLogger(__name__)


def get_current_user() -> None:
    """Stub: returns None until auth is implemented."""
    return None


def require_auth(f):
    """
    Placeholder auth decorator.
    Currently passes all requests through.
    To activate: replace the wrapper body with a real session/token check.
    Usage:
        @require_auth
        @api_bp.route("/protected")
        def protected_route():
            ...
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger.debug("require_auth: auth not enabled — passing through")
        return f(*args, **kwargs)

    return wrapper
