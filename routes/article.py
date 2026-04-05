from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from markdown_it import MarkdownIt
import difflib

from models import db
from models.article import Article, Revision, Category, Keyword
from routes import get_current_user

article_bp = Blueprint('article', __name__)

md = MarkdownIt()

@article_bp.route('/')
def index():
    user = get_current_user()
    articles = Article.query.all()

    lastest_articles = articles[-5:]

    return render_template('index.html', user=user, articles=lastest_articles, count=len(articles))


@article_bp.route('/random')
def random_article():
    article = Article.query.order_by(func.random()).first()
    if article:
        return redirect(url_for('article.view_article', id=article.id))
    return redirect(url_for('article.index'))


@article_bp.route('/search')
def search():
    user = get_current_user()
    query = request.args.get('q', '')
    results = []
    if query:
        results = Article.query.outerjoin(Keyword).filter(
            or_(
                Article.title.ilike(f'%{query}%'),
                Keyword.word.ilike(f'%{query}%')
            )
        ).all()
    return render_template('search.html', user=user, query=query, results=results)


@article_bp.route('/categories')
def categories():
    user = get_current_user()
    cats = Category.query.all()
    admin_cat_ids = set()
    is_super = False
    if user:
        is_super = any(g.is_super_admin for g in user.groups)
        for g in user.groups:
            for c in g.categories:
                admin_cat_ids.add(c.id)
    return render_template('categories.html', user=user, categories=cats, admin_cat_ids=admin_cat_ids,
                           is_super=is_super)


@article_bp.route('/category/<int:id>')
def view_category(id):
    user = get_current_user()
    category = Category.query.get_or_404(id)
    admin_cat_ids = set()
    is_super = False
    if user:
        is_super = any(g.is_super_admin for g in user.groups)
        for g in user.groups:
            for c in g.categories:
                admin_cat_ids.add(c.id)
    return render_template('category.html', user=user, category=category, admin_cat_ids=admin_cat_ids,
                           is_super=is_super)


@article_bp.route('/article/<int:id>')
def view_article(id):
    user = get_current_user()
    article = Article.query.get_or_404(id)
    revision = Revision.query.filter_by(article_id=id, is_approved=True).order_by(Revision.created_at.desc()).first()
    content = None

    if revision:
        content = md.render(revision.content)

    return render_template('article.html', user=user, article=article, revision=revision, content=content)


import difflib

import difflib
from flask import render_template


@article_bp.route('/article/<int:id>/history')
def article_history(id):
    user = get_current_user()
    article = Article.query.get_or_404(id)

    revisions = Revision.query.filter_by(article_id=id, is_approved=True) \
        .order_by(Revision.created_at.desc()).all()

    diffs = []
    for i in range(len(revisions)):
        current_rev = revisions[i]
        prev_content = revisions[i + 1].content if i + 1 < len(revisions) else ""

        d = difflib.HtmlDiff()

        diff_html = d.make_table(
            prev_content.splitlines(),
            current_rev.content.splitlines(),
            context=True,
            numlines=3
        )

        diffs.append({
            'rev': current_rev,
            'diff_html': diff_html
        })

    return render_template('history.html', user=user, article=article, diffs=diffs)


@article_bp.route('/category/<int:category_id>/article/new', methods=['GET', 'POST'])
def create_article(category_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    category = Category.query.get_or_404(category_id)

    is_admin = any(g.is_super_admin for g in user.groups)
    if not is_admin:
        for g in user.groups:
            if category in g.categories:
                is_admin = True
                break

    if not is_admin:
        return redirect(url_for('article.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        new_article = Article(title=title, category_id=category_id)
        db.session.add(new_article)
        db.session.commit()

        rev = Revision(article_id=new_article.id, user_id=user.id, content=content, is_approved=True,
                       approved_by_id=user.id)
        db.session.add(rev)

        keywords = request.form.get('keywords', '').split(',')
        for kw in keywords:
            if kw.strip():
                db.session.add(Keyword(article_id=new_article.id, word=kw.strip()))

        db.session.commit()
        return redirect(url_for('article.view_article', id=new_article.id))

    return render_template('create_article.html', user=user, category=category)


@article_bp.route('/article/<int:id>/edit', methods=['GET', 'POST'])
def edit_article(id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    article = Article.query.get_or_404(id)

    is_admin = any(g.is_super_admin for g in user.groups)
    if not is_admin:
        for g in user.groups:
            if article.category in g.categories:
                is_admin = True
                break

    if request.method == 'POST':
        content = request.form.get('content')

        rev = Revision(article_id=id, user_id=user.id, content=content, is_approved=is_admin,
                       approved_by_id=user.id if is_admin else None)
        db.session.add(rev)

        if is_admin:
            Keyword.query.filter_by(article_id=id).delete()

            keywords = request.form.get('keywords', '').split(',')
            for kw in keywords:
                if kw.strip():
                    db.session.add(Keyword(article_id=id, word=kw.strip()))

        db.session.commit()
        return redirect(url_for('article.view_article', id=id))

    latest_rev = Revision.query.filter_by(article_id=id).order_by(Revision.created_at.desc()).first()
    content = latest_rev.content if latest_rev else ""
    return render_template('edit.html', user=user, article=article, content=content, is_admin=is_admin)


@article_bp.route('/article/<int:id>/delete', methods=['POST'])
def delete_article(id):
    user = get_current_user()
    if not user or not any(g.is_super_admin for g in user.groups):
        return redirect(url_for('article.index'))

    article = Article.query.get_or_404(id)

    category_id = article.category.id

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('article.view_category', id=category_id))