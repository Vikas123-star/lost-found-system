-- ============================================
-- Lost & Found Management System - Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS lost_found_db;
USE lost_found_db;

-- Categories Table
CREATE TABLE IF NOT EXISTS categories (
    cat_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Lost Items Table
CREATE TABLE IF NOT EXISTS lost_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    cat_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    date_lost DATE NOT NULL,
    image_path VARCHAR(500),
    status ENUM('reported', 'verified', 'claimed', 'closed') DEFAULT 'reported',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (cat_id) REFERENCES categories(cat_id),
    INDEX idx_status (status),
    INDEX idx_cat_id (cat_id),
    INDEX idx_location (location(50))
);

-- Found Items Table
CREATE TABLE IF NOT EXISTS found_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    cat_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    date_found DATE NOT NULL,
    image_path VARCHAR(500),
    status ENUM('reported', 'verified', 'claimed', 'closed') DEFAULT 'reported',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (cat_id) REFERENCES categories(cat_id),
    INDEX idx_status (status),
    INDEX idx_cat_id (cat_id),
    INDEX idx_location (location(50))
);

-- Claims Table
CREATE TABLE IF NOT EXISTS claims (
    claim_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    item_type ENUM('lost', 'found') NOT NULL,
    message TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Admin Logs Table
CREATE TABLE IF NOT EXISTS admin_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    target_type VARCHAR(50),
    target_id INT,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================
-- Seed Data
-- ============================================

INSERT INTO categories (name) VALUES
('Electronics'), ('Clothing'), ('Accessories'), ('Documents'),
('Bags & Wallets'), ('Keys'), ('Jewelry'), ('Books'), ('Sports Equipment'), ('Other');

-- Admin user (password: admin123)
INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@lostfound.com', 'scrypt:32768:8:1$salt$hash', 'admin');

-- Sample regular users (password: user123)
INSERT INTO users (name, email, password, role) VALUES
('Alice Johnson', 'alice@example.com', 'scrypt:32768:8:1$salt$hash', 'user'),
('Bob Smith', 'bob@example.com', 'scrypt:32768:8:1$salt$hash', 'user');

-- Sample Lost Items
INSERT INTO lost_items (user_id, title, description, cat_id, location, date_lost, status) VALUES
(2, 'Black iPhone 14', 'Black iPhone 14 Pro with cracked screen protector, has a blue case', 1, 'Central Park, NY', '2024-01-10', 'verified'),
(2, 'Blue Denim Jacket', 'Medium sized blue denim jacket with patches on sleeve', 2, 'Main Library', '2024-01-12', 'reported'),
(3, 'Car Keys with Red Keychain', 'Toyota car keys with a red Minnie Mouse keychain', 6, 'Westfield Mall, Food Court', '2024-01-15', 'claimed');

-- Sample Found Items
INSERT INTO found_items (user_id, title, description, cat_id, location, date_found, status) VALUES
(3, 'Silver Laptop Bag', 'Gray laptop bag with initials JD, contains charger', 5, 'City Bus Route 42', '2024-01-11', 'verified'),
(2, 'Prescription Glasses', 'Black frame prescription glasses in a red case', 3, 'Coffee Central Cafe', '2024-01-13', 'reported'),
(3, 'Student ID Card', 'State University student ID for Michael Torres', 4, 'University Cafeteria', '2024-01-16', 'claimed');

-- Sample Claims
INSERT INTO claims (user_id, item_id, item_type, message, status) VALUES
(2, 1, 'found', 'I believe the silver laptop bag belongs to me. My initials are JD and I lost it on bus route 42.', 'approved'),
(3, 1, 'lost', 'I found the iPhone matching this description near the park entrance.', 'pending');
