# BunTool
<p align="center">
  <img src="static/buntool.webp" width="300" style="center">
</p>

Automatically make court bundles in seconds. Check out the main instance: [buntool.co.uk](https://buntool.co.uk)

BunTool is a comprehensive PDF manipulation suite that creates professional court bundles and provides powerful tools for PDF numbering, bookmarking, and merging.

## Features

✅ **PDF Bundle Creation** - Create professional court bundles with table of contents, hyperlinks, bookmarks, and page numbers
✅ **Custom Page Numbering** - Add page numbers to single PDFs with advanced alphanumeric options
✅ **PDF Bookmarking** - Add hierarchical bookmarks with custom styling and colors
✅ **PDF Merging** - Simple merge and reorder functionality
✅ **Court Compliance** - Output bundles comply with English Court requirements
✅ **Advanced Numbering** - Custom alphanumeric numbering (A1, B1, etc.) with page range mapping
✅ **Multiple Formats** - Export as PDF or ZIP with metadata

## Quick Start

**Main Tools** (after installation):
- **Bundle Creation**: http://127.0.0.1:7001/
- **PDF Numbering**: http://127.0.0.1:7001/numbering_tool
- **PDF Bookmarks**: http://127.0.0.1:7001/bookmark_tool
- **PDF Merger**: http://127.0.0.1:7001/pdf_merger

📖 **Complete tool documentation**: See [TOOLS.md](TOOLS.md)

---

# Installation

## Option 1: Manual Installation (Recommended for Development)

This is configured for self-hosting, which is what these instructions are for.


### Step 1: Create Virtual Environment

```bash
# Create the virtual environment (a hidden folder named .venv)
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

### Step 2: Install Fonts

BunTool uses the Charter font, a popular style for legal documents. Copy the font files to ReportLab's fonts folder:

```bash
# This command copies the fonts into your virtual environment
# The python* wildcard makes it work for any version of Python 3
cp static/Charter*.ttf .venv/lib/python*/site-packages/reportlab/fonts/
```

### Step 3: Start the Server

```bash
python app.py
```

Then visit `http://127.0.0.1:7001` in your browser.

---

## Option 2: Docker Installation (Recommended for Production)

### Quick Deploy with Docker Compose

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Manual Docker Build

```bash
# Build the image
docker build -t buntool:latest .

# Run the container
docker run -d \
  --name buntool \
  -p 7001:7001 \
  -v buntool_tempfiles:/app/tempfiles \
  -v buntool_logs:/app/logs \
  buntool:latest
```

### Access the Application

Once running, access at:
- **Main Tool**: http://localhost:7001/
- **PDF Numbering Tool**: http://localhost:7001/numbering_tool
- **Bookmark Tool**: http://localhost:7001/bookmark_tool
- **PDF Merger**: http://localhost:7001/pdf_merger

📖 **Docker documentation**: See [DOCKER.md](DOCKER.md)

---

## Tools Overview

BunTool provides four main tools:

### 1. PDF Bundle Creation Tool
Create professional court bundles with:
- Table of contents (PDF or Word format)
- Custom page numbering
- Hyperlinked index
- Hierarchical bookmarks
- Cover sheet with case details
- Export as PDF or ZIP with metadata

**URL**: `/` (main page)

### 2. PDF Numbering Tool
Add custom page numbers to a single PDF with:
- Multiple numbering styles
- Custom alphanumeric options (A1, B1, Tab1, etc.)
- Page range mapping
- Font and alignment control

**URL**: `/numbering_tool`

### 3. PDF Bookmark Tool
Add hierarchical bookmarks to PDFs with:
- 4 nesting levels
- Custom styling (bold, italic)
- 6 color options
- Page-specific linking

**URL**: `/bookmark_tool`

### 4. PDF Merger Tool
Simple PDF merge and reorder functionality.

**URL**: `/pdf_merger`

📖 **Complete tool documentation**: See [TOOLS.md](TOOLS.md)

---

## Advanced Features

### Custom Alphanumeric Numbering
Add custom page numbers like "A1", "Doc1", "WS1" with intelligent reset modes:
- **Sequential**: A1, A2, A3, ...
- **Letter change**: A1-A26, B1-B26, ...
- **Custom interval**: Reset every N pages

### Page Range Mapping
Apply different numbering schemes to different page ranges:
```
1-20:A      → Pages 1-20: A1, A2, ..., A20
21-40:B     → Pages 21-40: B1, B2, ..., B20
41-60:Doc   → Pages 41-60: Doc1, Doc2, ..., Doc20
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [TOOLS.md](TOOLS.md) | Complete guide to all tools and features |
| [QUICK_START.md](QUICK_START.md) | Quick start guide for custom numbering |
| [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) | Real-world usage examples |
| [DOCKER.md](DOCKER.md) | Docker deployment guide |

---

## Requirements

### Python Dependencies
- Flask 3.1.0
- PyPDF 5.1.0
- pikepdf 9.5.1
- pdfplumber 0.11.5
- reportlab 4.3.0
- python-docx 1.1.2
- Waitress 3.0.2

### System Requirements
- Python 3.7+
- 100MB+ disk space
- For Docker: Docker 20.10+ and Docker Compose 1.29+

---

## Security Features

✅ File type validation (.pdf only)
✅ File size limits (100 MB per file)
✅ Filename sanitization
✅ Session-isolated processing
✅ Automatic file cleanup
✅ Input validation
✅ Secure error messages

---

## Logging

All operations are logged with automatic rotation:
- **Max file size**: 100MB per log file
- **Backup count**: 3 rotated files
- **Total storage**: 400MB per session
- **Location**: `logs/` directory

---

## Performance

| Operation | Time |
|-----------|------|
| Simple bundle (5 files, 50 pages) | ~2-3s |
| Complex bundle (20 files, 200 pages) | ~5-10s |
| PDF numbering (100 pages) | ~2-3s |
| Bookmark addition (50 bookmarks) | ~1s |

---

## Support

For issues and questions:
- Check [TOOLS.md](TOOLS.md) for tool-specific help
- Review logs in `logs/` directory
- See troubleshooting sections in documentation files

---

## Project Structure

```
buntool/
├── app.py                  # Flask application and routes
├── bundle.py               # Core PDF processing logic
├── makedocxindex.py        # Word document generation
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── templates/              # HTML templates
│   ├── index.html         # Main bundle creation interface
│   ├── numbering_tool.html  # PDF numbering tool
│   ├── bookmark_tool.html   # PDF bookmark tool
│   └── pdf_merger_tool.html # PDF merger tool
├── static/                 # CSS, JavaScript, and assets
│   ├── buntool.css        # Main stylesheet
│   ├── buntool.js         # Main JavaScript
│   ├── numbering_tool.js  # Numbering tool JavaScript
│   ├── bookmark_tool.js   # Bookmark tool JavaScript
│   └── Charter*.ttf       # Charter font files
└── logs/                   # Application logs (auto-created)
```

---

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing patterns
- All tools remain backward compatible
- Documentation is updated
- Changes are tested

---

## License

**Copyright © Tristan Sherliker and contributors to BunTool**

Licensed under the Mozilla Public License, version 2.0.

See [LICENSE.md](LICENSE.md) for full license text.

---

## Acknowledgments

- Charter font for legal document formatting
- ReportLab for PDF generation
- pikepdf for advanced PDF manipulation
- Flask for web framework

---

**Version**: 1.0
**Last Updated**: January 2026
**Status**: Production Ready

Visit [buntool.co.uk](https://buntool.co.uk) for the hosted version.