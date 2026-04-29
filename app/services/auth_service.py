import logging
import os
from functools import wraps

from flask import jsonify, redirect, request, session, url_for

logger = logging.getLogger(__name__)


def _admin_username() -> str:
    return (os.getenv("ADMIN_USERNAME", "admin") or "admin").strip()


def _admin_password() -> str:
    return (os.getenv("ADMIN_PASSWORD", "") or "").strip()


def _is_api_request() -> bool:
    return request.path.startswith("/api/")


def get_current_user() -> dict | None:
    username = session.get("admin_username")
    if not username:
        return None
    return {"username": username, "role": "admin"}


def login_admin(username: str, password: str) -> bool:
    if not _admin_password():
        logger.warning("ADMIN_PASSWORD is not configured; admin login disabled")
        return False

    if username.strip() == _admin_username() and password == _admin_password():
        session["admin_username"] = _admin_username()
        return True
    return False


def logout_admin() -> None:
    session.pop("admin_username", None)


def require_auth(f):
    """Protect route with session-based admin auth."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if get_current_user() is None:
            if _is_api_request():
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("auth.login_page", next=request.path))
        return f(*args, **kwargs)

    return wrapper
