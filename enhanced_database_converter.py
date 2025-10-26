"""
Enhanced Database Converter - Converts enhanced vendor markdown files to comprehensive database formats
"""

import json
import csv
import os
import re
from pathlib import Path
from datetime import datetime

class EnhancedDatabaseConverter:
    """Converts enhanced vendor markdown files to comprehensive database formats."""
    
    def __init__(self, vendor_database_dir="vendor_database"):
        self.vendor_database_dir = Path(vendor_database_dir)
        self.output_dir = Path("database_exports")
        self.output_dir.mkdir(exist_ok=True)
    
    def convert_all_formats(self):
        """Convert all enhanced vendor markdown files to comprehensive database formats."""
        print("Converting enhanced vendor markdown files to database formats...")
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
            vendor_data = self._parse_enhanced_markdown_file(vendor_file)
            if vendor_data:
                vendors_data.append(vendor_data)
        
        # Save as JSON
        json_file = self.output_dir / "enhanced_vendors_database.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(vendors_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Saved JSON: {json_file.name}")
    
    def _convert_to_csv(self, vendor_files):
        """Convert markdown files to comprehensive CSV format."""
        print("\nConverting to CSV format...")
        
        # Main vendors CSV
        vendors_csv = self.output_dir / "vendors.csv"
        services_csv = self.output_dir / "services.csv"
        products_csv = self.output_dir / "products.csv"
        service_features_csv = self.output_dir / "service_features.csv"
        service_benefits_csv = self.output_dir / "service_benefits.csv"
        service_use_cases_csv = self.output_dir / "service_use_cases.csv"
        product_features_csv = self.output_dir / "product_features.csv"
        product_benefits_csv = self.output_dir / "product_benefits.csv"
        product_use_cases_csv = self.output_dir / "product_use_cases.csv"
        tech_stack_csv = self.output_dir / "technology_stack.csv"
        industries_csv = self.output_dir / "industries.csv"
        features_csv = self.output_dir / "general_features.csv"
        benefits_csv = self.output_dir / "general_benefits.csv"
        use_cases_csv = self.output_dir / "general_use_cases.csv"
        integrations_csv = self.output_dir / "integrations.csv"
        certifications_csv = self.output_dir / "certifications.csv"
        
        # Main vendors table
        with open(vendors_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'vendor_id', 'company_name', 'website', 'domain', 
                'description', 'title', 'contact_email', 'contact_phone',
                'total_pages_scraped', 'scraped_at', 'last_updated'
            ])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
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
        
        # Services table
        with open(services_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'vendor_id', 'service_name', 'category', 'description', 
                'url', 'pricing'
            ])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for service in vendor_data['services']:
                        writer.writerow([
                            vendor_data['vendor_id'],
                            service['name'],
                            service['category'],
                            service['description'],
                            service['url'],
                            service['pricing']
                        ])
        
        # Products table
        with open(products_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'vendor_id', 'product_name', 'category', 'description', 
                'url', 'pricing', 'target_audience', 'requirements', 
                'deployment', 'support'
            ])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for product in vendor_data['products']:
                        writer.writerow([
                            vendor_data['vendor_id'],
                            product['name'],
                            product['category'],
                            product['description'],
                            product['url'],
                            product['pricing'],
                            product['target_audience'],
                            product['requirements'],
                            product['deployment'],
                            product['support']
                        ])
        
        # Service features table
        with open(service_features_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'service_name', 'feature'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for service in vendor_data['services']:
                        for feature in service['features']:
                            writer.writerow([
                                vendor_data['vendor_id'],
                                service['name'],
                                feature
                            ])
        
        # Service benefits table
        with open(service_benefits_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'service_name', 'benefit'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for service in vendor_data['services']:
                        for benefit in service['benefits']:
                            writer.writerow([
                                vendor_data['vendor_id'],
                                service['name'],
                                benefit
                            ])
        
        # Service use cases table
        with open(service_use_cases_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'service_name', 'use_case'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for service in vendor_data['services']:
                        for use_case in service['use_cases']:
                            writer.writerow([
                                vendor_data['vendor_id'],
                                service['name'],
                                use_case
                            ])
        
        # Product features table
        with open(product_features_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'product_name', 'feature'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for product in vendor_data['products']:
                        for feature in product['features']:
                            writer.writerow([
                                vendor_data['vendor_id'],
                                product['name'],
                                feature
                            ])
        
        # Product benefits table
        with open(product_benefits_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'product_name', 'benefit'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for product in vendor_data['products']:
                        for benefit in product['benefits']:
                            writer.writerow([
                                vendor_data['vendor_id'],
                                product['name'],
                                benefit
                            ])
        
        # Product use cases table
        with open(product_use_cases_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'product_name', 'use_case'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for product in vendor_data['products']:
                        for use_case in product['use_cases']:
                            writer.writerow([
                                vendor_data['vendor_id'],
                                product['name'],
                                use_case
                            ])
        
        # Technology stack table
        with open(tech_stack_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'technology'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for tech in vendor_data['technology_stack']:
                        writer.writerow([vendor_data['vendor_id'], tech])
        
        # Industries table
        with open(industries_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'industry'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for industry in vendor_data['industry_focus']:
                        writer.writerow([vendor_data['vendor_id'], industry])
        
        # General features table
        with open(features_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'feature'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for feature in vendor_data['features']:
                        writer.writerow([vendor_data['vendor_id'], feature])
        
        # General benefits table
        with open(benefits_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'benefit'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for benefit in vendor_data['benefits']:
                        writer.writerow([vendor_data['vendor_id'], benefit])
        
        # General use cases table
        with open(use_cases_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'use_case'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for use_case in vendor_data['use_cases']:
                        writer.writerow([vendor_data['vendor_id'], use_case])
        
        # Integrations table
        with open(integrations_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'integration'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for integration in vendor_data['integrations']:
                        writer.writerow([vendor_data['vendor_id'], integration])
        
        # Certifications table
        with open(certifications_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vendor_id', 'certification'])
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    for cert in vendor_data['certifications']:
                        writer.writerow([vendor_data['vendor_id'], cert])
        
        print(f"  ✓ Saved CSV files:")
        print(f"    - {vendors_csv.name}")
        print(f"    - {services_csv.name}")
        print(f"    - {products_csv.name}")
        print(f"    - {service_features_csv.name}")
        print(f"    - {service_benefits_csv.name}")
        print(f"    - {service_use_cases_csv.name}")
        print(f"    - {product_features_csv.name}")
        print(f"    - {product_benefits_csv.name}")
        print(f"    - {product_use_cases_csv.name}")
        print(f"    - {tech_stack_csv.name}")
        print(f"    - {industries_csv.name}")
        print(f"    - {features_csv.name}")
        print(f"    - {benefits_csv.name}")
        print(f"    - {use_cases_csv.name}")
        print(f"    - {integrations_csv.name}")
        print(f"    - {certifications_csv.name}")
    
    def _convert_to_sql(self, vendor_files):
        """Convert markdown files to comprehensive SQL format."""
        print("\nConverting to SQL format...")
        
        sql_file = self.output_dir / "enhanced_vendors_database.sql"
        
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("-- Enhanced Vendor Database SQL Import Script\n")
            f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Create tables
            f.write(self._generate_enhanced_create_tables_sql())
            f.write("\n")
            
            # Insert data
            f.write("-- Insert vendor data\n")
            
            for vendor_file in vendor_files:
                vendor_data = self._parse_enhanced_markdown_file(vendor_file)
                if vendor_data:
                    f.write(self._generate_enhanced_insert_sql(vendor_data))
        
        print(f"  ✓ Saved SQL: {sql_file.name}")
    
    def _generate_enhanced_create_tables_sql(self):
        """Generate enhanced SQL CREATE TABLE statements."""
        return """
-- Create enhanced tables
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
    category VARCHAR(100),
    description TEXT,
    url VARCHAR(255),
    pricing VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    url VARCHAR(255),
    pricing VARCHAR(100),
    target_audience TEXT,
    requirements TEXT,
    deployment TEXT,
    support TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS service_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    feature TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS service_benefits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    benefit TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS service_use_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    use_case TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS product_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    feature TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS product_benefits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    benefit TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS product_use_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    use_case TEXT,
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

CREATE TABLE IF NOT EXISTS general_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    feature TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS general_benefits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    benefit TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS general_use_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    use_case TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS integrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    integration TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS certifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    certification TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);
"""
    
    def _generate_enhanced_insert_sql(self, vendor_data):
        """Generate enhanced SQL INSERT statements for a vendor."""
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
            sql += f"INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('{vendor_data['vendor_id']}', '{service['name'].replace("'", "''")}', '{service['category']}', '{service['description'].replace("'", "''")}', '{service['url']}', '{service['pricing'] or ''}');\n"
            
            # Insert service features
            for feature in service['features']:
                sql += f"INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('{vendor_data['vendor_id']}', '{service['name'].replace("'", "''")}', '{feature.replace("'", "''")}');\n"
            
            # Insert service benefits
            for benefit in service['benefits']:
                sql += f"INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('{vendor_data['vendor_id']}', '{service['name'].replace("'", "''")}', '{benefit.replace("'", "''")}');\n"
            
            # Insert service use cases
            for use_case in service['use_cases']:
                sql += f"INSERT INTO service_use_cases (vendor_id, service_name, use_case) VALUES ('{vendor_data['vendor_id']}', '{service['name'].replace("'", "''")}', '{use_case.replace("'", "''")}');\n"
        
        # Insert products
        for product in vendor_data['products']:
            sql += f"INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('{vendor_data['vendor_id']}', '{product['name'].replace("'", "''")}', '{product['category']}', '{product['description'].replace("'", "''")}', '{product['url']}', '{product['pricing'] or ''}', '{product['target_audience'].replace("'", "''")}', '{product['requirements'].replace("'", "''")}', '{product['deployment'].replace("'", "''")}', '{product['support'].replace("'", "''")}');\n"
            
            # Insert product features
            for feature in product['features']:
                sql += f"INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('{vendor_data['vendor_id']}', '{product['name'].replace("'", "''")}', '{feature.replace("'", "''")}');\n"
            
            # Insert product benefits
            for benefit in product['benefits']:
                sql += f"INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('{vendor_data['vendor_id']}', '{product['name'].replace("'", "''")}', '{benefit.replace("'", "''")}');\n"
            
            # Insert product use cases
            for use_case in product['use_cases']:
                sql += f"INSERT INTO product_use_cases (vendor_id, product_name, use_case) VALUES ('{vendor_data['vendor_id']}', '{product['name'].replace("'", "''")}', '{use_case.replace("'", "''")}');\n"
        
        # Insert technology stack
        for tech in vendor_data['technology_stack']:
            sql += f"INSERT INTO technology_stack (vendor_id, technology) VALUES ('{vendor_data['vendor_id']}', '{tech.replace("'", "''")}');\n"
        
        # Insert industries
        for industry in vendor_data['industry_focus']:
            sql += f"INSERT INTO industries (vendor_id, industry) VALUES ('{vendor_data['vendor_id']}', '{industry.replace("'", "''")}');\n"
        
        # Insert general features
        for feature in vendor_data['features']:
            sql += f"INSERT INTO general_features (vendor_id, feature) VALUES ('{vendor_data['vendor_id']}', '{feature.replace("'", "''")}');\n"
        
        # Insert general benefits
        for benefit in vendor_data['benefits']:
            sql += f"INSERT INTO general_benefits (vendor_id, benefit) VALUES ('{vendor_data['vendor_id']}', '{benefit.replace("'", "''")}');\n"
        
        # Insert general use cases
        for use_case in vendor_data['use_cases']:
            sql += f"INSERT INTO general_use_cases (vendor_id, use_case) VALUES ('{vendor_data['vendor_id']}', '{use_case.replace("'", "''")}');\n"
        
        # Insert integrations
        for integration in vendor_data['integrations']:
            sql += f"INSERT INTO integrations (vendor_id, integration) VALUES ('{vendor_data['vendor_id']}', '{integration.replace("'", "''")}');\n"
        
        # Insert certifications
        for cert in vendor_data['certifications']:
            sql += f"INSERT INTO certifications (vendor_id, certification) VALUES ('{vendor_data['vendor_id']}', '{cert.replace("'", "''")}');\n"
        
        sql += "\n"
        return sql
    
    def _parse_enhanced_markdown_file(self, file_path):
        """Parse an enhanced vendor markdown file and extract structured data."""
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
            services = self._extract_enhanced_services(content)
            
            # Extract products
            products = self._extract_enhanced_products(content)
            
            # Extract technology stack
            technology_stack = self._extract_list_items(content, 'Technology Stack')
            
            # Extract industry focus
            industry_focus = self._extract_list_items(content, 'Industry Focus')
            
            # Extract general features
            features = self._extract_list_items(content, 'General Features')
            
            # Extract general benefits
            benefits = self._extract_list_items(content, 'General Benefits')
            
            # Extract general use cases
            use_cases = self._extract_list_items(content, 'General Use Cases')
            
            # Extract integrations
            integrations = self._extract_list_items(content, 'Integrations')
            
            # Extract certifications
            certifications = self._extract_list_items(content, 'Certifications')
            
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
                'features': features,
                'benefits': benefits,
                'use_cases': use_cases,
                'integrations': integrations,
                'certifications': certifications,
                'total_pages_scraped': int(total_pages_scraped) if total_pages_scraped.isdigit() else 0,
                'scraped_at': scraped_at,
                'last_updated': last_updated
            }
            
        except Exception as e:
            print(f"  Error parsing {file_path.name}: {e}")
            return None
    
    def _extract_enhanced_services(self, content):
        """Extract enhanced service information from content."""
        services = []
        
        # Find services section
        section_pattern = r'## Services Offered\n(.*?)(?=\n## |\n---|\Z)'
        section_match = re.search(section_pattern, content, re.DOTALL)
        
        if not section_match:
            return services
        
        section_content = section_match.group(1)
        
        # Extract individual services
        service_pattern = r'### \d+\. (.+?)\n- \*\*Category\*\*: (.+?)\n- \*\*URL\*\*: (.+?)\n- \*\*Description\*\*: (.+?)(?:\n- \*\*Pricing\*\*: (.+?))?'
        matches = re.findall(service_pattern, section_content, re.DOTALL)
        
        for match in matches:
            service_name = match[0].strip()
            category = match[1].strip()
            url = match[2].strip()
            description = match[3].strip()
            pricing = match[4].strip() if match[4] else None
            
            # Extract features, benefits, and use cases for this service
            features = self._extract_service_section_items(section_content, service_name, 'Features')
            benefits = self._extract_service_section_items(section_content, service_name, 'Benefits')
            use_cases = self._extract_service_section_items(section_content, service_name, 'Use Cases')
            
            services.append({
                'name': service_name,
                'category': category,
                'description': description,
                'url': url,
                'pricing': pricing,
                'features': features,
                'benefits': benefits,
                'use_cases': use_cases
            })
        
        return services
    
    def _extract_enhanced_products(self, content):
        """Extract enhanced product information from content."""
        products = []
        
        # Find products section
        section_pattern = r'## Products\n(.*?)(?=\n## |\n---|\Z)'
        section_match = re.search(section_pattern, content, re.DOTALL)
        
        if not section_match:
            return products
        
        section_content = section_match.group(1)
        
        # Extract individual products
        product_pattern = r'### \d+\. (.+?)\n- \*\*Category\*\*: (.+?)\n- \*\*URL\*\*: (.+?)\n- \*\*Description\*\*: (.+?)(?:\n- \*\*Pricing\*\*: (.+?))?'
        matches = re.findall(product_pattern, section_content, re.DOTALL)
        
        for match in matches:
            product_name = match[0].strip()
            category = match[1].strip()
            url = match[2].strip()
            description = match[3].strip()
            pricing = match[4].strip() if match[4] else None
            
            # Extract additional product information
            target_audience = self._extract_product_field(section_content, product_name, 'Target Audience')
            requirements = self._extract_product_field(section_content, product_name, 'Requirements')
            deployment = self._extract_product_field(section_content, product_name, 'Deployment')
            support = self._extract_product_field(section_content, product_name, 'Support')
            
            # Extract features, benefits, and use cases for this product
            features = self._extract_product_section_items(section_content, product_name, 'Features')
            benefits = self._extract_product_section_items(section_content, product_name, 'Benefits')
            use_cases = self._extract_product_section_items(section_content, product_name, 'Use Cases')
            
            products.append({
                'name': product_name,
                'category': category,
                'description': description,
                'url': url,
                'pricing': pricing,
                'target_audience': target_audience,
                'requirements': requirements,
                'deployment': deployment,
                'support': support,
                'features': features,
                'benefits': benefits,
                'use_cases': use_cases
            })
        
        return products
    
    def _extract_service_section_items(self, content, service_name, item_type):
        """Extract items (features, benefits, use cases) for a specific service."""
        items = []
        
        # Find the service section
        service_pattern = rf'### \d+\. {re.escape(service_name)}.*?(?=’### \d+\. |\Z)'
        service_match = re.search(service_pattern, content, re.DOTALL)
        
        if not service_match:
            return items
        
        service_content = service_match.group(0)
        
        # Extract items
        item_pattern = rf'- \*\*{item_type}\*\*:\n(.*?)(?=\n- \*\*|\n### |\Z)'
        item_match = re.search(item_pattern, service_content, re.DOTALL)
        
        if item_match:
            items_text = item_match.group(1)
            item_lines = items_text.split('\n')
            for line in item_lines:
                line = line.strip()
                if line.startswith('- '):
                    item = line[2:].strip()
                    if item:
                        items.append(item)
        
        return items
    
    def _extract_product_section_items(self, content, product_name, item_type):
        """Extract items (features, benefits, use cases) for a specific product."""
        items = []
        
        # Find the product section
        product_pattern = rf'### \d+\. {re.escape(product_name)}.*?(?=’### \d+\. |\Z)'
        product_match = re.search(product_pattern, content, re.DOTALL)
        
        if not product_match:
            return items
        
        product_content = product_match.group(0)
        
        # Extract items
        item_pattern = rf'- \*\*{item_type}\*\*:\n(.*?)(?=\n- \*\*|\n### |\Z)'
        item_match = re.search(item_pattern, product_content, re.DOTALL)
        
        if item_match:
            items_text = item_match.group(1)
            item_lines = items_text.split('\n')
            for line in item_lines:
                line = line.strip()
                if line.startswith('- '):
                    item = line[2:].strip()
                    if item:
                        items.append(item)
        
        return items
    
    def _extract_product_field(self, content, product_name, field_name):
        """Extract a specific field for a product."""
        # Find the product section
        product_pattern = rf'### \d+\. {re.escape(product_name)}.*?(?=’### \d+\. |\Z)'
        product_match = re.search(product_pattern, content, re.DOTALL)
        
        if not product_match:
            return ''
        
        product_content = product_match.group(0)
        
        # Extract field
        field_pattern = rf'- \*\*{field_name}\*\*: (.+?)(?=\n- \*\*|\n### |\Z)'
        field_match = re.search(field_pattern, product_content, re.DOTALL)
        
        if field_match:
            return field_match.group(1).strip()
        
        return ''
    
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

def main():
    """Main function to convert enhanced markdown files to database formats."""
    converter = EnhancedDatabaseConverter()
    converter.convert_all_formats()

if __name__ == "__main__":
    main()
