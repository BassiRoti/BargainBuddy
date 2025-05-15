from app import create_app, db
from app.models import Product

def update_categories():
    app = create_app()
    with app.app_context():
        # Update existing products with appropriate categories based on their titles
        products = Product.query.all()
        for product in products:
            title = product.title.lower()
            if any(term in title for term in ['tv', 'phone', 'headphone', 'laptop', 'nintendo', 'playstation', 'console']):
                product.category = 'Electronics'
            elif any(term in title for term in ['pot', 'vacuum', 'mixer', 'coffee', 'air fryer', 'kitchen']):
                product.category = 'Home & Kitchen'
            elif any(term in title for term in ['sneakers', 'jeans', 'jacket', 'sunglasses', 'shoes']):
                product.category = 'Clothing'
            elif any(term in title for term in ['lego', 'game', 'toy', 'barbie', 'monopoly']):
                product.category = 'Toys & Games'
            elif any(term in title for term in ['cream', 'hair', 'beauty', 'styler', 'toothbrush']):
                product.category = 'Beauty & Personal Care'
            else:
                product.category = 'Other'
        
        db.session.commit()
        print("Categories updated successfully!")

if __name__ == '__main__':
    update_categories() 