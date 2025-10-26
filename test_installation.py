"""
Test script to verify the Vendor Research Tool installation.
"""

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import trafilatura
        print("✓ trafilatura imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import trafilatura: {e}")
        return False
    
    try:
        from markdownify import markdownify
        print("✓ markdownify imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import markdownify: {e}")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import requests: {e}")
        return False
    
    try:
        from rich.console import Console
        print("✓ rich imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import rich: {e}")
        return False
    
    try:
        import click
        print("✓ click imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import click: {e}")
        return False
    
    try:
        from src.scrapers.web_scraper import WebScraper
        print("✓ WebScraper imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import WebScraper: {e}")
        return False
    
    try:
        from src.processors.content_processor import ContentProcessor
        print("✓ ContentProcessor imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ContentProcessor: {e}")
        return False
    
    try:
        from src.research.vendor_researcher import VendorResearcher
        print("✓ VendorResearcher imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import VendorResearcher: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of the tool."""
    try:
        from src.scrapers.web_scraper import WebScraper
        from src.processors.content_processor import ContentProcessor
        
        # Test scraper initialization
        scraper = WebScraper()
        print("✓ WebScraper initialized successfully")
        
        # Test processor initialization
        processor = ContentProcessor()
        print("✓ ContentProcessor initialized successfully")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Vendor Research Tool installation...")
    print("=" * 50)
    
    if test_imports():
        print("\n✓ All imports successful!")
        
        if test_basic_functionality():
            print("✓ Basic functionality test passed!")
            print("\n🎉 Installation test completed successfully!")
            print("You can now use the Vendor Research Tool.")
            print("\nTry running: python main.py research https://example.com")
        else:
            print("\n✗ Basic functionality test failed.")
    else:
        print("\n✗ Some imports failed. Please check your installation.")
        print("Run: pip install -r requirements.txt")
