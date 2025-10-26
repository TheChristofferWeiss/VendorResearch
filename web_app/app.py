"""
Vendor Research Web Application
A comprehensive web interface for vendor management, scraping, and analysis.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import json
from datetime import datetime
import subprocess
import threading
import time

from models.database import db, Vendor, Service, Product, ServiceFeature, ProductFeature
from services.scraper_service import ScraperService
from services.extractor_service import ExtractorService
from services.chat_service import ChatService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendor_research.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Initialize services
scraper_service = ScraperService()
extractor_service = ExtractorService()
chat_service = ChatService()

# Global variables for tracking scraping progress
scraping_status = {}
extraction_status = {}

@app.route('/')
def index():
    """Main dashboard page."""
    vendors = Vendor.query.all()
    return render_template('index.html', vendors=vendors)

@app.route('/admin')
def admin():
    """Admin panel for vendor management."""
    vendors = Vendor.query.all()
    return render_template('admin.html', vendors=vendors)

@app.route('/vendor/<int:vendor_id>')
def vendor_detail(vendor_id):
    """Detailed vendor view."""
    vendor = Vendor.query.get_or_404(vendor_id)
    return render_template('vendor_detail.html', vendor=vendor)

@app.route('/chat')
def chat():
    """Chat interface for querying the database."""
    return render_template('chat.html')

# API Routes

@app.route('/api/vendors', methods=['POST'])
def add_vendor():
    """Add a new vendor to scrape."""
    data = request.get_json()
    
    vendor = Vendor(
        name=data['name'],
        website=data['website'],
        description=data.get('description', ''),
        status='pending'
    )
    
    db.session.add(vendor)
    db.session.commit()
    
    return jsonify({'success': True, 'vendor_id': vendor.id})

@app.route('/api/vendors/<int:vendor_id>/scrape', methods=['POST'])
def scrape_vendor(vendor_id):
    """Start scraping a vendor."""
    vendor = Vendor.query.get_or_404(vendor_id)
    
    if vendor.status == 'scraping':
        return jsonify({'error': 'Vendor is already being scraped'}), 400
    
    # Start scraping in background thread
    vendor.status = 'scraping'
    db.session.commit()
    
    def scrape_worker():
        try:
            # Update scraping status
            scraping_status[vendor_id] = {'status': 'starting', 'progress': 0}
            
            # Run the scraper
            result = scraper_service.scrape_vendor(vendor.website)
            
            if result:
                vendor.raw_data = json.dumps(result)
                vendor.scraped_at = datetime.utcnow()
                vendor.status = 'scraped'
                scraping_status[vendor_id] = {'status': 'completed', 'progress': 100}
            else:
                vendor.status = 'failed'
                scraping_status[vendor_id] = {'status': 'failed', 'progress': 0}
            
            db.session.commit()
            
        except Exception as e:
            vendor.status = 'failed'
            scraping_status[vendor_id] = {'status': 'failed', 'error': str(e)}
            db.session.commit()
    
    # Start background thread
    thread = threading.Thread(target=scrape_worker)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Scraping started'})

@app.route('/api/vendors/<int:vendor_id>/extract', methods=['POST'])
def extract_vendor(vendor_id):
    """Extract services and products from scraped data."""
    vendor = Vendor.query.get_or_404(vendor_id)
    
    if not vendor.raw_data:
        return jsonify({'error': 'No scraped data available'}), 400
    
    if vendor.status == 'extracting':
        return jsonify({'error': 'Vendor is already being processed'}), 400
    
    # Start extraction in background thread
    vendor.status = 'extracting'
    db.session.commit()
    
    def extract_worker():
        try:
            # Update extraction status
            extraction_status[vendor_id] = {'status': 'starting', 'progress': 0}
            
            # Parse raw data
            raw_data = json.loads(vendor.raw_data)
            
            # Extract services and products
            result = extractor_service.extract_from_raw_data(raw_data)
            
            if result:
                # Save services
                for service_data in result.get('services', []):
                    service = Service(
                        vendor_id=vendor.id,
                        name=service_data['name'],
                        category=service_data.get('category', ''),
                        description=service_data.get('description', ''),
                        url=service_data.get('url', ''),
                        pricing=service_data.get('pricing', '')
                    )
                    db.session.add(service)
                    
                    # Save service features
                    for feature in service_data.get('features', []):
                        service_feature = ServiceFeature(
                            service_id=service.id,
                            feature=feature
                        )
                        db.session.add(service_feature)
                
                # Save products
                for product_data in result.get('products', []):
                    product = Product(
                        vendor_id=vendor.id,
                        name=product_data['name'],
                        category=product_data.get('category', ''),
                        description=product_data.get('description', ''),
                        url=product_data.get('url', ''),
                        pricing=product_data.get('pricing', ''),
                        target_audience=product_data.get('target_audience', ''),
                        requirements=product_data.get('requirements', ''),
                        deployment=product_data.get('deployment', ''),
                        support=product_data.get('support', '')
                    )
                    db.session.add(product)
                    
                    # Save product features
                    for feature in product_data.get('features', []):
                        product_feature = ProductFeature(
                            product_id=product.id,
                            feature=feature
                        )
                        db.session.add(product_feature)
                
                vendor.status = 'completed'
                extraction_status[vendor_id] = {'status': 'completed', 'progress': 100}
            else:
                vendor.status = 'failed'
                extraction_status[vendor_id] = {'status': 'failed', 'progress': 0}
            
            db.session.commit()
            
        except Exception as e:
            vendor.status = 'failed'
            extraction_status[vendor_id] = {'status': 'failed', 'error': str(e)}
            db.session.commit()
    
    # Start background thread
    thread = threading.Thread(target=extract_worker)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Extraction started'})

@app.route('/api/vendors/<int:vendor_id>/status')
def get_vendor_status(vendor_id):
    """Get scraping/extraction status for a vendor."""
    vendor = Vendor.query.get_or_404(vendor_id)
    
    status_data = {
        'vendor_status': vendor.status,
        'scraping_status': scraping_status.get(vendor_id, {}),
        'extraction_status': extraction_status.get(vendor_id, {})
    }
    
    return jsonify(status_data)

@app.route('/api/chat', methods=['POST'])
def chat_query():
    """Handle chat queries about the database."""
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        response = chat_service.process_query(query)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vendors/<int:vendor_id>/raw-data')
def get_raw_data(vendor_id):
    """Get raw scraped data for a vendor."""
    vendor = Vendor.query.get_or_404(vendor_id)
    
    if not vendor.raw_data:
        return jsonify({'error': 'No raw data available'}), 404
    
    return jsonify(json.loads(vendor.raw_data))

@app.route('/api/vendors/<int:vendor_id>/services')
def get_vendor_services(vendor_id):
    """Get services for a vendor."""
    vendor = Vendor.query.get_or_404(vendor_id)
    services = Service.query.filter_by(vendor_id=vendor_id).all()
    
    services_data = []
    for service in services:
        features = ServiceFeature.query.filter_by(service_id=service.id).all()
        services_data.append({
            'id': service.id,
            'name': service.name,
            'category': service.category,
            'description': service.description,
            'url': service.url,
            'pricing': service.pricing,
            'features': [f.feature for f in features]
        })
    
    return jsonify(services_data)

@app.route('/api/vendors/<int:vendor_id>/products')
def get_vendor_products(vendor_id):
    """Get products for a vendor."""
    vendor = Vendor.query.get_or_404(vendor_id)
    products = Product.query.filter_by(vendor_id=vendor_id).all()
    
    products_data = []
    for product in products:
        features = ProductFeature.query.filter_by(product_id=product.id).all()
        products_data.append({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'url': product.url,
            'pricing': product.pricing,
            'target_audience': product.target_audience,
            'requirements': product.requirements,
            'deployment': product.deployment,
            'support': product.support,
            'features': [f.feature for f in features]
        })
    
    return jsonify(products_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
