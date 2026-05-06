import os
import json
from datetime import datetime, date
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, jsonify, send_from_directory)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# ✅ IMPORT DB
from db import db, init_db

load_dotenv()

# ✅ CREATE APP FIRST
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# ✅ INIT DB
init_db(app)

# Other configs
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ─── ROUTES ─────────────────────────────────────────

# ─── ROUTES ─────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return "Working!"
@app.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category')
    location = request.args.get('location')
    item_type = request.args.get('type')

    categories = Category.query.all()

    lost_items = LostItem.query
    found_items = FoundItem.query

    if query:
        lost_items = lost_items.filter(LostItem.title.contains(query))
        found_items = found_items.filter(FoundItem.title.contains(query))

    if category_id:
        lost_items = lost_items.filter_by(cat_id=category_id)
        found_items = found_items.filter_by(cat_id=category_id)

    if location:
        lost_items = lost_items.filter(LostItem.location.contains(location))
        found_items = found_items.filter(FoundItem.location.contains(location))

    lost_items = lost_items.all()
    found_items = found_items.all()

    return render_template(
        'search.html',
        lost_items=lost_items,
        found_items=found_items,
        categories=categories
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))   # ✅ IMPORTANT

    # ✅ ALWAYS return something
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Simple insert (for now)
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():
    categories = Category.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        cat_id = request.form.get('cat_id')
        date_lost = request.form.get('date_lost')
        location = request.form.get('location')
        description = request.form.get('description')

        new_item = LostItem(
            title=title,
            cat_id=cat_id,
            date_lost=date_lost,
            location=location,
            description=description,
            user_id=session.get('user_id')
        )

        db.session.add(new_item)
        db.session.commit()

        flash('Lost item reported successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template(
        'report_item.html',
        item_type='lost',
        categories=categories
    )
@app.route('/report_found', methods=['GET', 'POST'])
def report_found():
    categories = Category.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        cat_id = request.form.get('cat_id')
        date_found = request.form.get('date_found')
        location = request.form.get('location')
        description = request.form.get('description')

        new_item = FoundItem(
            title=title,
            cat_id=cat_id,
            date_found=date_found,
            location=location,
            description=description,
            user_id=session.get('user_id')
        )

        db.session.add(new_item)
        db.session.commit()

        flash('Found item reported successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template(
        'report_item.html',
        item_type='found',
        categories=categories
    )

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # ✅ Fetch user data
    my_lost = LostItem.query.filter_by(user_id=user_id).all()
    my_found = FoundItem.query.filter_by(user_id=user_id).all()
    my_claims = Claim.query.filter_by(user_id=user_id).all()

    return render_template(
        'dashboard.html',
        my_lost=my_lost,
        my_found=my_found,
        my_claims=my_claims
    )

@app.route('/claim/<string:item_type>/<int:item_id>', methods=['GET', 'POST'])
def claim_item(item_type, item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 🔍 Get correct item
    item = None
    if item_type == 'lost':
        item = LostItem.query.get_or_404(item_id)
    elif item_type == 'found':
        item = FoundItem.query.get_or_404(item_id)
    else:
        return "Invalid item type", 400

    # 📝 Handle form submit
    if request.method == 'POST':
        message = request.form.get('message')

        new_claim = Claim(
            user_id=session['user_id'],
            item_id=item_id,
            item_type=item_type,
            message=message,
            status='pending'
        )

        db.session.add(new_claim)
        db.session.commit()

        flash('Claim submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    # 📄 Show claim page
    return render_template('claim.html', item=item, item_type=item_type)

# Admin pages (if used)
@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html')

@app.route('/admin/items')
def admin_items():
    return render_template('admin_items.html')

@app.route('/admin/claims')
def admin_claims():
    return render_template('admin_claims.html')
# ─── MODELS ─────────────────────────────────────────

class Category(db.Model):
    __tablename__ = 'categories'
    cat_id = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(100), nullable=False, unique=True)

class User(db.Model):
    __tablename__ = 'users'
    user_id    = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(150), nullable=False)
    email      = db.Column(db.String(255), nullable=False, unique=True)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.Enum('user', 'admin'), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active  = db.Column(db.Boolean, default=True)

class LostItem(db.Model):
    __tablename__ = 'lost_items'
    item_id     = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cat_id      = db.Column(db.Integer, db.ForeignKey('categories.cat_id'), nullable=False)
    location    = db.Column(db.String(255), nullable=False)
    date_lost   = db.Column(db.Date, nullable=False)
    image_path  = db.Column(db.String(500))
    status      = db.Column(db.Enum('reported', 'verified', 'claimed', 'closed'), default='reported')
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user        = db.relationship('User', backref='lost_items')
    category    = db.relationship('Category', backref='lost_items')

class FoundItem(db.Model):
    __tablename__ = 'found_items'
    item_id     = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cat_id      = db.Column(db.Integer, db.ForeignKey('categories.cat_id'), nullable=False)
    location    = db.Column(db.String(255), nullable=False)
    date_found  = db.Column(db.Date, nullable=False)
    image_path  = db.Column(db.String(500))
    status      = db.Column(db.Enum('reported', 'verified', 'claimed', 'closed'), default='reported')
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user        = db.relationship('User', backref='found_items')
    category    = db.relationship('Category', backref='found_items')

class Claim(db.Model):
    __tablename__ = 'claims'
    claim_id   = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    item_id    = db.Column(db.Integer, nullable=False)
    item_type  = db.Column(db.Enum('lost', 'found'), nullable=False)
    message    = db.Column(db.Text)
    status     = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user       = db.relationship('User', backref='claims')

class AdminLog(db.Model):
    __tablename__ = 'admin_logs'
    log_id      = db.Column(db.Integer, primary_key=True)
    admin_id    = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    action      = db.Column(db.String(255), nullable=False)
    target_type = db.Column(db.String(50))
    target_id   = db.Column(db.Integer)
    details     = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    admin       = db.relationship('User', backref='logs')

# ─── INIT ─────────────────────────────────────────

def seed_categories():
    if Category.query.count() == 0:
        cats = ['Electronics', 'Clothing', 'Accessories', 'Documents',
                'Bags & Wallets', 'Keys', 'Jewelry', 'Books', 'Sports Equipment', 'Other']
        for c in cats:
            db.session.add(Category(name=c))
        db.session.commit()

def create_admin():
    if not User.query.filter_by(role='admin').first():
        admin = User(name='Admin', email='admin@lostfound.com',
                     password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_categories()
        create_admin()
    app.run(debug=True)