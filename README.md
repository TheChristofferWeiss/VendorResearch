# Vendor Research Tool

A powerful Python-based web scraping and content extraction tool for vendor research. This tool uses **trafilatura** and **markdownify** to extract clean, structured content from vendor websites, making it easy to research and compare vendors.

## Features

- **Clean Content Extraction**: Uses trafilatura to extract main content, filtering out ads, navigation, and footers
- **Markdown Conversion**: Converts extracted content to clean markdown format
- **Structured Data Processing**: Automatically extracts vendor information including:
  - Contact information (email, phone)
  - Services offered
  - Technology stack
  - Pricing information
  - Social media links
- **Batch Processing**: Research multiple vendors at once
- **Rich Output**: Beautiful console output with progress bars and formatted tables
- **Export Options**: Save results in JSON, Markdown, and structured formats

## Technology Stack

- **trafilatura**: Powerful content extraction library
- **markdownify**: HTML to Markdown conversion
- **Beautiful Soup**: HTML parsing and link extraction
- **requests**: HTTP client for web scraping
- **Rich**: Beautiful terminal output
- **Click**: Command-line interface
- **python-dotenv**: Environment variable management

## Installation

1. **Clone or create the project directory:**
   ```bash
   mkdir -p ~/Projects/VendorResearch
   cd ~/Projects/VendorResearch
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers (if using Playwright):**
   ```bash
   playwright install
   ```

## Configuration

The tool uses environment variables for configuration. Create a `.env` file with your settings:

```env
# API Keys
GLADIA_API_KEY=your_api_key_here

# Configuration
MAX_CONCURRENT_REQUESTS=5
REQUEST_DELAY=1
USER_AGENT=VendorResearchBot/1.0
```

## Usage

### Basic Usage

Research individual vendors by providing URLs:

```bash
python main.py research https://example-vendor.com https://another-vendor.com
```

### Research from File

Create a text file with URLs (one per line) and use the `--file` option:

```bash
echo "https://vendor1.com" > vendors.txt
echo "https://vendor2.com" >> vendors.txt
python main.py research --file vendors.txt
```

### Custom Output Directory

Specify a custom output directory:

```bash
python main.py research https://vendor.com --output-dir my_research
```

### List Research Results

View all completed research:

```bash
python main.py list-results
```

### Show Specific Vendor

View detailed information for a specific vendor:

```bash
python main.py show-vendor "Vendor Name"
```

## Output Structure

The tool creates organized output in the specified directory:

```
research_output/
├── Vendor_Name/
│   ├── vendor_info.json      # Structured vendor data
│   ├── raw_data.json         # Raw scraped content
│   ├── report.md             # Formatted markdown report
│   └── content.md            # Extracted content in markdown
└── summary_report_TIMESTAMP.md  # Overall summary
```

## Example Output

### Console Output
The tool provides rich console output with progress bars and formatted tables:

```
┌─────────────────────────────────────────────────────────┐
│                 Vendor Research Tool                    │
│        Starting research for 3 vendor(s)               │
└─────────────────────────────────────────────────────────┘

✓ Successfully researched: Example Vendor
✓ Successfully researched: Another Vendor
✓ Successfully researched: Third Vendor

┌─────────────────────────────────────────────────────────┐
│                  Vendor Research Results                │
├──────────────┬─────────────────┬─────────┬──────────────┤
│ Vendor       │ Website         │ Contact │ Services     │
├──────────────┼─────────────────┼─────────┼──────────────┤
│ Example      │ example.com     │ info@   │ Web Dev,     │
│ Vendor       │                 │ example │ Consulting   │
└──────────────┴─────────────────┴─────────┴──────────────┘
```

### Generated Reports
The tool generates comprehensive markdown reports for each vendor:

```markdown
# Vendor Research Report: Example Vendor

## Basic Information
- **Website**: https://example.com
- **Description**: Leading provider of web development services...

## Contact Information
- **Email**: info@example.com
- **Phone**: +1-555-123-4567

## Services Offered
- Web Development
- Consulting
- Cloud Services

## Technology Stack
- Python
- React
- AWS
```

## Advanced Features

### Custom Scraping Configuration

You can modify the scraping behavior by editing the `WebScraper` class in `src/scrapers/web_scraper.py`:

- Adjust request delays
- Modify user agent strings
- Add custom headers
- Configure link filtering

### Content Processing

The `ContentProcessor` class in `src/processors/content_processor.py` can be extended to:

- Add custom extraction patterns
- Support additional data formats
- Implement custom filtering logic
- Add industry-specific processing

### Batch Processing

For large-scale vendor research, you can:

1. Create URL lists in text files
2. Use the batch processing capabilities
3. Configure concurrent request limits
4. Set appropriate delays between requests

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure you have write permissions to the output directory
2. **Network Issues**: Check your internet connection and firewall settings
3. **Rate Limiting**: Increase the `REQUEST_DELAY` in your `.env` file
4. **Missing Dependencies**: Run `pip install -r requirements.txt` again

### Debug Mode

Enable debug logging by modifying the logging level in `src/research/vendor_researcher.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

This tool is designed to be extensible. You can:

- Add new content extraction patterns
- Implement additional output formats
- Add support for new data sources
- Enhance the CLI interface

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue in the project repository

---

**Built with Python, trafilatura, markdownify, and other powerful open-source tools.**
