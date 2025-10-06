from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, Supplier
from app.forms import ProductForm

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
@login_required
def index():
    """List all products"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category', 0, type=int)
    
    query = Product.query
    
    # Apply search filter
    if search:
        query = query.filter(Product.name.contains(search) | Product.sku.contains(search))
    
    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.order_by(Product.name).paginate(
        page=page, per_page=10, error_out=False
    )
    
    categories = Category.query.order_by(Category.name).all()
    
    return render_template('products/index.html',
                         products=products,
                         categories=categories,
                         search=search,
                         category_id=category_id)


@bp.route('/<int:id>')
@login_required
def view(id):
    """View product details"""
    product = Product.query.get_or_404(id)
    return render_template('products/view.html', product=product)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new product"""
    form = ProductForm()
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            sku=form.sku.data,
            description=form.description.data,
            quantity=form.quantity.data,
            min_quantity=form.min_quantity.data,
            unit_price=form.unit_price.data,
            category_id=form.category.data,
            supplier_id=form.supplier.data
        )
        db.session.add(product)
        db.session.commit()
        
        flash(f'Product "{product.name}" created successfully!', 'success')
        return redirect(url_for('products.index'))
    
    return render_template('products/create.html', form=form)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit product"""
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.sku = form.sku.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        product.min_quantity = form.min_quantity.data
        product.unit_price = form.unit_price.data
        product.category_id = form.category.data
        product.supplier_id = form.supplier.data
        
        db.session.commit()
        
        flash(f'Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('products.view', id=product.id))
    
    return render_template('products/edit.html', form=form, product=product)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete product"""
    product = Product.query.get_or_404(id)
    name = product.name
    
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Product "{name}" deleted successfully!', 'success')
    return redirect(url_for('products.index'))


@bp.route('/low-stock')
@login_required
def low_stock():
    """List products with low stock"""
    products = Product.query.filter(
        Product.quantity <= Product.min_quantity
    ).order_by(Product.quantity).all()
    
    return render_template('products/low_stock.html', products=products)
