# Routes package
from flask import Blueprint

# Import blueprints to make them available when importing from app.routes
from app.routes.main import bp as main_bp
from app.routes.auth import bp as auth_bp
from app.routes.products import bp as products_bp
from app.routes.categories import bp as categories_bp
from app.routes.suppliers import bp as suppliers_bp
from app.routes.stock import bp as stock_bp
from app.routes.reports import bp as reports_bp
