from app import create_app, db
from app.models import Product

def check_database():
    app = create_app()
    with app.app_context():
        # Get all categories
        categories = db.session.query(Product.category).distinct().all()
        categories = [cat[0] for cat in categories]
        
        print("\nCategories and their products:")
        print("==============================")
        
        for category in categories:
            products = Product.query.filter_by(category=category).all()
            total_inventory = sum(p.inventory for p in products)
            print(f"\n{category}:")
            print(f"Number of unique products: {len(products)}")
            print(f"Total inventory across all products: {total_inventory}")
            print("\nProducts:")
            for product in products:
                print(f"- {product.title} (${float(product.price):.2f}, {product.inventory} in stock)")

if __name__ == '__main__':
    check_database() 