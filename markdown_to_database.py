"""
Markdown to Database Converter - Converts vendor markdown files to database-ready formats
"""

import json
import csv
import os
import re
from pathlib import Path
from datetime import datetime

class MarkdownToDatabaseConverter:
    """Converts vendor markdown files to various database formats."""
    
    def __init__(self, vendor_database_dir="vendor_database"):
        self.vendor_database_dir = Path(vendor_database_dir)
        self.output_dir = Path("database_exports")
        self.output_dir.mkdir(exist_ok=True)
    
    def convert_all_formats(self):
        """Convert all vendor markdown files to multiple database formats."""
        print("Converting vendor markdown files to database formats...")
        print("=" * 60)
        
        # Get all vendor markdown files
        vendor_files = [f for f in self.vendor_database_dir.glob("*.md") 
                       if not f.name.startswith("master_") and not f.name.startswith("database_")]
        
        print(f"Found {len(vendor_files)} vendor files to convert")
        
        # Convert to JSON
        self._convert_to_json(vendor_files)
        
        # Convert to CSV
        self._convert_to_csv(vendor_files)
        
        # Convert to SQL
        self._convert_to_sql(vendor_files)
        
        print(f"\n✓ Conversion completed! Files saved to: {self.output_dir}")
    
    def _convert_to_json(self, vendor_files):
        """Convert markdown files to JSON format."""
        print("\nConverting to JSON format...")
        
        vendors_data = []
        
        for vendor_file in vendor_files:
            vendor_data = self._parse_markdown_file(vendor_file)
            if vendor_data:
                vendors_data.append(vendor_data)
        
        # Save as JSON
        json_file = self.output_dir / "vendors_database.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(vendors_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Saved JSON: {json_file.name}")
    
    def _convert_to_csv(self, vendor_files):
        """Convert markdown files to CSV format."""
        print("\nConverting to CSV format...")
        
        # Main vendors CSV
        vendors_csv = self.output_dir / "vendors.csv"
        services_csv = self.output_dir / "services.csv"
        products_csv = self.output_dir / "products.csv"
        tech_stack_csv = self.output_dir / "technology_stack.csv"
        industries_csv = self.output_dir / "industries.csv"
        
        with open(vendors_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'vendor_id', 'company_name', 'website', 'domain', 
                'description', 'title', 'contact_email', 'contact_phone',
                'total_pages_scraped', 'scraped_at', 'last_updated'
            ])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_markdown_file(vendor_file)
                if vendor_data:
                    writer.writerow([
                        vendor_data['vendor_id'],
                        vendor_data['company_name'],
                        vendor_data['website'],
                        vendor_data['domain'],
                        vendor_data['description'],
                        vendor_data['title'],
                        vendor_data['contact_info'].get('email', ''),
                        vendor_data['contact_info'].get('phone', ''),
                        vendor_data['total_pages_scraped'],
                        vendor_data['scraped_at'],
                        vendor_data['last_updated']
                    ])
        
        # Services CSV
        with open(services_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'service_name'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_markdown_file(vendor_file)
                if vendor_data:
                    for service in vendor_data['services']:
                        writer.writerow([vendor_data['vendor_id'], service])
        
        # Products CSV
        with open(products_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'product_name', 'product_url', 'description', 'pricing'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_markdown_file(vendor_file)
                if vendor_data:
                    for product in vendor_data['products']:
                        writer.writerow([
                            vendor_data['vendor_id'],
                            product['name'],
                            product['url'],
                            product['description'],
                            product['pricing']
                        ])
        
        # Technology Stack CSV
        with open(tech_stack_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'technology'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_markdown_file(vendor_file)
                if vendor_data:
                    for tech in vendor_data['technology_stack']:
                        writer.writerow([vendor_data['vendor_id'], tech])
        
        # Industries CSV
        with open(industries_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'industry'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_markdown_file(vendor_file)
                if vendor_data:
                    for industry in vendor_data['industry_focus']:
                        writer.writerow([vendor_data['vendor_id'], industry])
        
        print(f"  ✓ Saved CSV files:")
        print(f"    - {vendors_csv.name}")
        print(f"    - {services_csv.name}")
        print(f"    - {products_csv.name}")
        print(f"    - {tech_stack_csv.name}")
        print(f"    - {industries_csv.name}")
    
    def _convert_to_sql(self, vendor_files):
        """Convert markdown files to SQL format."""
        print("\nConverting to SQL format...")
        
        sql_file = self.output_dir / "vendors_database.sql"
        
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("-- Vendor Database SQL Import Script\n")
            f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Create tables
            f.write(self._generate_create_tables_sql())
            f.write("\n")
            
            # Insert data
            f.write("-- Insert vendor data\n")
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_markdown_file(vendor_file)
                if vendor_data:
                    f.write(self._generate_insert_sql(vendor_data))
        
        print(f"  ✓ Saved SQL: {sql_file.name}")
    
    def _generate_create_tables_sql(self):
        """Generate SQL CREATE TABLE statements."""
        return """
-- Create tables
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    website VARCHAR(255),
    domain VARCHAR(255),
    description TEXT,
    title VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(255),
    total_pages_scraped INT DEFAULT 0,
    scraped_at DATETIME,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    product_url VARCHAR(255),
    description TEXT,
    pricing VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS technology_stack (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    technology VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS industries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    industry VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS geographic_presence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    country VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);
"""
    
    def _generate_insert_sql(self, vendor_data):
        """Generate SQL INSERT statements for a vendor."""
        sql = f"""
-- Insert vendor: {vendor_data['company_name']}
INSERT INTO vendors (vendor_id, company_name, website, domain, description, title, contact_email, contact_phone, total_pages_scraped, scraped_at, last_updated) VALUES (
    '{vendor_data['vendor_id']}',
    '{vendor_data['company_name'].replace("'", "''")}',
    '{vendor_data['website']}',
    '{vendor_data['domain']}',
    '{vendor_data['description'].replace("'", "''")}',
    '{vendor_data['title'].replace("'", "''")}',
    '{vendor_data['contact_info'].get('email', '')}',
    '{vendor_data['contact_info'].get('phone', '')}',
    {vendor_data['total_pages_scraped']},
    '{vendor_data['scraped_at']}',
    '{vendor_data['last_updated']}'
);

"""
        
        # Insert services
        for service in vendor_data['services']:
            sql += f"INSERT INTO services (vendor_id, service_name) VALUES ('{vendor_data['vendor_id']}', '{service.replace("'", "''")}');\n"
        
        # Insert products
        for product in vendor_data['products']:
            sql += f"INSERT INTO products (vendor_id, product_name, product_url, description, pricing) VALUES ('{vendor_data['vendor_id']}', '{product['name'].replace("'", "''")}', '{product['url']}', '{product['description'].replace("'", "''")}', '{product['pricing'] or ''}');\n"
        
        # Insert technology stack
        for tech in vendor_data['technology_stack']:
            sql += f"INSERT INTO technology_stack (vendor_id, technology) VALUES ('{vendor_data['vendor_id']}', '{tech.replace("'", "''")}');\n"
        
        # Insert industries
        for industry in vendor_data['industry_focus']:
            sql += f"INSERT INTO industries (vendor_id, industry) VALUES ('{vendor_data['vendor_id']}', '{industry.replace("'", "''")}');\n"
        
        sql += "\n"
        return sql
    
    def _parse_markdown_file(self, file_path):
        """Parse a vendor markdown file and extract structured data."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic information
            vendor_id = self._extract_field(content, 'Vendor ID')
            company_name = self._extract_field(content, 'Company Name')
            website = self._extract_field(content, 'Website')
            domain = self._extract_field(content, 'Domain')
            description = self._extract_field(content, 'Description')
            title = self._extract_field(content, 'Title')
            
            # Extract contact information
            contact_email = self._extract_field(content, 'Email')
            contact_phone = self._extract_field(content, 'Phone')
            
            # Extract services
            services = self._extract_list_items(content, 'Services Offered')
            
            # Extract products
            products = self._extract_products(content)
            
            # Extract technology stack
            technology_stack = self._extract_list_items(content, 'Technology Stack')
            
            # Extract industry focus
            industry_focus = self._extract_list_items(content, 'Industry Focus')
            
            # Extract geographic presence
            geographic_presence = self._extract_list_items(content, 'Geographic Presence')
            
            # Extract metadata
            total_pages_scraped = self._extract_field(content, 'Total Pages Scraped')
            scraped_at = self._extract_field(content, 'Scraped At')
            last_updated = self._extract_field(content, 'Last Updated')
            
            return {
                'vendor_id': vendor_id,
                'company_name': company_name,
                'website': website,
                'domain': domain,
                'description': description,
                'title': title,
                'contact_info': {
                    'email': contact_email,
                    'phone': contact_phone
                },
                'services': services,
                'products': products,
                'technology_stack': technology_stack,
                'industry_focus': industry_focus,
                'geographic_presence': geographic_presence,
                'total_pages_scraped': int(total_pages_scraped) if total_pages_scraped.isdigit() else 0,
                'scraped_at': scraped_at,
                'last_updated': last_updated
            }
            
        except Exception as e:
            print(f"  Error parsing {file_path.name}: {e}")
            return None
    
    def _extract_field(self, content, field_name):
        """Extract a field value from markdown content."""
        pattern = rf'- \*\*{field_name}\*\*: (.+)'
        match = re.search(pattern, content)
        return match.group(1).strip() if match else ''
    
    def _extract_list_items(self, content, section_name):
        """Extract list items from a section."""
        # Find the section
        section_pattern = rf'## {section_name}\n(.*?)(?=\n## |\n---|\Z)'
        section_match = re.search(section_pattern, content, re.DOTALL)
        
        if not section_match:
            return []
        
        section_content = section_match.group(1)
        
        # Extract list items
        items = []
        lines = section_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                item = line[2:].strip()
                if item:
                    items.append(item)
        
        return items
    
    def _extract_products(self, content):
        """Extract product information from content."""
        products = []
        
        # Find products section
        section_pattern = r'## Products\n(.*?)(?=\n## |\n---|\Z)'
        section_match = re.search(section_pattern, content, re.DOTALL)
        
        if not section_match:
            return products
        
        section_content = section_match.group(1)
        
        # Extract individual products
        product_pattern = r'### (.+?)\n- \*\*URL\*\*: (.+?)\n- \*\*Description\*\*: (.+?)(?:\n- \*\*Pricing\*\*: (.+?))?'
        matches = re.findall(product_pattern, section_content, re.DOTALL)
        
        for match in matches:
            product_name = match[0].strip()
            product_url = match[1].strip()
            description = match[2].strip()
            pricing = match[3].strip() if match[3] else None
            
            products.append({
                'name': product_name,
                'url': product_url,
                'description': description,
                'pricing': pricing
            })
        
        return products

def main():
    """Main function to convert markdown files to database formats."""
    converter = MarkdownToDatabaseConverter()
    converter.convert_all_formats()

if __name__ == "__main__":
    main()
