from app import create_app, db
from app.models import Product

def fix_categories():
    app = create_app()
    with app.app_context():
        # First, delete all products
        Product.query.delete()
        db.session.commit()

        # Define all products with correct categories
        products = {
            'Electronics': [
                {
                    'title': 'Smart LED TV 55"',
                    'price': 699.99,
                    'inventory': 50,
                    'expiry_year': 2025,
                    'max_discount': 150.00,
                    'description': 'Ultra HD 4K Smart LED TV with HDR support',
                    'image_filename': 'tv.jpg'
                },
                {
                    'title': 'Wireless Noise-Canceling Headphones',
                    'price': 199.99,
                    'inventory': 100,
                    'expiry_year': 2025,
                    'max_discount': 50.00,
                    'description': 'Premium wireless headphones with active noise cancellation',
                    'image_filename': 'headphones.jpg'
                },
                {
                    'title': 'Smartphone Pro Max',
                    'price': 999.99,
                    'inventory': 75,
                    'expiry_year': 2025,
                    'max_discount': 200.00,
                    'description': '6.7" OLED display, 5G capable, triple camera system',
                    'image_filename': 'smartphone.jpg'
                },
                {
                    'title': 'Dell XPS 13 Laptop',
                    'price': 1299.99,
                    'inventory': 30,
                    'expiry_year': 2025,
                    'max_discount': 200.00,
                    'description': 'Premium ultrabook with InfinityEdge display',
                    'image_filename': 'laptop.jpg'
                },
                {
                    'title': 'Apple iPad Pro',
                    'price': 799.99,
                    'inventory': 45,
                    'expiry_year': 2025,
                    'max_discount': 150.00,
                    'description': '11-inch Liquid Retina display, M1 chip',
                    'image_filename': 'ipad.jpg'
                }
            ],
            'Fashion': [
                {
                    'title': 'Designer Leather Handbag',
                    'price': 299.99,
                    'inventory': 30,
                    'expiry_year': 2025,
                    'max_discount': 75.00,
                    'description': 'Genuine leather designer handbag with gold hardware',
                    'image_filename': 'handbag.jpg'
                },
                {
                    'title': 'Men\'s Classic Watch',
                    'price': 159.99,
                    'inventory': 45,
                    'expiry_year': 2025,
                    'max_discount': 40.00,
                    'description': 'Stainless steel analog watch with leather strap',
                    'image_filename': 'watch.jpg'
                },
                {
                    'title': 'Athletic Running Shoes',
                    'price': 89.99,
                    'inventory': 120,
                    'expiry_year': 2024,
                    'max_discount': 30.00,
                    'description': 'Lightweight breathable running shoes with cushioned sole',
                    'image_filename': 'shoes.jpg'
                },
                {
                    'title': 'Designer Sunglasses',
                    'price': 199.99,
                    'inventory': 35,
                    'expiry_year': 2026,
                    'max_discount': 50.00,
                    'description': 'Polarized UV protection sunglasses',
                    'image_filename': 'sunglasses.jpg'
                },
                {
                    'title': 'Leather Wallet',
                    'price': 49.99,
                    'inventory': 80,
                    'expiry_year': 2026,
                    'max_discount': 15.00,
                    'description': 'Genuine leather bifold wallet',
                    'image_filename': 'wallet.jpg'
                }
            ],
            'Home & Living': [
                {
                    'title': 'Smart Coffee Maker',
                    'price': 129.99,
                    'inventory': 60,
                    'expiry_year': 2025,
                    'max_discount': 35.00,
                    'description': 'WiFi-enabled coffee maker with programmable brewing',
                    'image_filename': 'coffee_maker.jpg'
                },
                {
                    'title': 'Memory Foam Mattress',
                    'price': 599.99,
                    'inventory': 25,
                    'expiry_year': 2025,
                    'max_discount': 150.00,
                    'description': 'Queen size memory foam mattress with cooling technology',
                    'image_filename': 'mattress.jpg'
                },
                {
                    'title': 'Robot Vacuum Cleaner',
                    'price': 249.99,
                    'inventory': 40,
                    'expiry_year': 2025,
                    'max_discount': 70.00,
                    'description': 'Smart robot vacuum with mapping technology',
                    'image_filename': 'vacuum.jpg'
                },
                {
                    'title': 'Air Purifier',
                    'price': 199.99,
                    'inventory': 50,
                    'expiry_year': 2025,
                    'max_discount': 50.00,
                    'description': 'HEPA air purifier with smart sensors',
                    'image_filename': 'air_purifier.jpg'
                },
                {
                    'title': 'Stand Mixer',
                    'price': 299.99,
                    'inventory': 30,
                    'expiry_year': 2025,
                    'max_discount': 75.00,
                    'description': 'Professional stand mixer with multiple attachments',
                    'image_filename': 'mixer.jpg'
                }
            ],
            'Gaming': [
                {
                    'title': 'Gaming Console Pro',
                    'price': 499.99,
                    'inventory': 35,
                    'expiry_year': 2025,
                    'max_discount': 100.00,
                    'description': 'Next-gen gaming console with 4K graphics',
                    'image_filename': 'console.jpg'
                },
                {
                    'title': 'Gaming Laptop',
                    'price': 1299.99,
                    'inventory': 20,
                    'expiry_year': 2025,
                    'max_discount': 300.00,
                    'description': '15.6" gaming laptop with RTX graphics',
                    'image_filename': 'gaming_laptop.jpg'
                },
                {
                    'title': 'Gaming Mouse',
                    'price': 59.99,
                    'inventory': 150,
                    'expiry_year': 2025,
                    'max_discount': 20.00,
                    'description': 'RGB gaming mouse with programmable buttons',
                    'image_filename': 'gaming_mouse.jpg'
                },
                {
                    'title': 'Gaming Keyboard',
                    'price': 129.99,
                    'inventory': 75,
                    'expiry_year': 2025,
                    'max_discount': 30.00,
                    'description': 'Mechanical gaming keyboard with RGB lighting',
                    'image_filename': 'keyboard.jpg'
                },
                {
                    'title': 'Gaming Headset',
                    'price': 89.99,
                    'inventory': 100,
                    'expiry_year': 2025,
                    'max_discount': 25.00,
                    'description': 'Surround sound gaming headset with mic',
                    'image_filename': 'headset.jpg'
                }
            ],
            'Beauty & Personal Care': [
                {
                    'title': 'Hair Dryer Pro',
                    'price': 199.99,
                    'inventory': 40,
                    'expiry_year': 2025,
                    'max_discount': 50.00,
                    'description': 'Professional hair dryer with ionic technology',
                    'image_filename': 'hair_dryer.jpg'
                },
                {
                    'title': 'Electric Toothbrush',
                    'price': 89.99,
                    'inventory': 60,
                    'expiry_year': 2025,
                    'max_discount': 25.00,
                    'description': 'Smart electric toothbrush with pressure sensor',
                    'image_filename': 'toothbrush.jpg'
                },
                {
                    'title': 'Face Cream',
                    'price': 49.99,
                    'inventory': 100,
                    'expiry_year': 2024,
                    'max_discount': 15.00,
                    'description': 'Hydrating face cream with natural ingredients',
                    'image_filename': 'face_cream.jpg'
                },
                {
                    'title': 'Hair Straightener',
                    'price': 129.99,
                    'inventory': 45,
                    'expiry_year': 2025,
                    'max_discount': 35.00,
                    'description': 'Ceramic hair straightener with temperature control',
                    'image_filename': 'straightener.jpg'
                },
                {
                    'title': 'Electric Shaver',
                    'price': 159.99,
                    'inventory': 50,
                    'expiry_year': 2025,
                    'max_discount': 40.00,
                    'description': 'Waterproof electric shaver with precision trimmer',
                    'image_filename': 'shaver.jpg'
                }
            ]
        }

        # Add all products to database
        for category, category_products in products.items():
            for product_data in category_products:
                product = Product(
                    title=product_data['title'],
                    price=product_data['price'],
                    inventory=product_data['inventory'],
                    expiry_year=product_data['expiry_year'],
                    max_discount=product_data['max_discount'],
                    description=product_data['description'],
                    image_filename=product_data['image_filename'],
                    category=category
                )
                db.session.add(product)

        db.session.commit()
        print("Categories fixed successfully!")

if __name__ == '__main__':
    fix_categories() 