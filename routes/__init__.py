from flask import request

from models.user import Session, User


def get_current_user():
    token = request.cookies.get('session_token')
    if not token:
        return None
    session_record = Session.query.filter_by(token=token).first()
    if session_record:
        return User.query.get(session_record.user_id)
    return None
