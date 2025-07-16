from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from bson import ObjectId

app = Flask(__name__)
app.secret_key = "your_super_secret_key_change_this_in_production"

# MongoDB setup
# For local MongoDB: app.config["MONGO_URI"] = "mongodb://localhost:27017/foodApp"
# For MongoDB Atlas (cloud): Use the connection string below
app.config["MONGO_URI"] = "mongodb://localhost:27017/foodApp"
mongo = PyMongo(app)

# Initialize database with sample data
def init_database():
    """Initialize database with sample food items if they don't exist"""
    if mongo.db.food_items.count_documents({}) == 0:
        sample_food_items = [
            {
                "name": "Veg Biryani",
                "category": "veg",
                "price": 120,
                "description": "Aromatic basmati rice cooked with fresh vegetables and aromatic spices",
                "image": "/static/images/menu/veg/veg-biryani.jpg",
                "available": True,
                "rating": 4.5,
                "preparation_time": "25 minutes"
            },
            {
                "name": "Aloo Paratha",
                "category": "veg",
                "price": 150,
                "description": "Whole wheat flatbread stuffed with spiced potato mixture",
                "image": "/static/images/menu/veg/aloo-paratha.jpg",
                "available": True,
                "rating": 4.3,
                "preparation_time": "15 minutes"
            },
            {
                "name": "Dal Tadka",
                "category": "veg",
                "price": 120,
                "description": "Yellow lentils tempered with aromatic spices and herbs",
                "image": "/static/images/menu/veg/dal-tadka.jpg",
                "available": True,
                "rating": 4.2,
                "preparation_time": "20 minutes"
            },
            {
                "name": "Aloo Gobi",
                "category": "veg",
                "price": 180,
                "description": "Potato and cauliflower curry with Indian spices",
                "image": "/static/images/menu/veg/Aloo-Gobi.jpg",
                "available": True,
                "rating": 4.4,
                "preparation_time": "30 minutes"
            },
            {
                "name": "Chocolate Ice Cream",
                "category": "desserts",
                "price": 80,
                "description": "Rich and creamy chocolate ice cream",
                "image": "/static/images/menu/desserts and icream/desserts-icecream.jpg",
                "available": True,
                "rating": 4.6,
                "preparation_time": "5 minutes"
            },
            {
                "name": "Protein Shake",
                "category": "gym",
                "price": 200,
                "description": "High protein shake with whey protein and fruits",
                "image": "/static/images/menu/gym/gym-food.jpg",
                "available": True,
                "rating": 4.7,
                "preparation_time": "10 minutes"
            },
            {
                "name": "Pani Puri",
                "category": "street-chaat",
                "price": 50,
                "description": "Crispy puris filled with spiced potato and tangy water",
                "image": "/static/images/menu/street-chaat/pani-puri.jpg",
                "available": True,
                "rating": 4.8,
                "preparation_time": "10 minutes"
            },
            {
                "name": "Samosa",
                "category": "street-chaat",
                "price": 40,
                "description": "Crispy pastry filled with spicy potato mixture",
                "image": "/static/images/menu/street-chaat/samosa.jpg",
                "available": True,
                "rating": 4.7,
                "preparation_time": "8 minutes"
            },
            {
                "name": "Missal Pav",
                "category": "street-chaat",
                "price": 150,
                "description": "Spicy sprouted bean curry served with pav",
                "image": "/static/images/menu/street-chaat/missal-pav.jpg",
                "available": True,
                "rating": 4.6,
                "preparation_time": "12 minutes"
            },
            {
                "name": "Chole Bhature",
                "category": "street-chaat",
                "price": 60,
                "description": "Spicy chickpeas served with fried bread",
                "image": "/static/images/menu/street-chaat/chole-bhature.jpg",
                "available": True,
                "rating": 4.9,
                "preparation_time": "15 minutes"
            },
            {
                "name": "Gajar Halwa",
                "category": "desserts",
                "price": 250,
                "description": "Traditional Indian carrot pudding with nuts and ghee",
                "image": "/static/images/menu/desserts and icream/Deserts/gajar-halwa.jpg",
                "available": True,
                "rating": 4.7,
                "preparation_time": "30 minutes"
            },
            {
                "name": "Cow Milk Kheer",
                "category": "desserts",
                "price": 160,
                "description": "Classic rice pudding made with cow milk, rice, and cardamom",
                "image": "/static/images/menu/desserts and icream/Deserts/kheer.jpg",
                "available": True,
                "rating": 4.6,
                "preparation_time": "25 minutes"
            },
            {
                "name": "Dryfruit Barfi",
                "category": "desserts",
                "price": 190,
                "description": "Rich barfi made with assorted dry fruits and khoya",
                "image": "/static/images/menu/desserts and icream/Deserts/dryfruit-barfi.jpg",
                "available": True,
                "rating": 4.8,
                "preparation_time": "20 minutes"
            },
            {
                "name": "Gulab Jamun",
                "category": "desserts",
                "price": 90,
                "description": "Soft milk-solid balls soaked in rose-flavored sugar syrup",
                "image": "/static/images/menu/desserts and icream/Deserts/gulab-jamun.jpg",
                "available": True,
                "rating": 4.9,
                "preparation_time": "15 minutes"
            }
        ]
        mongo.db.food_items.insert_many(sample_food_items)

    # Only seed the 4 street chaat items in the 'street-chaat' category
    if mongo.db.food_items.count_documents({"category": "street-chaat"}) != 4:
        mongo.db.food_items.delete_many({"category": "street-chaat"})
        sample_chaat = [
            {
                "name": "Pani Puri",
                "category": "street-chaat",
                "price": 50,
                "description": "Crispy puris filled with spiced potato and tangy water",
                "image": "/static/images/menu/street-chaat/pani-puri.jpg",
                "available": True,
                "rating": 4.8,
                "preparation_time": "10 minutes"
            },
            {
                "name": "Samosa",
                "category": "street-chaat",
                "price": 40,
                "description": "Crispy pastry filled with spicy potato mixture",
                "image": "/static/images/menu/street-chaat/samosa.jpg",
                "available": True,
                "rating": 4.7,
                "preparation_time": "8 minutes"
            },
            {
                "name": "Missal Pav",
                "category": "street-chaat",
                "price": 150,
                "description": "Spicy sprouted bean curry served with pav",
                "image": "/static/images/menu/street-chaat/missal-pav.jpg",
                "available": True,
                "rating": 4.6,
                "preparation_time": "12 minutes"
            },
            {
                "name": "Chole Bhature",
                "category": "street-chaat",
                "price": 60,
                "description": "Spicy chickpeas served with fried bread",
                "image": "/static/images/menu/street-chaat/chole-bhature.jpg",
                "available": True,
                "rating": 4.9,
                "preparation_time": "15 minutes"
            }
        ]
        mongo.db.food_items.insert_many(sample_chaat)

