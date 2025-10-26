"""
Enhanced Product and Service Extractor - Extracts comprehensive information for each distinct product and service
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

class EnhancedProductServiceExtractor:
    """Extracts comprehensive product and service information from vendor data."""
    
    def __init__(self, research_output_dir="research_output"):
        self.research_output_dir = Path(research_output_dir)
        self.database_output_dir = Path("vendor_database")
        self.database_output_dir.mkdir(exist_ok=True)
    
    def extract_all_vendors(self):
        """Extract comprehensive product and service information from all vendors."""
        vendor_dirs = [d for d in self.research_output_dir.iterdir() if d.is_dir()]
        
        print(f"Found {len(vendor_dirs)} vendor directories to process")
        
        all_vendor_data = []
        
        for vendor_dir in vendor_dirs:
            print(f"Processing: {vendor_dir.name}")
            vendor_data = self._extract_comprehensive_vendor_data(vendor_dir)
            if vendor_data:
                all_vendor_data.append(vendor_data)
                self._save_vendor_to_database(vendor_data)
        
        # Create master database file
        self._create_master_database(all_vendor_data)
        
        print(f"\n✓ Processed {len(all_vendor_data)} vendors")
        print(f"Database files saved to: {self.database_output_dir}")
        
        return all_vendor_data
    
    def _extract_comprehensive_vendor_data(self, vendor_dir):
        """Extract comprehensive data from a vendor directory."""
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
            
            # Extract comprehensive vendor information
            extracted_data = {
                'vendor_id': self._generate_vendor_id(vendor_data.get('name', '')),
                'company_name': vendor_data.get('name', ''),
                'website': vendor_data.get('url', ''),
                'domain': self._extract_domain(vendor_data.get('url', '')),
                'description': vendor_data.get('description', ''),
                'title': vendor_data.get('title', ''),
                'contact_info': vendor_data.get('contact_info', {}),
                'services': self._extract_comprehensive_services(vendor_data),
                'products': self._extract_comprehensive_products(vendor_data),
                'technology_stack': self._extract_technology_stack(vendor_data),
                'pricing_info': self._extract_comprehensive_pricing(vendor_data),
                'industry_focus': self._extract_industry_focus(vendor_data),
                'geographic_presence': self._extract_geographic_presence(vendor_data),
                'features': self._extract_features(vendor_data),
                'benefits': self._extract_benefits(vendor_data),
                'use_cases': self._extract_use_cases(vendor_data),
                'integrations': self._extract_integrations(vendor_data),
                'certifications': self._extract_certifications(vendor_data),
                'total_pages_scraped': vendor_data.get('total_pages_scraped', 0),
                'scraped_at': vendor_data.get('scraped_at', ''),
                'last_updated': datetime.now().isoformat()
            }
            
            return extracted_data
            
        except Exception as e:
            print(f"  Error processing {vendor_dir.name}: {e}")
            return None
    
    def _extract_comprehensive_services(self, vendor_data):
        """Extract comprehensive service information."""
        services = []
        
        # Get services from main vendor data
        if 'services' in vendor_data:
            for service in vendor_data['services']:
                services.append({
                    'name': service,
                    'description': '',
                    'features': [],
                    'benefits': [],
                    'use_cases': [],
                    'pricing': None,
                    'url': vendor_data.get('url', ''),
                    'category': 'general'
                })
        
        # Extract detailed services from individual pages
        for page in vendor_data.get('pages', []):
            page_url = page.get('url', '')
            page_title = page.get('title', '')
            page_content = page.get('content', '')
            
            # Check if this is a service page
            if self._is_service_page(page_url, page_title):
                service_info = {
                    'name': self._extract_service_name(page_title, page_content),
                    'description': self._extract_service_description(page_content),
                    'features': self._extract_service_features(page_content),
                    'benefits': self._extract_service_benefits(page_content),
                    'use_cases': self._extract_service_use_cases(page_content),
                    'pricing': self._extract_service_pricing(page_content),
                    'url': page_url,
                    'category': self._extract_service_category(page_url, page_title)
                }
                services.append(service_info)
        
        # Remove duplicates and merge information
        return self._merge_duplicate_services(services)
    
    def _extract_comprehensive_products(self, vendor_data):
        """Extract comprehensive product information."""
        products = []
        
        # Extract detailed products from individual pages
        for page in vendor_data.get('pages', []):
            page_url = page.get('url', '')
            page_title = page.get('title', '')
            page_content = page.get('content', '')
            
            # Check if this is a product page
            if self._is_product_page(page_url, page_title):
                product_info = {
                    'name': self._extract_product_name(page_title, page_content),
                    'description': self._extract_product_description(page_content),
                    'features': self._extract_product_features(page_content),
                    'benefits': self._extract_product_benefits(page_content),
                    'use_cases': self._extract_product_use_cases(page_content),
                    'pricing': self._extract_product_pricing(page_content),
                    'url': page_url,
                    'category': self._extract_product_category(page_url, page_title),
                    'target_audience': self._extract_target_audience(page_content),
                    'requirements': self._extract_requirements(page_content),
                    'deployment': self._extract_deployment_info(page_content),
                    'support': self._extract_support_info(page_content)
                }
                products.append(product_info)
        
        return products
    
    def _is_service_page(self, url, title):
        """Determine if a page is a service page."""
        service_indicators = [
            '/services/', '/service/', '/solutions/', '/solutions-',
            'service', 'solutions', 'consulting', 'support', 'training',
            'implementation', 'migration', 'optimization', 'maintenance'
        ]
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        return any(indicator in url_lower or indicator in title_lower 
                  for indicator in service_indicators)
    
    def _is_product_page(self, url, title):
        """Determine if a page is a product page."""
        product_indicators = [
            '/product/', '/products/', '/tuote/', '/solutions/',
            'product', 'solution', 'platform', 'software', 'tool',
            'course', 'kurssi', 'bundle', 'package'
        ]
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        return any(indicator in url_lower or indicator in title_lower 
                  for indicator in product_indicators)
    
    def _extract_service_name(self, title, content):
        """Extract service name from page title and content."""
        # Clean up title
        clean_title = re.sub(r'\s*-\s*.*$', '', title)
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        return clean_title.strip()
    
    def _extract_service_description(self, content):
        """Extract service description from content."""
        # Look for description patterns
        desc_patterns = [
            r'([^.]{50,200}\.)',  # Sentences of 50-200 chars
            r'([A-Z][^.]{30,150}\.)'  # Capitalized sentences
        ]
        
        for pattern in desc_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].strip()
        
        # Fallback to first 200 characters
        return content[:200].strip() + '...' if len(content) > 200 else content.strip()
    
    def _extract_service_features(self, content):
        """Extract service features from content."""
        features = []
        
        # Look for feature indicators
        feature_patterns = [
            r'•\s*([^•\n]+)',
            r'-\s*([^-\n]+)',
            r'\*\s*([^*\n]+)',
            r'✓\s*([^✓\n]+)',
            r'Features?:\s*([^.\n]+)',
            r'Includes?:\s*([^.\n]+)'
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                feature = match.strip()
                if len(feature) > 10 and len(feature) < 200:
                    features.append(feature)
        
        return features[:10]  # Limit to top 10 features
    
    def _extract_service_benefits(self, content):
        """Extract service benefits from content."""
        benefits = []
        
        # Look for benefit indicators
        benefit_patterns = [
            r'Benefits?:\s*([^.\n]+)',
            r'Advantages?:\s*([^.\n]+)',
            r'Why choose[^?]*\?[^.]*\.([^.\n]+)',
            r'Improves?\s+([^.\n]+)',
            r'Reduces?\s+([^.\n]+)',
            r'Increases?\s+([^.\n]+)'
        ]
        
        for pattern in benefit_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                benefit = match.strip()
                if len(benefit) > 10 and len(benefit) < 200:
                    benefits.append(benefit)
        
        return benefits[:10]  # Limit to top 10 benefits
    
    def _extract_service_use_cases(self, content):
        """Extract service use cases from content."""
        use_cases = []
        
        # Look for use case indicators
        use_case_patterns = [
            r'Use cases?:\s*([^.\n]+)',
            r'Perfect for:\s*([^.\n]+)',
            r'Ideal for:\s*([^.\n]+)',
            r'Best suited for:\s*([^.\n]+)',
            r'Designed for:\s*([^.\n]+)'
        ]
        
        for pattern in use_case_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                use_case = match.strip()
                if len(use_case) > 10 and len(use_case) < 200:
                    use_cases.append(use_case)
        
        return use_cases[:10]  # Limit to top 10 use cases
    
    def _extract_service_pricing(self, content):
        """Extract service pricing from content."""
        price_pattern = re.compile(r'[\$€£¥]\s*[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day|user|seat))?', re.IGNORECASE)
        prices = price_pattern.findall(content)
        return prices[0] if prices else None
    
    def _extract_service_category(self, url, title):
        """Extract service category from URL and title."""
        url_lower = url.lower()
        title_lower = title.lower()
        
        if 'consulting' in url_lower or 'consulting' in title_lower:
            return 'consulting'
        elif 'training' in url_lower or 'training' in title_lower:
            return 'training'
        elif 'support' in url_lower or 'support' in title_lower:
            return 'support'
        elif 'implementation' in url_lower or 'implementation' in title_lower:
            return 'implementation'
        elif 'security' in url_lower or 'security' in title_lower:
            return 'security'
        elif 'cloud' in url_lower or 'cloud' in title_lower:
            return 'cloud'
        else:
            return 'general'
    
    def _extract_product_name(self, title, content):
        """Extract product name from page title and content."""
        # Clean up title
        clean_title = re.sub(r'\s*-\s*.*$', '', title)
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        return clean_title.strip()
    
    def _extract_product_description(self, content):
        """Extract product description from content."""
        # Look for description patterns
        desc_patterns = [
            r'([^.]{50,300}\.)',  # Sentences of 50-300 chars
            r'([A-Z][^.]{30,200}\.)'  # Capitalized sentences
        ]
        
        for pattern in desc_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].strip()
        
        # Fallback to first 300 characters
        return content[:300].strip() + '...' if len(content) > 300 else content.strip()
    
    def _extract_product_features(self, content):
        """Extract product features from content."""
        features = []
        
        # Look for feature indicators
        feature_patterns = [
            r'•\s*([^•\n]+)',
            r'-\s*([^-\n]+)',
            r'\*\s*([^*\n]+)',
            r'✓\s*([^✓\n]+)',
            r'Features?:\s*([^.\n]+)',
            r'Includes?:\s*([^.\n]+)',
            r'Capabilities?:\s*([^.\n]+)'
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                feature = match.strip()
                if len(feature) > 10 and len(feature) < 200:
                    features.append(feature)
        
        return features[:15]  # Limit to top 15 features
    
    def _extract_product_benefits(self, content):
        """Extract product benefits from content."""
        benefits = []
        
        # Look for benefit indicators
        benefit_patterns = [
            r'Benefits?:\s*([^.\n]+)',
            r'Advantages?:\s*([^.\n]+)',
            r'Why choose[^?]*\?[^.]*\.([^.\n]+)',
            r'Improves?\s+([^.\n]+)',
            r'Reduces?\s+([^.\n]+)',
            r'Increases?\s+([^.\n]+)',
            r'Delivers?\s+([^.\n]+)'
        ]
        
        for pattern in benefit_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                benefit = match.strip()
                if len(benefit) > 10 and len(benefit) < 200:
                    benefits.append(benefit)
        
        return benefits[:15]  # Limit to top 15 benefits
    
    def _extract_product_use_cases(self, content):
        """Extract product use cases from content."""
        use_cases = []
        
        # Look for use case indicators
        use_case_patterns = [
            r'Use cases?:\s*([^.\n]+)',
            r'Perfect for:\s*([^.\n]+)',
            r'Ideal for:\s*([^.\n]+)',
            r'Best suited for:\s*([^.\n]+)',
            r'Designed for:\s*([^.\n]+)',
            r'Target audience:\s*([^.\n]+)'
        ]
        
        for pattern in use_case_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                use_case = match.strip()
                if len(use_case) > 10 and len(use_case) < 200:
                    use_cases.append(use_case)
        
        return use_cases[:15]  # Limit to top 15 use cases
    
    def _extract_product_pricing(self, content):
        """Extract product pricing from content."""
        price_pattern = re.compile(r'[\$€£¥]\s*[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day|user|seat))?', re.IGNORECASE)
        prices = price_pattern.findall(content)
        return prices[0] if prices else None
    
    def _extract_product_category(self, url, title):
        """Extract product category from URL and title."""
        url_lower = url.lower()
        title_lower = title.lower()
        
        if 'security' in url_lower or 'security' in title_lower:
            return 'security'
        elif 'cloud' in url_lower or 'cloud' in title_lower:
            return 'cloud'
        elif 'software' in url_lower or 'software' in title_lower:
            return 'software'
        elif 'platform' in url_lower or 'platform' in title_lower:
            return 'platform'
        elif 'course' in url_lower or 'course' in title_lower:
            return 'course'
        elif 'tool' in url_lower or 'tool' in title_lower:
            return 'tool'
        else:
            return 'general'
    
    def _extract_target_audience(self, content):
        """Extract target audience from content."""
        audience_patterns = [
            r'Target audience:\s*([^.\n]+)',
            r'Perfect for:\s*([^.\n]+)',
            r'Ideal for:\s*([^.\n]+)',
            r'Designed for:\s*([^.\n]+)',
            r'Best suited for:\s*([^.\n]+)'
        ]
        
        for pattern in audience_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return ''
    
    def _extract_requirements(self, content):
        """Extract system requirements from content."""
        req_patterns = [
            r'Requirements?:\s*([^.\n]+)',
            r'System requirements?:\s*([^.\n]+)',
            r'Prerequisites?:\s*([^.\n]+)',
            r'Minimum requirements?:\s*([^.\n]+)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return ''
    
    def _extract_deployment_info(self, content):
        """Extract deployment information from content."""
        deploy_patterns = [
            r'Deployment:\s*([^.\n]+)',
            r'Installation:\s*([^.\n]+)',
            r'Setup:\s*([^.\n]+)',
            r'Implementation:\s*([^.\n]+)'
        ]
        
        for pattern in deploy_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return ''
    
    def _extract_support_info(self, content):
        """Extract support information from content."""
        support_patterns = [
            r'Support:\s*([^.\n]+)',
            r'Customer support:\s*([^.\n]+)',
            r'Technical support:\s*([^.\n]+)',
            r'Help desk:\s*([^.\n]+)'
        ]
        
        for pattern in support_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return ''
    
    def _merge_duplicate_services(self, services):
        """Merge duplicate services and combine information."""
        merged = {}
        
        for service in services:
            name = service['name'].lower().strip()
            if name in merged:
                # Merge information
                merged[name]['features'].extend(service['features'])
                merged[name]['benefits'].extend(service['benefits'])
                merged[name]['use_cases'].extend(service['use_cases'])
                if not merged[name]['pricing'] and service['pricing']:
                    merged[name]['pricing'] = service['pricing']
                if not merged[name]['description'] and service['description']:
                    merged[name]['description'] = service['description']
            else:
                merged[name] = service
        
        # Remove duplicates from lists
        for service in merged.values():
            service['features'] = list(set(service['features']))
            service['benefits'] = list(set(service['benefits']))
            service['use_cases'] = list(set(service['use_cases']))
        
        return list(merged.values())
    
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
    
    def _extract_comprehensive_pricing(self, vendor_data):
        """Extract comprehensive pricing information from vendor data."""
        pricing_info = []
        
        for page in vendor_data.get('pages', []):
            content = page.get('content', '')
            price_pattern = re.compile(r'[\$€£¥]\s*[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day|user|seat))?', re.IGNORECASE)
            prices = price_pattern.findall(content)
            pricing_info.extend(prices)
        
        return list(set(pricing_info))  # Remove duplicates
    
    def _extract_industry_focus(self, vendor_data):
        """Extract industry focus from vendor data."""
        industry_keywords = [
            'healthcare', 'financial', 'government', 'legal', 'manufacturing',
            'education', 'retail', 'technology', 'energy', 'automotive',
            'real estate', 'insurance', 'banking', 'telecommunications'
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
    
    def _extract_features(self, vendor_data):
        """Extract general features from vendor data."""
        features = []
        
        for page in vendor_data.get('pages', []):
            content = page.get('content', '')
            feature_patterns = [
                r'•\s*([^•\n]+)',
                r'-\s*([^-\n]+)',
                r'\*\s*([^*\n]+)',
                r'✓\s*([^✓\n]+)'
            ]
            
            for pattern in feature_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    feature = match.strip()
                    if len(feature) > 10 and len(feature) < 200:
                        features.append(feature)
        
        return list(set(features))[:20]  # Limit to top 20 unique features
    
    def _extract_benefits(self, vendor_data):
        """Extract general benefits from vendor data."""
        benefits = []
        
        for page in vendor_data.get('pages', []):
            content = page.get('content', '')
            benefit_patterns = [
                r'Benefits?:\s*([^.\n]+)',
                r'Advantages?:\s*([^.\n]+)',
                r'Improves?\s+([^.\n]+)',
                r'Reduces?\s+([^.\n]+)',
                r'Increases?\s+([^.\n]+)'
            ]
            
            for pattern in benefit_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    benefit = match.strip()
                    if len(benefit) > 10 and len(benefit) < 200:
                        benefits.append(benefit)
        
        return list(set(benefits))[:20]  # Limit to top 20 unique benefits
    
    def _extract_use_cases(self, vendor_data):
        """Extract general use cases from vendor data."""
        use_cases = []
        
        for page in vendor_data.get('pages', []):
            content = page.get('content', '')
            use_case_patterns = [
                r'Use cases?:\s*([^.\n]+)',
                r'Perfect for:\s*([^.\n]+)',
                r'Ideal for:\s*([^.\n]+)',
                r'Best suited for:\s*([^.\n]+)'
            ]
            
            for pattern in use_case_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    use_case = match.strip()
                    if len(use_case) > 10 and len(use_case) < 200:
                        use_cases.append(use_case)
        
        return list(set(use_cases))[:20]  # Limit to top 20 unique use cases
    
    def _extract_integrations(self, vendor_data):
        """Extract integration information from vendor data."""
        integrations = []
        
        for page in vendor_data.get('pages', []):
            content = page.get('content', '')
            integration_patterns = [
                r'Integrates? with:\s*([^.\n]+)',
                r'Compatible with:\s*([^.\n]+)',
                r'Works with:\s*([^.\n]+)',
                r'Supports?:\s*([^.\n]+)'
            ]
            
            for pattern in integration_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    integration = match.strip()
                    if len(integration) > 10 and len(integration) < 200:
                        integrations.append(integration)
        
        return list(set(integrations))[:15]  # Limit to top 15 unique integrations
    
    def _extract_certifications(self, vendor_data):
        """Extract certification information from vendor data."""
        certifications = []
        
        for page in vendor_data.get('pages', []):
            content = page.get('content', '')
            cert_patterns = [
                r'Certified:\s*([^.\n]+)',
                r'Certification:\s*([^.\n]+)',
                r'Compliant with:\s*([^.\n]+)',
                r'Meets? standards?:\s*([^.\n]+)'
            ]
            
            for pattern in cert_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    cert = match.strip()
                    if len(cert) > 10 and len(cert) < 200:
                        certifications.append(cert)
        
        return list(set(certifications))[:15]  # Limit to top 15 unique certifications
    
    def _generate_vendor_id(self, company_name):
        """Generate a unique vendor ID from company name."""
        clean_name = re.sub(r'[^\w\s]', '', company_name.lower())
        clean_name = re.sub(r'\s+', '_', clean_name.strip())
        return clean_name[:50]
    
    def _extract_domain(self, url):
        """Extract domain from URL."""
        if url:
            parsed = urlparse(url)
            return parsed.netloc.replace('www.', '')
        return ''
    
    def _save_vendor_to_database(self, vendor_data):
        """Save comprehensive vendor data to database markdown file."""
        vendor_id = vendor_data['vendor_id']
        
        # Create markdown content
        markdown_content = self._generate_comprehensive_vendor_markdown(vendor_data)
        
        # Save to file
        filename = f"{vendor_id}.md"
        filepath = self.database_output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  ✓ Saved: {filename}")
    
    def _generate_comprehensive_vendor_markdown(self, vendor_data):
        """Generate comprehensive markdown content for vendor database entry."""
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
        
        # Services Section
        if vendor_data['services']:
            md += "\n## Services Offered\n"
            for i, service in enumerate(vendor_data['services'], 1):
                md += f"\n### {i}. {service['name']}\n"
                md += f"- **Category**: {service['category']}\n"
                md += f"- **URL**: {service['url']}\n"
                md += f"- **Description**: {service['description']}\n"
                if service['pricing']:
                    md += f"- **Pricing**: {service['pricing']}\n"
                
                if service['features']:
                    md += "- **Features**:\n"
                    for feature in service['features'][:10]:
                        md += f"  - {feature}\n"
                
                if service['benefits']:
                    md += "- **Benefits**:\n"
                    for benefit in service['benefits'][:10]:
                        md += f"  - {benefit}\n"
                
                if service['use_cases']:
                    md += "- **Use Cases**:\n"
                    for use_case in service['use_cases'][:10]:
                        md += f"  - {use_case}\n"
        
        # Products Section
        if vendor_data['products']:
            md += "\n## Products\n"
            for i, product in enumerate(vendor_data['products'], 1):
                md += f"\n### {i}. {product['name']}\n"
                md += f"- **Category**: {product['category']}\n"
                md += f"- **URL**: {product['url']}\n"
                md += f"- **Description**: {product['description']}\n"
                if product['pricing']:
                    md += f"- **Pricing**: {product['pricing']}\n"
                
                if product['target_audience']:
                    md += f"- **Target Audience**: {product['target_audience']}\n"
                
                if product['requirements']:
                    md += f"- **Requirements**: {product['requirements']}\n"
                
                if product['deployment']:
                    md += f"- **Deployment**: {product['deployment']}\n"
                
                if product['support']:
                    md += f"- **Support**: {product['support']}\n"
                
                if product['features']:
                    md += "- **Features**:\n"
                    for feature in product['features'][:15]:
                        md += f"  - {feature}\n"
                
                if product['benefits']:
                    md += "- **Benefits**:\n"
                    for benefit in product['benefits'][:15]:
                        md += f"  - {benefit}\n"
                
                if product['use_cases']:
                    md += "- **Use Cases**:\n"
                    for use_case in product['use_cases'][:15]:
                        md += f"  - {use_case}\n"
        
        # Technology Stack
        if vendor_data['technology_stack']:
            md += "\n## Technology Stack\n"
            for tech in sorted(vendor_data['technology_stack']):
                md += f"- {tech}\n"
        
        # Pricing Information
        if vendor_data['pricing_info']:
            md += "\n## Pricing Information\n"
            for price in vendor_data['pricing_info']:
                md += f"- {price}\n"
        
        # Industry Focus
        if vendor_data['industry_focus']:
            md += "\n## Industry Focus\n"
            for industry in sorted(vendor_data['industry_focus']):
                md += f"- {industry}\n"
        
        # Geographic Presence
        if vendor_data['geographic_presence']:
            md += "\n## Geographic Presence\n"
            for geo in sorted(vendor_data['geographic_presence']):
                md += f"- {geo}\n"
        
        # Features
        if vendor_data['features']:
            md += "\n## General Features\n"
            for feature in vendor_data['features']:
                md += f"- {feature}\n"
        
        # Benefits
        if vendor_data['benefits']:
            md += "\n## General Benefits\n"
            for benefit in vendor_data['benefits']:
                md += f"- {benefit}\n"
        
        # Use Cases
        if vendor_data['use_cases']:
            md += "\n## General Use Cases\n"
            for use_case in vendor_data['use_cases']:
                md += f"- {use_case}\n"
        
        # Integrations
        if vendor_data['integrations']:
            md += "\n## Integrations\n"
            for integration in vendor_data['integrations']:
                md += f"- {integration}\n"
        
        # Certifications
        if vendor_data['certifications']:
            md += "\n## Certifications\n"
            for cert in vendor_data['certifications']:
                md += f"- {cert}\n"
        
        md += f"""
