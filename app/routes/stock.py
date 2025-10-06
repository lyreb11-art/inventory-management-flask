from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, StockTransaction
from app.forms import StockTransactionForm

bp = Blueprint('stock', __name__, url_prefix='/stock')


@bp.route('/')
@login_required
def index():
    """List all stock transactions"""
    page = request.args.get('page', 1, type=int)
    product_id = request.args.get('product', 0, type=int)
    
    query = StockTransaction.query
    
    # Apply product filter
    if product_id:
        query = query.filter_by(product_id=product_id)
    
    transactions = query.order_by(StockTransaction.transaction_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    products = Product.query.order_by(Product.name).all()
    
    return render_template('stock/index.html',
                         transactions=transactions,
                         products=products,
                         product_id=product_id)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add stock (stock in)"""
    form = StockTransactionForm()
    form.transaction_type.data = 'IN'
    
    if form.validate_on_submit():
        product = Product.query.get_or_404(form.product.data)
        
        # Create transaction
        transaction = StockTransaction(
            product_id=product.id,
            user_id=current_user.id,
            transaction_type='IN',
            quantity=form.quantity.data,
            unit_price=form.unit_price.data,
            notes=form.notes.data
        )
        
        # Update product quantity
        product.quantity += form.quantity.data
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Successfully added {form.quantity.data} units to "{product.name}"', 'success')
        return redirect(url_for('stock.index'))
    
    return render_template('stock/add.html', form=form)


@bp.route('/remove', methods=['GET', 'POST'])
@login_required
def remove():
    """Remove stock (stock out)"""
    form = StockTransactionForm()
    form.transaction_type.data = 'OUT'
    
    if form.validate_on_submit():
        product = Product.query.get_or_404(form.product.data)
        
        # Check if sufficient stock
        if product.quantity < form.quantity.data:
            flash(f'Insufficient stock! Available: {product.quantity}', 'danger')
            return render_template('stock/remove.html', form=form)
        
        # Create transaction
        transaction = StockTransaction(
            product_id=product.id,
            user_id=current_user.id,
            transaction_type='OUT',
            quantity=form.quantity.data,
            unit_price=form.unit_price.data,
            notes=form.notes.data
        )
        
        # Update product quantity
        product.quantity -= form.quantity.data
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Successfully removed {form.quantity.data} units from "{product.name}"', 'success')
        return redirect(url_for('stock.index'))
    
    return render_template('stock/remove.html', form=form)
