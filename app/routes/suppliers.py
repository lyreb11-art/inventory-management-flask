from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Supplier
from app.forms import SupplierForm

bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')


@bp.route('/')
@login_required
def index():
    """List all suppliers"""
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template('suppliers/index.html', suppliers=suppliers)


@bp.route('/<int:id>')
@login_required
def view(id):
    """View supplier details"""
    supplier = Supplier.query.get_or_404(id)
    return render_template('suppliers/view.html', supplier=supplier)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new supplier"""
    form = SupplierForm()
    
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            contact_person=form.contact_person.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(supplier)
        db.session.commit()
        
        flash(f'Supplier "{supplier.name}" created successfully!', 'success')
        return redirect(url_for('suppliers.index'))
    
    return render_template('suppliers/create.html', form=form)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit supplier"""
    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=supplier)
    
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.contact_person = form.contact_person.data
        supplier.email = form.email.data
        supplier.phone = form.phone.data
        supplier.address = form.address.data
        db.session.commit()
        
        flash(f'Supplier "{supplier.name}" updated successfully!', 'success')
        return redirect(url_for('suppliers.view', id=supplier.id))
    
    return render_template('suppliers/edit.html', form=form, supplier=supplier)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete supplier"""
    supplier = Supplier.query.get_or_404(id)
    name = supplier.name
    
    if supplier.products.count() > 0:
        flash(f'Cannot delete supplier "{name}" because it has products!', 'danger')
        return redirect(url_for('suppliers.index'))
    
    db.session.delete(supplier)
    db.session.commit()
    
    flash(f'Supplier "{name}" deleted successfully!', 'success')
    return redirect(url_for('suppliers.index'))
