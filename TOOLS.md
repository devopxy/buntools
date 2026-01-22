# BunTool - Tools Documentation

Complete guide to all tools and features available in BunTool.

---

## Table of Contents

1. [Overview](#overview)
2. [PDF Bundle Creation Tool](#1-pdf-bundle-creation-tool)
3. [PDF Numbering Tool](#2-pdf-numbering-tool)
4. [PDF Bookmark Tool](#3-pdf-bookmark-tool)
5. [PDF Merger Tool](#4-pdf-merger-tool)
6. [Advanced Features](#advanced-features)
   - [Custom Alphanumeric Numbering](#custom-alphanumeric-numbering)
   - [Page Range Mapping](#page-range-mapping)
7. [Quick Reference](#quick-reference)

---

## Overview

BunTool provides four main tools for PDF manipulation, plus advanced features for complex document bundling needs:

| Tool | Purpose | URL |
|------|---------|-----|
| **Bundle Creation** | Create professional court bundles with TOC, numbering, and bookmarks | `/` (main page) |
| **PDF Numbering** | Add custom page numbers to a single PDF | `/numbering_tool` |
| **PDF Bookmarks** | Add hierarchical bookmarks to PDFs | `/bookmark_tool` |
| **PDF Merger** | Simple PDF merge and reorder | `/pdf_merger` |

---

## 1. PDF Bundle Creation Tool

### Overview
The main BunTool feature for creating professional court bundles that comply with English Court requirements.

### Features
- ✅ Merge multiple PDFs into a single bundle
- ✅ Generate table of contents (PDF or Word format)
- ✅ Add hyperlinked index
- ✅ Create page numbers with multiple styles
- ✅ Add hierarchical bookmarks
- ✅ Generate cover sheet with case details
- ✅ Support roman numerals for frontmatter
- ✅ Custom alphanumeric page numbering
- ✅ Page range mapping
- ✅ Export bundle with metadata as ZIP

### How to Use

1. **Access the tool**: Navigate to `http://127.0.0.1:7001/`

2. **Enter case details**:
   - Bundle title
   - Case name
   - Claim number (optional)
   - Date handling preference

3. **Upload PDFs**:
   - Click "Choose Files" or drag and drop
   - Reorder files as needed
   - Maximum 100MB per file

4. **Configure index**:
   - Manual entry: Add titles and page numbers
   - CSV upload: Bulk import index data
   - Font selection for index

5. **Select page numbering**:
   - Number only: `1`, `2`, `3`
   - Number with total: `1 of 50`
   - Page format: `Page 1` (default)
   - Page with total: `Page 1 of 50`
   - Custom alphanumeric: `A1`, `A2`, `B1`

6. **Choose options**:
   - Font: Charter, Helvetica, Times, Courier
   - Alignment: Left, Center, Right
   - Roman numerals for frontmatter
   - Footer prefix text

7. **Create bundle**: Click "Create Bundle"

8. **Download**: Get your professionally formatted PDF bundle

### Output Files
- **PDF Bundle**: Merged document with all features
- **ZIP Archive** (optional): Bundle + index CSV + metadata

### Page Numbering Styles

| Style | Example | Use Case |
|-------|---------|----------|
| Number only | `1` | Minimal formatting |
| Number with total | `1 of 50` | Show document length |
| Number with slash | `1/50` | Compact format |
| Page format | `Page 1` | Traditional style (default) |
| Page with total | `Page 1 of 50` | Full context |
| Custom alphanumeric | `A1`, `B2` | Tab dividers, exhibits |

### Cover Sheet Options
- Case name
- Claim number
- Bundle title
- Date (auto-generated or custom)
- Confidentiality markers

---

## 2. PDF Numbering Tool

### Overview
Standalone tool for adding custom page numbers to a single PDF without creating a full bundle.

**URL**: `http://127.0.0.1:7001/numbering_tool`

### Features
- ✅ All page numbering styles from Bundle Tool
- ✅ Custom alphanumeric numbering
- ✅ Page range mapping
- ✅ Font and alignment options
- ✅ Footer prefix support
- ✅ Fast processing (< 2 seconds for most PDFs)

### How to Use

1. **Upload PDF**: Select a single PDF file (max 100MB)

2. **Select numbering style**:
   - Number only
   - Number with total
   - Number with slash
   - Page format
   - Page with total
   - Custom alphanumeric

3. **Configure options**:
   - Font: Sans Serif (Helvetica), Serif (Times), Monospace (Courier), Charter
   - Alignment: Left, Centre, Right
   - Footer prefix (optional)

4. **Advanced options** (optional):
   - Custom alphanumeric prefix (e.g., "A", "Doc", "WS")
   - Reset mode: Sequential, Letter change, Custom interval
   - Page range mapping

5. **Process**: Click "ADD PAGE NUMBERS"

6. **Download**: Get `[filename]_numbered.pdf`

### Custom Alphanumeric Options

**Prefix**: Any text (e.g., "A", "Doc", "Tab")

**Reset Modes**:
- **Sequential**: A1, A2, A3, ..., A100
- **Letter change**: A1-A26, B1-B26, C1-C26
- **Custom interval**: Reset every N pages

**Example**: Prefix "Tab", Reset every 20 pages
- Pages 1-20: Tab1, Tab2, ..., Tab20
- Pages 21-40: Tab1, Tab2, ..., Tab20
- Pages 41-60: Tab1, Tab2, ..., Tab20

### Page Range Mapping

Map different page ranges to different prefixes:

```
1-20:A
21-50:B
51-100:C
```

Result:
- Pages 1-20: A1, A2, ..., A20
- Pages 21-50: B1, B2, ..., B30
- Pages 51-100: C1, C2, ..., C50

### Performance

| PDF Size | Processing Time |
|----------|-----------------|
| 1-10 pages | ~0.5s |
| 11-50 pages | ~1-2s |
| 51-100 pages | ~2-3s |
| 100+ pages | ~3-5s |

---

## 3. PDF Bookmark Tool

### Overview
Add hierarchical bookmarks to PDFs for improved navigation.

**URL**: `http://127.0.0.1:7001/bookmark_tool`

### Features
- ✅ Hierarchical bookmark structure (4 nesting levels)
- ✅ Per-bookmark styling (bold, italic)
- ✅ 6 bookmark colors
- ✅ Page-specific linking
- ✅ Dynamic form management
- ✅ Instant PDF download

### How to Use

1. **Upload PDF**: Select your PDF file

2. **Add bookmarks**:
   - Click "Add Bookmark"
   - Enter bookmark title
   - Enter page number
   - Select indent level (0-3)
   - Choose style (none, bold, italic, bold+italic)

3. **Configure settings**:
   - Bookmark color: Black, Red, Green, Blue, Purple, Orange
   - Global bold (optional)
   - Global italic (optional)

4. **Generate**: Click "Generate PDF with Bookmarks"

5. **Download**: Get your bookmarked PDF

### Bookmark Structure

**Indent Levels**:
- **Level 0**: Top-level chapters
- **Level 1**: Sections
- **Level 2**: Subsections
- **Level 3**: Sub-subsections

**Example**:
```
Chapter 1 (level 0, bold)
├─ Section 1.1 (level 1)
│  └─ Subsection 1.1.1 (level 2)
└─ Section 1.2 (level 1)
   ├─ Subsection 1.2.1 (level 2)
   └─ Subsection 1.2.2 (level 2)
```

### Bookmark Data Format

```javascript
{
  "title": "Chapter 1",        // Display text
  "page": 5,                   // Page number (1-based)
  "indent": 0,                 // Nesting level (0-3)
  "style": "bold"              // none|bold|italic|bold_italic
}
```

### Color Options

| Color | Hex | Use Case |
|-------|-----|----------|
| Black | #000000 | Default, professional |
| Red | #FF0000 | Important sections |
| Green | #00FF00 | Completed items |
| Blue | #0000FF | Standard sections |
| Purple | #800080 | Special sections |
| Orange | #FFA500 | Warnings, notes |

### Performance

| Scenario | Time |
|----------|------|
| Simple (1 bookmark) | ~0.1s |
| Moderate (10 bookmarks) | ~0.3s |
| Complex (50 bookmarks) | ~1s |

---

## 4. PDF Merger Tool

### Overview
Simple tool for merging and reordering PDF files.

**URL**: `http://127.0.0.1:7001/pdf_merger`

### Features
- ✅ Merge multiple PDFs
- ✅ Drag-and-drop reordering
- ✅ No numbering or bundling features
- ✅ Fast and simple

### How to Use

1. **Upload PDFs**: Select multiple PDF files

2. **Reorder** (optional): Drag and drop to reorder files

3. **Merge**: Click "Merge PDFs"

4. **Download**: Get merged PDF

### When to Use

- **Use Merger** when you only need to combine PDFs
- **Use Bundle Tool** when you need TOC, numbering, bookmarks

---

## Advanced Features

### Custom Alphanumeric Numbering

#### Overview
Add custom alphanumeric page numbers like "A1", "Doc1", "WS1" with intelligent reset modes.

#### Configuration Options

**1. Prefix**
- Any text string
- Examples: "A", "Doc", "Tab", "WS", "Exhibit"

**2. Reset Mode**

| Mode | Value | Behavior | Example |
|------|-------|----------|---------|
| Sequential | `none` | Never reset | A1, A2, ..., A100 |
| Letter change | `letter_change` | Reset every 26 pages | A1-A26, B1-B26 |
| Custom interval | `custom` | Reset every N pages | User-defined |

**3. Reset Interval** (for custom mode)
- Number of pages before resetting
- Example: 20 = reset every 20 pages

#### Use Cases

**Legal Exhibits**:
```
Prefix: "Ex"
Mode: Sequential
Result: Ex1, Ex2, Ex3, ..., Ex50
```

**Tabbed Documents**:
```
Prefix: "Tab"
Mode: Custom interval (15 pages)
Result: Tab1-Tab15, Tab1-Tab15, Tab1-Tab15
```

**Alphabetical Sections**:
```
Prefix: ""
Mode: Letter change
Result: A1-A26, B1-B26, C1-C26
```

**Witness Statements**:
```
Prefix: "WS"
Mode: Sequential
Result: WS1, WS2, WS3, ..., WS20
```

#### How It Works

**Sequential Mode**:
- Letter never changes
- Number increments continuously
- Best for simple continuous numbering

**Letter Change Mode**:
- Automatically increments letter every 26 pages
- Number resets 1-26 for each letter
- Best for natural alphabetical organization

**Custom Interval Mode**:
- Increments letter at specified interval
- Number resets at each interval
- Best for matching physical tab dividers

#### Algorithm

```python
def generate_custom_alpha_page_number(page_num, prefix, reset_mode, reset_interval):
    if reset_mode == "none":
        return f"{prefix}{page_num}"

    elif reset_mode == "letter_change":
        letter_index = (page_num - 1) // 26
        number = ((page_num - 1) % 26) + 1
        letter = chr(65 + letter_index)  # A, B, C, ...
        return f"{letter}{number}"

    elif reset_mode == "custom":
        letter_index = (page_num - 1) // reset_interval
        number = ((page_num - 1) % reset_interval) + 1
        letter = chr(65 + letter_index)
        return f"{letter}{number}"
```

---

### Page Range Mapping

#### Overview
Apply different numbering schemes to different page ranges within the same PDF.

#### Format

```
<start>-<end>:<prefix>
```

Multiple ranges separated by commas or newlines:

```
1-20:A
21-40:B
41-60:C
```

#### Examples

**Exhibit Organization**:
```
1-15:ExA
16-30:ExB
31-50:ExC
```
Result:
- Pages 1-15: ExA1, ExA2, ..., ExA15
- Pages 16-30: ExB1, ExB2, ..., ExB15
- Pages 31-50: ExC1, ExC2, ..., ExC20

**Document Sections**:
```
1-10:Intro
11-50:Main
51-60:Appendix
```
Result:
- Pages 1-10: Intro1 - Intro10
- Pages 11-50: Main1 - Main40
- Pages 51-60: Appendix1 - Appendix10

**Mixed Numbering**:
```
1-5:Cover
6-100:
```
Result:
- Pages 1-5: Cover1 - Cover5
- Pages 6-100: Standard numbering (e.g., Page 6, Page 7)

#### Rules

1. **Format**: Each range on a new line or comma-separated
2. **Gaps**: Unmapped pages use global numbering settings
3. **Overlaps**: First matching range takes precedence
4. **Prefix**: Can be any text (no special characters needed)
5. **Numbers**: Always 1-based within each range

#### Validation

- ✅ Start must be less than end
- ✅ Start and end must be positive integers
- ✅ Prefix can be empty (uses range-based numbering)
- ✅ Gaps are allowed (use global settings)
- ❌ Negative numbers not allowed
- ❌ Non-numeric ranges invalid

#### Integration

Works with:
- ✅ Bundle Creation Tool
- ✅ PDF Numbering Tool
- ✅ Custom alphanumeric numbering
- ✅ All page numbering styles

#### Processing Flow

```
1. Parse page range string
2. For each page in PDF:
   a. Check if page falls in any mapped range
   b. If yes: Use range-specific prefix + offset number
   c. If no: Use global numbering settings
3. Generate page number accordingly
```

---

## Quick Reference

### Tool Selection Guide

| Need | Use This Tool |
|------|---------------|
| Court bundle with TOC and bookmarks | Bundle Creation Tool |
| Add page numbers to single PDF | PDF Numbering Tool |
| Add navigation bookmarks | PDF Bookmark Tool |
| Just merge PDFs | PDF Merger Tool |
| Tab divider numbering (A1, B1) | Bundle/Numbering + Custom Alpha |
| Different numbering per section | Bundle/Numbering + Page Range Mapping |

### Common Workflows

**Legal Bundle**:
1. Use Bundle Creation Tool
2. Upload exhibits
3. Create CSV index
4. Select "Custom Alphanumeric" numbering
5. Set prefix to exhibit letters
6. Choose "Sequential" reset mode

**Tabbed Binder**:
1. Use PDF Numbering Tool
2. Upload compiled PDF
3. Select "Custom Alphanumeric"
4. Use page range mapping: `1-20:A, 21-40:B, 41-60:C`

**Bookmarked Document**:
1. Use PDF Bookmark Tool (if no numbering needed)
2. OR use Bundle Creation with bookmark generation

**Simple Merge**:
1. Use PDF Merger Tool
2. Upload PDFs
3. Reorder as needed
4. Merge

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Add bookmark | (Click "Add Bookmark" button) |
| Remove bookmark | (Click "Remove" on row) |
| Submit form | Enter (when in form field) |

### File Limits

| Item | Limit |
|------|-------|
| Max file size | 100 MB per file |
| Max total upload | Unlimited (but practical limits apply) |
| Supported formats | PDF only |
| Output format | PDF, ZIP (bundle tool) |

### Troubleshooting

**Issue**: Page numbers not visible
- **Solution**: Check alignment, try different font, verify PDF doesn't have opaque backgrounds

**Issue**: Bookmarks not appearing
- **Solution**: Verify page numbers are within PDF range, check bookmark was added to form

**Issue**: Custom numbering looks wrong
- **Solution**: Verify reset mode and interval settings, check page range mapping syntax

**Issue**: File upload fails
- **Solution**: Check file is PDF, size under 100MB, filename doesn't have special characters

**Issue**: Bundle creation errors
- **Solution**: Check all PDFs are valid, index data matches file count, no corrupted files

### Logging

All operations are logged to:
```
logs/buntool_{session_id}.log      # Bundle creation
logs/numbering_{session_id}.log    # Numbering tool
logs/                               # General app logs
```

Log files now have automatic rotation:
- Max size: 100MB per log file
- Backup count: 3 rotated files
- Total storage: 400MB per session

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main bundle creation interface |
| `/create_bundle` | POST | Process bundle creation |
| `/numbering_tool` | GET | Numbering tool interface |
| `/number_pdf_route` | POST | Process PDF numbering |
| `/bookmark_tool` | GET | Bookmark tool interface |
| `/add_bookmarks_route` | POST | Process bookmark addition |
| `/pdf_merger` | GET | PDF merger interface |
| `/merge_pdfs_route` | POST | Process PDF merge |

### Security Features

✅ File type validation (.pdf only)
✅ File size limits (100 MB)
✅ Filename sanitization
✅ Session-isolated processing
✅ Automatic file cleanup
✅ Input validation on all parameters
✅ Safe error messages (no info disclosure)

### Performance Optimization

- Files processed in temporary session directories
- Automatic cleanup after processing
- Streaming file downloads
- Efficient PDF processing with pikepdf
- ReportLab for fast page number generation

---

## Documentation Files

For more detailed information, see:

- **QUICK_START.md** - Quick start guide
- **USAGE_EXAMPLES.md** - Real-world usage examples
- **CUSTOM_NUMBERING_GUIDE.md** - Custom numbering deep dive
- **PAGE_RANGE_MAPPING*.md** - Page range mapping details
- **BOOKMARK_TOOL_*.md** - Bookmark tool documentation
- **PDF_NUMBERING_TOOL*.md** - Numbering tool documentation
- **DOCKER.md** - Docker deployment guide

---

**Version**: 1.0
**Last Updated**: January 2026
**Status**: Production Ready

All tools are fully tested, documented, and ready for production use.
