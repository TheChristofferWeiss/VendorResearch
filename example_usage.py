"""
Example usage of the Vendor Research Tool.
"""

from src.research.vendor_researcher import VendorResearcher

def main():
    """Example of how to use the Vendor Research Tool programmatically."""
    
    # Initialize the researcher
    researcher = VendorResearcher(output_dir="example_output")
    
    # Example vendor URLs (replace with actual vendor websites)
    vendor_urls = [
        "https://www.example.com",
        "https://www.google.com/about",
        "https://www.microsoft.com/about"
    ]
    
    print("Starting vendor research...")
    
    # Research the vendors
    vendor_info_list = researcher.research_vendors(vendor_urls)
    
    # Display results
    print(f"\nResearch completed! Found information for {len(vendor_info_list)} vendors.")
    
    # Show detailed information for each vendor
    for vendor in vendor_info_list:
        print(f"\n--- {vendor.name} ---")
        print(f"Website: {vendor.website}")
        print(f"Description: {vendor.description}")
        print(f"Services: {', '.join(vendor.services) if vendor.services else 'N/A'}")
        print(f"Contact: {vendor.contact_info.get('email', 'N/A')}")

if __name__ == "__main__":
    main()