def insert_sample_gym_food_items():
    sample_gym_items = [
        {
            "name": "Avocado Smoothie",
            "category": "gym",
            "subcategory": "shakes",
            "price": 320,
            "description": "Creamy avocado smoothie with honey and milk",
            "image": "/static/images/menu/gym/shakes and smoothies/avacado-smoothie.jpg",
            "available": True,
            "rating": 4.8,
            "preparation_time": "5 minutes"
        },
        {
            "name": "Almond Milk",
            "category": "gym",
            "subcategory": "shakes",
            "price": 70,
            "description": "Fresh almond milk, lightly sweetened",
            "image": "/static/images/menu/gym/shakes and smoothies/almond-milk.jpg",
            "available": True,
            "rating": 4.6,
            "preparation_time": "3 minutes"
        },
        {
            "name": "Banana Peanut Butter Shake",
            "category": "gym",
            "subcategory": "shakes",
            "price": 110,
            "description": "Banana shake with peanut butter and milk",
            "image": "/static/images/menu/gym/shakes and smoothies/banana-shake.jpg",
            "available": True,
            "rating": 4.7,
            "preparation_time": "4 minutes"
        },
        {
            "name": "Paneer Tikka",
            "category": "gym",
            "subcategory": "protein",
            "price": 260,
            "description": "Grilled paneer with spices",
            "image": "/static/images/menu/gym/paneer-tikka.jpg",
            "available": True,
            "rating": 4.9,
            "preparation_time": "15 minutes"
        },
        {
            "name": "Palak Paneer",
            "category": "gym",
            "subcategory": "protein",
            "price": 280,
            "description": "Spinach curry with paneer cubes",
            "image": "/static/images/menu/gym/palak-paneer.jpg",
            "available": True,
            "rating": 4.8,
            "preparation_time": "20 minutes"
        },
        {
            "name": "Rajma Chawal",
            "category": "gym",
            "subcategory": "protein",
            "price": 100,
            "description": "Kidney beans curry with rice",
            "image": "/static/images/menu/gym/rajma-chawal.jpg",
            "available": True,
            "rating": 4.7,
            "preparation_time": "25 minutes"
        },
        {
            "name": "Multigrain Toast with Avocado",
            "category": "gym",
            "subcategory": "protein",
            "price": 290,
            "description": "Multigrain toast topped with avocado",
            "image": "/static/images/menu/gym/avocado-toast.jpg",
            "available": True,
            "rating": 4.6,
            "preparation_time": "7 minutes"
        },
        {
            "name": "Mint Cucumber Water",
            "category": "gym",
            "subcategory": "detox",
            "price": 50,
            "description": "Refreshing water with mint and cucumber",
            "image": "/static/images/menu/gym/mint-cucumber-water.jpg",
            "available": True,
            "rating": 4.5,
            "preparation_time": "2 minutes"
        },
        {
            "name": "Carrot Beetroot Detox Juice",
            "category": "gym",
            "subcategory": "detox",
            "price": 50,
            "description": "Detox juice with carrot and beetroot",
            "image": "/static/images/menu/gym/carrot-beetroot-juice.jpg",
            "available": True,
            "rating": 4.6,
            "preparation_time": "3 minutes"
        },
        {
            "name": "Coconut Water with Chia Seeds",
            "category": "gym",
            "subcategory": "detox",
            "price": 120,
            "description": "Coconut water with chia seeds",
            "image": "/static/images/menu/gym/coconut-chia.jpg",
            "available": True,
            "rating": 4.7,
            "preparation_time": "2 minutes"
        },
        {
            "name": "Aloe Vera Juice",
            "category": "gym",
            "subcategory": "detox",
            "price": 60,
            "description": "Aloe vera juice for detox",
            "image": "/static/images/menu/gym/aloe-vera-juice.jpg",
            "available": True,
            "rating": 4.6,
            "preparation_time": "2 minutes"
        }
    ]
    for item in sample_gym_items:
        if not mongo.db.food_items.find_one({"name": item["name"]}):
            mongo.db.food_items.insert_one(item)

