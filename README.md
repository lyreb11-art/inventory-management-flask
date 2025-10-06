# Inventory Management System - Flask Application

A comprehensive web-based inventory management system built with Flask, featuring user authentication, product management, stock tracking, and detailed reporting.

## 🚀 Features

### Core Features
- **User Authentication**
  - Secure login and registration
  - Password hashing with Werkzeug
  - Session management with Flask-Login
  - Admin user functionality

- **Product Management**
  - Create, Read, Update, Delete (CRUD) operations
  - Product categorization
  - SKU-based product identification
  - Supplier association
  - Low stock alerts
  - Search and filter functionality
  - Pagination for large datasets

- **Stock Management**
  - Stock IN/OUT transactions
  - Real-time quantity tracking
  - Transaction history
  - Minimum quantity thresholds
  - Automatic low stock notifications

- **Category & Supplier Management**
  - Organize products by categories
  - Manage supplier information
  - Contact and address management
  - Relationship tracking

- **Dashboard & Reporting**
  - Real-time inventory statistics
  - Total inventory value calculation
  - Low stock alerts
  - Recent transactions overview
  - Top products by value
  - Category-wise stock analysis
  - Export functionality (CSV)

### Technical Features
- Responsive design with Bootstrap 5
- RESTful API architecture
- SQLAlchemy ORM for database operations
- Flask-WTF for form handling and validation
- Flash messages for user feedback
- Database migrations with Flask-Migrate
- CSRF protection

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 🛠️ Installation

### 1. Clone the Repository

```bash
cd inventory-management-flask
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` file with your settings:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///inventory.db
FLASK_APP=run.py
FLASK_ENV=development
```

### 5. Initialize Database

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

Or simply run the application (database will be created automatically):
```bash
python run.py
```

## 🚀 Running the Application

### Development Server

```bash
python run.py
```

The application will be available at: `http://localhost:5000`

### Default Admin Credentials

```
Username: admin
Password: admin123
```

**⚠️ Important:** Change the admin password after first login in production!

## 📁 Project Structure

```
inventory-management-flask/
│
├── app/
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── forms.py                 # WTForms definitions
│   │
│   ├── routes/                  # Blueprint routes
│   │   ├── __init__.py
│   │   ├── main.py              # Dashboard routes
│   │   ├── auth.py              # Authentication routes
│   │   ├── products.py          # Product CRUD routes
│   │   ├── categories.py        # Category CRUD routes
│   │   ├── suppliers.py         # Supplier CRUD routes
│   │   ├── stock.py             # Stock transaction routes
│   │   └── reports.py           # Reporting routes
│   │
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html            # Base template
│   │   ├── dashboard.html       # Dashboard
│   │   ├── auth/                # Auth templates
│   │   ├── products/            # Product templates
│   │   ├── categories/          # Category templates
│   │   ├── suppliers/           # Supplier templates
│   │   ├── stock/               # Stock templates
│   │   └── reports/             # Report templates
│   │
│   └── static/                  # Static files
│       ├── css/
│       │   └── style.css        # Custom styles
│       └── js/
│           └── script.js        # Custom JavaScript
│
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # Project documentation
```

## 📊 Database Schema

### User
- `id`: Primary key
- `username`: Unique username
- `email`: User email
- `password_hash`: Hashed password
- `is_admin`: Admin flag
- `created_at`: Registration timestamp

### Category
- `id`: Primary key
- `name`: Category name
- `description`: Category description
- `created_at`: Creation timestamp

### Supplier
- `id`: Primary key
- `name`: Supplier name
- `contact_person`: Contact name
- `email`: Supplier email
- `phone`: Phone number
- `address`: Physical address
- `created_at`: Creation timestamp

### Product
- `id`: Primary key
- `name`: Product name
- `sku`: Stock Keeping Unit (unique)
- `description`: Product description
- `quantity`: Current stock quantity
- `min_quantity`: Minimum stock threshold
- `unit_price`: Price per unit
- `category_id`: Foreign key to Category
- `supplier_id`: Foreign key to Supplier
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### StockTransaction
- `id`: Primary key
- `product_id`: Foreign key to Product
- `user_id`: Foreign key to User
- `transaction_type`: 'IN' or 'OUT'
- `quantity`: Transaction quantity
- `unit_price`: Price at transaction time
- `notes`: Transaction notes
- `transaction_date`: Transaction timestamp

## 🔒 Security Features

- Password hashing using Werkzeug
- CSRF protection on all forms
- SQL injection prevention via SQLAlchemy ORM
- Session-based authentication
- Login required decorators for protected routes

## 📈 Usage Guide

