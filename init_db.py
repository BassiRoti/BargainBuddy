from app import create_app, db
from app.models import User, Product, Cart, CartItem, Order, OrderItem

app = create_app()

with app.app_context():
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        name='Admin User',
        is_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create some sample products
    products = [
        Product(
            title='Sample Product 1',
            price=99.99,
            inventory=100,
            expiry_year=2025,
            max_discount=15.00,
            image_filename='default.png'
        ),
        Product(
            title='Sample Product 2',
            price=149.99,
            inventory=50,
            expiry_year=2026,
            max_discount=22.50,
            image_filename='default.png'
        )
    ]
    
    for product in products:
        db.session.add(product)
    
    # Commit all changes
    db.session.commit()
    
    print("Database initialized successfully!") 