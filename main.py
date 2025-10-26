"""
Vendor Research Tool - CLI Application
A Python-based web scraping and content extraction tool for vendor research.
"""

import click
import json
from pathlib import Path
from typing import List

from src.research.vendor_researcher import VendorResearcher
from rich.console import Console
from rich.panel import Panel

console = Console()

@click.group()
def cli():
    """Vendor Research Tool - Extract and analyze vendor information from websites."""
    pass

@cli.command()
@click.argument('urls', nargs=-1, required=True)
@click.option('--output-dir', '-o', default='research_output', help='Output directory for results')
@click.option('--file', '-f', help='File containing URLs (one per line)')
def research(urls, output_dir, file):
    """Research vendors by scraping their websites."""
    
    # Collect URLs
    all_urls = list(urls)
    
    if file:
        file_path = Path(file)
        if file_path.exists():
            with open(file_path, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip()]
                all_urls.extend(file_urls)
        else:
            console.print(f"[red]Error: File {file} not found.[/red]")
            return
    
    if not all_urls:
        console.print("[red]Error: No URLs provided.[/red]")
        return
    
    console.print(Panel.fit(
        f"[bold green]Starting research for {len(all_urls)} vendor(s)[/bold green]",
        title="Vendor Research Tool"
    ))
    
    # Initialize researcher
    researcher = VendorResearcher(output_dir=output_dir)
    
    # Conduct research
    try:
        vendor_info_list = researcher.research_vendors(all_urls)
        
        # Display results
        console.print("\n[bold green]Research completed![/bold green]")
        researcher.display_results(vendor_info_list)
        
    except Exception as e:
        console.print(f"[red]Error during research: {e}[/red]")

@cli.command()
@click.option('--output-dir', '-o', default='research_output', help='Output directory to search')
def list_results(output_dir):
    """List all research results."""
    output_path = Path(output_dir)
    
    if not output_path.exists():
        console.print(f"[red]Output directory {output_dir} not found.[/red]")
        return
    
    console.print(Panel.fit(
        f"[bold blue]Research Results in {output_dir}[/bold blue]",
        title="Vendor Research Tool"
    ))
    
    vendor_dirs = [d for d in output_path.iterdir() if d.is_dir()]
    
    if not vendor_dirs:
        console.print("[yellow]No research results found.[/yellow]")
        return
    
    from rich.table import Table
    table = Table()
    table.add_column("Vendor", style="cyan")
    table.add_column("Files", style="green")
    table.add_column("Last Modified", style="yellow")
    
    for vendor_dir in vendor_dirs:
        files = list(vendor_dir.glob('*'))
        file_count = len(files)
        last_modified = max(f.stat().st_mtime for f in files) if files else 0
        
        from datetime import datetime
        last_modified_str = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M')
        
        table.add_row(
            vendor_dir.name.replace('_', ' ').title(),
            str(file_count),
            last_modified_str
        )
    
    console.print(table)

@cli.command()
@click.argument('vendor_name')
@click.option('--output-dir', '-o', default='research_output', help='Output directory to search')
def show_vendor(vendor_name, output_dir):
    """Show detailed information for a specific vendor."""
    output_path = Path(output_dir)
    vendor_path = output_path / vendor_name.replace(' ', '_').replace('/', '_')
    
    if not vendor_path.exists():
        console.print(f"[red]Vendor '{vendor_name}' not found in {output_dir}.[/red]")
        return
    
    # Load vendor info
    vendor_info_file = vendor_path / 'vendor_info.json'
    if vendor_info_file.exists():
        with open(vendor_info_file, 'r') as f:
            vendor_data = json.load(f)
        
        console.print(Panel.fit(
            f"[bold blue]{vendor_data.get('name', vendor_name)}[/bold blue]",
            title="Vendor Information"
        ))
        
        console.print(f"**Website**: {vendor_data.get('website', 'N/A')}")
        console.print(f"**Description**: {vendor_data.get('description', 'N/A')}")
        
        if vendor_data.get('contact_info'):
            console.print("\n**Contact Information**:")
            for key, value in vendor_data['contact_info'].items():
                console.print(f"  - {key.title()}: {value}")
        
        if vendor_data.get('services'):
            console.print(f"\n**Services**: {', '.join(vendor_data['services'])}")
        
        if vendor_data.get('technology_stack'):
            console.print(f"\n**Technology Stack**: {', '.join(vendor_data['technology_stack'])}")
        
        if vendor_data.get('social_links'):
            console.print("\n**Social Media**:")
            for platform, url in vendor_data['social_links'].items():
                console.print(f"  - {platform.title()}: {url}")
    
    else:
        console.print(f"[red]Vendor information file not found for {vendor_name}.[/red]")

if __name__ == '__main__':
    cli()