# -------------- AUTH ROUTES -----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')  # Optional email field

        # Check if username already exists
        if users.find_one({'username': username}):
            flash("Username already exists.")
            return redirect(url_for('register'))

        # Create user document with hashed password
        user_doc = {
            'username': username,
            'password': generate_password_hash(password),
            'email': email,
            'created_at': datetime.utcnow(),
            'role': 'customer',
            'address': '',
            'phone': ''
        }
        
        users.insert_one(user_doc)
        flash("Registered successfully. Please log in.")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['user_id'] = str(user['_id'])
            session['role'] = user.get('role', 'customer')
            flash("Login successful.")
            return redirect(url_for('home'))
        flash("Invalid username or password.")
    
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        users = mongo.db.users
        username = request.form['username']
        new_password = request.form['new_password']

        user = users.find_one({'username': username})
        if user:
            hashed_password = generate_password_hash(new_password)
            users.update_one(
                {'username': username}, 
                {'$set': {'password': hashed_password}}
            )
            flash("Password reset successfully.")
            return redirect(url_for('login'))
        flash("Username not found.")
    
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# -------------- MAIN ROUTES -----------------

@app.route('/')
def home():
    # Always show home page, even if not logged in
    # If user is logged in, pass user info; else, pass None
    user = session.get('user')
    categories = ['veg', 'desserts', 'gym', 'street-chaat']
    food_by_category = {}
    for category in categories:
        food_by_category[category] = list(mongo.db.food_items.find(
            {'category': category, 'available': True}
        ).limit(4))
    return render_template('home.html', user=user, food_by_category=food_by_category)

# Update the desserts route to exclude ice-cream subcategory
@app.route('/desserts')
def desserts():
    desserts = list(mongo.db.food_items.find({
        '$and': [
            {'category': 'desserts'},
            {'available': True},
            {'$or': [
                {'subcategory': {'$exists': False}},
                {'subcategory': {'$ne': 'ice-cream'}}
            ]}
        ]
    }))
    return render_template('desserts.html', desserts=desserts)

@app.route('/ice-cream')
def ice_cream():
    ice_creams = list(mongo.db.food_items.find({'category': 'desserts', 'subcategory': 'ice-cream', 'available': True}))
    return render_template('ice-cream.html', ice_creams=ice_creams)

