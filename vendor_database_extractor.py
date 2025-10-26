"""
Vendor Database Extractor - Extracts vendor information into structured markdown for database storage
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

class VendorDatabaseExtractor:
    """Extracts vendor information into database-ready markdown format."""
    
    def __init__(self, research_output_dir="research_output"):
        self.research_output_dir = Path(research_output_dir)
        self.database_output_dir = Path("vendor_database")
        self.database_output_dir.mkdir(exist_ok=True)
    
    def extract_all_vendors(self):
        """Extract information from all vendors in the research output directory."""
        vendor_dirs = [d for d in self.research_output_dir.iterdir() if d.is_dir()]
        
        print(f"Found {len(vendor_dirs)} vendor directories to process")
        
        all_vendor_data = []
        
        for vendor_dir in vendor_dirs:
            print(f"Processing: {vendor_dir.name}")
            vendor_data = self._extract_vendor_data(vendor_dir)
            if vendor_data:
                all_vendor_data.append(vendor_data)
                self._save_vendor_to_database(vendor_data)
        
        # Create master database file
        self._create_master_database(all_vendor_data)
        
        print(f"\n✓ Processed {len(all_vendor_data)} vendors")
        print(f"Database files saved to: {self.database_output_dir}")
        
        return all_vendor_data
    
    def _extract_vendor_data(self, vendor_dir):
        """Extract structured data from a vendor directory."""
        try:
            # Look for comprehensive vendor info file
            vendor_info_file = vendor_dir / "comprehensive_vendor_info.json"
            if not vendor_info_file.exists():
                vendor_info_file = vendor_dir / "vendor_info.json"
            
            if not vendor_info_file.exists():
                print(f"  Warning: No vendor info file found in {vendor_dir.name}")
                return None
            
            with open(vendor_info_file, 'r', encoding='utf-8') as f:
                vendor_data = json.load(f)
            
            # Extract structured information
            extracted_data = {
                'vendor_id': self._generate_vendor_id(vendor_data.get('name', '')),
                'company_name': vendor_data.get('name', ''),
                'website': vendor_data.get('url', ''),
                'domain': self._extract_domain(vendor_data.get('url', '')),
                'description': vendor_data.get('description', ''),
                'title': vendor_data.get('title', ''),
                'contact_info': vendor_data.get('contact_info', {}),
                'services': self._extract_services(vendor_data),
                'products': self._extract_products(vendor_data),
                'technology_stack': self._extract_technology_stack(vendor_data),
                'pricing_info': self._extract_pricing_info(vendor_data),
                'industry_focus': self._extract_industry_focus(vendor_data),
                'geographic_presence': self._extract_geographic_presence(vendor_data),
                'total_pages_scraped': vendor_data.get('total_pages_scraped', 0),
                'scraped_at': vendor_data.get('scraped_at', ''),
                'last_updated': datetime.now().isoformat()
            }
            
            return extracted_data
            
        except Exception as e:
            print(f"  Error processing {vendor_dir.name}: {e}")
            return None
    
    def _generate_vendor_id(self, company_name):
        """Generate a unique vendor ID from company name."""
        # Clean and normalize company name
        clean_name = re.sub(r'[^\w\s]', '', company_name.lower())
        clean_name = re.sub(r'\s+', '_', clean_name.strip())
        return clean_name[:50]  # Limit length
    
    def _extract_domain(self, url):
        """Extract domain from URL."""
        if url:
            parsed = urlparse(url)
            return parsed.netloc.replace('www.', '')
        return ''
    
    def _extract_services(self, vendor_data):
        """Extract and consolidate services from all pages."""
        all_services = set()
        
        # Get services from main vendor data
        if 'services' in vendor_data:
            all_services.update(vendor_data['services'])
        
        # Get services from individual pages
        for page in vendor_data.get('pages', []):
            if 'services' in page:
                all_services.update(page['services'])
        
        return list(all_services)
    
    def _extract_products(self, vendor_data):
        """Extract product information from vendor data."""
        products = []
        
        # Look for product-specific pages
        for page in vendor_data.get('pages', []):
            page_url = page.get('url', '')
            page_title = page.get('title', '')
            page_content = page.get('content', '')
            
            # Check if this is a product page
            if self._is_product_page(page_url, page_title):
                product_info = {
                    'name': self._extract_product_name(page_title, page_content),
                    'url': page_url,
                    'description': self._extract_product_description(page_content),
                    'pricing': self._extract_product_pricing(page_content)
                }
                products.append(product_info)
        
        return products
    
    def _is_product_page(self, url, title):
        """Determine if a page is a product page."""
        product_indicators = [
            '/product/', '/tuote/', '/solutions/', '/services/',
            'product', 'solution', 'service', 'course', 'kurssi'
        ]
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        return any(indicator in url_lower or indicator in title_lower 
                  for indicator in product_indicators)
    
    def _extract_product_name(self, title, content):
        """Extract product name from page title and content."""
        # Clean up title
        clean_title = re.sub(r'\s*-\s*.*$', '', title)
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        return clean_title.strip()
    
    def _extract_product_description(self, content):
        """Extract product description from content."""
        # Take first 200 characters as description
        if content:
            return content[:200].strip() + '...' if len(content) > 200 else content.strip()
        return ''
    
    def _extract_product_pricing(self, content):
        """Extract pricing information from content."""
        price_pattern = re.compile(r'[\$€£¥]\s*[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day))?', re.IGNORECASE)
        prices = price_pattern.findall(content)
        return prices[0] if prices else None
    
    def _extract_technology_stack(self, vendor_data):
        """Extract technology stack from vendor data."""
        all_tech = set()
        
        # Get tech stack from main vendor data
        if 'technology_stack' in vendor_data:
            all_tech.update(vendor_data['technology_stack'])
        
        # Get tech stack from individual pages
        for page in vendor_data.get('pages', []):
            if 'technology_stack' in page:
                all_tech.update(page['technology_stack'])
        
        return list(all_tech)
    
    def _extract_pricing_info(self, vendor_data):
        """Extract pricing information from vendor data."""
        pricing_info = []
        
        for page in vendor_data.get('pages', []):
            content = page.get('content', '')
            price_pattern = re.compile(r'[\$€£¥]\s*[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day))?', re.IGNORECASE)
            prices = price_pattern.findall(content)
            pricing_info.extend(prices)
        
        return list(set(pricing_info))  # Remove duplicates
    
    def _extract_industry_focus(self, vendor_data):
        """Extract industry focus from vendor data."""
        industry_keywords = [
            'healthcare', 'financial', 'government', 'legal', 'manufacturing',
            'education', 'retail', 'technology', 'energy', 'automotive'
        ]
        
        industries = []
        all_content = vendor_data.get('description', '') + ' ' + vendor_data.get('title', '')
        
        for page in vendor_data.get('pages', []):
            all_content += ' ' + page.get('content', '')
        
        content_lower = all_content.lower()
        
        for industry in industry_keywords:
            if industry in content_lower:
                industries.append(industry.title())
        
        return list(set(industries))
    
    def _extract_geographic_presence(self, vendor_data):
        """Extract geographic presence from vendor data."""
        geo_indicators = []
        
        # Look for language/region indicators in URLs
        for page in vendor_data.get('pages', []):
            url = page.get('url', '')
            if '/fi/' in url:
                geo_indicators.append('Finland')
            elif '/de/' in url:
                geo_indicators.append('Germany')
            elif '/fr/' in url:
                geo_indicators.append('France')
            elif '/es/' in url:
                geo_indicators.append('Spain')
            elif '/ja/' in url:
                geo_indicators.append('Japan')
        
        return list(set(geo_indicators))
    
    def _save_vendor_to_database(self, vendor_data):
        """Save individual vendor data to database markdown file."""
        vendor_id = vendor_data['vendor_id']
        
        # Create markdown content
        markdown_content = self._generate_vendor_markdown(vendor_data)
        
        # Save to file
        filename = f"{vendor_id}.md"
        filepath = self.database_output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  ✓ Saved: {filename}")
    
    def _generate_vendor_markdown(self, vendor_data):
        """Generate markdown content for vendor database entry."""
        md = f"""# {vendor_data['company_name']}