### Adding a New Product

1. Navigate to **Products > Add Product**
2. Fill in the product details:
   - Name and SKU (unique)
   - Description
   - Initial quantity
   - Minimum quantity (for low stock alerts)
   - Unit price
   - Select category and supplier
3. Click **Save**

### Managing Stock

**Adding Stock:**
1. Go to **Stock > Add Stock**
2. Select the product
3. Enter quantity to add
4. Optionally add unit price and notes
5. Click **Submit**

**Removing Stock:**
1. Go to **Stock > Remove Stock**
2. Select the product
3. Enter quantity to remove
4. The system will validate sufficient stock
5. Click **Submit**

### Generating Reports

1. Navigate to **Reports**
2. View statistics and summaries
3. Export data:
   - **Export Products**: Downloads all products as CSV
   - **Export Transactions**: Downloads transaction history as CSV

### Low Stock Monitoring

- Dashboard shows low stock count
- Products > Low Stock Alert lists all products below minimum threshold
- Low stock products are highlighted in yellow on the products page

## 🎨 Customization

### Changing Theme Colors

Edit `app/static/css/style.css`:

```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #0dcaf0;
}
```

### Modifying Low Stock Threshold

Edit `config.py`:

```python
LOW_STOCK_THRESHOLD = 10  # Change to desired value
```

### Pagination Settings

Edit `config.py`:

```python
ITEMS_PER_PAGE = 10  # Items per page in lists
```

## 🐛 Troubleshooting

### Database Issues

If you encounter database errors:

```bash
# Delete the database file
rm inventory.db

# Recreate the database
python run.py
```

### Port Already in Use

Change the port in `run.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Module Import Errors

Ensure virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## 🚀 Deployment

### Production Considerations

1. **Change Secret Key:**
   - Generate a strong secret key
   - Set in `.env` file

2. **Disable Debug Mode:**
   ```python
   # In config.py
   DEBUG = False
   ```

3. **Use Production Database:**
   - PostgreSQL or MySQL recommended
   - Update `DATABASE_URL` in `.env`

4. **Use Production Server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

5. **Set Up HTTPS:**
   - Use reverse proxy (Nginx/Apache)
   - Configure SSL certificates

## 📝 API Endpoints

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/register` - Registration page
- `POST /auth/register` - Process registration
- `GET /auth/logout` - Logout

### Products
- `GET /products/` - List all products
- `GET /products/<id>` - View product details
- `GET /products/create` - New product form
- `POST /products/create` - Create new product
- `GET /products/<id>/edit` - Edit product form
- `POST /products/<id>/edit` - Update product
- `POST /products/<id>/delete` - Delete product
- `GET /products/low-stock` - Low stock products

### Stock
- `GET /stock/` - Transaction history
- `GET /stock/add` - Add stock form
- `POST /stock/add` - Process stock addition
- `GET /stock/remove` - Remove stock form
- `POST /stock/remove` - Process stock removal

### Categories
- `GET /categories/` - List categories
- `GET /categories/create` - New category form
- `POST /categories/create` - Create category
- `GET /categories/<id>/edit` - Edit category form
- `POST /categories/<id>/edit` - Update category
- `POST /categories/<id>/delete` - Delete category

### Suppliers
- `GET /suppliers/` - List suppliers
- `GET /suppliers/<id>` - View supplier details
- `GET /suppliers/create` - New supplier form
- `POST /suppliers/create` - Create supplier
- `GET /suppliers/<id>/edit` - Edit supplier form
- `POST /suppliers/<id>/edit` - Update supplier
- `POST /suppliers/<id>/delete` - Delete supplier

### Reports
- `GET /reports/` - Reports dashboard
- `GET /reports/export/products` - Export products CSV
- `GET /reports/export/transactions` - Export transactions CSV

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Flask documentation
- Bootstrap team
- SQLAlchemy documentation
- Flask-Login contributors

## 📞 Support

For support, email your-email@example.com or open an issue in the repository.

## 🔄 Version History

- **1.0.0** (2024-01-XX)
  - Initial release
  - Complete CRUD operations for products, categories, and suppliers
  - Stock management system
  - Dashboard and reporting
  - User authentication

## 🎯 Future Enhancements

- [ ] Barcode scanning support
- [ ] Email notifications for low stock
- [ ] Advanced reporting with charts
- [ ] Multi-warehouse support
- [ ] Purchase order management
- [ ] Sales tracking
- [ ] Mobile app integration
- [ ] Batch import/export
- [ ] User roles and permissions
- [ ] Audit trail for all transactions

---

**Made with ❤️ using Flask**
