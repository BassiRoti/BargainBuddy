from flask import render_template, request, redirect, url_for, jsonify, flash, session
from werkzeug.utils import secure_filename
import os
from app import db
import math
from app.models import Product, User, Cart, CartItem, Order, OrderItem
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime, timedelta
from sqlalchemy import func

def init_routes(app):
    
    @app.context_processor
    def inject_categories():
        """Make categories available to all templates."""
        # Get distinct categories from the database
        categories = db.session.query(Product.category).distinct().all()
        categories = [cat[0] for cat in categories]
        
        # Get category counts
        category_counts = {}
        for cat in categories:
            category_counts[cat] = Product.query.filter_by(category=cat).count()
            
        return dict(categories=categories, category_counts=category_counts)

    def allowed_file(filename):
        """Check if the file has an allowed extension."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route("/")
    def home():
        """Home Page: Displays product listings."""
        if current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
            
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', None)
        search = request.args.get('search', None)
        sort = request.args.get('sort', 'relevance')
        per_page = 12
        
        # Base query
        query = Product.query
        
        # Apply search filter if specified
        if search:
            search_terms = search.split()
            conditions = []
            for term in search_terms:
                search_term = f"%{term}%"
                conditions.append(
                    db.or_(
                        Product.title.ilike(search_term),
                        Product.description.ilike(search_term),
                        Product.category.ilike(search_term)
                    )
                )
            query = query.filter(db.and_(*conditions))
        
        # Apply category filter if specified
        if category:
            query = query.filter_by(category=category)
            
        # Apply sorting
        if sort == 'price_low':
            query = query.order_by(Product.price.asc())
        elif sort == 'price_high':
            query = query.order_by(Product.price.desc())
        elif sort == 'newest':
            query = query.order_by(Product.created_at.desc())
        else:  # relevance - default for search results
            if search:
                # For MySQL, we'll sort by title matching the search term first, then by date
                query = query.order_by(
                    # Items with exact title match come first
                    Product.title.like(search).desc(),
                    # Then items where title starts with search term
                    Product.title.like(f"{search}%").desc(),
                    # Then by creation date
                    Product.created_at.desc()
                )
            else:
                query = query.order_by(Product.created_at.desc())
            
        # Get paginated products
        products = query.paginate(page=page, per_page=per_page)
        
        return render_template("index.html", 
                             products=products, 
                             current_category=category,
                             search_query=search,
                             current_sort=sort)

    @app.route("/category/<category>")
    def category_products(category):
        """Display products for a specific category with pagination."""
        page = request.args.get('page', 1, type=int)
        sort_by = request.args.get('sort', 'newest')  # Default sort by newest
        per_page = 12
        
        # Base query
        query = Product.query.filter_by(category=category)
        
        # Apply sorting
        if sort_by == 'price_low':
            query = query.order_by(Product.price.asc())
        elif sort_by == 'price_high':
            query = query.order_by(Product.price.desc())
        elif sort_by == 'newest':
            query = query.order_by(Product.created_at.desc())
        else:  # Default to title
            query = query.order_by(Product.title.asc())
        
        # Get paginated products
        products = query.paginate(page=page, per_page=per_page)
        
        return render_template("category_products.html", 
                             products=products,
                             category=category,
                             sort_by=sort_by)

    @app.route("/make-admin/<int:user_id>")
    def make_admin(user_id):
        """Make a user an admin."""
        user = User.query.get_or_404(user_id)
        user.is_admin = True
        db.session.commit()
        flash(f"User {user.username} is now an admin!", "success")
        return redirect(url_for("home"))

    @app.route("/add-product", methods=["GET", "POST"])
    @login_required
    def add_product():
        """Add Product Page: Allows user to add new products with images."""
        if not current_user.is_admin:
            flash("Only admins can add products.", "error")
            return redirect(url_for("home"))
            
        if request.method == "POST":
            title = request.form["title"]
            description = request.form["description"]
            price = float(request.form["price"])
            inventory = int(request.form["inventory"])
            expiry_year = int(request.form["expiry_year"])
            
            # Handle category selection
            selected_category = request.form.get("category")
            new_category_input = request.form.get("new_category", "").strip()

            final_category = ""
            if new_category_input:
                final_category = new_category_input
            elif selected_category:
                final_category = selected_category
            
            if not final_category:
                flash("Please select an existing category or enter a new one.", "error")
                return redirect(request.url) # Or render_template with current form data

            max_discount = price * 0.15 # Default max_discount, can be adjusted

            file = request.files.get("image")
            image_filename = None
            if file and allowed_file(file.filename):
                image_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            elif file and file.filename: # File was provided but not allowed type
                flash("Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.", "error")
                return redirect(request.url)
            # If no file is provided, image_filename remains None, which is acceptable for Product model

            if (price > 0 and inventory > 0 and expiry_year >= datetime.now().year):
                new_product = Product(
                    title=title,
                    description=description,
                    price=price,
                    inventory=inventory,
                    expiry_year=expiry_year,
                    max_discount=max_discount,
                    image_filename=image_filename,
                    category=final_category, # Use the determined category
                    seller_id=current_user.id
                )
                db.session.add(new_product)
                db.session.commit()
                flash('Product Successfully Added!', 'success')
            else:
                flash_messages = []
                if not price > 0: flash_messages.append("Price must be greater than 0.")
                if not inventory > 0: flash_messages.append("Inventory must be greater than 0.")
                if not expiry_year >= datetime.now().year: flash_messages.append(f"Expiry year must be {datetime.now().year} or later.")
                flash("Error adding product: " + " ".join(flash_messages), 'danger')
                # It would be better to re-render the form with errors and existing data here
                # For now, redirecting, but data will be lost.
                return redirect(request.url)

            return redirect(url_for("admin_products")) # Redirect to admin products list
        return render_template("add_product.html")

    @app.route("/chat-bot/<int:product_id>", methods=["GET", "POST"])
    @login_required
    def chat_bot(product_id):
        """Bargaining Chat Bot Page."""
        if current_user.is_admin:
            flash('Admins cannot use the bargaining feature.', 'error')
            return redirect(url_for('admin_products'))
            
        product = Product.query.get_or_404(product_id)
        if request.method == "POST":
            offered_price = float(request.form["offered_price"])
            max_discount = float(request.form["max_discount"])
            
            # Calculate discount
            discount = product.price - offered_price
            
            if discount <= 0:
                return jsonify({"response": "I'm sorry, but that's not a valid offer. Please make an offer below the current price."})
            elif discount > max_discount:
                return jsonify({"response": f"I'm sorry, but I can't accept that offer. The maximum discount I can offer is ${max_discount:.2f}."})
            
            # Calculate acceptance probability based on discount
            acceptance_probability = 1 - (discount / max_discount)
            is_accepted = np.random.random() < acceptance_probability
            
            if is_accepted:
                return jsonify({
                    "response": f"Great! I accept your offer of ${offered_price:.2f}. Would you like to proceed with the purchase?",
                    "accepted": True,
                    "final_price": offered_price
                })
            else:
                counter_offer = product.price - (max_discount * 0.7)
                return jsonify({
                    "response": f"I can't accept that offer, but I can offer you ${counter_offer:.2f}. Would you like to accept this counter-offer?",
                    "accepted": False,
                    "counter_offer": counter_offer
                })
        
        return render_template("chat_bot.html", product=product)

    @app.route('/product/<int:product_id>')
    def product_page(product_id):
        """Product Page: Display details and optimized pricing for a specific product."""
        if current_user.is_authenticated and current_user.is_admin:
            flash('Admins should use the admin product view instead.', 'warning')
            return redirect(url_for('admin_products'))
            
        product = Product.query.get_or_404(product_id)
        
        # Refresh product data to ensure we have the latest inventory information
        db.session.refresh(product)
        
        # Get related products from the same category (excluding current product)
        related_products = Product.query.filter(
            Product.category == product.category,
            Product.id != product.id
        ).limit(4).all()

        return render_template('product.html', 
                             product=product,
                             related_products=related_products)
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form["name"]
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            
            # Check if user exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already registered!", "danger")
                return redirect(url_for("register"))
            
            # Create and store new user
            new_user = User(username=username, email=email, name=name)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                if user.is_admin:
                    # It's an admin/seller trying to use the general login
                    flash("Admin/Seller accounts should use the designated Seller Login page.", "warning")
                    return redirect(url_for("seller_login")) # Redirect to seller/admin login
                else:
                    # It's a regular user
                    login_user(user)
                    flash("Login successful!", "success")
                    return redirect(url_for("home"))
            else:
                flash("Invalid credentials!", "danger")

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))

    @app.route('/cart')
    @login_required
    def cart():
        if current_user.is_admin:
            flash('Admins cannot access the shopping cart.', 'error')
            return redirect(url_for('admin_dashboard'))
            
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        
        # Refresh product data to ensure we have the latest inventory information
        # Also identify any out-of-stock items
        out_of_stock_items = []
        for item in cart.items:
            db.session.refresh(item.product)
            if item.product.inventory < item.quantity:
                out_of_stock_items.append(item)
        
        # Calculate total with negotiated prices
        total = 0.0  # Initialize as float
        for item in cart.items:
            # Skip out-of-stock items in total calculation
            if item in out_of_stock_items:
                continue
                
            # Get negotiated price from query parameters if available
            negotiated_price = request.args.get(f'price_{item.product_id}', type=float)
            # Convert price to float
            price = float(negotiated_price if negotiated_price is not None else item.product.price)
            total += price * item.quantity
            
        return render_template('cart.html', cart=cart, total=total, float=float, out_of_stock_items=out_of_stock_items)

    @app.route('/api/cart/add', methods=['POST'])
    @login_required
    def add_to_cart():
        if current_user.is_admin:
            return jsonify({'error': 'Admins cannot use shopping cart features'}), 403
            
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return jsonify({'error': 'Invalid quantity'}), 400
        
        product = Product.query.get_or_404(product_id)
        if product.inventory < quantity:
            return jsonify({'error': 'Not enough inventory'}), 400
        
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            new_quantity = cart_item.quantity + quantity
            if product.inventory < new_quantity:
                return jsonify({'error': 'Not enough inventory'}), 400
            cart_item.quantity = new_quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        
        # Update inventory
        product.inventory -= quantity
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Product added to cart'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error adding to cart'}), 500

    @app.route('/api/cart/update', methods=['POST'])
    @login_required
    def update_cart():
        if current_user.is_admin:
            return jsonify({'error': 'Admins cannot use shopping cart features'}), 403
            
        data = request.get_json()
        item_id = data.get('item_id')
        quantity_change = int(data.get('quantity_change', 0))
        
        cart_item = CartItem.query.get_or_404(item_id)
        if cart_item.cart.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Calculate new quantity
        new_quantity = cart_item.quantity + quantity_change
        
        # Handle quantity changes
        if new_quantity < 1:
            # Remove item if quantity becomes 0 or negative
            db.session.delete(cart_item)
        else:
            # Check if we have enough inventory
            if cart_item.product.inventory < new_quantity:
                return jsonify({'error': f'Only {cart_item.product.inventory} items available in stock'}), 400
            
            # Update quantity
            cart_item.quantity = new_quantity
            
            # Update inventory
            cart_item.product.inventory -= quantity_change
        
        try:
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error updating cart'}), 500

    @app.route('/api/cart/remove', methods=['POST'])
    @login_required
    def remove_from_cart():
        if current_user.is_admin:
            return jsonify({'error': 'Admins cannot use shopping cart features'}), 403
            
        data = request.get_json()
        item_id = data.get('item_id')
        
        cart_item = CartItem.query.get_or_404(item_id)
        if cart_item.cart.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Restore inventory
        product = Product.query.get(cart_item.product_id)
        if product:
            product.inventory += cart_item.quantity
        
        db.session.delete(cart_item)
        try:
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error removing item: {str(e)}'}), 500

    @app.route('/api/chatbot', methods=['POST'])
    @login_required
    def chatbot():
        if current_user.is_admin:
            return jsonify({'error': 'Admins cannot use the bargaining feature'}), 403
            
        data = request.get_json()
        message = data.get('message')
        product_id = data.get('product_id')
        
        product = Product.query.get_or_404(product_id)
        # Simple response for now
        response = f"I can help you negotiate the price of {product.title}. The current price is ${product.price}. What's your offer?"
        
        return jsonify({'message': response})

    @app.route('/orders')
    @login_required
    def orders():
        if current_user.is_admin:
            flash('Admins should use the admin orders view instead.', 'warning')
            return redirect(url_for('admin_orders'))
            
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return render_template('orders.html', orders=orders)

    @app.route('/api/orders/create', methods=['POST'])
    @login_required
    def create_order():
        try:
            data = request.get_json() or {}
            shipping_address = data.get('shipping_address')
            
            if not shipping_address:
                return jsonify({'error': 'Shipping address is required'}), 400
                
            cart = Cart.query.filter_by(user_id=current_user.id).first()
            if not cart or not cart.items:
                return jsonify({'error': 'Cart is empty'}), 400
            
            # Refresh product data to ensure we have the latest inventory information
            out_of_stock_items = []
            for item in cart.items:
                db.session.refresh(item.product)
                if item.product.inventory < item.quantity:
                    out_of_stock_items.append(item)
            
            # If any items are out of stock, return an error
            if out_of_stock_items:
                # Create a nice error message listing all out of stock items
                error_message = "Some items in your cart are out of stock or quantities have changed:\n"
                for item in out_of_stock_items:
                    error_message += f"- {item.product.title}: Requested {item.quantity}, only {item.product.inventory} available\n"
                return jsonify({'error': error_message}), 400
            
            # Calculate total amount
            total_amount = sum(float(item.product.price) * item.quantity for item in cart.items)
            
            # Create order
            order = Order(
                user_id=current_user.id, 
                status='pending', 
                total_amount=total_amount,
                shipping_address=shipping_address
            )
            db.session.add(order)
            db.session.flush()  # Get the order ID without committing
            
            # Create order items and update inventory
            for item in cart.items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=float(item.product.price)
                )
                db.session.add(order_item)
                
                # Update inventory
                item.product.inventory -= item.quantity
            
            # Clear the cart
            CartItem.query.filter_by(cart_id=cart.id).delete()
            
            try:
                db.session.commit()
                return jsonify({'success': True, 'order_id': order.id})
            except Exception as e:
                db.session.rollback()
                error_detail = str(e)
                print(f"Error committing order: {error_detail}")
                return jsonify({'error': f'Database error: {error_detail}'}), 500
        except Exception as e:
            error_detail = str(e)
            print(f"Error creating order: {error_detail}")
            return jsonify({'error': f'Error creating order: {error_detail}'}), 500

    # Admin Routes
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('home'))
        
        # Get statistics for the current admin/seller
        total_products = Product.query.filter_by(seller_id=current_user.id).count()
        
        # Orders related to the current admin/seller
        seller_orders_query = Order.query.join(Order.items).join(OrderItem.product).filter(Product.seller_id == current_user.id)
        
        total_orders = seller_orders_query.distinct(Order.id).count()
        total_revenue = db.session.query(func.sum(Order.total_amount)).select_from(Order).join(Order.items).join(OrderItem.product).filter(Product.seller_id == current_user.id).scalar() or 0
        recent_orders = seller_orders_query.distinct().order_by(Order.created_at.desc()).limit(5).all()

        total_users = User.query.count() # Total users remains a site-wide stat, not seller-specific

        low_stock_products = Product.query.filter(Product.seller_id == current_user.id, Product.inventory < 10).all()
        
        # Get category statistics for the current admin/seller
        categories_query = db.session.query(Product.category).filter(Product.seller_id == current_user.id).distinct().all()
        categories = [cat[0] for cat in categories_query if cat[0]] 
        
        category_counts = {}
        for category in categories:
            category_counts[category] = Product.query.filter_by(category=category, seller_id=current_user.id).count()
        
        return render_template('admin/dashboard.html',
                             total_products=total_products,
                             total_orders=total_orders,
                             total_users=total_users, # This is site-wide
                             total_revenue=total_revenue,
                             recent_orders=recent_orders,
                             low_stock_products=low_stock_products,
                             categories=categories,
                             category_counts=category_counts)

    @app.route('/admin/category/<category>')
    @login_required
    def admin_category_products(category):
        """Admin view for managing products in a specific category."""
        if not current_user.is_admin:
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("home"))
            
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        # Get products for the category and current admin
        products = Product.query.filter_by(category=category, seller_id=current_user.id).paginate(page=page, per_page=per_page)
        
        # Get category statistics
        total_inventory = db.session.query(func.sum(Product.inventory)).\
            filter(Product.category == category, Product.seller_id == current_user.id).scalar() or 0
        avg_price = db.session.query(func.avg(Product.price)).\
            filter(Product.category == category, Product.seller_id == current_user.id).scalar() or 0
        product_count = Product.query.filter_by(category=category, seller_id=current_user.id).count()
        
        stats = {
            'total_inventory': total_inventory,
            'avg_price': round(float(avg_price), 2) if avg_price else 0,
            'product_count': product_count
        }
        
        return render_template("admin/category_products.html",
                             category=category,
                             products=products,
                             stats=stats)

    @app.route('/admin/products')
    @login_required
    def admin_products():
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        
        print(f"Accessed /admin/products by user: {current_user.username}, ID: {current_user.id}, is_admin: {current_user.is_admin}") # DEBUG LINE

        products = Product.query.filter_by(seller_id=current_user.id).all()
        print(f"Found {len(products)} products for seller ID {current_user.id}") # DEBUG LINE
        return render_template('admin/products.html', products=products)

    @app.route('/admin/orders')
    @login_required
    def admin_orders():
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index')) # Assuming 'index' is your home page or a general redirect
        
        # Fetch orders that contain products sold by the current admin/seller
        orders = Order.query.join(Order.items).join(OrderItem.product).filter(Product.seller_id == current_user.id).distinct().order_by(Order.created_at.desc()).all()
        return render_template('admin/orders.html', orders=orders)

    @app.route('/api/admin/products/<int:product_id>')
    @login_required
    def get_product(product_id):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        product = Product.query.filter_by(id=product_id, seller_id=current_user.id).first_or_404()
        # If first_or_404() doesn't find it because seller_id doesn't match, it raises 404, which is appropriate.
        
        return jsonify({
            'id': product.id,
            'title': product.title,
            'price': float(product.price),
            'inventory': product.inventory,
            'expiry_year': product.expiry_year,
            'category': product.category,
            'description': product.description,
            'max_discount': float(product.max_discount) if product.max_discount is not None else 0.0,
            'image_filename': product.image_filename
        })

    @app.route('/api/admin/products/update/<int:product_id>', methods=['POST'])
    @login_required
    def update_product(product_id):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403

        product = Product.query.filter_by(id=product_id, seller_id=current_user.id).first()
        if not product:
            return jsonify({'error': 'Product not found or you do not have permission to edit it.'}), 404
        
        # Access form data
        product.title = request.form.get('title', product.title)
        product.price = request.form.get('price', product.price, type=float)
        product.inventory = request.form.get('inventory', product.inventory, type=int)
        product.expiry_year = request.form.get('expiry_year', product.expiry_year, type=int)
        product.category = request.form.get('category', product.category)
        product.description = request.form.get('description', product.description)
        
        # Handle max_discount - it was calculated from percentage in some templates
        # Assuming 'max_discount' is sent directly or calculated before this point if needed.
        if 'max_discount' in request.form:
             product.max_discount = float(request.form.get('max_discount'))
        elif 'max_discount_percentage' in request.form and request.form.get('price'):
            price = float(request.form.get('price'))
            percentage = float(request.form.get('max_discount_percentage'))
            if price > 0 and percentage > 0:
                product.max_discount = (price * percentage / 100)
            else:
                product.max_discount = 0.00

        # Handle file upload
        file = request.files.get("image")
        if file and file.filename: # Check if a file was actually selected
            if allowed_file(file.filename):
                # Delete old image if it exists and is different from new one
                if product.image_filename and product.image_filename != secure_filename(file.filename):
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
                    if os.path.exists(old_image_path):
                        try:
                            os.remove(old_image_path)
                        except OSError as e:
                            app.logger.error(f"Error deleting old image {old_image_path}: {e}")

                image_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                product.image_filename = image_filename
            else:
                # It might be better to return a JSON error than flash here, as it's an API endpoint
                return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.'}), 400
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Product updated successfully'})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating product {product_id}: {e}")
            return jsonify({'error': 'Failed to update product.'}), 500

    @app.route('/api/admin/products/delete/<int:product_id>', methods=['POST'])
    @login_required
    def delete_product(product_id):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        product = Product.query.filter_by(id=product_id, seller_id=current_user.id).first()
        if not product:
            return jsonify({'error': 'Product not found or you do not have permission to delete it.'}), 404
            
        # Delete image file if it exists
        if product.image_filename:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except OSError as e:
                    app.logger.error(f"Error deleting image file {image_path}: {e}")
                    # Potentially return an error or just log and continue with DB deletion

        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product deleted successfully'})

    @app.route('/api/admin/orders/<int:order_id>')
    @login_required
    def get_order(order_id):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Check if the order contains any product from the current seller admin
        order = Order.query.join(Order.items).join(OrderItem.product).filter(
            Order.id == order_id,
            Product.seller_id == current_user.id
        ).first_or_404() # first_or_404 will raise 404 if no such order for this seller

        return jsonify({
            'id': order.id,
            'user': {
                'name': order.user.name,
                'email': order.user.email
            },
            'created_at': order.created_at.isoformat(),
            'total': float(order.total_amount), # This is total for the whole order
            'status': order.status,
            'items': [{ # Show all items, front-end can highlight/filter if needed, or filter here
                'product': {
                    'id': item.product.id, # Added product ID
                    'title': item.product.title,
                    'is_seller_product': item.product.seller_id == current_user.id # Flag if item is by current seller
                },
                'quantity': item.quantity,
                'price': float(item.price)
            } for item in order.items]
        })

    @app.route('/api/admin/orders/update/<int:order_id>', methods=['POST'])
    @login_required
    def update_order(order_id):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Ensure the admin has at least one product in this order before allowing status update
        order_check = Order.query.join(Order.items).join(OrderItem.product).filter(
            Order.id == order_id,
            Product.seller_id == current_user.id
        ).first()

        if not order_check:
            return jsonify({'error': 'Order not found or you do not have permission to update it.'}), 404
            
        order = Order.query.get_or_404(order_id) # Get the order again to update it
        data = request.get_json()
        
        new_status = data.get('status', order.status)
        # Add any validation for allowed status transitions if necessary
        order.status = new_status
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Order status updated successfully'})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating order {order_id} status: {e}")
            return jsonify({'error': 'Failed to update order status.'}), 500

    @app.route("/seller/register", methods=["GET", "POST"])
    def seller_register():
        """Seller Registration Page: Allows users to register as sellers."""
        if request.method == "POST":
            name = request.form["name"]
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            business_name = request.form["business_name"]
            business_address = request.form["business_address"]
            
            # Check if user exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already registered!", "error")
                return redirect(url_for("seller_register"))
            
            # Check if username exists
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                flash("Username already taken!", "error")
                return redirect(url_for("seller_register"))
            
            # Create and store new seller
            new_seller = User(
                username=username,
                email=email,
                name=name,
                business_name=business_name,
                business_address=business_address,
                is_admin=True  # Set as admin/seller
            )
            new_seller.set_password(password)
            db.session.add(new_seller)
            db.session.commit()
            
            flash("Seller registration successful! Please login.", "success")
            return redirect(url_for("login"))

        return render_template("seller/register.html", hide_nav=True)

    @app.route("/seller/login", methods=["GET", "POST"])
    def seller_login():
        """Seller Login Page: Allows sellers to login."""
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = User.query.filter_by(email=email).first()

            if user and user.is_admin and user.check_password(password):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Invalid credentials or not a seller account!", "error")

        return render_template("seller/login.html", hide_nav=True)

    @app.route('/all-categories')
    def all_categories():
        """Display all product categories with detailed statistics."""
        # Get all unique categories
        categories = db.session.query(Product.category).distinct().all()
        categories = [cat[0] for cat in categories]
        
        # Get category counts
        category_counts = {}
        category_stats = {}
        
        for category in categories:
            products = Product.query.filter_by(category=category)
            count = products.count()
            category_counts[category] = count
            
            if count > 0:
                min_price = db.session.query(db.func.min(Product.price)).filter(Product.category == category).scalar()
                max_price = db.session.query(db.func.max(Product.price)).filter(Product.category == category).scalar()
                total_inventory = db.session.query(db.func.sum(Product.inventory)).filter(Product.category == category).scalar()
                
                category_stats[category] = {
                    'min_price': float(min_price) if min_price else 0,
                    'max_price': float(max_price) if max_price else 0,
                    'total_inventory': total_inventory or 0
                }
            else:
                category_stats[category] = {
                    'min_price': 0,
                    'max_price': 0,
                    'total_inventory': 0
                }
        
        return render_template('all_categories.html', 
                             categories=categories,
                             category_counts=category_counts,
                             category_stats=category_stats)

    @app.route('/api/search/suggestions')
    def search_suggestions():
        """API endpoint for search suggestions."""
        query = request.args.get('q', '').strip()
        if not query or len(query) < 2:
            return jsonify([])
            
        # Search in product titles and categories
        search_term = f"%{query}%"
        
        # Get matching products
        products = Product.query.filter(
            db.or_(
                Product.title.ilike(search_term),
                Product.description.ilike(search_term)
            )
        ).limit(5).all()
        
        # Get matching categories
        categories = db.session.query(Product.category).filter(
            Product.category.ilike(search_term)
        ).distinct().limit(3).all()
        
        suggestions = []
        
        # Add product suggestions
        for product in products:
            suggestions.append({
                'type': 'product',
                'title': product.title,
                'category': product.category
            })
            
        # Add category suggestions
        for category in categories:
            if len(suggestions) >= 8:  # Limit total suggestions
                break
            suggestions.append({
                'type': 'category',
                'title': f'All in {category[0]}',
                'category': category[0]
            })
            
        return jsonify(suggestions)