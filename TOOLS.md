# Court Bundle Tools - Tools Documentation

Complete guide to all tools and features available in Court Bundle Tools.

---

## Table of Contents

1. [Overview](#overview)
2. [PDF Bundle Creation Tool](#1-pdf-bundle-creation-tool)
3. [PDF Numbering Tool](#2-pdf-numbering-tool)
4. [PDF Bookmark Tool](#3-pdf-bookmark-tool)
5. [PDF Merger Tool](#4-pdf-merger-tool)
6. [PDF Editor Tool](#5-pdf-editor-tool)
7. [PDF Pagination & Page Size Tool](#6-pdf-pagination--page-size-tool)
8. [PDF OCR Tool](#7-pdf-ocr-tool)
9. [PDF Version Comparison Tool](#8-pdf-version-comparison-tool)
10. [PDF Metadata Cleaner Tool](#9-pdf-metadata-cleaner-tool)
11. [Advanced Features](#advanced-features)
    - [Custom Alphanumeric Numbering](#custom-alphanumeric-numbering)
    - [Page Range Mapping](#page-range-mapping)
12. [Quick Reference](#quick-reference)

---

## Overview

Court Bundle Tools provides nine main tools for PDF manipulation, plus advanced features for complex document bundling needs:

| Tool | Purpose | URL |
|------|---------|-----|
| **Bundle Creation** | Create professional court bundles with TOC, numbering, and bookmarks | `/` (main page) |
| **PDF Numbering** | Add custom page numbers to a single PDF | `/numbering_tool` |
| **PDF Bookmarks** | Add hierarchical bookmarks to PDFs | `/bookmark_tool` |
| **PDF Merger** | Simple PDF merge and reorder | `/pdf_merger` |
| **PDF Editor** | Reorder, delete, and rotate pages | `/pdf_editor` |
| **PDF Pagination & Size** | Resize pages to standard/custom sizes | `/pagination_tool` |
| **PDF OCR** | Make scanned PDFs searchable | `/ocr_tool` |
| **PDF Version Comparison** | Compare two PDF versions and highlight differences | `/version_compare` |
| **PDF Metadata Cleaner** | Remove privacy-sensitive metadata from PDFs | `/metadata_cleaner` |

---

## 1. PDF Bundle Creation Tool

### Overview
The main Court Bundle Tools feature for creating professional court bundles that comply with English Court requirements.

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

## 5. PDF Editor Tool

### Overview
Edit a single PDF by reordering, deleting, and rotating pages.

**URL**: `http://127.0.0.1:7001/pdf_editor`

### Features
- ✅ Drag-and-drop reordering
- ✅ Delete pages
- ✅ Rotate pages left/right
- ✅ Page thumbnails preview
- ✅ Fast download of edited PDF

### How to Use

1. **Upload PDF**: Select a single PDF file
2. **Reorder pages**: Drag page cards to the desired order
3. **Rotate**: Use rotate buttons to adjust orientation
4. **Delete**: Remove any page you don't want
5. **Download**: Click "Apply edits and download"

### When to Use

- Clean up scanned bundles
- Reorder exhibits
- Fix landscape pages

---

## 6. PDF Pagination & Page Size Tool

### Overview
Resize pages to a standard or custom page size.

**URL**: `http://127.0.0.1:7001/pagination_tool`

### Features
- ✅ Resize to A4, A3, Legal, or Letter
- ✅ Custom size in millimeters

### How to Use

1. **Upload PDF**: Select a single PDF file
2. **Choose target size**: A4, A3, Legal, Letter, or Custom (mm)
3. **Download**: Click "Create paginated PDF"

### Notes

- Pages are scaled to fit the target size and centered.
- Output file is a new PDF; original file is unchanged.

---

## 7. PDF OCR Tool

### Overview
Add an OCR text layer to scanned PDFs to make them searchable.

**URL**: `http://127.0.0.1:7001/ocr_tool`

### Features
- ✅ OCR for scanned PDFs
- ✅ Skip pages that already contain text
- ✅ Deskew scanned pages
- ✅ Language selection (Tesseract language codes)

### How to Use

1. **Upload PDF**: Select a scanned PDF
2. **Choose language**: Default is `eng` (English). You can use `eng+fra`, `deu`, etc.
3. **Options**:
   - Skip pages with existing text (recommended)
   - Deskew pages
4. **Download**: Click "Run OCR" to get a searchable PDF

### Notes
- Requires `ocrmypdf`, `tesseract-ocr`, and `ghostscript` on the host system.
- Install additional language packs for non-English OCR.

---

## 8. PDF Version Comparison Tool

### Overview
Compare two PDF versions and generate a detailed HTML report showing text differences, structural changes, and metadata variations.

**URL**: `http://127.0.0.1:7001/version_compare`

### Features
- ✅ **Text Comparison**: Page-by-page text extraction and diff generation
- ✅ **Structural Comparison**: Metadata, bookmarks, page count differences
- ✅ **HTML Report**: Standalone, downloadable HTML report with embedded CSS
- ✅ **Summary Statistics**: High-level overview of changes
- ✅ **Detailed Page-by-Page**: Collapsible sections for each modified page
- ✅ **Unified Diff Format**: Industry-standard diff output
- ✅ **Color-Coded Highlighting**: Green (added), red (removed), yellow (modified)
- ✅ **Whitespace Normalization**: Optional ignore whitespace differences

### How to Use

1. **Upload Version 1 (Original)**:
   - Select the original/older PDF file
   - Maximum file size: 100 MB

2. **Upload Version 2 (Modified)**:
   - Select the modified/newer PDF file
   - Maximum file size: 100 MB

3. **Select Options**:
   - **Ignore whitespace differences**: Recommended for formatted documents
   - Normalizes whitespace before comparison

4. **Compare PDFs**:
   - Click "Compare PDFs" button
   - Processing time depends on file size (typically 2-30 seconds)

5. **Download Report**:
   - Automatically downloads HTML report
   - Open in any web browser
   - No internet connection required

### Report Structure

The generated HTML report contains:

#### Summary Section
- **Percentage Changed**: Overall change percentage
- **Total Changes**: Count of modified/added/removed pages
- **Page Difference**: Net change in page count
- **Statistics**: Identical, modified, added, and removed pages

#### Structural Differences
- **File Information**: Size comparison, page counts
- **Metadata Differences**: Author, title, creation date, etc.
- **Bookmark Differences**: Added/removed bookmarks with page numbers

#### Page-by-Page Comparison
- **Collapsible Sections**: Click to expand details for each page
- **Unified Diff**: Line-by-line changes in standard diff format
- **Side-by-Side View**: Preview of text from both versions
- **Statistics**: Lines added/removed per page
- **Navigation**: Sticky navigation bar for quick access

### Use Cases

**Legal Documents**:
- Compare contract revisions
- Track changes between draft versions
- Identify modifications in legal briefs
- Verify final vs. draft documents

**Court Bundles**:
- Compare bundle versions before filing
- Identify changes in exhibits
- Track updates to witness statements
- Verify pagination changes

**Compliance**:
- Document version control
- Change tracking for audits
- Regulatory filing comparisons
- Quality assurance checks

### Tips & Best Practices

**Before Comparing**:
- Ensure both files are text-searchable (not scanned images)
- Use OCR tool first if files are scanned
- Check file sizes (under 100 MB recommended)
- Use descriptive filenames for clarity

**Comparison Options**:
- Enable "Ignore whitespace" for documents with formatting changes
- Disable for documents where spacing is significant

**Interpreting Results**:
- Green = content added in Version 2
- Red = content removed from Version 1
- Yellow = content modified between versions
- Gray = identical content (not shown in detailed view)

**Performance**:
- Small files (10 pages): ~2 seconds
- Medium files (50 pages): ~10 seconds
- Large files (100+ pages): ~30 seconds

### Limitations

- **Text-based comparison only**: Does not detect visual/image differences
- **Scanned PDFs**: Requires OCR before comparison
- **No content reflow detection**: Shows textual changes, not formatting
- **File size limit**: 100 MB per file
- **Language**: Works best with left-to-right text

### Technical Details

**Comparison Algorithm**:
- Uses `pdfplumber` for text extraction
- Python `difflib` for unified diff generation
- pikepdf for metadata and bookmark extraction
- pypdf for document properties parsing

**Output Format**:
- Standalone HTML file
- Embedded CSS (no external dependencies)
- Responsive design (mobile-friendly)
- Jinja2 templating

---

## 9. PDF Metadata Cleaner Tool

### Overview
Remove privacy-sensitive metadata from PDF files to protect confidential information and comply with privacy requirements.

**URL**: `http://127.0.0.1:7001/metadata_cleaner`

### Features
- ✅ **Document Metadata Removal**: Author, title, subject, keywords, creator, producer
- ✅ **XMP Metadata Removal**: Extended metadata including Adobe XMP, Dublin Core
- ✅ **Date Anonymization**: Set creation/modification dates to epoch time (1970-01-01)
- ✅ **Optional Annotation Removal**: Remove comments, highlights, sticky notes
- ✅ **Optional Bookmark Removal**: Remove document outline/table of contents
- ✅ **Preserves Content**: Does not modify text, images, or page structure
- ✅ **Detailed Report**: Shows exactly what was removed

### How to Use

1. **Upload PDF**:
   - Select a PDF file to clean
   - Maximum file size: 100 MB

2. **Select Cleaning Options**:

   **Recommended Options (Default: ON)**:
   - ✅ **Remove Document Metadata**: Strips title, author, subject, keywords, creator, producer
   - ✅ **Remove XMP Metadata**: Removes extended metadata (Adobe XMP, Dublin Core, custom fields)
   - ✅ **Anonymize Dates**: Sets creation/modification dates to 1970-01-01 instead of removing them

   **Optional Cleaning (Default: OFF)**:
   - ☐ **Remove Annotations**: Removes comments, highlights, sticky notes (may affect usability)
   - ☐ **Remove Bookmarks**: Removes document outline/TOC (may affect navigation)

3. **Clean PDF**:
   - Click "Clean PDF Metadata" button
   - Processing is fast (typically <2 seconds)

4. **Download Cleaned PDF**:
   - Automatically downloads file with "_cleaned" suffix
   - Example: `contract.pdf` → `contract_cleaned.pdf`

### What Gets Removed

#### Document Properties (Standard Metadata)
The following fields are removed when "Remove Document Metadata" is enabled:

- **Title**: Document title
- **Author**: Creator/author name
- **Subject**: Document subject/description
- **Keywords**: Search keywords and tags
- **Creator**: Application that created the document
- **Producer**: PDF generation software
- **Company**: Organization name (if present)
- **SourceModified**: Original file modification info
- **Trapped**: PDF trapping information

#### XMP Metadata (Extended Metadata)
When "Remove XMP Metadata" is enabled, removes:

- Adobe XMP metadata stream
- Dublin Core metadata
- Custom metadata fields
- Extended properties
- Rights management information
- Document history

#### Dates
When "Anonymize Dates" is enabled:

- **CreationDate**: Set to `D:19700101000000Z` (January 1, 1970)
- **ModDate**: Set to `D:19700101000000Z`

This preserves the date fields (some systems require them) while removing actual timestamp information.

#### Annotations (Optional)
When "Remove Annotations" is enabled:

- Comments and text notes
- Highlights and underlines
- Sticky notes
- Stamps and shapes
- Form field comments
- Review markup

⚠️ **Warning**: Removing annotations may affect document usability if they contain important information.

#### Bookmarks (Optional)
When "Remove Bookmarks" is enabled:

- Document outline/table of contents
- Nested bookmark structure
- All bookmark destinations

⚠️ **Warning**: Removing bookmarks may make navigation difficult in long documents.

### Use Cases

**Legal Documents**:
- Remove lawyer/firm identifying information before filing
- Strip metadata before discovery production
- Clean documents before sharing with opposing counsel
- Anonymize author information for blind review

**Court Submissions**:
- Ensure no metadata leaks sensitive information
- Comply with court e-filing requirements
- Remove internal comments before filing
- Strip version history and edit tracking

**Public Disclosure**:
- Clean documents before FOIA/public records release
- Remove internal organizational information
- Strip employee names and identifiers
- Anonymize creation software/workflow

**Privacy Compliance**:
- GDPR compliance for document sharing
- Remove personal identifying information
- Data minimization for external sharing
- Pseudonymization of authored documents

**Evidence Handling**:
- Strip metadata that could compromise investigation
- Remove identifying information from exhibits
- Clean documents before expert review
- Anonymize sources for sensitive cases

### Tips & Best Practices

**Before Cleaning**:
- **Make a backup**: Always keep the original file
- **Review content**: Ensure no sensitive info in actual text/images
- **Check requirements**: Verify what metadata your recipient needs
- **Test functionality**: Ensure bookmarks/annotations aren't critical

**Recommended Settings**:
- For **general use**: Enable all three recommended options (metadata, XMP, dates)
- For **maximum privacy**: Enable all five options
- For **court filing**: Enable metadata and XMP only (preserve bookmarks)
- For **internal review**: Enable metadata only (preserve dates for tracking)

**After Cleaning**:
- **Verify the result**: Open cleaned PDF and check functionality
- **Inspect metadata**: Use PDF properties to confirm cleaning
- **Test navigation**: If bookmarks were removed, verify TOC
- **Check annotations**: If removed, ensure no critical info lost

**What Won't Be Removed**:
- Text content in the PDF
- Images and graphics
- Page structure and layout
- Fonts and formatting
- Form fields (unless annotations are removed)
- Digital signatures (preserved separately)

### Verification

To verify metadata has been removed:

**Adobe Acrobat**:
1. File → Properties → Description tab
2. Check that fields are empty or show "Unknown"
3. Additional Metadata → Show all fields

**Preview (macOS)**:
1. Tools → Show Inspector
2. Check Info tab for empty fields

**PDFtk**:
```bash
pdftk input_cleaned.pdf dump_data
```

**ExifTool**:
```bash
exiftool input_cleaned.pdf
```

### Limitations

- **Does not remove text**: Sensitive info in actual document content is not affected
- **Does not remove images**: Photos, logos, signatures remain unchanged
- **Does not sanitize filenames**: Rename file separately if needed
- **Does not remove digital signatures**: Signature metadata preserved
- **Does not affect permissions**: File permissions/restrictions unchanged

### Technical Details

**Implementation**:
- Uses `pikepdf` library for PDF manipulation
- Direct metadata stream modification
- XMP removal at PDF object level
- Date anonymization preserves field structure

**Performance**:
- Small files (<1 MB): <1 second
- Medium files (1-10 MB): 1-2 seconds
- Large files (10-100 MB): 2-5 seconds

**Compatibility**:
- Works with PDF versions 1.3-2.0
- Preserves PDF/A compliance (if dates not anonymized)
- Compatible with all major PDF readers
- Maintains file structure integrity

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
| Reorder/rotate/delete pages | PDF Editor Tool |
| Resize to A4/A3/Legal/Custom | PDF Pagination & Size Tool |
| Make scanned PDFs searchable | PDF OCR Tool |
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

---

## Contact & Support

**Ojas Capital Limited**
Email: [info@ojascapital.co.uk](mailto:info@ojascapital.co.uk)

---

## License & Attribution

Licensed under the Mozilla Public License, version 2.0.

**Copyright Information**:
- **Current Maintainer**: Copyright © 2026 Ojas Capital Limited
- **Original Author**: Based on original work by Tristan Sherliker and contributors to BunTool
