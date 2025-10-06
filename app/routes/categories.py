from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Category
from app.forms import CategoryForm

bp = Blueprint('categories', __name__, url_prefix='/categories')


@bp.route('/')
@login_required
def index():
    """List all categories"""
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories/index.html', categories=categories)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category "{category.name}" created successfully!', 'success')
        return redirect(url_for('categories.index'))
    
    return render_template('categories/create.html', form=form)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit category"""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        
        flash(f'Category "{category.name}" updated successfully!', 'success')
        return redirect(url_for('categories.index'))
    
    return render_template('categories/edit.html', form=form, category=category)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete category"""
    category = Category.query.get_or_404(id)
    name = category.name
    
    if category.products.count() > 0:
        flash(f'Cannot delete category "{name}" because it has products!', 'danger')
        return redirect(url_for('categories.index'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash(f'Category "{name}" deleted successfully!', 'success')
    return redirect(url_for('categories.index'))
