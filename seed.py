from datetime import datetime
from werkzeug.security import generate_password_hash

# Imports will be attempted within the app_context setup

def create_admin_and_products(app_instance, db_instance, user_model, product_model):
    """
    Creates a default admin user if one doesn't exist,
    and then adds some sample products for that admin.
    Requires app, db, User, and Product to be passed in.
    """
    User = user_model
    Product = product_model
    db = db_instance

    # --- Admin User Details ---
    admin_username = "abbas"
    admin_email = "abbas@gmail.com"
    admin_password = "12345678"
    admin_name = "abbas"

    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user:
        # If not found by username, try by email as a fallback, common for existing users
        admin_user = User.query.filter_by(email=admin_email).first()

    if not admin_user:
        print(f"Creating admin user: {admin_username}")
        hashed_password = generate_password_hash(admin_password)
        admin_user = User(
            username=admin_username,
            email=admin_email,
            password=hashed_password,
            name=admin_name, # Corrected from admin_username to admin_name
            is_admin=True,
            business_name=f"{admin_name}'s Store", # Example business name
            created_at=datetime.utcnow()
        )
        db.session.add(admin_user)
        try:
            db.session.commit()
            print(f"Admin user '{admin_username}' created successfully.")
            # Refresh admin_user to get ID if newly created
            db.session.refresh(admin_user)
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user '{admin_username}': {e}")
            # Attempt to fetch again if creation failed due to concurrent write or similar
            admin_user = User.query.filter_by(username=admin_username).first() 
            if not admin_user: 
                admin_user = User.query.filter_by(email=admin_email).first()
            if not admin_user:
                 print(f"Could not retrieve or create admin user '{admin_username}'. Aborting product seed.")
                 return # Critical to have an admin user
            else:
                print(f"Admin user '{admin_username}' already existed or was created concurrently.")

    else:
        print(f"Admin user '{admin_user.username}' already exists.")
        if not admin_user.is_admin:
            print(f"Updating user '{admin_user.username}' to be an admin.")
            admin_user.is_admin = True
            try:
                db.session.commit()
                print(f"User '{admin_user.username}' updated to admin successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Error updating user '{admin_user.username}' to admin: {e}")
                # Proceeding anyway, might still be able to add products if ID is valid
        # Ensure name is also updated if it was different
        if admin_user.name != admin_name:
            print(f"Updating name for user '{admin_user.username}' to '{admin_name}'.")
            admin_user.name = admin_name
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error updating name for user '{admin_user.username}': {e}")

    if not admin_user or not admin_user.id:
        print(f"Could not obtain a valid ID for admin user '{admin_username}'. Cannot add products.")
        return

    print(f"Using admin user: {admin_user.username} (ID: {admin_user.id}) for products.")

    products_data = [
        {
            "title": "Vintage Leather Wallet", "price": 29.99, "inventory": 50, "expiry_year": 2099,
            "max_discount": 5.00, "image_filename": "wallet.jpg",
            "description": "A stylish vintage leather wallet with multiple compartments.", "category": "Accessories"
        },
        {
            "title": "Wireless Bluetooth Headphones", "price": 79.50, "inventory": 30, "expiry_year": 2099,
            "max_discount": 10.00, "image_filename": "headphones.jpg",
            "description": "High-quality sound, long battery life, and comfortable design.", "category": "Electronics"
        },
        {
            "title": "Organic Green Tea", "price": 12.00, "inventory": 100, "expiry_year": 2026,
            "max_discount": 1.50, "image_filename": "greentea.jpg",
            "description": "Refreshing and healthy organic green tea, 50 bags.", "category": "Groceries"
        },
        {
            "title": "Smartwatch Series X", "price": 199.99, "inventory": 25, "expiry_year": 2099,
            "max_discount": 20.00, "image_filename": "smartwatch_x.jpg",
            "description": "Latest smartwatch with HR monitor, GPS, and long battery life.", "category": "Electronics"
        },
        {
            "title": "Portable Power Bank 20000mAh", "price": 45.00, "inventory": 75, "expiry_year": 2099,
            "max_discount": 5.00, "image_filename": "powerbank_20k.jpg",
            "description": "High-capacity power bank to charge your devices on the go.", "category": "Electronics"
        },
        {
            "title": "Ultra HD 4K Webcam", "price": 65.00, "inventory": 40, "expiry_year": 2099,
            "max_discount": 7.50, "image_filename": "webcam_4k.jpg",
            "description": "Crystal clear video for streaming and video conferencing.", "category": "Electronics"
        },
        {
            "title": "Noise Cancelling Earbuds", "price": 120.00, "inventory": 30, "expiry_year": 2099,
            "max_discount": 15.00, "image_filename": "earbuds_nc.jpg",
            "description": "Immersive sound experience with active noise cancellation.", "category": "Electronics"
        },
        {
            "title": "Espresso Coffee Machine", "price": 250.00, "inventory": 15, "expiry_year": 2099,
            "max_discount": 30.00, "image_filename": "espresso_machine.jpg",
            "description": "Barista-quality espresso at home. Easy to use and clean.", "category": "Home & Kitchen"
        },
        {
            "title": "Robotic Vacuum Cleaner", "price": 350.00, "inventory": 20, "expiry_year": 2099,
            "max_discount": 40.00, "image_filename": "robot_vacuum.jpg",
            "description": "Smart robotic vacuum with auto-charging and mapping.", "category": "Home & Kitchen"
        },
        {
            "title": "Air Fryer XL 5.8QT", "price": 89.99, "inventory": 60, "expiry_year": 2099,
            "max_discount": 10.00, "image_filename": "air_fryer_xl.jpg",
            "description": "Healthy cooking with less oil. Large capacity for families.", "category": "Home & Kitchen"
        },
        {
            "title": "Premium Chef Knife Set", "price": 150.00, "inventory": 35, "expiry_year": 2099,
            "max_discount": 20.00, "image_filename": "knife_set.jpg",
            "description": "High-carbon stainless steel knives for all your cooking needs.", "category": "Home & Kitchen"
        },
        {
            "title": "The Midnight Library", "price": 15.99, "inventory": 100, "expiry_year": 2099,
            "max_discount": 2.00, "image_filename": "midnight_library.jpg",
            "description": "A novel by Matt Haig. What if you could live all your possible lives?", "category": "Books"
        },
        {
            "title": "Sapiens: A Brief History of Humankind", "price": 18.50, "inventory": 80, "expiry_year": 2099,
            "max_discount": 2.50, "image_filename": "sapiens_book.jpg",
            "description": "By Yuval Noah Harari. A sweeping exploration of human history.", "category": "Books"
        },
        {
            "title": "Atomic Habits", "price": 14.00, "inventory": 120, "expiry_year": 2099,
            "max_discount": 1.50, "image_filename": "atomic_habits.jpg",
            "description": "An Easy & Proven Way to Build Good Habits & Break Bad Ones by James Clear.", "category": "Books"
        },
        {
            "title": "Men\'s Classic Cotton T-Shirt", "price": 19.99, "inventory": 200, "expiry_year": 2099,
            "max_discount": 3.00, "image_filename": "mens_tshirt.jpg",
            "description": "Comfortable and durable 100% cotton t-shirt.", "category": "Clothing & Fashion"
        },
        {
            "title": "Women\'s Yoga Pants", "price": 35.00, "inventory": 150, "expiry_year": 2099,
            "max_discount": 5.00, "image_filename": "womens_yoga_pants.jpg",
            "description": "Stretchy and breathable yoga pants for ultimate comfort.", "category": "Clothing & Fashion"
        },
        {
            "title": "Unisex Running Shoes", "price": 85.00, "inventory": 80, "expiry_year": 2099,
            "max_discount": 10.00, "image_filename": "running_shoes.jpg",
            "description": "Lightweight and supportive running shoes for all terrains.", "category": "Clothing & Fashion"
        },
        {
            "title": "Yoga Mat Premium", "price": 25.00, "inventory": 90, "expiry_year": 2099,
            "max_discount": 3.00, "image_filename": "yoga_mat.jpg",
            "description": "Eco-friendly, non-slip yoga mat for your daily practice.", "category": "Sports & Outdoors"
        },
        {
            "title": "Adjustable Dumbbell Set", "price": 120.00, "inventory": 40, "expiry_year": 2099,
            "max_discount": 15.00, "image_filename": "dumbbell_set.jpg",
            "description": "Space-saving adjustable dumbbells, perfect for home gyms.", "category": "Sports & Outdoors"
        },
        {
            "title": "Camping Tent for 2 Persons", "price": 75.00, "inventory": 50, "expiry_year": 2099,
            "max_discount": 8.00, "image_filename": "camping_tent.jpg",
            "description": "Waterproof and easy-to-setup tent for outdoor adventures.", "category": "Sports & Outdoors"
        },
        {
            "title": "Premium Arabica Coffee Beans 1kg", "price": 22.00, "inventory": 70, "expiry_year": 2025,
            "max_discount": 2.00, "image_filename": "coffee_beans.jpg",
            "description": "Whole bean arabica coffee, rich aroma and smooth taste.", "category": "Groceries"
        },
        {
            "title": "Extra Virgin Olive Oil 500ml", "price": 15.00, "inventory": 60, "expiry_year": 2025,
            "max_discount": 1.50, "image_filename": "olive_oil.jpg",
            "description": "Cold-pressed extra virgin olive oil, perfect for cooking and salads.", "category": "Groceries"
        },
        {
            "title": "Building Blocks Set (1000 pcs)", "price": 40.00, "inventory": 80, "expiry_year": 2099,
            "max_discount": 5.00, "image_filename": "building_blocks.jpg",
            "description": "Classic building blocks for endless creative fun.", "category": "Toys & Games"
        },
        {
            "title": "Strategy Board Game - Settlers", "price": 49.99, "inventory": 30, "expiry_year": 2099,
            "max_discount": 7.00, "image_filename": "board_game_settlers.jpg",
            "description": "Award-winning strategy board game for family and friends.", "category": "Toys & Games"
        },
        {
            "title": "Organic Face Serum", "price": 28.00, "inventory": 50, "expiry_year": 2025,
            "max_discount": 3.00, "image_filename": "face_serum.jpg",
            "description": "Hydrating and anti-aging face serum with natural ingredients.", "category": "Beauty & Personal Care"
        },
        {
            "title": "Electric Toothbrush Sonic", "price": 55.00, "inventory": 60, "expiry_year": 2099,
            "max_discount": 6.00, "image_filename": "electric_toothbrush.jpg",
            "description": "Advanced sonic toothbrush for superior cleaning.", "category": "Beauty & Personal Care"
        },
        {
            "title": "Gaming Mouse RGB", "price": 35.00, "inventory": 60, "expiry_year": 2099,
            "max_discount": 4.00, "image_filename": "gaming_mouse.jpg",
            "description": "Ergonomic gaming mouse with customizable RGB lighting.", "category": "Electronics"
        },
        {
            "title": "Mechanical Keyboard (Blue Switch)", "price": 70.00, "inventory": 45, "expiry_year": 2099,
            "max_discount": 8.00, "image_filename": "mech_keyboard.jpg",
            "description": "Tactile and responsive mechanical keyboard for typing and gaming.", "category": "Electronics"
        },
        {
            "title": "Bluetooth Speaker Waterproof", "price": 50.00, "inventory": 70, "expiry_year": 2099,
            "max_discount": 6.00, "image_filename": "bt_speaker.jpg",
            "description": "Portable and waterproof Bluetooth speaker for outdoor use.", "category": "Electronics"
        },
        {
            "title": "Blender High-Speed Pro", "price": 99.00, "inventory": 30, "expiry_year": 2099,
            "max_discount": 12.00, "image_filename": "blender_pro.jpg",
            "description": "Powerful blender for smoothies, soups, and more.", "category": "Home & Kitchen"
        },
        {
            "title": "Non-Stick Cookware Set (10 pcs)", "price": 120.00, "inventory": 25, "expiry_year": 2099,
            "max_discount": 15.00, "image_filename": "cookware_set.jpg",
            "description": "Durable non-stick pots and pans for everyday cooking.", "category": "Home & Kitchen"
        },
        {
            "title": "Smart WiFi Light Bulbs (4 pack)", "price": 30.00, "inventory": 100, "expiry_year": 2099,
            "max_discount": 4.00, "image_filename": "smart_bulbs.jpg",
            "description": "Color changing WiFi smart bulbs, compatible with Alexa/Google.", "category": "Home & Kitchen"
        },
        {
            "title": "The Silent Patient", "price": 13.50, "inventory": 90, "expiry_year": 2099,
            "max_discount": 1.50, "image_filename": "silent_patient.jpg",
            "description": "A gripping psychological thriller by Alex Michaelides.", "category": "Books"
        },
        {
            "title": "Dune by Frank Herbert", "price": 10.00, "inventory": 110, "expiry_year": 2099,
            "max_discount": 1.00, "image_filename": "dune_book.jpg",
            "description": "Classic science fiction epic, basis for the new movie.", "category": "Books"
        },
        {
            "title": "Men\'s Winter Jacket Parka", "price": 110.00, "inventory": 40, "expiry_year": 2099,
            "max_discount": 15.00, "image_filename": "mens_parka.jpg",
            "description": "Warm and waterproof parka jacket for cold weather.", "category": "Clothing & Fashion"
        },
        {
            "title": "Women\'s Summer Dress Floral", "price": 45.00, "inventory": 70, "expiry_year": 2099,
            "max_discount": 6.00, "image_filename": "womens_dress.jpg",
            "description": "Light and airy floral summer dress.", "category": "Clothing & Fashion"
        },
        {
            "title": "Leather Belt Reversible", "price": 28.00, "inventory": 100, "expiry_year": 2099,
            "max_discount": 3.00, "image_filename": "leather_belt.jpg",
            "description": "Genuine leather belt, reversible black/brown.", "category": "Accessories"
        },
        {
            "title": "Resistance Bands Set (5 pcs)", "price": 18.00, "inventory": 120, "expiry_year": 2099,
            "max_discount": 2.00, "image_filename": "resistance_bands.jpg",
            "description": "Versatile resistance bands for full-body workouts.", "category": "Sports & Outdoors"
        },
        {
            "title": "Insulated Water Bottle 32oz", "price": 22.00, "inventory": 150, "expiry_year": 2099,
            "max_discount": 2.50, "image_filename": "water_bottle.jpg",
            "description": "Keeps drinks cold for 24 hours or hot for 12 hours.", "category": "Sports & Outdoors"
        },
        {
            "title": "Hiking Backpack 50L", "price": 65.00, "inventory": 50, "expiry_year": 2099,
            "max_discount": 7.00, "image_filename": "hiking_backpack.jpg",
            "description": "Durable and spacious backpack for hiking and travel.", "category": "Sports & Outdoors"
        },
        {
            "title": "Organic Almond Milk (6 pack)", "price": 18.00, "inventory": 80, "expiry_year": 2025,
            "max_discount": 2.00, "image_filename": "almond_milk.jpg",
            "description": "Unsweetened organic almond milk, dairy-free alternative.", "category": "Groceries"
        },
        {
            "title": "Dark Chocolate Bar 85% Cocoa", "price": 3.50, "inventory": 200, "expiry_year": 2025,
            "max_discount": 0.50, "image_filename": "dark_chocolate.jpg",
            "description": "Rich and intense dark chocolate for connoisseurs.", "category": "Groceries"
        },
        {
            "title": "Assorted Herbal Tea Collection", "price": 10.00, "inventory": 90, "expiry_year": 2026,
            "max_discount": 1.00, "image_filename": "herbal_tea_set.jpg",
            "description": "A collection of soothing herbal teas, 40 bags.", "category": "Groceries"
        },
        {
            "title": "Plush Teddy Bear Large", "price": 25.00, "inventory": 60, "expiry_year": 2099,
            "max_discount": 3.00, "image_filename": "teddy_bear.jpg",
            "description": "Soft and cuddly large teddy bear, perfect gift.", "category": "Toys & Games"
        },
        {
            "title": "Remote Control Car Off-Road", "price": 45.00, "inventory": 40, "expiry_year": 2099,
            "max_discount": 5.00, "image_filename": "rc_car.jpg",
            "description": "High-speed off-road remote control car for all ages.", "category": "Toys & Games"
        },
        {
            "title": "Natural Shampoo & Conditioner Set", "price": 20.00, "inventory": 70, "expiry_year": 2025,
            "max_discount": 2.50, "image_filename": "shampoo_set.jpg",
            "description": "Sulfate-free shampoo and conditioner with natural oils.", "category": "Beauty & Personal Care"
        },
        {
            "title": "Beard Grooming Kit", "price": 30.00, "inventory": 50, "expiry_year": 2099,
            "max_discount": 4.00, "image_filename": "beard_kit.jpg",
            "description": "Complete beard grooming kit with oil, balm, comb, and brush.", "category": "Beauty & Personal Care"
        },
        {
            "title": "Sunscreen SPF 50+ (Family Size)", "price": 15.00, "inventory": 100, "expiry_year": 2026,
            "max_discount": 1.50, "image_filename": "sunscreen_spf50.jpg",
            "description": "Broad-spectrum SPF 50+ sunscreen, water-resistant.", "category": "Beauty & Personal Care"
        },
        {
            "title": "Ergonomic Office Chair", "price": 180.00, "inventory": 20, "expiry_year": 2099,
            "max_discount": 20.00, "image_filename": "office_chair.jpg",
            "description": "Comfortable ergonomic office chair with lumbar support.", "category": "Office Supplies"
        },
        {
            "title": "Wireless Mouse Ergonomic", "price": 22.00, "inventory": 80, "expiry_year": 2099,
            "max_discount": 2.00, "image_filename": "ergonomic_mouse.jpg",
            "description": "Vertical ergonomic wireless mouse for comfort.", "category": "Office Supplies"
        }
    ]

    products_added_count = 0
    for prod_data in products_data:
        existing_product = Product.query.filter_by(title=prod_data["title"], seller_id=admin_user.id).first()
        if existing_product:
            print(f"Product '{prod_data['title']}' by seller '{admin_user.username}' already exists. Skipping.")
            continue

        product = Product(
            title=prod_data["title"], price=prod_data["price"], inventory=prod_data["inventory"],
            expiry_year=prod_data["expiry_year"], max_discount=prod_data["max_discount"],
            image_filename=prod_data.get("image_filename"), description=prod_data["description"],
            category=prod_data["category"], created_at=datetime.utcnow(), seller_id=admin_user.id
        )
        db.session.add(product)
        print(f"Attempting to add product: {product.title}")
        products_added_count += 1

    if products_added_count > 0:
        try:
            db.session.commit()
            print(f"Successfully committed {products_added_count} new products.")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing products: {e}")
    else:
        print("No new products to add (all might exist already or data was empty).")

