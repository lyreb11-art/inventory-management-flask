from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes import main, auth, products, categories, suppliers, stock, reports
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(suppliers.bp)
    app.register_blueprint(stock.bp)
    app.register_blueprint(reports.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create admin user if doesn't exist
        from app.models import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@inventory.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    return app
