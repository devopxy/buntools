# Custom Alphanumeric Numbering - Usage Examples

## Real-World Scenarios

### Scenario 1: Legal Document Bundles with Section Markers
**Use Case:** A court bundle with multiple sections, each needs separate numbering

**Configuration:**
- Numbering Style: Custom Alphanumeric
- Prefix: "Pt" (for "Part")
- Reset Mode: Letter per 26 pages

**Result:**
```
Pt A1 (Part A, page 1)
Pt A2 (Part A, page 2)
...
Pt A26 (Part A, page 26)
Pt B1 (Part B, page 1)
Pt B2 (Part B, page 2)
```

**Benefit:** Easy to reference parts in court proceedings ("see Pt B5")

---

### Scenario 2: Multi-Tab Document Set
**Use Case:** Each physical tab in a printed bundle has its own numbering

**Configuration:**
- Numbering Style: Custom Alphanumeric
- Prefix: "" (empty)
- Reset Mode: Reset every 20 pages

**Result:**
```
Tab 1 (pages 1-20):   A1, A2, ..., A20
Tab 2 (pages 21-40):  B1, B2, ..., B20
Tab 3 (pages 41-60):  C1, C2, ..., C20
```

**Benefit:** Physical tabs align with PDF numbering

---

### Scenario 3: Witness Statement Bundle
**Use Case:** Each witness statement has separate numbering

**Configuration:**
- Numbering Style: Custom Alphanumeric
- Prefix: "WS" (for Witness Statement)
- Reset Mode: Sequential

**Result:**
```
WS1, WS2, WS3, ..., WS150
```

**Benefit:** Simple sequential numbering with prefix for clarity

---

### Scenario 4: Trial Bundle with Document Classes
**Use Case:** Different document types in separate sections

**Configuration per section:**
- Section A (Pleadings): Prefix="Plead", Reset="Sequential"
  - Result: Plead1, Plead2, Plead3, ...
  
- Section B (Evidence): Prefix="Ev", Reset="Letter change (every 26)"
  - Result: EvA1, EvA2, ..., EvA26, EvB1, ...
  
- Section C (Judgment): Prefix="J", Reset="Every 30 pages"
  - Result: JA1-JA30, JB1-JB30, JC1-JC30, ...

**Benefit:** Each section clearly identified with appropriate numbering scheme

---

## Advanced Use Cases

### Use Case: Tab Index Integration
**Problem:** Need to print tabs with matching PDF numbering

**Solution:**
1. Determine how many pages per physical tab
2. Set Reset Mode to "Reset every N pages"
3. Match N with your physical tab page count
4. Print tabs labeled A, B, C, etc.
5. Print PDF with matching pagination

**Example:**
- 5 physical tabs, 40 pages total (~8 pages per tab)
- Set: Custom Alpha, Prefix="", Reset every 8 pages
- Result: A1-A8, B1-B8, C1-C8, D1-D8, E1-E8
- Print tabs labeled A, B, C, D, E

---

### Use Case: Reference System for Emails
**Problem:** Need to cite pages in correspondence

**Solution:**
Use meaningful prefix that appears in emails

**Configuration:**
- Prefix: "RE-" (for document reference)
- Reset: Sequential
- Result: RE-1, RE-2, RE-3, ..., RE-100

**Benefit:** Easy to write in emails: "see page RE-47"

---

## Comparison: When to Use Which Mode

| Reset Mode | Best For | Example |
|-----------|----------|---------|
| Sequential | Simple, continuous numbering | "Doc1" through "Doc500" |
| Letter Change | Natural 26-page grouping | "EvA1-EvA26, EvB1-EvB26" |
| Custom Interval | Matching physical tabs or sections | 20-page sections: "A1-A20, B1-B20" |

---

## Tips & Tricks

### Tip 1: International Characters
**Can I use numbers in other languages?**
Currently optimized for English letters (A-Z). Works with any text prefix though:
- "第1章1" (Japanese: Chapter 1)
- "Chapitre1" (French: Chapter)
- Custom prefixes work with any UTF-8 text

### Tip 2: Longer Prefixes
**What if I use a 10-character prefix?**
No problem! Any length prefix works:
- Prefix: "EVIDENCE-TAB" → "EVIDENCE-TAB1", "EVIDENCE-TAB2", ...

### Tip 3: Combining with Other Settings
**Can I use custom numbering with roman preface?**
Yes! Complete compatibility:
- Preface uses roman numerals: i, ii, iii, ...
- Main content uses custom alpha: A1, A2, A3, ...
- Frontmatter offset is automatically calculated

### Tip 4: Font Styling
**Does font selection affect custom numbering?**
No, custom numbering works with all fonts:
- Traditional (Charter)
- Serif (Times)
- Sans-serif (Helvetica)
- Mono (Courier)

