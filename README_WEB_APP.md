# Vendor Research Web Application

A complete web interface for vendor management, scraping, and analysis with a chat interface for querying the database.

## 🎯 System Overview

This web application provides:

1. **Admin Panel** - Add and manage vendors
2. **Web Scraping** - Extract content from vendor websites
3. **Data Extraction** - Extract services and products from scraped data
4. **Database Storage** - Store all data in SQLite database
5. **Chat Interface** - Query the database using natural language
6. **Vendor Details** - View detailed vendor information

## 🚀 Quick Start

### 1. Start the Application
```bash
cd ~/Projects/VendorResearch
python start_web_app.py
```

### 2. Access the Web Interface
- **Main Dashboard**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Chat Interface**: http://localhost:8000/chat

## 📊 Features

### Admin Panel
- **Add Vendors**: Add new vendors with name, website, and description
- **Scrape Vendors**: Start scraping vendor websites
- **Extract Data**: Extract services and products from scraped data
- **View Raw Data**: See the raw scraped content
- **Status Tracking**: Monitor scraping and extraction progress

### Vendor Management
- **Vendor List**: View all vendors with their status
- **Detailed View**: See comprehensive vendor information
- **Services**: View extracted services with features and pricing
- **Products**: View extracted products with detailed information
- **Raw Data**: Access original scraped content

### Chat Interface
- **Natural Language Queries**: Ask questions about the database
- **Suggested Queries**: Pre-built questions to get started
- **Real-time Responses**: Get instant answers about vendors, services, and products

## 🗄️ Database Schema

### Tables

#### vendors
- `id` - Primary key
- `name` - Vendor name
- `website` - Vendor website URL
- `description` - Vendor description
- `status` - Current status (pending, scraping, scraped, extracting, completed, failed)
- `raw_data` - JSON string of scraped data
- `scraped_at` - When data was scraped
- `created_at` - When record was created

#### services
- `id` - Primary key
- `vendor_id` - Foreign key to vendors
- `name` - Service name
- `category` - Service category
- `description` - Service description
- `url` - URL to service page
- `pricing` - Pricing information

#### products
- `id` - Primary key
- `vendor_id` - Foreign key to vendors
- `name` - Product name
- `category` - Product category
- `description` - Product description
- `url` - URL to product page
- `pricing` - Pricing information
- `target_audience` - Target audience
- `requirements` - System requirements
- `deployment` - Deployment information
- `support` - Support information

#### service_features
- `id` - Primary key
- `service_id` - Foreign key to services
- `feature` - Feature description

#### product_features
- `id` - Primary key
- `product_id` - Foreign key to products
- `feature` - Feature description

## 🔧 Usage Examples

### Adding a Vendor
1. Go to Admin Panel (http://localhost:8000/admin)
2. Fill in vendor information:
   - Name: "Arctic Wolf"
   - Website: "https://arcticwolf.com"
   - Description: "Cybersecurity company"
3. Click "Add Vendor"

### Scraping a Vendor
1. In Admin Panel, find the vendor
2. Click "Scrape" button
3. Wait for scraping to complete
4. View raw data when scraping is complete

### Extracting Services and Products
1. After scraping is complete, click "Extract" button
2. Wait for extraction to complete
3. View extracted services and products in vendor details

### Querying the Database
1. Go to Chat Interface (http://localhost:8000/chat)
2. Ask questions like:
   - "Which vendors offer cybersecurity services?"
   - "What products are available for endpoint security?"
   - "Show me vendors with cloud solutions"
   - "Which vendors offer training services?"

## 📈 Example Queries

### Service Queries
- "Which vendors offer cybersecurity services?"
- "Show me vendors with cloud solutions"
- "What training services are available?"
- "Which vendors offer consulting services?"

### Product Queries
- "What products are available for endpoint security?"
- "Show me security products"
- "What software solutions are available?"
- "Which vendors offer platform solutions?"

### Feature Queries
- "Which vendors have AI features?"
- "Show me vendors with machine learning capabilities"
- "What automation features are available?"
- "Which vendors offer real-time monitoring?"

### Pricing Queries
- "What are the pricing options for security products?"
- "Show me vendors with free tiers"
- "What are the enterprise pricing options?"
- "Which vendors offer subscription models?"

## 🎯 Chat Interface Features

### Natural Language Processing
The chat interface uses text search to understand your questions and provide relevant answers.

### Suggested Queries
Pre-built questions to help you get started:
- Cybersecurity Services
- Endpoint Security
- Cloud Solutions
- Training Services
- Pricing Information
- AWS Support

### Real-time Responses
Get instant answers about:
- Vendor information
- Service offerings
- Product details
- Feature lists
- Pricing information
- Contact details

## 🔍 Advanced Features

### Data Extraction
- Automatically extracts services and products
- Identifies features and benefits
- Extracts pricing information
- Determines target audiences

### Status Tracking
- Real-time progress updates
- Error handling and reporting
- Background processing
- Status notifications

### Web Scraping
- Uses curl for reliable content fetching
- Handles multiple pages per vendor
- Filters relevant content
- Respects website policies

## 🚀 Next Steps

1. **Add More Vendors**: Use the admin panel to add more vendors
2. **Scrape Data**: Start scraping vendor websites
3. **Extract Information**: Extract services and products
4. **Query Database**: Use the chat interface to explore the data
5. **Analyze Results**: Review extracted information for insights

## 📝 Notes

- All data is extracted from publicly available websites
- Scraping is done respectfully with delays between requests
- Data is stored locally in SQLite database
- Chat interface provides intelligent search capabilities
- System handles multiple vendors and large datasets

## 🔧 Troubleshooting

### Common Issues

1. **Scraping Fails**: Check if the website is accessible and not blocking requests
2. **Extraction Fails**: Ensure raw data is available and properly formatted
3. **Chat Not Working**: Check if the database has data and services are running
4. **Database Errors**: Ensure SQLite database is properly initialized

### Solutions

1. **Check Logs**: Review console output for error messages
2. **Verify Dependencies**: Ensure all required packages are installed
3. **Test Components**: Use the simple test application to verify functionality
4. **Restart Services**: Restart the web application if needed

## 📊 Sample Data

### Vendor Example
```
Name: Arctic Wolf
Website: https://arcticwolf.com
Description: Cybersecurity company
Status: completed
Services: 5 services extracted
Products: 3 products extracted
```

### Service Example
```
Name: Aurora Endpoint Security
Category: Security
Description: AI-driven endpoint protection
Pricing: Contact for pricing
URL: https://arcticwolf.com/solutions/endpoint-security/
```

### Product Example
```
Name: Managed Detection and Response
Category: Security
Description: 24x7 monitoring and response
Pricing: Contact for pricing
Target Audience: Enterprise organizations
```

---

**Built for comprehensive vendor research with intelligent querying capabilities.**