## Basic Information
- **Vendor ID**: {vendor_data['vendor_id']}
- **Company Name**: {vendor_data['company_name']}
- **Website**: {vendor_data['website']}
- **Domain**: {vendor_data['domain']}
- **Description**: {vendor_data['description']}
- **Title**: {vendor_data['title']}

## Contact Information
"""
        
        for key, value in vendor_data['contact_info'].items():
            md += f"- **{key.title()}**: {value}\n"
        
        if vendor_data['services']:
            md += "\n## Services Offered\n"
            for service in sorted(vendor_data['services']):
                md += f"- {service}\n"
        
        if vendor_data['products']:
            md += "\n## Products\n"
            for product in vendor_data['products']:
                md += f"### {product['name']}\n"
                md += f"- **URL**: {product['url']}\n"
                md += f"- **Description**: {product['description']}\n"
                if product['pricing']:
                    md += f"- **Pricing**: {product['pricing']}\n"
                md += "\n"
        
        if vendor_data['technology_stack']:
            md += "\n## Technology Stack\n"
            for tech in sorted(vendor_data['technology_stack']):
                md += f"- {tech}\n"
        
        if vendor_data['pricing_info']:
            md += "\n## Pricing Information\n"
            for price in vendor_data['pricing_info']:
                md += f"- {price}\n"
        
        if vendor_data['industry_focus']:
            md += "\n## Industry Focus\n"
            for industry in sorted(vendor_data['industry_focus']):
                md += f"- {industry}\n"
        
        if vendor_data['geographic_presence']:
            md += "\n## Geographic Presence\n"
            for geo in sorted(vendor_data['geographic_presence']):
                md += f"- {geo}\n"
        
        md += f"""
