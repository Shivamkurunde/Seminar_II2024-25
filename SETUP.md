# 🍽️ Food Delivery App - Database Setup Guide

## 📋 Prerequisites

1. **Python 3.7+** (Already installed)
2. **MongoDB** (Choose one option below)
3. **Required Python packages** (Already installed via requirements.txt)

## 🗄️ Database Setup Options

### Option A: MongoDB Atlas (Cloud - Recommended for beginners)

1. **Create MongoDB Atlas Account**
   - Go to: https://www.mongodb.com/atlas
   - Sign up for a free account
   - Create a new cluster (free tier)

2. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string

3. **Update app.py**
   - Replace the MongoDB URI in `app.py`:
   ```python
   app.config["MONGO_URI"] = "your_mongodb_atlas_connection_string"
   ```

### Option B: Local MongoDB Installation

1. **Download MongoDB Community Server**
   - Go to: https://www.mongodb.com/try/download/community
   - Download for Windows
   - Run installer and follow setup

2. **Start MongoDB Service**
   ```bash
   # MongoDB should start automatically on Windows
   # If not, start it manually
   ```

3. **Use Local Connection**
   ```python
   app.config["MONGO_URI"] = "mongodb://localhost:27017/foodApp"
   ```

## 🚀 Running the Application

1. **Install Dependencies** (Already done)
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open browser: http://localhost:5000
   - Register a new account
   - Start exploring!

## 📊 Database Collections

The app will automatically create these collections:

- **users** - User accounts and authentication
- **food_items** - Menu items with categories
- **cart** - Shopping cart items
- **orders** - Order history and details

## 🔧 Features Added

### ✅ Enhanced Security
- Password hashing with Werkzeug
- Secure session management
- Input validation

### ✅ Database Integration
- MongoDB collections for all data
- API endpoints for cart management
- Order processing system
- User management

### ✅ Dynamic Content
- Food items loaded from database
- Real-time cart updates
- Order history tracking

### ✅ Admin Features
- Admin dashboard (access via `/admin`)
- Food item management
- Order monitoring

## 🛠️ Troubleshooting

### Common Issues:

1. **MongoDB Connection Error**
   - Check if MongoDB is running
   - Verify connection string
   - Ensure network connectivity

2. **Import Errors**
   - Run: `pip install -r requirements.txt`
   - Check Python version (3.7+)

3. **Port Already in Use**
   - Change port in app.py: `app.run(debug=True, port=5001)`

## 📱 Next Steps

After setup, you can:
1. Add more food items via admin panel
2. Customize the UI/UX
3. Add payment integration
4. Implement email notifications
5. Add order tracking

## 🆘 Support

If you encounter issues:
1. Check the console for error messages
2. Verify MongoDB connection
3. Ensure all dependencies are installed
4. Check file permissions 