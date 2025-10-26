"""
Chat service for the Vendor Research Web Application.
"""

import os
import json
from models.database import db, Vendor, Service, Product, ServiceFeature, ProductFeature
import re

class ChatService:
    """Service for handling chat queries about the database."""
    
    def __init__(self):
        self.setup_vector_database()
    
    def setup_vector_database(self):
        """Setup vector database for semantic search."""
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer
            
            # Initialize ChromaDB
            self.chroma_client = chromadb.Client()
            self.collection = self.chroma_client.create_collection("vendor_data")
            
            # Initialize sentence transformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load existing data
            self.load_existing_data()
            
        except ImportError:
            print("ChromaDB or sentence-transformers not available. Using simple text search.")
            self.chroma_client = None
            self.collection = None
            self.model = None
    
    def load_existing_data(self):
        """Load existing vendor data into vector database."""
        if not self.collection:
            return
        
        try:
            # Get all vendors with their services and products
            vendors = Vendor.query.all()
            
            documents = []
            metadatas = []
            ids = []
            
            for vendor in vendors:
                # Add vendor information
                vendor_text = f"Vendor: {vendor.name}. Description: {vendor.description or ''}. Website: {vendor.website}."
                
                # Add services
                for service in vendor.services:
                    service_text = f"Service: {service.name}. Category: {service.category or ''}. Description: {service.description or ''}. Pricing: {service.pricing or ''}."
                    for feature in service.features:
                        service_text += f" Feature: {feature.feature}."
                    
                    documents.append(service_text)
                    metadatas.append({
                        'type': 'service',
                        'vendor_id': vendor.id,
                        'vendor_name': vendor.name,
                        'service_id': service.id,
                        'service_name': service.name
                    })
                    ids.append(f"service_{service.id}")
                
                # Add products
                for product in vendor.products:
                    product_text = f"Product: {product.name}. Category: {product.category or ''}. Description: {product.description or ''}. Pricing: {product.pricing or ''}. Target Audience: {product.target_audience or ''}."
                    for feature in product.features:
                        product_text += f" Feature: {feature.feature}."
                    
                    documents.append(product_text)
                    metadatas.append({
                        'type': 'product',
                        'vendor_id': vendor.id,
                        'vendor_name': vendor.name,
                        'product_id': product.id,
                        'product_name': product.name
                    })
                    ids.append(f"product_{product.id}")
            
            # Add to ChromaDB
            if documents:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                
        except Exception as e:
            print(f"Error loading existing data: {e}")
    
    def process_query(self, query):
        """Process a natural language query about the database."""
        try:
            # Try semantic search first
            if self.collection and self.model:
                return self._semantic_search(query)
            else:
                return self._text_search(query)
                
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def _semantic_search(self, query):
        """Perform semantic search using vector database."""
        try:
            # Query the vector database
            results = self.collection.query(
                query_texts=[query],
                n_results=5
            )
            
            if not results['documents'][0]:
                return "No relevant information found in the database."
            
            response = "Here's what I found:\n\n"
            
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                if distance < 0.8:  # Only include relevant results
                    if metadata['type'] == 'service':
                        response += f"**Service**: {metadata['service_name']} by {metadata['vendor_name']}\n"
                        response += f"{doc}\n\n"
                    elif metadata['type'] == 'product':
                        response += f"**Product**: {metadata['product_name']} by {metadata['vendor_name']}\n"
                        response += f"{doc}\n\n"
            
            return response
            
        except Exception as e:
            return f"Error in semantic search: {str(e)}"
    
    def _text_search(self, query):
        """Perform simple text search."""
        try:
            query_lower = query.lower()
            response = "Here's what I found:\n\n"
            
            # Search in services
            services = Service.query.all()
            found_services = []
            
            for service in services:
                if (query_lower in service.name.lower() or 
                    query_lower in (service.description or '').lower() or
                    query_lower in (service.category or '').lower()):
                    found_services.append(service)
            
            if found_services:
                response += "**Services:**\n"
                for service in found_services:
                    response += f"- {service.name} by {service.vendor.name}\n"
                    if service.description:
                        response += f"  Description: {service.description[:100]}...\n"
                    if service.pricing:
                        response += f"  Pricing: {service.pricing}\n"
                response += "\n"
            
            # Search in products
            products = Product.query.all()
            found_products = []
            
            for product in products:
                if (query_lower in product.name.lower() or 
                    query_lower in (product.description or '').lower() or
                    query_lower in (product.category or '').lower()):
                    found_products.append(product)
            
            if found_products:
                response += "**Products:**\n"
                for product in found_products:
                    response += f"- {product.name} by {product.vendor.name}\n"
                    if product.description:
                        response += f"  Description: {product.description[:100]}...\n"
                    if product.pricing:
                        response += f"  Pricing: {product.pricing}\n"
                response += "\n"
            
            # Search in features
            service_features = ServiceFeature.query.all()
            product_features = ProductFeature.query.all()
            
            found_features = []
            for feature in service_features:
                if query_lower in feature.feature.lower():
                    found_features.append(('service', feature))
            
            for feature in product_features:
                if query_lower in feature.feature.lower():
                    found_features.append(('product', feature))
            
            if found_features:
                response += "**Features:**\n"
                for feature_type, feature in found_features:
                    if feature_type == 'service':
                        response += f"- {feature.feature} (Service: {feature.service.name} by {feature.service.vendor.name})\n"
                    else:
                        response += f"- {feature.feature} (Product: {feature.product.name} by {feature.product.vendor.name})\n"
            
            if not found_services and not found_products and not found_features:
                response = "No relevant information found in the database. Try searching for specific services, products, or features."
            
            return response
            
        except Exception as e:
            return f"Error in text search: {str(e)}"
    
    def suggest_queries(self):
        """Suggest example queries for the user."""
        return [
            "Which vendors offer cybersecurity services?",
            "What products are available for endpoint security?",
            "Show me vendors with cloud solutions",
            "Which vendors offer training services?",
            "What are the pricing options for security products?",
            "Show me vendors that support AWS",
            "Which vendors offer consulting services?",
            "What products are available for small businesses?"
        ]
