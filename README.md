# lost-found-system
TrackIt — Lost & Found Management System
A full-stack web application for managing lost and found items, built with Flask + MySQL + modern dark UI.

📁 Project Structure
lost-found/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── schema.sql              # MySQL schema + seed data
├── .env                    # Environment variables (edit this!)
├── static/
│   ├── css/main.css        # Stylesheet (dark theme)
│   ├── js/main.js          # Frontend JavaScript
│   └── uploads/            # User-uploaded images (auto-created)
└── templates/
    ├── base.html           # Base layout
    ├── index.html          # Home page
    ├── login.html          # Login page
    ├── register.html       # Register page
    ├── dashboard.html      # User dashboard
    ├── report_item.html    # Report lost/found item form
    ├── search.html         # Search & filter page
    ├── claim.html          # Claim item form
    ├── admin_dashboard.html
    ├── admin_items.html
    ├── admin_claims.html
    └── admin_users.html
⚙️ Prerequisites
Python 3.10+
MySQL 8.0+
pip
🚀 Setup Instructions
1. Clone / open in VS Code
Open the lost-found/ folder in VS Code.

2. Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Set up MySQL database
Open MySQL Workbench or terminal and run:

CREATE DATABASE lost_found_db;
Then import the schema (optional — Flask auto-creates tables):

mysql -u root -p lost_found_db < schema.sql
5. Configure .env
Edit the .env file with your MySQL credentials:

SECRET_KEY=change-this-to-a-random-string
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=lost_found_db
6. Run the application
python app.py
The app will:

Auto-create all database tables
Seed categories automatically
Create default admin account
Open: http://localhost:5000

🔑 Default Credentials
Role	Email	Password
Admin	admin@lostfound.com	admin123
Register new user accounts from the Register page.

