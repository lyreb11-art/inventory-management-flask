from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, FloatField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length
from app.models import User, Product


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    """Registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose another.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another.')


class CategoryForm(FlaskForm):
    """Category form"""
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')


class SupplierForm(FlaskForm):
    """Supplier form"""
    name = StringField('Supplier Name', validators=[DataRequired(), Length(max=100)])
    contact_person = StringField('Contact Person', validators=[Length(max=100)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone', validators=[Length(max=20)])
    address = TextAreaField('Address')


class ProductForm(FlaskForm):
    """Product form"""
    name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    sku = StringField('SKU', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    min_quantity = IntegerField('Minimum Quantity', 
                               validators=[DataRequired(), NumberRange(min=0)])
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', coerce=int)
    supplier = SelectField('Supplier', coerce=int)
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        from app.models import Category, Supplier
        self.category.choices = [(0, '-- Select Category --')] + [
            (c.id, c.name) for c in Category.query.order_by(Category.name).all()
        ]
        self.supplier.choices = [(0, '-- Select Supplier --')] + [
            (s.id, s.name) for s in Supplier.query.order_by(Supplier.name).all()
        ]


class StockTransactionForm(FlaskForm):
    """Stock transaction form"""
    product = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    unit_price = FloatField('Unit Price', validators=[NumberRange(min=0)])
    notes = TextAreaField('Notes')
    transaction_type = HiddenField('Transaction Type')
    
    def __init__(self, *args, **kwargs):
        super(StockTransactionForm, self).__init__(*args, **kwargs)
        from app.models import Product
        self.product.choices = [(p.id, f'{p.name} ({p.sku})') 
                               for p in Product.query.order_by(Product.name).all()]
