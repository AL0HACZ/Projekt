import secrets
from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.user import User, Session
from routes import get_current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        display_name = request.form.get('display_name')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Uživatelské jméno již existuje")

        new_user = User(
            username=username,
            display_name=display_name,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            user.last_login = datetime.utcnow()
            token = secrets.token_hex(32)
            new_session = Session(
                user_id=user.id,
                token=token,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(new_session)
            db.session.commit()
            resp = make_response(redirect(url_for('article.index')))
            resp.set_cookie('session_token', token)
            return resp
        else:
            return render_template('login.html', error="Neplatné přihlašovací údaje")
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    token = request.cookies.get('session_token')
    if token:
        Session.query.filter_by(token=token).delete()
        db.session.commit()
    resp = make_response(redirect(url_for('article.index')))
    resp.delete_cookie('session_token')
    return resp


@auth_bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    current_user = get_current_user()
    return render_template('profile.html', user=current_user, profile_user=user)


@auth_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        about_me = request.form.get('about_me')
        password = request.form.get('password')

        if display_name:
            user.display_name = display_name
        if about_me is not None:
            user.about_me = about_me
        if password:
            user.password_hash = generate_password_hash(password)

        db.session.commit()
        return redirect(url_for('auth.profile', username=user.username))

    return render_template('settings.html', user=user)