def run_seed():
    """Imports app components, creates app context, and runs the seeder."""
    app_instance = None
    try:
        from app import create_app  # Assuming create_app is in app/__init__.py
        app_instance = create_app()
        print("Successfully created Flask app instance.")
    except ImportError as e_create_app:
        print(f"Failed to import create_app from app: {e_create_app}")
        print("Ensure app/__init__.py has a function named 'create_app'.")
        return
    except Exception as e_generic_create_app:
        print(f"An error occurred while calling create_app(): {e_generic_create_app}")
        return

    if not app_instance:
        print("Flask app instance was not created. Aborting seed.")
        return

    with app_instance.app_context():
        print("Entered Flask app context.")
        db_instance = None
        UserModel = None
        ProductModel = None
        try:
            from app import db as imported_db # Assuming db is initialized in app/__init__.py or accessible via app package
            db_instance = imported_db
            from app.models import User as ImportedUser, Product as ImportedProduct # Assuming models are in app/models.py
            UserModel = ImportedUser
            ProductModel = ImportedProduct
            print("Successfully imported db, User, and Product models within app context.")
        except ImportError as e_import_models:
            print(f"Failed to import db, User, or Product from the app package: {e_import_models}")
            print("Please ensure:")
            print("1. 'db = SQLAlchemy()' is defined globally in 'app/__init__.py'.")
            print("2. 'User' and 'Product' models are defined in 'app/models.py'.")
            print("3. 'app/models.py' correctly imports 'db' (e.g., 'from app import db').")
            return
        except Exception as e_generic_import:
            print(f"An error occurred importing db/models within app_context: {e_generic_import}")
            return
            
        if not all([db_instance, UserModel, ProductModel]):
            print("One or more components (db, User, Product) failed to import. Aborting seed.")
            return

        create_admin_and_products(app_instance, db_instance, UserModel, ProductModel)

if __name__ == '__main__':
    print("--- Starting Database Seed Process ---")
    run_seed()
    print("--- Database Seed Process Finished ---")
    print("\nTroubleshooting notes if seeding failed:")
    print("- Check the error messages above for specific import failures.")
    print("- Ensure your Flask app structure matches assumptions:")
    print("  - 'app/__init__.py' contains 'db = SQLAlchemy()' globally and a 'create_app()' function.")
    print("  - 'app/models.py' contains your User and Product models and imports 'db' from 'app'.")
    print("- If 'python seed.py' consistently fails, try the flask shell method with careful manual imports:")
    print("  1. Activate virtual environment.")
    print("  2. `flask shell`")
    print("  3. >>> from app import create_app, db")
    print("  4. >>> from app.models import User, Product")
    print("  5. >>> current_app = create_app()")
    print("  6. >>> with current_app.app_context():")
    print("  7. ...    from seed import create_admin_and_products")
    print("  8. ...    create_admin_and_products(current_app, db, User, Product)") 