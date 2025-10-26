"""
Content processor for analyzing and organizing scraped vendor information.
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class VendorInfo:
    """Structured vendor information."""
    name: str
    website: str
    description: Optional[str] = None
    contact_info: Dict[str, str] = None
    services: List[str] = None
    pricing_info: Optional[str] = None
    technology_stack: List[str] = None
    case_studies: List[str] = None
    certifications: List[str] = None
    social_links: Dict[str, str] = None
    
    def __post_init__(self):
        if self.contact_info is None:
            self.contact_info = {}
        if self.services is None:
            self.services = []
        if self.technology_stack is None:
            self.technology_stack = []
        if self.case_studies is None:
            self.case_studies = []
        if self.certifications is None:
            self.certifications = []
        if self.social_links is None:
            self.social_links = {}

class ContentProcessor:
    """Processes scraped content to extract vendor information."""
    
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
        self.price_pattern = re.compile(r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day))?', re.IGNORECASE)
        
    def extract_vendor_info(self, scraped_data: Dict) -> VendorInfo:
        """
        Extract structured vendor information from scraped content.
        
        Args:
            scraped_data: Dictionary containing scraped content
            
        Returns:
            VendorInfo object with extracted information
        """
        content = scraped_data.get('content', '') or ''
        title = scraped_data.get('title', '') or ''
        url = scraped_data.get('url', '')
        
        # Extract vendor name (use title or domain)
        vendor_name = self._extract_vendor_name(title, url)
        
        # Extract contact information
        contact_info = self._extract_contact_info(content)
        
        # Extract services
        services = self._extract_services(content)
        
        # Extract technology stack
        tech_stack = self._extract_technology_stack(content)
        
        # Extract pricing information
        pricing_info = self._extract_pricing_info(content)
        
        # Extract social links
        social_links = self._extract_social_links(scraped_data.get('links', []))
        
        return VendorInfo(
            name=vendor_name,
            website=url,
            description=self._extract_description(content),
            contact_info=contact_info,
            services=services,
            pricing_info=pricing_info,
            technology_stack=tech_stack,
            social_links=social_links
        )
    
    def _extract_vendor_name(self, title: str, url: str) -> str:
        """Extract vendor name from title or URL."""
        if title:
            # Remove common suffixes
            title = re.sub(r'\s*-\s*(Home|About|Services|Contact).*$', '', title, flags=re.IGNORECASE)
            return title.strip()
        
        # Fallback to domain name
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace('www.', '')
    
    def _extract_contact_info(self, content: str) -> Dict[str, str]:
        """Extract contact information from content."""
        contact_info = {}
        
        # Extract emails
        emails = self.email_pattern.findall(content)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone numbers
        phones = self.phone_pattern.findall(content)
        if phones:
            contact_info['phone'] = ''.join(phones[0])
        
        return contact_info
    
    def _extract_services(self, content: str) -> List[str]:
        """Extract services offered by the vendor."""
        # Common service keywords
        service_keywords = [
            'consulting', 'development', 'design', 'marketing', 'analytics',
            'cloud', 'hosting', 'support', 'maintenance', 'integration',
            'custom software', 'web development', 'mobile app', 'e-commerce',
            'data analytics', 'business intelligence', 'automation', 'AI',
            'machine learning', 'cybersecurity', 'devops', 'infrastructure'
        ]
        
        services = []
        content_lower = content.lower()
        
        for keyword in service_keywords:
            if keyword in content_lower:
                services.append(keyword.title())
        
        return list(set(services))  # Remove duplicates
    
    def _extract_technology_stack(self, content: str) -> List[str]:
        """Extract technology stack mentioned in content."""
        # Common technology keywords
        tech_keywords = [
            'python', 'javascript', 'react', 'vue', 'angular', 'node.js',
            'java', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'apache', 'nginx', 'linux', 'windows', 'macos'
        ]
        
        tech_stack = []
        content_lower = content.lower()
        
        for tech in tech_keywords:
            if tech in content_lower:
                tech_stack.append(tech.title())
        
        return list(set(tech_stack))
    
    def _extract_pricing_info(self, content: str) -> Optional[str]:
        """Extract pricing information from content."""
        prices = self.price_pattern.findall(content)
        if prices:
            return prices[0]
        return None
    
    def _extract_description(self, content: str) -> Optional[str]:
        """Extract a brief description from content."""
        # Take first 200 characters as description
        if content:
            return content[:200].strip() + '...' if len(content) > 200 else content.strip()
        return None
    
    def _extract_social_links(self, links: List[Dict]) -> Dict[str, str]:
        """Extract social media links."""
        social_platforms = {
            'linkedin': 'linkedin.com',
            'twitter': 'twitter.com',
            'facebook': 'facebook.com',
            'instagram': 'instagram.com',
            'youtube': 'youtube.com',
            'github': 'github.com'
        }
        
        social_links = {}
        
        for link in links:
            url = link.get('url', '').lower()
            for platform, domain in social_platforms.items():
                if domain in url:
                    social_links[platform] = link.get('url', '')
                    break
        
        return social_links
    
    def generate_report(self, vendor_info: VendorInfo) -> str:
        """Generate a formatted report for vendor information."""
        report = f"""
# Vendor Research Report: {vendor_info.name}

## Basic Information
- **Website**: {vendor_info.website}
- **Description**: {vendor_info.description or 'No description available'}

## Contact Information
"""
        
        for key, value in vendor_info.contact_info.items():
            report += f"- **{key.title()}**: {value}\n"
        
        if vendor_info.services:
            report += "\n## Services Offered\n"
            for service in vendor_info.services:
                report += f"- {service}\n"
        
        if vendor_info.technology_stack:
            report += "\n## Technology Stack\n"
            for tech in vendor_info.technology_stack:
                report += f"- {tech}\n"
        
        if vendor_info.pricing_info:
            report += f"\n## Pricing\n- {vendor_info.pricing_info}\n"
        
        if vendor_info.social_links:
            report += "\n## Social Media\n"
            for platform, url in vendor_info.social_links.items():
                report += f"- **{platform.title()}**: {url}\n"
        
        return report
