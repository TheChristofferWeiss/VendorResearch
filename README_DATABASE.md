# Vendor Research Database System

A comprehensive system for scraping vendor websites, extracting structured information, and storing it in database-ready formats for querying and analysis.

## 🎯 System Overview

This system provides a complete pipeline for vendor research:

1. **Web Scraping** - Extract content from vendor websites
2. **Data Processing** - Structure and organize vendor information
3. **Database Export** - Convert to multiple database formats
4. **Query Ready** - Prepare data for database storage and querying

## 📁 Project Structure

```
VendorResearch/
├── improved_vendor_scraper.py          # Main web scraper
├── vendor_database_extractor.py        # Extract structured data
├── markdown_to_database.py             # Convert to database formats
├── research_output/                    # Raw scraped data
├── vendor_database/                    # Structured markdown files
└── database_exports/                   # Database-ready files
```

## 🚀 Quick Start

### 1. Scrape a Vendor Website
```bash
python improved_vendor_scraper.py https://vendor-website.com
```

### 2. Extract Structured Data
```bash
python vendor_database_extractor.py
```

### 3. Convert to Database Formats
```bash
python markdown_to_database.py
```

## 📊 Database Formats Generated

### JSON Format
- **File**: `database_exports/vendors_database.json`
- **Use**: API integration, data exchange
- **Structure**: Complete vendor data in JSON format

### CSV Format
- **Files**: Multiple CSV files for different data types
  - `vendors.csv` - Main vendor information
  - `services.csv` - Services offered by vendors
  - `products.csv` - Products with pricing
  - `technology_stack.csv` - Technologies used
  - `industries.csv` - Industry focus areas
- **Use**: Excel import, data analysis tools

### SQL Format
- **File**: `database_exports/vendors_database.sql`
- **Use**: Direct database import (MySQL, PostgreSQL, etc.)
- **Structure**: Complete SQL schema with INSERT statements

## 🗄️ Database Schema

### Main Tables

#### vendors
- `vendor_id` - Unique identifier
- `company_name` - Full company name
- `website` - Company website URL
- `domain` - Website domain
- `description` - Company description
- `contact_email` - Primary email contact
- `contact_phone` - Primary phone contact
- `total_pages_scraped` - Number of pages scraped
- `scraped_at` - When data was scraped
- `last_updated` - When record was last updated

#### services
- `vendor_id` - Foreign key to vendors
- `service_name` - Name of the service

#### products
- `vendor_id` - Foreign key to vendors
- `product_name` - Name of the product
- `product_url` - URL to product page
- `description` - Product description
- `pricing` - Pricing information

#### technology_stack
- `vendor_id` - Foreign key to vendors
- `technology` - Technology name

#### industries
- `vendor_id` - Foreign key to vendors
- `industry` - Industry name

## 📈 Example Queries

### Find All Cybersecurity Vendors
```sql
SELECT v.company_name, v.website, s.service_name
FROM vendors v
JOIN services s ON v.vendor_id = s.vendor_id
WHERE s.service_name LIKE '%cybersecurity%';
```

### Find Vendors with Specific Technology
```sql
SELECT v.company_name, v.website, t.technology
FROM vendors v
JOIN technology_stack t ON v.vendor_id = t.vendor_id
WHERE t.technology = 'AWS';
```

### Find Vendors by Industry
```sql
SELECT v.company_name, v.website, i.industry
FROM vendors v
JOIN industries i ON v.vendor_id = i.vendor_id
WHERE i.industry = 'Healthcare';
```

### Find Vendors with Pricing Information
```sql
SELECT v.company_name, p.product_name, p.pricing
FROM vendors v
JOIN products p ON v.vendor_id = p.vendor_id
WHERE p.pricing IS NOT NULL AND p.pricing != '';
```

## 🔧 Usage Examples

### Scrape Multiple Vendors
```bash
# Scrape individual vendors
python improved_vendor_scraper.py https://vendor1.com
python improved_vendor_scraper.py https://vendor2.com
python improved_vendor_scraper.py https://vendor3.com

# Extract all vendor data
python vendor_database_extractor.py

# Convert to database formats
python markdown_to_database.py
```

### Import into Database
```bash
# MySQL
mysql -u username -p database_name < database_exports/vendors_database.sql

# PostgreSQL
psql -U username -d database_name -f database_exports/vendors_database.sql
```

## 📋 Data Fields Extracted

### Basic Information
- Company name and website
- Domain and description
- Contact information (email, phone)
- Website title and metadata

### Services & Products
- Complete list of services offered
- Product catalog with descriptions
- Pricing information when available
- Product URLs for reference

### Technical Information
- Technology stack used
- Industry focus areas
- Geographic presence
- Compliance and certifications

### Metadata
- Scraping timestamps
- Number of pages processed
- Data quality indicators

## 🎯 Use Cases

### Vendor Research
- Compare vendors by services and pricing
- Identify technology partnerships
- Analyze market presence

### Procurement
- Find vendors by specific requirements
- Compare pricing and features
- Identify industry specialists

### Market Analysis
- Track technology trends
- Analyze service offerings
- Monitor competitive landscape

### Lead Generation
- Find vendors by industry focus
- Identify contact information
- Track vendor capabilities

## 🔍 Data Quality

The system ensures high-quality data through:
- **Comprehensive Scraping** - Multiple pages per vendor
- **Structured Extraction** - Consistent data format
- **Validation** - Data quality checks
- **Metadata Tracking** - Source and timestamp information

## 📊 Sample Data

### Vendor Example
```
Company: Arctic Wolf | We Make Security Work
Website: https://arcticwolf.com
Services: Cybersecurity, Cloud Security, Incident Response
Products: 20+ security products and services
Technology: AWS, Azure, Go, React
Industries: Healthcare, Financial, Government
Contact: pr@arcticwolf.com
```

## 🚀 Next Steps

1. **Import Data** - Load CSV/SQL files into your database
2. **Create Indexes** - Optimize for common queries
3. **Build API** - Create REST API for data access
4. **Dashboard** - Build visualization dashboard
5. **Automation** - Schedule regular vendor updates

## 📝 Notes

- All data is extracted from publicly available websites
- Pricing information is extracted when available
- Contact information is validated during extraction
- Data is updated with timestamps for tracking
- System handles multiple languages and regions

---

**Built for comprehensive vendor research and database storage.**