## Metadata
- **Total Pages Scraped**: {vendor_data['total_pages_scraped']}
- **Scraped At**: {vendor_data['scraped_at']}
- **Last Updated**: {vendor_data['last_updated']}

---
*Generated by Enhanced Product and Service Extractor*
"""
        
        return md
    
    def _create_master_database(self, all_vendor_data):
        """Create a master database file with all vendors."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        master_file = self.database_output_dir / f"master_database_{timestamp}.md"
        
        md = f"""# Master Vendor Database - Enhanced Product & Service Information

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Vendors: {len(all_vendor_data)}

## Vendor Summary

"""
        
        for vendor in all_vendor_data:
            md += f"### {vendor['company_name']}\n"
            md += f"- **ID**: {vendor['vendor_id']}\n"
            md += f"- **Website**: {vendor['website']}\n"
            md += f"- **Services**: {len(vendor['services'])} services\n"
            md += f"- **Products**: {len(vendor['products'])} products\n"
            md += f"- **Contact**: {vendor['contact_info'].get('email', 'N/A')}\n\n"
        
        md += "\n## Enhanced Data Structure\n\n"
        md += "Each vendor now includes comprehensive information for:\n"
        md += "- **Services**: Detailed features, benefits, use cases, and pricing\n"
        md += "- **Products**: Complete product information with target audience and requirements\n"
        md += "- **Features**: Detailed feature lists for each service/product\n"
        md += "- **Benefits**: Specific benefits for each offering\n"
        md += "- **Use Cases**: Real-world applications and scenarios\n"
        md += "- **Integrations**: Compatibility and integration information\n"
        md += "- **Certifications**: Compliance and certification details\n"
        
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"✓ Created master database: {master_file.name}")

def main():
    """Main function to extract comprehensive vendor data."""
    extractor = EnhancedProductServiceExtractor()
    
    print("Starting enhanced product and service extraction...")
    print("=" * 60)
    
    # Extract all vendor data
    vendor_data = extractor.extract_all_vendors()
    
    print("\n" + "=" * 60)
    print("Enhanced vendor data extraction completed!")
    print(f"Processed {len(vendor_data)} vendors with comprehensive product/service information")

if __name__ == "__main__":
    main()
