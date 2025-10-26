"""
Extractor service for the Vendor Research Web Application.
"""

import re
from urllib.parse import urlparse

class ExtractorService:
    """Service for extracting services and products from scraped data."""
    
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
    
    def extract_from_raw_data(self, raw_data):
        """Extract services and products from raw scraped data."""
        try:
            result = {
                'services': [],
                'products': []
            }
            
            # Extract services from all pages
            for page in raw_data.get('pages', []):
                page_url = page.get('url', '')
                page_title = page.get('title', '')
                page_content = page.get('content', '')
                
                # Check if this is a service page
                if self._is_service_page(page_url, page_title):
                    service_info = {
                        'name': self._extract_service_name(page_title, page_content),
                        'category': self._extract_service_category(page_url, page_title),
                        'description': self._extract_service_description(page_content),
                        'url': page_url,
                        'pricing': self._extract_service_pricing(page_content),
                        'features': self._extract_service_features(page_content),
                        'benefits': self._extract_service_benefits(page_content),
                        'use_cases': self._extract_service_use_cases(page_content)
                    }
                    result['services'].append(service_info)
                
                # Check if this is a product page
                if self._is_product_page(page_url, page_title):
                    product_info = {
                        'name': self._extract_product_name(page_title, page_content),
                        'category': self._extract_product_category(page_url, page_title),
                        'description': self._extract_product_description(page_content),
                        'url': page_url,
                        'pricing': self._extract_product_pricing(page_content),
                        'target_audience': self._extract_target_audience(page_content),
                        'requirements': self._extract_requirements(page_content),
                        'deployment': self._extract_deployment_info(page_content),
                        'support': self._extract_support_info(page_content),
                        'features': self._extract_product_features(page_content),
                        'benefits': self._extract_product_benefits(page_content),
                        'use_cases': self._extract_product_use_cases(page_content)
                    }
                    result['products'].append(product_info)
            
            return result
            
        except Exception as e:
            print(f"Error extracting from raw data: {e}")
            return None
    
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
        clean_title = re.sub(r'\s*-\s*.*$', '', title)
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        return clean_title.strip()
    
    def _extract_service_description(self, content):
        """Extract service description from content."""
        desc_patterns = [
            r'([^.]{50,200}\.)',
            r'([A-Z][^.]{30,150}\.)'
        ]
        
        for pattern in desc_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].strip()
        
        return content[:200].strip() + '...' if len(content) > 200 else content.strip()
    
    def _extract_service_features(self, content):
        """Extract service features from content."""
        features = []
        
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
        
        return features[:10]
    
    def _extract_service_benefits(self, content):
        """Extract service benefits from content."""
        benefits = []
        
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
        
        return benefits[:10]
    
    def _extract_service_use_cases(self, content):
        """Extract service use cases from content."""
        use_cases = []
        
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
        
        return use_cases[:10]
    
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
        clean_title = re.sub(r'\s*-\s*.*$', '', title)
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        return clean_title.strip()
    
    def _extract_product_description(self, content):
        """Extract product description from content."""
        desc_patterns = [
            r'([^.]{50,300}\.)',
            r'([A-Z][^.]{30,200}\.)'
        ]
        
        for pattern in desc_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].strip()
        
        return content[:300].strip() + '...' if len(content) > 300 else content.strip()
    
    def _extract_product_features(self, content):
        """Extract product features from content."""
        features = []
        
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
        
        return features[:15]
    
    def _extract_product_benefits(self, content):
        """Extract product benefits from content."""
        benefits = []
        
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
        
        return benefits[:15]
    
    def _extract_product_use_cases(self, content):
        """Extract product use cases from content."""
        use_cases = []
        
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
        
        return use_cases[:15]
    
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