@app.route('/Dessert-Icream')
def dessert_icecream():
    desserts = list(mongo.db.food_items.find({'category': 'desserts', 'available': True}))
    return render_template('Dessert-Icream.html', desserts=desserts)

@app.route('/gym-food')
def gym_food():
    gym_foods = list(mongo.db.food_items.find({'category': 'gym', 'available': True}))
    return render_template('gym-food.html', gym_foods=gym_foods)

@app.route('/gym-protein')
def gym_protein():
    paneer = mongo.db.food_items.find_one({'name': 'Paneer Tikka'})
    palak = mongo.db.food_items.find_one({'name': 'Palak Paneer'})
    rajma = mongo.db.food_items.find_one({'name': 'Rajma Chawal'})
    return render_template(
        'gym-protein.html',
        paneer_id=str(paneer['_id']) if paneer else '',
        palak_id=str(palak['_id']) if palak else '',
        rajma_id=str(rajma['_id']) if rajma else ''
    )

@app.route('/gym-detox')
def gym_detox():
    mint = mongo.db.food_items.find_one({'name': 'Mint Cucumber Water'})
    carrot = mongo.db.food_items.find_one({'name': 'Carrot Beetroot Detox Juice'})
    coconut = mongo.db.food_items.find_one({'name': 'Coconut Water with Chia Seeds'})
    return render_template(
        'gym-detox.html',
        mint_id=str(mint['_id']) if mint else '',
        carrot_id=str(carrot['_id']) if carrot else '',
        coconut_id=str(coconut['_id']) if coconut else ''
    )

@app.route('/gym-shakes')
def gym_shakes():
    # Fetch the three shakes by name
    avocado = mongo.db.food_items.find_one({'name': 'Avocado Smoothie'})
    almond = mongo.db.food_items.find_one({'name': 'Almond Milk'})
    banana = mongo.db.food_items.find_one({'name': 'Banana Peanut Butter Shake'})
    return render_template(
        'gym-shakes.html',
        avocado_id=str(avocado['_id']) if avocado else '',
        almond_id=str(almond['_id']) if almond else '',
        banana_id=str(banana['_id']) if banana else ''
    )

@app.route('/street-chaat')
def street_chaat():
    chaat_items = list(mongo.db.food_items.find({'category': 'street-chaat', 'available': True}))
    return render_template('street-chaat.html', chaat_items=chaat_items)

@app.route('/veg')
def veg():
    veg_items = list(mongo.db.food_items.find({'category': 'veg', 'available': True}))
    return render_template('veg.html', veg_items=veg_items)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash("Please login to access your cart.")
        return redirect(url_for('login'))
    user_id = session['user_id']
    cart_items = list(mongo.db.cart.find({'user_id': user_id}))
    # Populate food item details
    for item in cart_items:
        try:
            food_item = mongo.db.food_items.find_one({'_id': ObjectId(item['food_item_id'])})
        except Exception:
            food_item = None
        if food_item:
            item['name'] = food_item.get('name')
            item['price'] = food_item.get('price')
            item['image'] = food_item.get('image')
            item['description'] = food_item.get('description')
        item['cart_id'] = str(item['_id'])
        item['food_item_id'] = str(item['food_item_id'])
    return render_template('cart.html', cart_items=cart_items, user=session['user'])

# -------------- API ROUTES FOR CART AND ORDERS -----------------

@app.route('/api/cart', methods=['GET'])
def get_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    user_id = session['user_id']
    cart_items = list(mongo.db.cart.find({'user_id': user_id}))
    # Populate food item details
    for item in cart_items:
        try:
            food_item = mongo.db.food_items.find_one({'_id': ObjectId(item['food_item_id'])})
        except Exception:
            food_item = None
        if food_item:
            item['food_details'] = food_item
            item['name'] = food_item.get('name')
            item['price'] = food_item.get('price')
            item['image'] = food_item.get('image')
            item['description'] = food_item.get('description')
        # Convert ObjectId to string for frontend
        item['cart_id'] = str(item['_id'])
        item['food_item_id'] = str(item['food_item_id'])
    return jsonify(cart_items)

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.get_json()
    food_item_id = data.get('food_item_id')
    quantity = data.get('quantity', 1)
    try:
        food_item_id_obj = ObjectId(food_item_id)
    except Exception:
        return jsonify({'error': 'Invalid food item ID'}), 400
    # Check if food item exists
    food_item = mongo.db.food_items.find_one({'_id': food_item_id_obj})
    if not food_item:
        return jsonify({'error': 'Food item not found'}), 404
    user_id = session['user_id']
    # Check if item already in cart
    existing_item = mongo.db.cart.find_one({
        'user_id': user_id,
        'food_item_id': str(food_item_id_obj)
    })
    if existing_item:
        # Update quantity
        mongo.db.cart.update_one(
            {'_id': existing_item['_id']},
            {'$inc': {'quantity': quantity}}
        )
    else:
        # Add new item to cart
        cart_item = {
            'user_id': user_id,
            'food_item_id': str(food_item_id_obj),
            'quantity': quantity,
            'added_at': datetime.utcnow()
        }
        mongo.db.cart.insert_one(cart_item)
    return jsonify({'message': 'Item added to cart successfully'})

