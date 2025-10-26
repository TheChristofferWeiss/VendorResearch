"""
Main vendor research application that orchestrates web scraping and content processing.
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from ..scrapers.web_scraper import WebScraper
from ..processors.content_processor import ContentProcessor, VendorInfo

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VendorResearcher:
    """Main class for conducting vendor research."""
    
    def __init__(self, output_dir: str = "research_output"):
        self.console = Console()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.scraper = WebScraper(
            user_agent=os.getenv('USER_AGENT', 'VendorResearchBot/1.0'),
            delay=float(os.getenv('REQUEST_DELAY', '1.0'))
        )
        self.processor = ContentProcessor()
    
    def research_vendors(self, vendor_urls: List[str]) -> List[VendorInfo]:
        """
        Research multiple vendors by scraping their websites.
        
        Args:
            vendor_urls: List of vendor website URLs to research
            
        Returns:
            List of VendorInfo objects
        """
        self.console.print(Panel.fit(
            f"[bold blue]Starting vendor research for {len(vendor_urls)} vendors[/bold blue]",
            title="Vendor Research Tool"
        ))
        
        vendor_info_list = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Researching vendors...", total=len(vendor_urls))
            
            for i, url in enumerate(vendor_urls, 1):
                progress.update(task, description=f"Researching vendor {i}/{len(vendor_urls)}: {url}")
                
                try:
                    # Scrape the vendor website
                    scraped_data = self.scraper.scrape_url(url)
                    
                    if scraped_data:
                        # Process the content
                        vendor_info = self.processor.extract_vendor_info(scraped_data)
                        vendor_info_list.append(vendor_info)
                        
                        # Save individual results
                        self._save_vendor_data(vendor_info, scraped_data)
                        
                        self.console.print(f"[green]✓[/green] Successfully researched: {vendor_info.name}")
                    else:
                        self.console.print(f"[red]✗[/red] Failed to scrape: {url}")
                
                except Exception as e:
                    logger.error(f"Error researching {url}: {e}")
                    self.console.print(f"[red]✗[/red] Error researching {url}: {e}")
                
                progress.update(task, advance=1)
        
        # Generate summary report
        self._generate_summary_report(vendor_info_list)
        
        return vendor_info_list
    
    def _save_vendor_data(self, vendor_info: VendorInfo, scraped_data: Dict):
        """Save vendor data to files."""
        vendor_name = vendor_info.name.replace(' ', '_').replace('/', '_')
        vendor_dir = self.output_dir / vendor_name
        vendor_dir.mkdir(exist_ok=True)
        
        # Save raw scraped data
        with open(vendor_dir / 'raw_data.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False, default=str)
        
        # Save processed vendor info
        vendor_dict = {
            'name': vendor_info.name,
            'website': vendor_info.website,
            'description': vendor_info.description,
            'contact_info': vendor_info.contact_info,
            'services': vendor_info.services,
            'pricing_info': vendor_info.pricing_info,
            'technology_stack': vendor_info.technology_stack,
            'case_studies': vendor_info.case_studies,
            'certifications': vendor_info.certifications,
            'social_links': vendor_info.social_links
        }
        
        with open(vendor_dir / 'vendor_info.json', 'w', encoding='utf-8') as f:
            json.dump(vendor_dict, f, indent=2, ensure_ascii=False)
        
        # Save markdown report
        report = self.processor.generate_report(vendor_info)
        with open(vendor_dir / 'report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save markdown content
        if scraped_data.get('markdown'):
            with open(vendor_dir / 'content.md', 'w', encoding='utf-8') as f:
                f.write(scraped_data['markdown'])
    
    def _generate_summary_report(self, vendor_info_list: List[VendorInfo]):
        """Generate a summary report of all vendors."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create summary table
        table = Table(title="Vendor Research Summary")
        table.add_column("Vendor", style="cyan")
        table.add_column("Website", style="blue")
        table.add_column("Services", style="green")
        table.add_column("Tech Stack", style="yellow")
        table.add_column("Contact", style="magenta")
        
        for vendor in vendor_info_list:
            services = ', '.join(vendor.services[:3]) if vendor.services else 'N/A'
            tech_stack = ', '.join(vendor.technology_stack[:3]) if vendor.technology_stack else 'N/A'
            contact = vendor.contact_info.get('email', 'N/A')
            
            table.add_row(
                vendor.name,
                vendor.website,
                services,
                tech_stack,
                contact
            )
        
        self.console.print(table)
        
        # Save summary to file
        summary_file = self.output_dir / f"summary_report_{timestamp}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Vendor Research Summary Report\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total vendors researched: {len(vendor_info_list)}\n\n")
            
            for vendor in vendor_info_list:
                f.write(f"## {vendor.name}\n")
                f.write(f"- **Website**: {vendor.website}\n")
                f.write(f"- **Services**: {', '.join(vendor.services) if vendor.services else 'N/A'}\n")
                f.write(f"- **Tech Stack**: {', '.join(vendor.technology_stack) if vendor.technology_stack else 'N/A'}\n")
                f.write(f"- **Contact**: {vendor.contact_info.get('email', 'N/A')}\n\n")
        
        self.console.print(f"\n[green]Summary report saved to: {summary_file}[/green]")
    
    def display_results(self, vendor_info_list: List[VendorInfo]):
        """Display research results in a formatted table."""
        if not vendor_info_list:
            self.console.print("[red]No vendor information to display.[/red]")
            return
        
        table = Table(title="Vendor Research Results")
        table.add_column("Vendor", style="cyan", no_wrap=True)
        table.add_column("Website", style="blue")
        table.add_column("Description", style="white")
        table.add_column("Services", style="green")
        table.add_column("Contact", style="magenta")
        
        for vendor in vendor_info_list:
            description = (vendor.description[:50] + '...') if vendor.description and len(vendor.description) > 50 else vendor.description or 'N/A'
            services = ', '.join(vendor.services[:2]) if vendor.services else 'N/A'
            contact = vendor.contact_info.get('email', 'N/A')
            
            table.add_row(
                vendor.name,
                vendor.website,
                description,
                services,
                contact
            )
        
        self.console.print(table)
