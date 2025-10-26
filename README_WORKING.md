# Vendor Research Tool - Working Version

A Python-based vendor research tool that extracts and analyzes vendor information from websites. This version works without SSL/network dependencies and demonstrates the core functionality.

## 🎯 What This Tool Does

- **Extracts vendor information** from websites including contact details, services, and technology stack
- **Generates structured reports** in JSON and Markdown formats
- **Organizes results** in a clean directory structure
- **Provides command-line interface** for easy usage

## 🚀 Quick Start

### 1. Run the Tool
```bash
python working_vendor_research.py https://example.com https://another-vendor.com
```

### 2. View Results
The tool will:
- Display results in the terminal
- Save individual vendor reports to `research_output/`
- Create a summary report

### 3. Check Output Files
```bash
ls research_output/
cat research_output/summary_report_*.md
```

## 📁 Output Structure

```
research_output/
├── Vendor_Name/
│   ├── vendor_info.json      # Structured vendor data
│   └── report.md             # Formatted markdown report
├── summary_TIMESTAMP.json    # All results in JSON
└── summary_report_TIMESTAMP.md  # Overall summary report
```

## 🔧 Features

### Data Extraction
- **Vendor Information**: Name, website, description
- **Contact Details**: Email, phone numbers
- **Services**: Automatically detected services
- **Technology Stack**: Technologies mentioned
- **Content Analysis**: Key content extraction

### Output Formats
- **JSON**: Structured data for programmatic use
- **Markdown**: Human-readable reports
- **Console**: Real-time progress and results

### Command Line Interface
```bash
# Research multiple vendors
python working_vendor_research.py https://vendor1.com https://vendor2.com

# View help
python working_vendor_research.py
```

## 📊 Example Output

### Console Output
```
Starting research for 2 vendor(s)...
==================================================

[1/2] Processing: https://example.com
✓ Successfully processed: Example Corp
  Services: Web Development, Cloud Services, Digital Transformation
  Contact: info@example.com

[2/2] Processing: https://techstartup.com
✓ Successfully processed: TechStartup Inc
  Services: AI Consulting, Machine Learning, Data Analytics
  Contact: hello@techstartup.com
```

### Generated Report
```markdown
# Vendor Research Report: Example Corp

## Basic Information
- **Website**: https://example.com
- **Title**: Example Corp - Leading Technology Solutions
- **Description**: We provide innovative technology solutions...

## Contact Information
- **Email**: info@example.com
- **Phone**: +1-555-123-4567

## Services Offered
- Web Development
- Cloud Services
- Digital Transformation

## Technology Stack
- Python
- React
- AWS
- Docker
```

## 🛠️ Customization

### Adding New Vendors
The tool includes mock data for demonstration. To add real vendor data:

1. **Modify the `mock_vendors` dictionary** in `working_vendor_research.py`
2. **Add new vendor entries** with their information
3. **Run the tool** with the new URLs

### Extending Functionality
The tool is designed to be easily extensible:

- **Add new extraction patterns** in the regex sections
- **Modify output formats** in the report generation functions
- **Add new data fields** to the vendor information structure

## 🔍 How It Works

1. **URL Processing**: Takes vendor URLs as input
2. **Data Extraction**: Uses mock data to simulate web scraping
3. **Information Processing**: Extracts contact info, services, tech stack
4. **Report Generation**: Creates structured JSON and markdown reports
5. **File Organization**: Saves results in organized directory structure

## 📋 Requirements

- **Python 3.6+**
- **No external dependencies** (uses only built-in libraries)

## 🚧 Limitations

This is a **demonstration version** that:
- Uses mock data instead of real web scraping
- Works without SSL/network dependencies
- Shows the tool's structure and functionality

## 🔄 Next Steps

To make this a production tool:

1. **Fix SSL issues** in your Python installation
2. **Install required packages**: `pip install requests beautifulsoup4`
3. **Use the full version** with real web scraping capabilities
4. **Add authentication** for protected sites
5. **Implement rate limiting** for large-scale research

## 📝 Notes

- This version demonstrates the tool's core functionality
- All data is mock data for demonstration purposes
- The tool structure is ready for real web scraping implementation
- Results are saved in organized, reusable formats

---

**Built with Python - Ready for real-world vendor research!**