@app.route('/api/cart/update', methods=['PUT'])
def update_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity')
    try:
        cart_item_id_obj = ObjectId(cart_item_id)
    except Exception:
        return jsonify({'error': 'Invalid cart item ID'}), 400
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        mongo.db.cart.delete_one({'_id': cart_item_id_obj})
    else:
        # Update quantity
        mongo.db.cart.update_one(
            {'_id': cart_item_id_obj},
            {'$set': {'quantity': quantity}}
        )
    return jsonify({'message': 'Cart updated successfully'})

@app.route('/api/cart/remove/<cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    try:
        cart_item_id_obj = ObjectId(cart_item_id)
    except Exception:
        return jsonify({'error': 'Invalid cart item ID'}), 400
    mongo.db.cart.delete_one({'_id': cart_item_id_obj})
    return jsonify({'message': 'Item removed from cart'})

@app.route('/api/orders', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    user_id = session['user_id']
    
    # Get user's cart items
    cart_items = list(mongo.db.cart.find({'user_id': user_id}))
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate total and prepare order items
    total_amount = 0
    order_items = []
    
    for cart_item in cart_items:
        food_item = mongo.db.food_items.find_one({'_id': cart_item['food_item_id']})
        if food_item:
            item_total = food_item['price'] * cart_item['quantity']
            total_amount += item_total
            
            order_items.append({
                'food_item_id': cart_item['food_item_id'],
                'food_name': food_item['name'],
                'quantity': cart_item['quantity'],
                'price': food_item['price'],
                'item_total': item_total
            })
    
    # Create order document
    order = {
        'user_id': user_id,
        'username': session['user'],
        'items': order_items,
        'total_amount': total_amount,
        'status': 'pending',
        'order_date': datetime.utcnow(),
        'delivery_address': data.get('delivery_address', ''),
        'phone': data.get('phone', ''),
        'payment_method': data.get('payment_method', 'cash_on_delivery')
    }
    
    # Insert order
    result = mongo.db.orders.insert_one(order)
    
    # Clear user's cart
    mongo.db.cart.delete_many({'user_id': user_id})
    
    return jsonify({
        'message': 'Order placed successfully',
        'order_id': str(result.inserted_id),
        'total_amount': total_amount
    })

@app.route('/api/orders/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    orders = list(mongo.db.orders.find({'user_id': user_id}).sort('order_date', -1))
    return jsonify(orders)

# -------------- ADMIN ROUTES -----------------

@app.route('/admin')
def admin_dashboard():
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied. Admin privileges required.")
        return redirect(url_for('home'))
    
    # Get statistics
    total_users = mongo.db.users.count_documents({})
    total_orders = mongo.db.orders.count_documents({})
    total_food_items = mongo.db.food_items.count_documents({})
    recent_orders = list(mongo.db.orders.find().sort('order_date', -1).limit(5))
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_orders=total_orders,
                         total_food_items=total_food_items,
                         recent_orders=recent_orders)

@app.route('/admin/food-items', methods=['GET', 'POST'])
def admin_food_items():
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied. Admin privileges required.")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Add new food item
        food_item = {
            'name': request.form['name'],
            'category': request.form['category'],
            'price': float(request.form['price']),
            'description': request.form['description'],
            'image': request.form['image'],
            'available': True,
            'rating': 0,
            'preparation_time': request.form['preparation_time']
        }
        mongo.db.food_items.insert_one(food_item)
        flash("Food item added successfully!")
        return redirect(url_for('admin_food_items'))
    
    food_items = list(mongo.db.food_items.find())
    return render_template('admin_food_items.html', food_items=food_items)

if __name__ == '__main__':
    # Initialize database with sample data
    init_database()
    insert_sample_gym_food_items()
    app.run(debug=True)
