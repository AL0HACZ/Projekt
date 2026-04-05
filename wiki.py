import os
from flask import Flask
from dotenv import load_dotenv
from models import db
from routes.auth import auth_bp
from routes.article import article_bp
from routes.admin import admin_bp

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB', 'sqlite:///autopedia.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET', 'autopedia_very_secret')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(article_bp)
app.register_blueprint(admin_bp)

#with app.app_context():
#    db.create_all()
#    from models.user import User, Group
#    from werkzeug.security import generate_password_hash
#    if not User.query.filter_by(username='admin').first():
#        admin = User(username='admin', display_name='Administrátor', password_hash=generate_password_hash('admin'))
#        super_group = Group(name='Administrátoři', is_super_admin=True)
#        admin.groups.append(super_group)
#        db.session.add(admin)
#        db.session.add(super_group)
#        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)