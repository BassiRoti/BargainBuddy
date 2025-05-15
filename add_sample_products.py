from app import create_app, db
from app.models import Product, User
from datetime import datetime

app = create_app()

# Define sample product data directly
products_data = [
    # Electronics
    {
        'title': 'Samsung 4K Smart TV 55"',
        'price': 699.99,
        'inventory': 15,
        'expiry_year': 2026,
        'max_discount': 150.00,
        'description': 'Experience stunning clarity and vivid colors with this Samsung 55-inch 4K Smart TV. Features built-in streaming apps and voice control.',
        'image_filename': 'samsung_tv.jpg'
    },
    {
        'title': 'Apple iPhone 13 Pro',
        'price': 999.99,
        'inventory': 25,
        'expiry_year': 2025,
        'max_discount': 200.00,
        'description': 'The latest iPhone with A15 Bionic chip, Pro camera system, and Super Retina XDR display with ProMotion.',
        'image_filename': 'iphone13.jpg'
    },
    {
        'title': 'Sony WH-1000XM4 Headphones',
        'price': 349.99,
        'inventory': 30,
        'expiry_year': 2025,
        'max_discount': 75.00,
        'description': 'Industry-leading noise cancellation with premium sound quality. Up to 30 hours of battery life.',
        'image_filename': 'sony_headphones.jpg'
    },
    {
        'title': 'Dell XPS 13 Laptop',
        'price': 1299.99,
        'inventory': 10,
        'expiry_year': 2026,
        'max_discount': 250.00,
        'description': '13-inch InfinityEdge display, 11th Gen Intel Core i7, 16GB RAM, 512GB SSD.',
        'image_filename': 'dell_xps.jpg'
    },
    {
        'title': 'Nintendo Switch OLED',
        'price': 349.99,
        'inventory': 20,
        'expiry_year': 2025,
        'max_discount': 50.00,
        'description': 'Featuring a vibrant 7-inch OLED screen, enhanced audio, and 64GB of internal storage.',
        'image_filename': 'nintendo_switch.jpg'
    },
    
    # Home & Kitchen
    {
        'title': 'Instant Pot Duo 7-in-1',
        'price': 99.99,
        'inventory': 40,
        'expiry_year': 2026,
        'max_discount': 30.00,
        'description': 'Pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yogurt maker, and warmer in one appliance.',
        'image_filename': 'instant_pot.jpg'
    },
    {
        'title': 'Dyson V11 Cordless Vacuum',
        'price': 599.99,
        'inventory': 12,
        'expiry_year': 2025,
        'max_discount': 100.00,
        'description': 'Intelligent cordless vacuum with powerful suction and up to 60 minutes of run time.',
        'image_filename': 'dyson_vacuum.jpg'
    },
    {
        'title': 'KitchenAid Stand Mixer',
        'price': 379.99,
        'inventory': 15,
        'expiry_year': 2027,
        'max_discount': 80.00,
        'description': 'Professional 5-quart mixer with 10-speed settings and various attachments for versatile cooking.',
        'image_filename': 'kitchenaid_mixer.jpg'
    },
    {
        'title': 'Nespresso Vertuo Coffee Maker',
        'price': 199.99,
        'inventory': 25,
        'expiry_year': 2025,
        'max_discount': 50.00,
        'description': 'Makes both coffee and espresso with the touch of a button. Includes Aeroccino milk frother.',
        'image_filename': 'nespresso.jpg'
    },
    {
        'title': 'Cuisinart Air Fryer Toaster Oven',
        'price': 199.99,
        'inventory': 18,
        'expiry_year': 2026,
        'max_discount': 60.00,
        'description': '7-in-1 appliance: air fryer, convection oven, toaster, broiler, and more.',
        'image_filename': 'cuisinart_airfryer.jpg'
    },
    
    # Clothing
    {
        'title': 'Nike Air Max 270 Sneakers',
        'price': 150.00,
        'inventory': 35,
        'expiry_year': 2024,
        'max_discount': 45.00,
        'description': 'Lifestyle sneakers with the first-ever Max Air unit designed specifically for Nike Sportswear.',
        'image_filename': 'nike_airmax.jpg'
    },
    {
        'title': 'Levi\'s 501 Original Jeans',
        'price': 69.99,
        'inventory': 50,
        'expiry_year': 2024,
        'max_discount': 25.00,
        'description': 'The iconic straight fit jeans that started it all. Original fit, straight leg, button fly.',
        'image_filename': 'levis_jeans.jpg'
    },
    {
        'title': 'North Face Thermoball Jacket',
        'price': 199.99,
        'inventory': 20,
        'expiry_year': 2024,
        'max_discount': 60.00,
        'description': 'Lightweight, packable insulation that keeps you warm even when wet.',
        'image_filename': 'northface_jacket.jpg'
    },
    {
        'title': 'Ray-Ban Aviator Sunglasses',
        'price': 154.00,
        'inventory': 25,
        'expiry_year': 2026,
        'max_discount': 40.00,
        'description': 'Iconic pilot-shaped sunglasses with 100% UV protection.',
        'image_filename': 'rayban_aviator.jpg'
    },
    {
        'title': 'Adidas Ultraboost Running Shoes',
        'price': 180.00,
        'inventory': 30,
        'expiry_year': 2024,
        'max_discount': 50.00,
        'description': 'Responsive running shoes with energy-returning Boost cushioning.',
        'image_filename': 'adidas_ultraboost.jpg'
    },
    
    # Toys & Games
    {
        'title': 'LEGO Star Wars Millennium Falcon',
        'price': 159.99,
        'inventory': 15,
        'expiry_year': 2025,
        'max_discount': 35.00,
        'description': 'Iconic Millennium Falcon set with 1,353 pieces and 7 minifigures.',
        'image_filename': 'lego_falcon.jpg'
    },
    {
        'title': 'PlayStation 5 Console',
        'price': 499.99,
        'inventory': 8,
        'expiry_year': 2026,
        'max_discount': 50.00,
        'description': 'Next-gen gaming console with ultra-high speed SSD, 3D audio, and haptic feedback.',
        'image_filename': 'ps5.jpg'
    },
    {
        'title': 'Monopoly Board Game',
        'price': 19.99,
        'inventory': 40,
        'expiry_year': 2025,
        'max_discount': 5.00,
        'description': 'Classic property trading board game for the whole family.',
        'image_filename': 'monopoly.jpg'
    },
    {
        'title': 'Fisher-Price Learning Toy',
        'price': 29.99,
        'inventory': 35,
        'expiry_year': 2024,
        'max_discount': 10.00,
        'description': 'Educational toy that helps develop motor skills and interactive learning for toddlers.',
        'image_filename': 'fisher_price.jpg'
    },
    {
        'title': 'Barbie Dreamhouse',
        'price': 179.99,
        'inventory': 12,
        'expiry_year': 2025,
        'max_discount': 45.00,
        'description': 'Three-story dollhouse with 8 rooms, a working elevator, pool, and 70+ accessories.',
        'image_filename': 'barbie_dreamhouse.jpg'
    },
    
    # Beauty & Personal Care
    {
        'title': 'Dyson Airwrap Complete Styler',
        'price': 549.99,
        'inventory': 10,
        'expiry_year': 2026,
        'max_discount': 100.00,
        'description': 'Complete styling system with multiple attachments for various hair types.',
        'image_filename': 'dyson_airwrap.jpg'
    },
    {
        'title': 'La Mer Moisturizing Cream',
        'price': 190.00,
        'inventory': 15,
        'expiry_year': 2024,
        'max_discount': 40.00,
        'description': 'Luxury face cream with sea kelp, minerals, and other nutrients for hydration.',
        'image_filename': 'lamer_cream.jpg'
    },
    {
        'title': 'Philips Sonicare DiamondClean',
        'price': 199.99,
        'inventory': 25,
        'expiry_year': 2025,
        'max_discount': 60.00,
        'description': 'Advanced sonic toothbrush with 5 cleaning modes and smart brush head recognition.',
        'image_filename': 'philips_sonicare.jpg'
    },
    {
        'title': 'Olaplex Hair Perfector No. 3',
        'price': 28.00,
        'inventory': 40,
        'expiry_year': 2024,
        'max_discount': 8.00,
        'description': 'At-home hair treatment that reduces breakage and visibly strengthens hair.',
        'image_filename': 'olaplex.jpg'
    },
    {
        'title': 'Theragun Elite Massage Gun',
        'price': 399.00,
        'inventory': 12,
        'expiry_year': 2025,
        'max_discount': 80.00,
        'description': 'Premium deep tissue massage device with 5 built-in speeds and smart app integration.',
        'image_filename': 'theragun.jpg'
    }
]

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        print("Admin user not found! Please run init_db.py first to create the admin user.")
    else:
        print(f"Found admin user: {admin.username} ({admin.email})")
        
        print(f"Adding {len(products_data)} products to the database...")
        
        # Add products to database
        for product_data in products_data:
            new_product = Product(
                title=product_data['title'],
                price=product_data['price'],
                inventory=product_data['inventory'],
                expiry_year=product_data['expiry_year'],
                max_discount=product_data['max_discount'],
                description=product_data['description'],
                image_filename=product_data['image_filename'],
                created_at=datetime.utcnow()
            )
            db.session.add(new_product)
        
        # Commit changes
        db.session.commit()
        print(f"Successfully added {len(products_data)} products to the database!")
        print("You can now login as admin (username: admin, password: admin123) to view and manage these products.") 