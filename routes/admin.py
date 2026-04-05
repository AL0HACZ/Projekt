from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash

from models import db
from models.article import Revision, Category, Article
from models.user import User, Group
from routes import get_current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def dashboard():
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    return render_template('admin_dashboard.html', user=user)


@admin_bp.route('/admin/revisions')
def pending_revisions():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if any(g.is_super_admin for g in user.groups):
        revisions = Revision.query.filter_by(is_approved=False).all()
    else:
        admin_cat_ids = []
        for g in user.groups:
            admin_cat_ids.extend([c.id for c in g.categories])
        if not admin_cat_ids:
            return redirect(url_for('article.index'))
        revisions = Revision.query.join(Article).filter(Revision.is_approved == False,
                                                        Article.category_id.in_(admin_cat_ids)).all()

    return render_template('revisions.html', user=user, revisions=revisions)


@admin_bp.route('/admin/revisions/<int:id>/approve', methods=['POST'])
def approve_revision(id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    rev = Revision.query.get_or_404(id)
    rev.is_approved = True
    rev.approved_by_id = user.id
    db.session.commit()
    return redirect(url_for('admin.pending_revisions'))


@admin_bp.route('/admin/revisions/<int:id>/deny', methods=['POST'])
def deny_revision(id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    rev = Revision.query.get_or_404(id)
    db.session.delete(rev)
    db.session.commit()
    return redirect(url_for('admin.pending_revisions'))


@admin_bp.route('/admin/users', methods=['GET'])
def manage_users():
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    users = User.query.all()
    return render_template('manage_users.html', user=user, users=users)


@admin_bp.route('/admin/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    target_user = User.query.get_or_404(id)
    if request.method == 'POST':
        target_user.username = request.form.get('username')
        target_user.display_name = request.form.get('display_name')
        target_user.about_me = request.form.get('about_me')
        db.session.commit()
        return redirect(url_for('admin.manage_users'))
    return render_template('edit_user.html', user=user, target_user=target_user)


@admin_bp.route('/admin/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    target_user = User.query.get_or_404(id)
    if target_user.id != user.id:
        db.session.delete(target_user)
        db.session.commit()
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/admin/users/<int:id>/reset_password', methods=['POST'])
def reset_password(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    target_user = User.query.get_or_404(id)
    new_password = request.form.get('new_password')
    if new_password:
        target_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/admin/categories', methods=['GET', 'POST'])
def manage_categories():
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    if request.method == 'POST':
        name = request.form.get('name')
        cat_type = request.form.get('type')
        if name and cat_type:
            cat = Category(name=name, type=cat_type)
            db.session.add(cat)
            db.session.commit()
    categories = Category.query.all()
    return render_template('manage_categories.html', user=user, categories=categories)


@admin_bp.route('/admin/categories/<int:id>/edit', methods=['GET', 'POST'])
def edit_category(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    cat = Category.query.get_or_404(id)
    if request.method == 'POST':
        cat.name = request.form.get('name')
        cat.type = request.form.get('type')
        db.session.commit()
        return redirect(url_for('admin.manage_categories'))
    return render_template('edit_category.html', user=user, category=cat)


@admin_bp.route('/admin/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/admin/groups', methods=['GET', 'POST'])
def manage_groups():
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    if request.method == 'POST':
        name = request.form.get('name')
        is_super = request.form.get('is_super_admin') == 'on'
        if name:
            group = Group(name=name, is_super_admin=is_super)
            db.session.add(group)
            db.session.commit()
    groups = Group.query.all()
    return render_template('manage_groups.html', user=user, groups=groups)


@admin_bp.route('/admin/groups/<int:id>/edit', methods=['GET', 'POST'])
def edit_group(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    group = Group.query.get_or_404(id)
    if request.method == 'POST':
        group.name = request.form.get('name')
        group.is_super_admin = request.form.get('is_super_admin') == 'on'

        user_ids = request.form.getlist('user_ids')
        group.users = User.query.filter(User.id.in_(user_ids)).all()

        category_ids = request.form.getlist('category_ids')
        group.categories = Category.query.filter(Category.id.in_(category_ids)).all()

        db.session.commit()
        return redirect(url_for('admin.manage_groups'))

    users = User.query.all()
    categories = Category.query.all()
    return render_template('edit_group.html', user=user, group=group, users=users, categories=categories)


@admin_bp.route('/admin/groups/<int:id>/delete', methods=['POST'])
def delete_group(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('admin.manage_groups'))