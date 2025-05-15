-- Sample Products for BargainBuddy
-- Run this script in DBeaver to populate your database with sample products

-- Select the database first
USE bargainbuddy;

-- Electronics
INSERT INTO products (title, price, inventory, expiry_year, max_discount, description, image_filename, created_at) VALUES
('Samsung 4K Smart TV 55"', 699.99, 15, 2026, 150.00, 'Experience stunning clarity and vivid colors with this Samsung 55-inch 4K Smart TV. Features built-in streaming apps and voice control.', 'samsung_tv.jpg', NOW()),
('Apple iPhone 13 Pro', 999.99, 25, 2025, 200.00, 'The latest iPhone with A15 Bionic chip, Pro camera system, and Super Retina XDR display with ProMotion.', 'iphone13.jpg', NOW()),
('Sony WH-1000XM4 Headphones', 349.99, 30, 2025, 75.00, 'Industry-leading noise cancellation with premium sound quality. Up to 30 hours of battery life.', 'sony_headphones.jpg', NOW()),
('Dell XPS 13 Laptop', 1299.99, 10, 2026, 250.00, '13-inch InfinityEdge display, 11th Gen Intel Core i7, 16GB RAM, 512GB SSD.', 'dell_xps.jpg', NOW()),
('Nintendo Switch OLED', 349.99, 20, 2025, 50.00, 'Featuring a vibrant 7-inch OLED screen, enhanced audio, and 64GB of internal storage.', 'nintendo_switch.jpg', NOW());

-- Home & Kitchen
INSERT INTO products (title, price, inventory, expiry_year, max_discount, description, image_filename, created_at) VALUES
('Instant Pot Duo 7-in-1', 99.99, 40, 2026, 30.00, 'Pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yogurt maker, and warmer in one appliance.', 'instant_pot.jpg', NOW()),
('Dyson V11 Cordless Vacuum', 599.99, 12, 2025, 100.00, 'Intelligent cordless vacuum with powerful suction and up to 60 minutes of run time.', 'dyson_vacuum.jpg', NOW()),
('KitchenAid Stand Mixer', 379.99, 15, 2027, 80.00, 'Professional 5-quart mixer with 10-speed settings and various attachments for versatile cooking.', 'kitchenaid_mixer.jpg', NOW()),
('Nespresso Vertuo Coffee Maker', 199.99, 25, 2025, 50.00, 'Makes both coffee and espresso with the touch of a button. Includes Aeroccino milk frother.', 'nespresso.jpg', NOW()),
('Cuisinart Air Fryer Toaster Oven', 199.99, 18, 2026, 60.00, '7-in-1 appliance: air fryer, convection oven, toaster, broiler, and more.', 'cuisinart_airfryer.jpg', NOW());

-- Clothing
INSERT INTO products (title, price, inventory, expiry_year, max_discount, description, image_filename, created_at) VALUES
('Nike Air Max 270 Sneakers', 150.00, 35, 2024, 45.00, 'Lifestyle sneakers with the first-ever Max Air unit designed specifically for Nike Sportswear.', 'nike_airmax.jpg', NOW()),
('Levi\'s 501 Original Jeans', 69.99, 50, 2024, 25.00, 'The iconic straight fit jeans that started it all. Original fit, straight leg, button fly.', 'levis_jeans.jpg', NOW()),
('North Face Thermoball Jacket', 199.99, 20, 2024, 60.00, 'Lightweight, packable insulation that keeps you warm even when wet.', 'northface_jacket.jpg', NOW()),
('Ray-Ban Aviator Sunglasses', 154.00, 25, 2026, 40.00, 'Iconic pilot-shaped sunglasses with 100% UV protection.', 'rayban_aviator.jpg', NOW()),
('Adidas Ultraboost Running Shoes', 180.00, 30, 2024, 50.00, 'Responsive running shoes with energy-returning Boost cushioning.', 'adidas_ultraboost.jpg', NOW());

-- Toys & Games
INSERT INTO products (title, price, inventory, expiry_year, max_discount, description, image_filename, created_at) VALUES
('LEGO Star Wars Millennium Falcon', 159.99, 15, 2025, 35.00, 'Iconic Millennium Falcon set with 1,353 pieces and 7 minifigures.', 'lego_falcon.jpg', NOW()),
('PlayStation 5 Console', 499.99, 8, 2026, 50.00, 'Next-gen gaming console with ultra-high speed SSD, 3D audio, and haptic feedback.', 'ps5.jpg', NOW()),
('Monopoly Board Game', 19.99, 40, 2025, 5.00, 'Classic property trading board game for the whole family.', 'monopoly.jpg', NOW()),
('Fisher-Price Learning Toy', 29.99, 35, 2024, 10.00, 'Educational toy that helps develop motor skills and interactive learning for toddlers.', 'fisher_price.jpg', NOW()),
('Barbie Dreamhouse', 179.99, 12, 2025, 45.00, 'Three-story dollhouse with 8 rooms, a working elevator, pool, and 70+ accessories.', 'barbie_dreamhouse.jpg', NOW());

-- Beauty & Personal Care
INSERT INTO products (title, price, inventory, expiry_year, max_discount, description, image_filename, created_at) VALUES
('Dyson Airwrap Complete Styler', 549.99, 10, 2026, 100.00, 'Complete styling system with multiple attachments for various hair types.', 'dyson_airwrap.jpg', NOW()),
('La Mer Moisturizing Cream', 190.00, 15, 2024, 40.00, 'Luxury face cream with sea kelp, minerals, and other nutrients for hydration.', 'lamer_cream.jpg', NOW()),
('Philips Sonicare DiamondClean', 199.99, 25, 2025, 60.00, 'Advanced sonic toothbrush with 5 cleaning modes and smart brush head recognition.', 'philips_sonicare.jpg', NOW()),
('Olaplex Hair Perfector No. 3', 28.00, 40, 2024, 8.00, 'At-home hair treatment that reduces breakage and visibly strengthens hair.', 'olaplex.jpg', NOW()),
('Theragun Elite Massage Gun', 399.00, 12, 2025, 80.00, 'Premium deep tissue massage device with 5 built-in speeds and smart app integration.', 'theragun.jpg', NOW()); 