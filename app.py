from flask import Flask, request, render_template, jsonify
import socket
import requests
import whois
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

from flask_wtf import CSRFProtect



app = Flask(__name__)

# Initialize CSRF protection
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'csrfmiddlewaretoken'  # Make sure to set a strong secret key
# Route for home page (GET request)
@app.route('/')
def index():
    own_ip_address = get_client_ip()
    return render_template('index.html', own_ip_address=own_ip_address)


# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/fslip'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)  # Initialize SQLAlchemy with app directly
# migrate = Migrate(app, db)  # Initialize Flask-Migrate with app and db

# # Define the VisitorIP model
# class VisitorIP(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ip_address = db.Column(db.String(100), unique=True, nullable=False)
#     visit_time = db.Column(db.DateTime, default=datetime.utcnow)
#     visit_count = db.Column(db.Integer, default=1)

#     def increment_visit_count(self):
#         self.visit_count += 1
#         db.session.commit()

# Function to get client IP
def get_client_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip

# Function to get WHOIS info
def get_whois_info(ip_address):
    return whois.whois(ip_address)
    
# Function to get reverse DNS
def get_reverse_dns(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return None

# Function to get geolocation
def get_geolocation(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    if response.status_code == 200:
        data = response.json()
        country = data.get('country', 'Unknown')
        region = data.get('region', 'Unknown')
        return country, region
    return None, None

# Route for home page
@app.route('/sendip', methods=['POST'])
def sendip():
    ip_address = request.form.get('theip')
    whois_info = get_whois_info(ip_address)
    own_ip_address = get_client_ip()

    # # Check if the IP address is already in the database
    # visitor = VisitorIP.query.filter_by(ip_address=own_ip_address).first()

    # if visitor:
    #     # Increment the visit count if the IP is already in the database
    #     visitor.increment_visit_count()
    # else:
    #     # Create a new entry if IP address is not found
    #     new_visitor = VisitorIP(ip_address=own_ip_address)
    #     db.session.add(new_visitor)
    #     db.session.commit()

    if request.method == 'POST':
        ip_address = request.form.get('theip')
        whois_info = get_whois_info(ip_address)
        return jsonify(str(whois_info))

    # # Fetch all visitor IP records
    # visitor_ips = VisitorIP.query.all()

    # for visitor in visitor_ips:
    #     print(f"IP Address: {visitor.ip_address}, Visit Count: {visitor.visit_count}")

    return render_template('index.html', own_ip_address=own_ip_address)

if __name__ == "__main__":
    app.run(debug=True)