### Tip 5: Pre-numbering Your Files
**Can I use custom numbering with CSV index?**
Yes, completely independent:
- CSV index determines document titles and descriptions
- Custom numbering only affects the footer page numbers
- Both work together seamlessly

---

## Common Mistakes & Solutions

### ❌ Mistake 1: Forgetting Reset Interval
- **Problem:** Selected "Reset every N pages" but didn't set interval
- **Solution:** Always ensure interval is set when using custom reset

### ❌ Mistake 2: Very Long Prefix + Long Bundles
- **Problem:** "VeryLongPrefix100" takes up too much footer space
- **Solution:** Keep prefix short (1-3 characters) for long bundles

### ❌ Mistake 3: Mixing Reset Modes
- **Problem:** Expecting "letter change" to reset at intervals
- **Solution:** Choose ONE reset mode; they don't combine

### ❌ Mistake 4: Not Accounting for Frontmatter
- **Problem:** Expected first document to be "A1" but got offset
- **Solution:** This is correct! Frontmatter has different numbering (roman numerals or no number)

---

## Logging & Troubleshooting

When custom numbering is used, the bundle creation log will show:

```
....Page numbering style: custom_alpha
....Custom alpha prefix: A
....Custom alpha reset mode: letter_change
```

Check the log file (located in `logs/buntool_[SESSION_ID].log`) to verify your settings were correctly passed through.

---

## Future Enhancement Ideas

1. **Reverse Numbering**: Z1, Z2 down to A1, A2
2. **Roman + Alpha**: i, ii, iii in preface; A1, A2 in main
3. **Custom Separators**: "A-1" instead of "A1", "A_1", etc.
4. **Multi-Part Prefixes**: "Chapter-A-1", "Chapter-B-1"
5. **Auto-Prefix from Metadata**: Derive prefix from PDF metadata or CSV data

---

## Contact & Support

**Ojas Capital Limited**
Email: [info@ojascapital.co.uk](mailto:info@ojascapital.co.uk)

---

**Copyright © 2026 Ojas Capital Limited** | Based on original work by Tristan Sherliker

---

# PDF Editor & Pagination Tool - Usage Examples

## PDF Editor Tool Examples

### Example 1: Fix a Scanned Document Order
**Use Case:** A scan came in with pages out of order and one extra page.

**Steps:**
1. Open **PDF Editor Tool** (`/pdf_editor`)
2. Drag pages into the correct order
3. Delete the unwanted page
4. Download the edited PDF

**Result:** Clean, correctly ordered document.

---

### Example 2: Rotate Landscape Pages
**Use Case:** Some pages are sideways after scanning.

**Steps:**
1. Upload the PDF
2. Rotate affected pages left/right
3. Download the edited PDF

**Result:** All pages upright and readable.

---

## PDF Pagination & Page Size Tool Examples

### Example 1: Convert to A4 with Page Numbers
**Use Case:** A mixed-size PDF needs to be standardized for court filing.

**Configuration:**
- Page size: **A4**

**Result:** All pages resized to A4 with consistent sizing.

---

### Example 2: Legal Size with "X of Y"
**Use Case:** A Legal-sized document must be standardized for printing.

**Configuration:**
- Page size: **Legal**

**Result:** Legal-sized pages with consistent dimensions.

---

### Example 3: Custom Page Size (mm)
**Use Case:** A document needs to match a custom print template.

**Configuration:**
- Page size: **Custom**
- Width: **180 mm**
- Height: **250 mm**

**Result:** PDF resized to the exact custom dimensions.

---

## PDF OCR Tool Examples

### Example 1: Make a Scanned PDF Searchable
**Use Case:** You scanned a bundle and need text search before filing.

**Configuration:**
- Language: `eng`
- Skip pages with text: **On**
- Deskew: **On**

**Result:** Searchable PDF with a text layer.

---

### Example 2: Bilingual Document (English + French)
**Use Case:** A document contains English and French text.

**Configuration:**
- Language: `eng+fra`
- Skip pages with text: **On**
- Deskew: **On**

**Result:** Searchable bilingual PDF with accurate OCR for both languages.

---

## PDF Version Comparison Tool Examples

### Example 1: Compare Contract Revisions
**Use Case:** Client sent revised contract. You need to identify all changes before approval.

**Process:**
1. Upload original contract as **Version 1**
2. Upload revised contract as **Version 2**
3. Enable "Ignore whitespace differences"
4. Click "Compare PDFs"

**Result:**
- HTML report showing:
  - Summary: 12% of pages changed (6 out of 50)
  - Modified pages: 6 (with line-by-line diffs)
  - Metadata changes: Author changed from "Smith & Co" to "Jones LLP"
  - Page count: Same (50 pages)

