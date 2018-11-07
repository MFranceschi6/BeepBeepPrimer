import functools
from flask_login import current_user, LoginManager
from monolith.database import User, db
from flask import redirect, g
from stravalib import exc

login_manager = LoginManager()


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        user._authenticated = True
    return user


def login_required(func):
    @functools.wraps(func)
    def _login_required(*args, **kw):
        if current_user is not None and current_user.is_authenticated:
            return func(*args, **kw)
        return redirect('/')
    return _login_required


def strava_token_required(func):
    @functools.wraps(func)
    def _strava_token_required(*args, **kw):
        try:
            return func(*args, **kw)
        except exc.AccessUnauthorized:
            if current_user is not None and hasattr(current_user, 'id'):
                q = db.session.query(User).filter(User.id == current_user.id)
                user = q.first()
                user.strava_token = None
                db.session.add(user)
                db.session.commit()
            return redirect('/')
    return _strava_token_required


def after_this_request(func):
    if not hasattr(g, 'call_after_request'):
        g.call_after_request = []
    g.call_after_request.append(func)
    return func