## Metadata
- **Total Pages Scraped**: {vendor_data['total_pages_scraped']}
- **Scraped At**: {vendor_data['scraped_at']}
- **Last Updated**: {vendor_data['last_updated']}

---
*Generated by Vendor Database Extractor*
"""
        
        return md
    
    def _create_master_database(self, all_vendor_data):
        """Create a master database file with all vendors."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        master_file = self.database_output_dir / f"master_database_{timestamp}.md"
        
        md = f"""# Master Vendor Database

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Vendors: {len(all_vendor_data)}

## Vendor Summary

"""
        
        for vendor in all_vendor_data:
            md += f"### {vendor['company_name']}\n"
            md += f"- **ID**: {vendor['vendor_id']}\n"
            md += f"- **Website**: {vendor['website']}\n"
            md += f"- **Services**: {', '.join(vendor['services'][:5]) if vendor['services'] else 'None'}\n"
            md += f"- **Products**: {len(vendor['products'])} products\n"
            md += f"- **Contact**: {vendor['contact_info'].get('email', 'N/A')}\n\n"
        
        md += "\n## Database Structure\n\n"
        md += "Each vendor has a separate markdown file with the following structure:\n"
        md += "- Basic Information (ID, Name, Website, Description)\n"
        md += "- Contact Information (Email, Phone, etc.)\n"
        md += "- Services Offered\n"
        md += "- Products (with pricing)\n"
        md += "- Technology Stack\n"
        md += "- Industry Focus\n"
        md += "- Geographic Presence\n"
        md += "- Metadata (scraping info)\n"
        
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"✓ Created master database: {master_file.name}")
    
    def create_database_schema(self):
        """Create a database schema file for reference."""
        schema_file = self.database_output_dir / "database_schema.md"
        
        schema = """# Vendor Database Schema

## Table: vendors

| Column | Type | Description |
|--------|------|-------------|
| vendor_id | VARCHAR(50) | Unique identifier for vendor |
| company_name | VARCHAR(255) | Full company name |
| website | VARCHAR(255) | Company website URL |
| domain | VARCHAR(255) | Website domain |
| description | TEXT | Company description |
| title | VARCHAR(255) | Website title |
| scraped_at | DATETIME | When data was scraped |
| last_updated | DATETIME | When record was last updated |

## Table: contact_info

| Column | Type | Description |
|--------|------|-------------|
| vendor_id | VARCHAR(50) | Foreign key to vendors table |
| contact_type | VARCHAR(50) | Type of contact (email, phone, etc.) |
| contact_value | VARCHAR(255) | Contact information value |

## Table: services

| Column | Type | Description |
|--------|------|-------------|
| vendor_id | VARCHAR(50) | Foreign key to vendors table |
| service_name | VARCHAR(255) | Name of the service |

## Table: products

| Column | Type | Description |
|--------|------|-------------|
| vendor_id | VARCHAR(50) | Foreign key to vendors table |
| product_name | VARCHAR(255) | Name of the product |
| product_url | VARCHAR(255) | URL to product page |
| description | TEXT | Product description |
| pricing | VARCHAR(100) | Pricing information |

## Table: technology_stack

| Column | Type | Description |
|--------|------|-------------|
| vendor_id | VARCHAR(50) | Foreign key to vendors table |
| technology | VARCHAR(100) | Technology name |

## Table: industry_focus

| Column | Type | Description |
|--------|------|-------------|
| vendor_id | VARCHAR(50) | Foreign key to vendors table |
| industry | VARCHAR(100) | Industry name |

## Table: geographic_presence

| Column | Type | Description |
|--------|------|-------------|
| vendor_id | VARCHAR(50) | Foreign key to vendors table |
| country | VARCHAR(100) | Country name |

---
*Schema generated by Vendor Database Extractor*
"""
        
        with open(schema_file, 'w', encoding='utf-8') as f:
            f.write(schema)
        
        print(f"✓ Created database schema: {schema_file.name}")

def main():
    """Main function to extract vendor data for database storage."""
    extractor = VendorDatabaseExtractor()
    
    print("Starting vendor database extraction...")
    print("=" * 50)
    
    # Extract all vendor data
    vendor_data = extractor.extract_all_vendors()
    
    # Create database schema
    extractor.create_database_schema()
    
    print("\n" + "=" * 50)
    print("Vendor database extraction completed!")
    print(f"Processed {len(vendor_data)} vendors")
    print(f"Database files saved to: vendor_database/")

if __name__ == "__main__":
    main()
