from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Product, Category, Supplier, StockTransaction
from app import db
from sqlalchemy import func, desc

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard with overview statistics"""
    # Get statistics
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_suppliers = Supplier.query.count()
    low_stock_count = Product.query.filter(
        Product.quantity <= Product.min_quantity
    ).count()
    
    # Calculate total inventory value
    total_value = db.session.query(
        func.sum(Product.quantity * Product.unit_price)
    ).scalar() or 0
    
    # Get low stock products
    low_stock_products = Product.query.filter(
        Product.quantity <= Product.min_quantity
    ).order_by(Product.quantity).limit(10).all()
    
    # Get recent transactions
    recent_transactions = StockTransaction.query.order_by(
        desc(StockTransaction.transaction_date)
    ).limit(10).all()
    
    # Get top products by value
    top_products = Product.query.order_by(
        desc(Product.quantity * Product.unit_price)
    ).limit(5).all()
    
    return render_template('dashboard.html',
                         total_products=total_products,
                         total_categories=total_categories,
                         total_suppliers=total_suppliers,
                         low_stock_count=low_stock_count,
                         total_value=total_value,
                         low_stock_products=low_stock_products,
                         recent_transactions=recent_transactions,
                         top_products=top_products)