**Benefit:** Quickly spot all changes without manual review. Color-coded highlighting makes differences obvious.

---

### Example 2: Verify Final vs. Draft Bundle
**Use Case:** Before filing, verify final bundle matches approved draft.

**Process:**
1. Upload draft bundle (approved version) as **Version 1**
2. Upload final bundle (to be filed) as **Version 2**
3. Disable "Ignore whitespace" (want exact match)
4. Click "Compare PDFs"

**Result:**
- HTML report showing:
  - Summary: 0% changed
  - Status: "The files are identical (byte-for-byte match). No differences found."

**Benefit:** Confidence that final version hasn't been accidentally modified.

---

### Example 3: Track Exhibit Changes
**Use Case:** Witness statement was updated. Find what changed.

**Process:**
1. Upload original witness statement as **Version 1**
2. Upload updated witness statement as **Version 2**
3. Enable "Ignore whitespace differences"
4. Click "Compare PDFs"

**Result:**
- HTML report showing:
  - Summary: 8% changed (2 out of 25 pages)
  - Page 5: Paragraph 12 modified (dates corrected)
  - Page 18: New paragraph added (additional detail)
  - Metadata: ModDate updated to new timestamp

**Benefit:** See exactly what witness changed in their statement. Generate audit trail.

---

### Example 4: Compare Bundle Versions for Court
**Use Case:** Court requested comparison of two submitted bundle versions.

**Process:**
1. Upload Version A (first submission) as **Version 1**
2. Upload Version B (corrected submission) as **Version 2**
3. Enable "Ignore whitespace differences"
4. Generate comparison report

**Result:**
- Downloadable HTML report showing:
  - Pages added: 2 (new exhibits)
  - Pages removed: 0
  - Pages modified: 5 (corrections to existing exhibits)
  - Bookmark changes: 2 new bookmarks for new exhibits
  - Full diff for each changed page

**Benefit:** Provide court with objective, detailed change report. Demonstrates transparency.

---

### Example 5: Quality Assurance Check
**Use Case:** QA process requires comparing produced document to specifications.

**Process:**
1. Upload specification/template as **Version 1**
2. Upload actual produced document as **Version 2**
3. Disable "Ignore whitespace" (spacing matters)
4. Generate report

**Result:**
- Identify any deviations from template
- Verify all required sections present
- Check formatting consistency
- Document compliance for records

**Benefit:** Systematic QA verification. Audit trail for compliance.

---

## PDF Metadata Cleaner Tool Examples

### Example 1: Clean Document Before Court Filing
**Use Case:** Remove law firm metadata before filing with court.

**Process:**
1. Upload PDF to metadata cleaner
2. Select recommended options (all checked by default):
   - ✅ Remove Document Metadata
   - ✅ Remove XMP Metadata
   - ✅ Anonymize Dates
3. Leave optional items unchecked:
   - ☐ Remove Annotations
   - ☐ Remove Bookmarks
4. Click "Clean PDF Metadata"

**What Gets Removed:**
- Author: "John Smith, Smith & Associates"
- Creator: "Microsoft Word 2021"
- Producer: "Adobe Acrobat DC 2023.006"
- Company: "Smith & Associates LLP"
- Title: "CONFIDENTIAL DRAFT - Jones v. Smith Brief"
- Keywords: "privileged, work product, draft"
- CreationDate: Set to 1970-01-01
- ModDate: Set to 1970-01-01

**What's Preserved:**
- Document content (text, images, formatting)
- Bookmarks/table of contents
- Page numbers
- Hyperlinks
- Form fields

**Result:** `brief_cleaned.pdf` with no identifying metadata. Safe for public filing.

**Benefit:** Protect attorney work product. Prevent metadata disclosure. Comply with e-filing rules.

---

### Example 2: Anonymize Document for Blind Review
**Use Case:** Submit expert report for peer review without revealing author.

**Process:**
1. Upload expert report PDF
2. Enable all five cleaning options:
   - ✅ Remove Document Metadata
   - ✅ Remove XMP Metadata
   - ✅ Anonymize Dates
   - ✅ Remove Annotations
   - ✅ Remove Bookmarks
3. Click "Clean PDF Metadata"

**What Gets Removed:**
- All author/creator information
- Internal comments and review notes
- Bookmarks (may contain identifying section names)
- Document history
- Software fingerprints
- Timestamps

**Additional Steps:**
- Manually redact author name from document text
- Remove headers/footers with firm name
- Rename file to generic name

**Result:** Completely anonymized document suitable for double-blind review.

**Benefit:** Ensure fair, unbiased peer review process.

