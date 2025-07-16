from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import json
import os

app = Flask(__name__)
app.secret_key = "your_super_secret_key_change_this_in_production"

# SQLite database setup
DATABASE = 'food_app.db'

def init_db():
    """Initialize SQLite database with tables and sample data"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            role TEXT DEFAULT 'customer',
            address TEXT,
            phone TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            available BOOLEAN DEFAULT 1,
            rating REAL DEFAULT 0,
            preparation_time TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            food_item_id INTEGER,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (food_item_id) REFERENCES food_items (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            total_amount REAL,
            status TEXT DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            delivery_address TEXT,
            phone TEXT,
            payment_method TEXT DEFAULT 'cash_on_delivery',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Check if sample data exists
    cursor.execute("SELECT COUNT(*) FROM food_items")
    if cursor.fetchone()[0] == 0:
        # Insert sample food items
        sample_items = [
            ("Veg Biryani", "veg", 120, "Aromatic basmati rice cooked with fresh vegetables and aromatic spices", "/static/images/menu/veg/veg-biryani.jpg", 1, 4.5, "25 minutes"),
            ("Aloo Paratha", "veg", 150, "Whole wheat flatbread stuffed with spiced potato mixture", "/static/images/menu/veg/aloo-paratha.jpg", 1, 4.3, "15 minutes"),
            ("Dal Tadka", "veg", 120, "Yellow lentils tempered with aromatic spices and herbs", "/static/images/menu/veg/dal-tadka.jpg", 1, 4.2, "20 minutes"),
            ("Aloo Gobi", "veg", 180, "Potato and cauliflower curry with Indian spices", "/static/images/menu/veg/Aloo-Gobi.jpg", 1, 4.4, "30 minutes"),
            ("Chocolate Ice Cream", "desserts", 80, "Rich and creamy chocolate ice cream", "/static/images/menu/desserts and icream/desserts-icecream.jpg", 1, 4.6, "5 minutes"),
            ("Protein Shake", "gym", 200, "High protein shake with whey protein and fruits", "/static/images/menu/gym/gym-food.jpg", 1, 4.7, "10 minutes"),
            ("Pani Puri", "street-chaat", 60, "Crispy puris filled with spiced potato and tangy water", "/static/images/menu/street-chaat/street-chaat.jpg", 1, 4.8, "15 minutes")
        ]
        cursor.executemany("INSERT INTO food_items (name, category, price, description, image, available, rating, preparation_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample_items)
        print("Database initialized with sample food items!")
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

# -------------- AUTH ROUTES -----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')

        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            flash("Username already exists.")
            conn.close()
            return redirect(url_for('register'))

        # Create user with hashed password
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            (username, hashed_password, email, 'customer')
        )
        conn.commit()
        conn.close()
        
        flash("Registered successfully. Please log in.")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash("Login successful.")
            return redirect(url_for('home'))
        flash("Invalid username or password.")
    
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        
        username = request.form['username']
        new_password = request.form['new_password']

        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            hashed_password = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()
            flash("Password reset successfully.")
            conn.close()
            return redirect(url_for('login'))
        conn.close()
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
    if 'user' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get food items by category
    categories = ['veg', 'desserts', 'gym', 'street-chaat']
    food_by_category = {}
    
    for category in categories:
        cursor.execute("SELECT * FROM food_items WHERE category = ? AND available = 1 LIMIT 4", (category,))
        food_by_category[category] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('home.html', 
                         user=session['user'], 
                         food_by_category=food_by_category)

@app.route('/veg')
def veg():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'veg' AND available = 1")
    veg_items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('veg.html', veg_items=veg_items)

@app.route('/desserts')
def desserts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'desserts' AND available = 1")
    desserts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('desserts.html', desserts=desserts)

@app.route('/gym-food')
def gym_food():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'gym' AND available = 1")
    gym_foods = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('gym-food.html', gym_foods=gym_foods)

@app.route('/street-chaat')
def street_chaat():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'street-chaat' AND available = 1")
    chaat_items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('street-chaat.html', chaat_items=chaat_items)

@app.route('/Dessert-Icream')
def dessert_icecream():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'desserts' AND available = 1")
    desserts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('Dessert-Icream.html', desserts=desserts)

@app.route('/ice-cream')
def ice_cream():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'desserts' AND available = 1")
    ice_creams = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('ice-cream.html', ice_creams=ice_creams)

@app.route('/gym-protein')
def gym_protein():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'gym' AND available = 1")
    proteins = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('gym-protein.html', proteins=proteins)

@app.route('/gym-detox')
def gym_detox():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'gym' AND available = 1")
    detox_items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('gym-detox.html', detox_items=detox_items)

@app.route('/gym-shakes')
def gym_shakes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE category = 'gym' AND available = 1")
    shakes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('gym-shakes.html', shakes=shakes)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash("Please login to access your cart.")
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user's cart items with food details
    cursor.execute("""
        SELECT c.id as cart_id, c.quantity, f.id as food_id, f.name, f.price, f.image, f.description
        FROM cart c 
        JOIN food_items f ON c.food_item_id = f.id 
        WHERE c.user_id = ?
    """, (session['user_id'],))
    
    cart_items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template('cart.html', cart_items=cart_items, user=session['user'])

# -------------- API ROUTES -----------------

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    food_item_id = data.get('food_item_id')
    quantity = data.get('quantity', 1)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if food item exists
    cursor.execute("SELECT * FROM food_items WHERE id = ?", (food_item_id,))
    food_item = cursor.fetchone()
    if not food_item:
        conn.close()
        return jsonify({'error': 'Food item not found'}), 404
    
    user_id = session['user_id']
    
    # Check if item already in cart
    cursor.execute("SELECT * FROM cart WHERE user_id = ? AND food_item_id = ?", (user_id, food_item_id))
    existing_item = cursor.fetchone()
    
    if existing_item:
        # Update quantity
        cursor.execute("UPDATE cart SET quantity = quantity + ? WHERE id = ?", (quantity, existing_item['id']))
    else:
        # Add new item to cart
        cursor.execute("INSERT INTO cart (user_id, food_item_id, quantity) VALUES (?, ?, ?)", (user_id, food_item_id, quantity))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item added to cart successfully'})

@app.route('/api/cart/update', methods=['PUT'])
def update_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity')
    
    conn = get_db()
    cursor = conn.cursor()
    
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        cursor.execute("DELETE FROM cart WHERE id = ? AND user_id = ?", (cart_item_id, session['user_id']))
    else:
        # Update quantity
        cursor.execute("UPDATE cart SET quantity = ? WHERE id = ? AND user_id = ?", (quantity, cart_item_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Cart updated successfully'})

@app.route('/api/cart/remove/<int:cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE id = ? AND user_id = ?", (cart_item_id, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item removed from cart'})

@app.route('/api/orders', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    user_id = session['user_id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user's cart items
    cursor.execute("""
        SELECT c.*, f.name, f.price 
        FROM cart c 
        JOIN food_items f ON c.food_item_id = f.id 
        WHERE c.user_id = ?
    """, (user_id,))
    cart_items = cursor.fetchall()
    
    if not cart_items:
        conn.close()
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate total
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # Create order
    cursor.execute("""
        INSERT INTO orders (user_id, username, total_amount, delivery_address, phone, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, session['user'], total_amount, data.get('delivery_address', ''), 
          data.get('phone', ''), data.get('payment_method', 'cash_on_delivery')))
    
    order_id = cursor.lastrowid
    
    # Clear user's cart
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': 'Order placed successfully',
        'order_id': order_id,
        'total_amount': total_amount
    })

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("🚀 Starting Food Delivery App with SQLite database...")
    print("📱 Access the app at: http://localhost:5000")
    print("👤 Register a new account to get started!")
    app.run(debug=True) 