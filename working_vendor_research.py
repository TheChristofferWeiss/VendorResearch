"""
Working Vendor Research Tool - Demonstrates the concept without SSL issues
"""

import json
import re
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime
import os

class MockVendorResearcher:
    """Mock vendor researcher that demonstrates the tool's functionality."""
    
    def __init__(self):
        # Regex patterns for extraction
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
        
        # Mock data for demonstration
        self.mock_vendors = {
            'example.com': {
                'name': 'Example Corp',
                'title': 'Example Corp - Leading Technology Solutions',
                'description': 'We provide innovative technology solutions for businesses worldwide.',
                'content': 'Example Corp specializes in web development, cloud services, and digital transformation. Our team of experts helps businesses leverage cutting-edge technologies including Python, React, AWS, and Docker. Contact us at info@example.com or call +1-555-123-4567.',
                'services': ['Web Development', 'Cloud Services', 'Digital Transformation'],
                'technology_stack': ['Python', 'React', 'AWS', 'Docker'],
                'contact_info': {'email': 'info@example.com', 'phone': '+1-555-123-4567'}
            },
            'techstartup.com': {
                'name': 'TechStartup Inc',
                'title': 'TechStartup - AI-Powered Solutions',
                'description': 'Revolutionary AI and machine learning solutions for modern businesses.',
                'content': 'TechStartup Inc is at the forefront of artificial intelligence and machine learning. We offer consulting services, custom AI development, and data analytics solutions. Our technology stack includes Python, TensorFlow, Kubernetes, and Azure. Reach us at hello@techstartup.com.',
                'services': ['AI Consulting', 'Machine Learning', 'Data Analytics'],
                'technology_stack': ['Python', 'TensorFlow', 'Kubernetes', 'Azure'],
                'contact_info': {'email': 'hello@techstartup.com'}
            }
        }
    
    def scrape_vendor(self, url):
        """Mock scrape a vendor website."""
        try:
            print(f"Processing: {url}")
            time.sleep(0.5)  # Simulate processing time
            
            # Extract domain for mock data lookup
            domain = urlparse(url).netloc.replace('www.', '')
            
            # Use mock data if available, otherwise create generic data
            if domain in self.mock_vendors:
                mock_data = self.mock_vendors[domain]
            else:
                mock_data = self._create_generic_mock_data(url)
            
            # Add URL and timestamp
            result = {
                'url': url,
                'name': mock_data['name'],
                'title': mock_data['title'],
                'description': mock_data['description'],
                'content': mock_data['content'],
                'contact_info': mock_data['contact_info'],
                'services': mock_data['services'],
                'technology_stack': mock_data['technology_stack'],
                'scraped_at': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None
    
    def _create_generic_mock_data(self, url):
        """Create generic mock data for unknown vendors."""
        domain = urlparse(url).netloc.replace('www.', '')
        vendor_name = domain.replace('.com', '').replace('.org', '').title()
        
        return {
            'name': f'{vendor_name} Inc',
            'title': f'{vendor_name} - Professional Services',
            'description': f'Professional services and solutions from {vendor_name}.',
            'content': f'{vendor_name} provides professional services including consulting, development, and support. We work with modern technologies and deliver high-quality solutions to our clients.',
            'services': ['Consulting', 'Development', 'Support'],
            'technology_stack': ['Python', 'JavaScript', 'Cloud Services'],
            'contact_info': {'email': f'info@{domain}'}
        }
    
    def research_vendors(self, urls):
        """Research multiple vendors."""
        results = []
        
        print(f"Starting research for {len(urls)} vendor(s)...")
        print("=" * 50)
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            result = self.scrape_vendor(url)
            
            if result:
                results.append(result)
                print(f"✓ Successfully processed: {result['name']}")
                print(f"  Services: {', '.join(result['services'][:3]) if result['services'] else 'None found'}")
                print(f"  Contact: {result['contact_info'].get('email', 'None found')}")
            else:
                print(f"✗ Failed to process: {url}")
            
            # Add delay between requests
            time.sleep(0.5)
        
        return results
    
    def save_results(self, results, output_dir="research_output"):
        """Save results to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save individual results
        for result in results:
            vendor_name = result['name'].replace(' ', '_').replace('/', '_')
            vendor_dir = os.path.join(output_dir, vendor_name)
            os.makedirs(vendor_dir, exist_ok=True)
            
            # Save vendor info
            with open(os.path.join(vendor_dir, 'vendor_info.json'), 'w') as f:
                json.dump(result, f, indent=2)
            
            # Create a markdown report
            report = self._generate_markdown_report(result)
            with open(os.path.join(vendor_dir, 'report.md'), 'w') as f:
                f.write(report)
        
        # Save summary
        summary_file = os.path.join(output_dir, f"summary_{timestamp}.json")
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Create summary report
        summary_report = self._generate_summary_report(results)
        summary_report_file = os.path.join(output_dir, f"summary_report_{timestamp}.md")
        with open(summary_report_file, 'w') as f:
            f.write(summary_report)
        
        print(f"\nResults saved to: {output_dir}")
        print(f"Summary saved to: {summary_file}")
        print(f"Summary report saved to: {summary_report_file}")
        
        return summary_file
    
    def _generate_markdown_report(self, result):
        """Generate a markdown report for a vendor."""
        report = f"""# Vendor Research Report: {result['name']}

## Basic Information
- **Website**: {result['url']}
- **Title**: {result['title']}
- **Description**: {result['description']}

## Contact Information
"""
        
        for key, value in result['contact_info'].items():
            report += f"- **{key.title()}**: {value}\n"
        
        if result['services']:
            report += "\n## Services Offered\n"
            for service in result['services']:
                report += f"- {service}\n"
        
        if result['technology_stack']:
            report += "\n## Technology Stack\n"
            for tech in result['technology_stack']:
                report += f"- {tech}\n"
        
        report += f"\n## Content Summary\n{result['content']}\n"
        
        report += f"\n---\n*Report generated on: {result['scraped_at']}*"
        
        return report
    
    def _generate_summary_report(self, results):
        """Generate a summary report of all vendors."""
        report = f"""# Vendor Research Summary Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total vendors researched: {len(results)}

"""
        
        for i, result in enumerate(results, 1):
            report += f"""## {i}. {result['name']}

- **Website**: {result['url']}
- **Description**: {result['description']}
- **Services**: {', '.join(result['services']) if result['services'] else 'N/A'}
- **Technology Stack**: {', '.join(result['technology_stack']) if result['technology_stack'] else 'N/A'}
- **Contact**: {result['contact_info'].get('email', 'N/A')}

"""
        
        return report
    
    def display_results(self, results):
        """Display results in a simple format."""
        if not results:
            print("No results to display.")
            return
        
        print("\n" + "=" * 60)
        print("VENDOR RESEARCH RESULTS")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['name']}")
            print(f"   URL: {result['url']}")
            print(f"   Description: {result['description'][:100]}..." if result['description'] else "   Description: None")
            
            if result['contact_info']:
                print("   Contact:")
                for key, value in result['contact_info'].items():
                    print(f"     {key.title()}: {value}")
            
            if result['services']:
                print(f"   Services: {', '.join(result['services'][:5])}")
            
            if result['technology_stack']:
                print(f"   Tech Stack: {', '.join(result['technology_stack'][:5])}")

def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python working_vendor_research.py <url1> [url2] [url3] ...")
        print("Example: python working_vendor_research.py https://example.com https://techstartup.com")
        print("\nNote: This is a demonstration version that works without SSL/network issues.")
        return
    
    urls = sys.argv[1:]
    
    researcher = MockVendorResearcher()
    results = researcher.research_vendors(urls)
    
    if results:
        researcher.display_results(results)
        researcher.save_results(results)
    else:
        print("No results obtained.")

if __name__ == "__main__":
    main()