---

### Example 3: Public Records Release (FOIA Compliance)
**Use Case:** Government agency responding to FOIA request needs to clean metadata.

**Process:**
1. Upload responsive document
2. Select options:
   - ✅ Remove Document Metadata (remove employee names)
   - ✅ Remove XMP Metadata (remove workflow info)
   - ✅ Anonymize Dates (if timestamps not public record)
   - ☐ Remove Annotations (preserve redactions if any)
   - ☐ Remove Bookmarks (preserve if helpful)
3. Click "Clean PDF Metadata"

**What Gets Removed:**
- Employee names in Author/Creator fields
- Internal software systems (Producer field)
- Department/organization names
- File creation workflows
- Document history

**What's Preserved:**
- Redactions (if implemented as annotations)
- Document structure
- Official content
- Accessibility features

**Result:** Document suitable for public release without privacy concerns.

**Benefit:** FOIA compliance. Privacy protection. Regulatory adherence.

---

### Example 4: Remove Internal Comments Before Sharing
**Use Case:** Share draft agreement with opposing counsel. Remove internal review notes.

**Process:**
1. Upload draft agreement with comments
2. Select options:
   - ✅ Remove Document Metadata
   - ✅ Remove XMP Metadata
   - ✅ Anonymize Dates
   - ✅ Remove Annotations (this removes comments!)
   - ☐ Remove Bookmarks (preserve navigation)
3. Click "Clean PDF Metadata"

**What Gets Removed:**
- Internal review comments
- Highlight markup
- Sticky notes
- Editing annotations
- Version history
- Track changes metadata

**Warning:**
- Save a copy BEFORE cleaning
- Annotations contain important review feedback
- Only clean when sharing externally

**Result:** Clean document without internal work product or privileged communications.

**Benefit:** Prevent accidental disclosure of privileged information or work product.

---

### Example 5: Maximum Privacy Cleaning
**Use Case:** High-stakes litigation. Opposing counsel known for metadata mining. Remove everything.

**Process:**
1. Upload document
2. Enable **ALL** options:
   - ✅ Remove Document Metadata
   - ✅ Remove XMP Metadata
   - ✅ Anonymize Dates
   - ✅ Remove Annotations
   - ✅ Remove Bookmarks
3. Click "Clean PDF Metadata"

**Additional Manual Steps:**
1. **Before cleaning:**
   - Save original with all metadata for your records
   - Extract and save bookmarks separately if needed
   - Document all annotations in separate file

2. **After cleaning:**
   - Verify metadata removed using PDF properties
   - Check with ExifTool or PDFtk for confirmation
   - Rename file to generic name (e.g., `exhibit_001.pdf`)
   - Review actual content for embedded metadata
   - Consider flattening form fields if present

3. **Verification checklist:**
   ```bash
   # Linux/macOS command line verification
   exiftool exhibit_001_cleaned.pdf
   pdftk exhibit_001_cleaned.pdf dump_data
   ```
   - Check Author: Should be blank/Unknown
   - Check Creator: Should be blank/Unknown
   - Check ModDate: Should be 1970-01-01
   - Check for XMP streams: Should be absent

**Result:** Minimally-metadata PDF with maximum privacy protection.

**Benefit:** Eliminate metadata-based discovery. Protect sensitive case strategy. Prevent fingerprinting.

---

### Example 6: Batch Cleaning Multiple Exhibits
**Use Case:** Need to clean 50 exhibits for production. Manual process too slow.

**Process (per file):**
1. Upload each exhibit one at a time
2. Use same settings for all:
   - ✅ Remove Document Metadata
   - ✅ Remove XMP Metadata
   - ✅ Anonymize Dates
   - ☐ Remove Annotations (preserve if redactions present)
   - ☐ Remove Bookmarks (preserve navigation)
3. Download each cleaned file

**Naming Convention:**
- Original: `2024-01-15_Email_CEO_CFO.pdf`
- Cleaned: `2024-01-15_Email_CEO_CFO_cleaned.pdf`
- Rename to: `Exhibit_A_001.pdf`

**Quality Control:**
- Spot-check 10% of cleaned files
- Verify metadata removal with PDF properties
- Test one file with ExifTool
- Ensure document content unchanged

**Result:** Clean exhibit set ready for production with no metadata leaks.

**Benefit:** Systematic, repeatable process. Quality assurance. Audit trail.

---

## Contact & Support

**Ojas Capital Limited**
Email: [info@ojascapital.co.uk](mailto:info@ojascapital.co.uk)

---

**Copyright © 2026 Ojas Capital Limited** | Based on original work by Tristan Sherliker

**Result:** OCR recognizes both languages and preserves readability.
