from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Category model for product categorization"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Supplier(db.Model):
    """Supplier model for vendor management"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='supplier', lazy='dynamic')
    
    def __repr__(self):
        return f'<Supplier {self.name}>'


class Product(db.Model):
    """Product model for inventory items"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    min_quantity = db.Column(db.Integer, default=10)
    unit_price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('StockTransaction', backref='product', lazy='dynamic', 
                                   cascade='all, delete-orphan')
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.min_quantity
    
    @property
    def total_value(self):
        return self.quantity * self.unit_price
    
    def __repr__(self):
        return f'<Product {self.name}>'


class StockTransaction(db.Model):
    """Stock transaction model for tracking inventory movements"""
    __tablename__ = 'stock_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'IN' or 'OUT'
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float)
    notes = db.Column(db.Text)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = db.relationship('User', backref='transactions')
    
    def __repr__(self):
        return f'<StockTransaction {self.transaction_type} {self.quantity}>'
