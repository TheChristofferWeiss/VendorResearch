"""
Database models for the Vendor Research Web Application.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vendor(db.Model):
    """Vendor model for storing vendor information."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, scraping, scraped, extracting, completed, failed
    raw_data = db.Column(db.Text)  # JSON string of scraped data
    scraped_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services = db.relationship('Service', backref='vendor', lazy=True, cascade='all, delete-orphan')
    products = db.relationship('Product', backref='vendor', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'description': self.description,
            'status': self.status,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Service(db.Model):
    """Service model for storing vendor services."""
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    pricing = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    features = db.relationship('ServiceFeature', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'url': self.url,
            'pricing': self.pricing,
            'features': [f.feature for f in self.features],
            'created_at': self.created_at.isoformat()
        }

class Product(db.Model):
    """Product model for storing vendor products."""
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    pricing = db.Column(db.String(100))
    target_audience = db.Column(db.Text)
    requirements = db.Column(db.Text)
    deployment = db.Column(db.Text)
    support = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    features = db.relationship('ProductFeature', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'url': self.url,
            'pricing': self.pricing,
            'target_audience': self.target_audience,
            'requirements': self.requirements,
            'deployment': self.deployment,
            'support': self.support,
            'features': [f.feature for f in self.features],
            'created_at': self.created_at.isoformat()
        }

class ServiceFeature(db.Model):
    """Service feature model for storing service features."""
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    feature = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'feature': self.feature
        }

class ProductFeature(db.Model):
    """Product feature model for storing product features."""
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    feature = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'feature': self.feature
        }
