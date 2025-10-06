from flask import Blueprint, render_template, send_file
from flask_login import login_required
from app.models import Product, StockTransaction, Category, Supplier
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta
import io
import csv

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/')
@login_required
def index():
    """Reports dashboard"""
    # Stock summary
    total_products = Product.query.count()
    total_stock_value = db.session.query(
        func.sum(Product.quantity * Product.unit_price)
    ).scalar() or 0
    low_stock_count = Product.query.filter(
        Product.quantity <= Product.min_quantity
    ).count()
    
    # Category wise stock
    category_stats = db.session.query(
        Category.name,
        func.count(Product.id).label('product_count'),
        func.sum(Product.quantity).label('total_quantity'),
        func.sum(Product.quantity * Product.unit_price).label('total_value')
    ).join(Product).group_by(Category.name).all()
    
    # Recent transactions summary
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    
    stock_in_week = db.session.query(
        func.sum(StockTransaction.quantity)
    ).filter(
        StockTransaction.transaction_type == 'IN',
        StockTransaction.transaction_date >= week_ago
    ).scalar() or 0
    
    stock_out_week = db.session.query(
        func.sum(StockTransaction.quantity)
    ).filter(
        StockTransaction.transaction_type == 'OUT',
        StockTransaction.transaction_date >= week_ago
    ).scalar() or 0
    
    return render_template('reports/index.html',
                         total_products=total_products,
                         total_stock_value=total_stock_value,
                         low_stock_count=low_stock_count,
                         category_stats=category_stats,
                         stock_in_week=stock_in_week,
                         stock_out_week=stock_out_week)


@bp.route('/export/products')
@login_required
def export_products():
    """Export products to CSV"""
    products = Product.query.all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['SKU', 'Name', 'Category', 'Supplier', 'Quantity', 
                    'Min Quantity', 'Unit Price', 'Total Value'])
    
    # Write data
    for product in products:
        writer.writerow([
            product.sku,
            product.name,
            product.category.name if product.category else '',
            product.supplier.name if product.supplier else '',
            product.quantity,
            product.min_quantity,
            product.unit_price,
            product.total_value
        ])
    
    # Create response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'products_{datetime.now().strftime("%Y%m%d")}.csv'
    )


@bp.route('/export/transactions')
@login_required
def export_transactions():
    """Export transactions to CSV"""
    transactions = StockTransaction.query.order_by(
        StockTransaction.transaction_date.desc()
    ).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Date', 'Product', 'Type', 'Quantity', 'Unit Price', 
                    'User', 'Notes'])
    
    # Write data
    for transaction in transactions:
        writer.writerow([
            transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            transaction.product.name,
            transaction.transaction_type,
            transaction.quantity,
            transaction.unit_price or '',
            transaction.user.username,
            transaction.notes or ''
        ])
    
    # Create response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'transactions_{datetime.now().strftime("%Y%m%d")}.csv'
    )
