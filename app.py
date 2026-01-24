from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
# import sys
import bundle as buntool
import shutil
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import uuid
from datetime import datetime
from waitress import serve
import csv
#import boto3

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # file size limit in MB
app.logger.setLevel(logging.DEBUG)

# s3 = boto3.client('s3')
# bucket_name = os.environ.get('s3_bucket', 'your-default-bucket')


# def upload_to_s3(file_path, s3_key):
#     s3.upload_file(file_path, bucket_name, s3_key)
#     return f"s3://{bucket_name}/{s3_key}"


def is_running_in_lambda():
    return 'AWS_LAMBDA_FUNCTION_NAME' in os.environ  # seems to work?


if is_running_in_lambda():
    logs_dir = os.path.join(tempfile.gettempdir(), 'logs')
else:
    logs_dir = os.path.join('logs')
os.makedirs(logs_dir, exist_ok=True)

BUNDLES_DIR = os.path.join(tempfile.gettempdir(), 'buntool', 'bundles')
os.makedirs(BUNDLES_DIR, exist_ok=True)


def save_uploaded_file(file, directory, filename=None):
    # Takes in a file object, the tmpfiles directory path, and an optional filename.
    # passes the filename (supplied, or original) through secure_filename.
    # creates a filepath by joining the tmp directory and filename.
    # saves the file to the filepath
    # returns the filepath if successful, None if not.
    if file and file.filename:
        filename = secure_filename(filename) or secure_filename(file.filename)
        filepath = os.path.join(directory, filename)
        file.save(filepath)
        app.logger.debug(f"Saved file: {filepath}")
        return filepath
    return None


def strtobool(value: str) -> bool:
    value = value.lower()
    if value in ("y", "yes", "on", "1", "true", "t", "True", "enabled"):
        return True
    return False


def get_output_filename(bundle_title, case_name, timestamp, fallback="Bundle"):
    # Takes in the bundle title, case name, and a timestamp.
    # purpose is to guard against extra-long filenames.
    # Returns the output filename picked among many fallback options.
    output_file = f"{bundle_title}_{case_name}_{timestamp}.pdf"
    if len(output_file) > 100:
        # take first 20 chars of bundle title and add case name:
        output_file = f"{bundle_title[:20]}_{case_name}_{timestamp}.pdf"
    if len(output_file) > 100:
        # take first 20 chars of bundle title, first 20 chars of case name, and add timestamp:
        output_file = f"{bundle_title[:30]}_{case_name[:30]}_{timestamp}.pdf"
    if len(output_file) > 100:
        # this should never happen:
        output_file = f"{fallback}_{timestamp}.pdf"
    if len(output_file) > 100:
        # this should doubly never happen:
        output_file = f"{timestamp}.pdf"
    return output_file


def synchronise_csv_index(uploaded_csv_path, filename_mappings):
    # takes the path of the uploaded csv file and a dictionary of filename mappings (due to sanitising filenames of uploads).
    # creates a new csv file with the same structure as the original, but with the filenames replaced with secure versions.
    # returns the path of the new csv file.
    sanitised_filenames_csv_path = uploaded_csv_path.replace('index_', 'securefilenames_index_')
    app.logger.info(f"secure_csv_path: {sanitised_filenames_csv_path}")
    try:
        with open(uploaded_csv_path, 'r', newline='', encoding='utf-8') as infile:
            with open(sanitised_filenames_csv_path, 'w', newline='', encoding='utf-8') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                # print content of input csv:
                app.logger.debug(f"Reading input CSV:")
                # try:
                #     header = next(reader)
                #     app.logger.debug(f"[APP]-- Read header: {header}")
                #     writer.writerow(header)
                #     app.logger.debug(f"[APP]-- Wrote header")
                # except StopIteration:
                #     app.logger.error("[APP]-- CSV file is empty!")
                #     return

                for row in reader:
                    app.logger.debug(f"Processing row: {row}")
                    try:
                        if row[0] == 'Filename' and row[2] == 'Page':
                            app.logger.debug(f"..Found header row")
                            writer.writerow(row)
                            continue
                        if len(row) > 3 and row[3] == '1':
                            app.logger.debug(f"..Found section marker row")
                            writer.writerow(row)
                            continue

                        original_upload_filename = row[0]
                        secure_name = filename_mappings.get(original_upload_filename)
                        if secure_name is None:
                            secure_name = secure_filename(original_upload_filename)

                        row[0] = secure_name
                        writer.writerow(row)
                        app.logger.debug(f"..Wrote processed file row: {row}")
                    except Exception as e:
                        app.logger.error(f"..Error processing row {row}: {str(e)}")
                        raise

    except Exception as e:
        app.logger.error(f"..Error in save_csv_index: {str(e)}")
        raise

    app.logger.info(f"..saved csv index as {sanitised_filenames_csv_path}")
    return sanitised_filenames_csv_path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/numbering_tool')
def numbering_tool():
    return render_template('numbering_tool.html')


@app.route('/number_pdf', methods=['POST'])
def number_pdf_route():
    '''
    Route handler for the PDF numbering tool.
    Accepts a single PDF file and applies custom page numbering.
    '''
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    session_id = str(uuid.uuid4())[:8]
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    app.logger.debug(f"[NT]PDF Numbering Tool Called - Session: {session_id}")
    
    try:
        # Validate file input
        if 'pdf_file' not in request.files:
            return jsonify({"status": "error", "message": "No PDF file provided"}), 400
        
        pdf_file = request.files['pdf_file']
        if not pdf_file or pdf_file.filename == '':
            return jsonify({"status": "error", "message": "No PDF file selected"}), 400
        
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "File must be a PDF"}), 400
        
        # Create temporary working directory
        base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'
        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)

        # Set up logging
        logs_path = os.path.join(logs_dir, f'numbering_{session_id}.log')
        session_file_handler = RotatingFileHandler(
            logs_path,
            maxBytes=100*1024*1024,  # 100MB limit
            backupCount=3,            # Keep 3 backup files
            encoding='utf-8'
        )
        session_file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-[NT]: %(message)s')
        session_file_handler.setFormatter(formatter)
        app.logger.addHandler(session_file_handler)
        
        app.logger.info(f"[NT]Processing PDF: {pdf_file.filename}")
        
        # Save uploaded PDF
        secure_pdf_name = secure_filename(pdf_file.filename)
        input_pdf_path = os.path.join(temp_dir, secure_pdf_name)
        pdf_file.save(input_pdf_path)
        
        app.logger.info(f"[NT]Saved input PDF to: {input_pdf_path}")
        
        # Extract form parameters
        page_num_align = request.form.get('page_num_align', 'right')
        footer_font = request.form.get('footer_font', 'sans')
        page_num_style = request.form.get('page_num_style', 'page_x')
        footer_prefix = request.form.get('footer_prefix', '')
        custom_alpha_prefix = request.form.get('custom_alpha_prefix', '')
        custom_alpha_reset = request.form.get('custom_alpha_reset', 'none')
        custom_alpha_reset_interval = request.form.get('custom_alpha_reset_interval', '20')
        use_page_range_mapping = request.form.get('use_page_range_mapping', 'off') == 'on'
        page_range_mapping_input = request.form.get('page_range_mapping_input', '') if use_page_range_mapping else ''
        
        app.logger.debug(f"[NT]Form parameters:")
        app.logger.debug(f"[NT]....page_num_align: {page_num_align}")
        app.logger.debug(f"[NT]....footer_font: {footer_font}")
        app.logger.debug(f"[NT]....page_num_style: {page_num_style}")
        app.logger.debug(f"[NT]....footer_prefix: {footer_prefix}")
        app.logger.debug(f"[NT]....custom_alpha_prefix: {custom_alpha_prefix}")
        app.logger.debug(f"[NT]....custom_alpha_reset: {custom_alpha_reset}")
        app.logger.debug(f"[NT]....custom_alpha_reset_interval: {custom_alpha_reset_interval}")
        app.logger.debug(f"[NT]....use_page_range_mapping: {use_page_range_mapping}")
        if use_page_range_mapping:
            app.logger.debug(f"[NT]....page_range_mapping: ENABLED")
            app.logger.debug(f"[NT]....page_range_mapping_input: {page_range_mapping_input}")
        else:
            app.logger.debug(f"[NT]....page_range_mapping: DISABLED")
        
        # Prepare numbering options
        numbering_options = {
            'page_num_align': page_num_align,
            'footer_font': footer_font,
            'page_num_style': page_num_style,
            'footer_prefix': footer_prefix,
            'custom_alpha_prefix': custom_alpha_prefix,
            'custom_alpha_reset': custom_alpha_reset,
            'custom_alpha_reset_interval': int(custom_alpha_reset_interval) if custom_alpha_reset_interval else 20,
            'page_range_mapping_string': page_range_mapping_input,
            'temp_dir': temp_dir,
            'logs_dir': logs_dir,
            'session_id': session_id
        }
        
        # Create output PDF
        output_pdf_filename = secure_pdf_name.replace('.pdf', '_numbered.pdf')
        output_pdf_path = os.path.join(temp_dir, output_pdf_filename)
        
        app.logger.info(f"[NT]Calling number_single_pdf...")
        try:
            result_pdf_path = buntool.number_single_pdf(
                input_pdf_path,
                output_pdf_path,
                numbering_options
            )
        except Exception as e:
            app.logger.error(f"[NT]Error in number_single_pdf: {str(e)}")
            return jsonify({"status": "error", "message": f"Error processing PDF: {str(e)}"}), 500
        
        if not result_pdf_path or not os.path.exists(result_pdf_path):
            app.logger.error(f"[NT]Output PDF not found at {result_pdf_path}")
            return jsonify({"status": "error", "message": "Failed to process PDF"}), 500
        
        app.logger.info(f"[NT]PDF successfully numbered. Sending to client...")
        
        # Send file to client
        return send_file(
            result_pdf_path,
            as_attachment=True,
            download_name=output_pdf_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"[NT]Unexpected error in number_pdf_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
    
    finally:
        # Clean up temporary files
        try:
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[NT]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[NT]Could not clean up temporary files: {str(e)}")


@app.route('/bookmark_tool')
def bookmark_tool():
    """Display the PDF bookmark tool interface"""
    return render_template('bookmark_tool.html')


@app.route('/add_bookmarks', methods=['POST'])
def add_bookmarks_route():
    """Process PDF file and add custom bookmarks"""
    session_id = str(uuid.uuid4())[:8]
    temp_dir = None
    base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'
    
    try:
        # Validate file upload
        if 'pdf_file' not in request.files:
            return jsonify({"status": "error", "message": "No PDF file provided"}), 400
        
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            return jsonify({"status": "error", "message": "No PDF file selected"}), 400
        
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "File must be a PDF"}), 400
        
        # Create temporary directory
        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"[BT]Created temp directory: {temp_dir}")
        
        # Save uploaded PDF
        input_pdf_path = os.path.join(temp_dir, 'input.pdf')
        pdf_file.save(input_pdf_path)
        app.logger.info(f"[BT]Saved uploaded PDF to: {input_pdf_path}")
        
        # Extract bookmark data from JSON
        try:
            import json
            bookmarks_json = request.form.get('bookmarks_json', '[]')
            bookmarks_list = json.loads(bookmarks_json)
            app.logger.debug(f"[BT]Parsed {len(bookmarks_list)} bookmarks")
        except Exception as e:
            app.logger.error(f"[BT]Error parsing bookmarks: {str(e)}")
            return jsonify({"status": "error", "message": "Invalid bookmark data"}), 400
        
        # Extract bookmark settings
        bookmark_settings = {
            'color': request.form.get('bookmark_color', 'black'),
            'bold': request.form.get('bookmark_bold') == 'on',
            'italic': request.form.get('bookmark_italic') == 'on'
        }
        app.logger.debug(f"[BT]Bookmark settings: {bookmark_settings}")
        
        # Generate output filename
        output_pdf_filename = 'document_with_bookmarks.pdf'
        output_pdf_path = os.path.join(temp_dir, output_pdf_filename)
        
        # Process PDF with bookmarks using pdftk shell script
        app.logger.info(f"[BT]Starting to add bookmarks to PDF using pdftk shell script...")
        # Prepare arguments for shell script
        shell_script = os.path.join(os.path.dirname(__file__), 'add_bookmarks.sh')
        args = [shell_script, input_pdf_path, output_pdf_path]
        for bm in bookmarks_list:
            title = bm.get('title', 'Untitled')
            page = str(bm.get('page', 1))
            args.append(title)
            args.append(page)
        import subprocess
        app.logger.debug(f"[BT]Calling shell: {' '.join([repr(a) for a in args])}")
        result = subprocess.run(args, capture_output=True, text=True)
        app.logger.debug(f"[BT]Shell stdout: {result.stdout}")
        if result.returncode != 0:
            app.logger.error(f"[BT]Shell script failed: {result.stderr}")
            return jsonify({"status": "error", "message": f"Shell script failed: {result.stderr}"}), 500
        app.logger.info(f"[BT]Successfully added bookmarks to PDF using pdftk shell script")
        result_pdf_path = output_pdf_path
    
        # Send file to client
        return send_file(
            result_pdf_path,
            as_attachment=True,
            download_name=output_pdf_filename,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        app.logger.error(f"[BT]Unexpected error in add_bookmarks_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
    
    finally:
        # Clean up temporary files
        try:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[BT]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[BT]Could not clean up temporary files: {str(e)}")


@app.route('/pdf_merger')
def pdf_merger():
    """Display the PDF merger tool interface"""
    return render_template('pdf_merger_tool.html')


@app.route('/pdf_editor')
def pdf_editor():
    """Display the PDF editor tool interface"""
    return render_template('pdf_editor_tool.html')


@app.route('/pagination_tool')
def pagination_tool():
    """Display the PDF pagination and resizing tool interface"""
    return render_template('pagination_tool.html')


@app.route('/ocr_tool')
def ocr_tool():
    """Display the OCR tool interface"""
    return render_template('ocr_tool.html')


@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs_route():
    """Process and merge multiple PDF files"""
    session_id = str(uuid.uuid4())[:8]
    temp_dir = None
    base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'
    
    try:
        # Validate files
        if 'files' not in request.files:
            return jsonify({"status": "error", "message": "No PDF files provided"}), 400
        
        files = request.files.getlist('files')
        if len(files) < 2:
            return jsonify({"status": "error", "message": "At least 2 PDF files are required"}), 400
        
        # Validate file types
        for pdf_file in files:
            if not pdf_file.filename.lower().endswith('.pdf'):
                return jsonify({"status": "error", "message": f"Invalid file type: {pdf_file.filename}"}), 400
        
        # Create temporary directory
        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"[PM]Created temp directory: {temp_dir}")
        
        # Save uploaded PDFs in order
        input_pdf_paths = []
        for idx, pdf_file in enumerate(files):
            if pdf_file.filename == '':
                continue
            
            pdf_path = os.path.join(temp_dir, f'{idx:03d}_{secure_filename(pdf_file.filename)}')
            pdf_file.save(pdf_path)
            input_pdf_paths.append(pdf_path)
            app.logger.info(f"[PM]Saved PDF {idx + 1}: {pdf_file.filename}")
        
        if len(input_pdf_paths) < 2:
            return jsonify({"status": "error", "message": "At least 2 valid PDF files required"}), 400
        
        # Extract bookmark labels for each file
        bookmarks_dict = {}
        for idx in range(len(files)):
            bookmark_key = f'bookmark_{idx}'
            bookmark_label = request.form.get(bookmark_key, '')
            if bookmark_label and bookmark_label.strip():
                bookmarks_dict[idx] = bookmark_label.strip()
                app.logger.debug(f"[PM]Bookmark for file {idx}: {bookmark_label}")
        
        # Get output filename
        output_filename = request.form.get('outputFilename', 'merged_document.pdf')
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        
        output_pdf_path = os.path.join(temp_dir, output_filename)
        
        # Merge PDFs
        try:
            app.logger.info(f"[PM]Starting to merge {len(input_pdf_paths)} PDFs...")
            result_pdf_path = buntool.merge_pdfs_simple(
                input_pdf_paths,
                output_pdf_path,
                bookmarks_dict if bookmarks_dict else None
            )
            app.logger.info(f"[PM]Successfully merged PDFs")
        except Exception as e:
            app.logger.error(f"[PM]Error merging PDFs: {str(e)}")
            return jsonify({"status": "error", "message": f"Error merging PDFs: {str(e)}"}), 500
        
        # Send file to client
        return send_file(
            result_pdf_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"[PM]Unexpected error in merge_pdfs_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500
    
    finally:
        # Clean up temporary files
        try:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[PM]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[PM]Could not clean up temporary files: {str(e)}")


@app.route('/paginate_pdf', methods=['POST'])
def paginate_pdf_route():
    """Resize pages to a target size for a single PDF"""
    session_id = str(uuid.uuid4())[:8]
    temp_dir = None
    base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'

    try:
        if 'pdf_file' not in request.files:
            return jsonify({"status": "error", "message": "No PDF file provided"}), 400

        pdf_file = request.files['pdf_file']
        if not pdf_file or pdf_file.filename == '':
            return jsonify({"status": "error", "message": "No PDF file selected"}), 400

        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "File must be a PDF"}), 400

        page_size = request.form.get('page_size', 'A4')
        custom_width_mm = request.form.get('custom_width_mm', '').strip()
        custom_height_mm = request.form.get('custom_height_mm', '').strip()

        size_map = {
            'A4': (595.0, 842.0),
            'A3': (842.0, 1191.0),
            'LEGAL': (612.0, 1008.0),
            'LETTER': (612.0, 792.0),
        }

        if page_size == 'CUSTOM':
            try:
                width_mm = float(custom_width_mm)
                height_mm = float(custom_height_mm)
            except ValueError:
                return jsonify({"status": "error", "message": "Custom size must be numeric"}), 400

            if width_mm <= 0 or height_mm <= 0:
                return jsonify({"status": "error", "message": "Custom size must be positive"}), 400

            points_per_mm = 72.0 / 25.4
            target_width = width_mm * points_per_mm
            target_height = height_mm * points_per_mm
            size_label = "custom"
        else:
            size_key = page_size.upper()
            if size_key not in size_map:
                return jsonify({"status": "error", "message": "Invalid page size"}), 400
            target_width, target_height = size_map[size_key]
            size_label = size_key.lower()

        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"[PS]Created temp directory: {temp_dir}")

        input_pdf_path = os.path.join(temp_dir, secure_filename(pdf_file.filename))
        pdf_file.save(input_pdf_path)
        app.logger.info(f"[PS]Saved uploaded PDF to: {input_pdf_path}")

        output_filename = request.form.get('output_filename', '').strip()
        if not output_filename:
            base_name = os.path.splitext(pdf_file.filename)[0]
            output_filename = f"{base_name}_paginated_{size_label}.pdf"
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'

        output_pdf_path = os.path.join(temp_dir, secure_filename(output_filename))

        result_pdf_path = buntool.resize_pdf_to_page_size(
            input_pdf_path,
            output_pdf_path,
            target_width,
            target_height
        )

        if not result_pdf_path or not os.path.exists(result_pdf_path):
            return jsonify({"status": "error", "message": "Error creating resized PDF"}), 500

        return send_file(
            output_pdf_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        app.logger.error(f"[PS]Unexpected error in paginate_pdf_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

    finally:
        try:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[PS]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[PS]Could not clean up temporary files: {str(e)}")


@app.route('/ocr_pdf', methods=['POST'])
def ocr_pdf_route():
    """Apply OCR to a single PDF file"""
    session_id = str(uuid.uuid4())[:8]
    temp_dir = None
    base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'

    try:
        if 'pdf_file' not in request.files:
            return jsonify({"status": "error", "message": "No PDF file provided"}), 400

        pdf_file = request.files['pdf_file']
        if not pdf_file or pdf_file.filename == '':
            return jsonify({"status": "error", "message": "No PDF file selected"}), 400

        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "File must be a PDF"}), 400

        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"[OCR]Created temp directory: {temp_dir}")

        input_pdf_path = os.path.join(temp_dir, secure_filename(pdf_file.filename))
        pdf_file.save(input_pdf_path)
        app.logger.info(f"[OCR]Saved uploaded PDF to: {input_pdf_path}")

        output_filename = request.form.get('output_filename', '').strip()
        if not output_filename:
            base_name = os.path.splitext(pdf_file.filename)[0]
            output_filename = f"{base_name}_ocr.pdf"
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'

        output_pdf_path = os.path.join(temp_dir, secure_filename(output_filename))

        language = request.form.get('language', 'eng').strip() or 'eng'
        skip_text = request.form.get('skip_text', 'on') == 'on'
        deskew = request.form.get('deskew', 'on') == 'on'

        import sys
        ocr_command = ['ocrmypdf']
        ocr_args = [
            '--output-type', 'pdf',
            '--optimize', '1',
        ]
        if language:
            ocr_args += ['--language', language]
        if skip_text:
            ocr_args.append('--skip-text')
        if deskew:
            ocr_args.append('--deskew')

        ocr_args += [input_pdf_path, output_pdf_path]

        import subprocess
        try:
            full_args = ocr_command + ocr_args
            app.logger.debug(f"[OCR]Running: {' '.join(full_args)}")
            result = subprocess.run(full_args, capture_output=True, text=True)
        except FileNotFoundError:
            full_args = [sys.executable, '-m', 'ocrmypdf'] + ocr_args
            app.logger.debug(f"[OCR]Running fallback: {' '.join(full_args)}")
            result = subprocess.run(full_args, capture_output=True, text=True)
        if result.returncode != 0:
            app.logger.error(f"[OCR]OCR failed: {result.stderr}")
            return jsonify({"status": "error", "message": f"OCR failed: {result.stderr.strip()}"}), 500

        if not os.path.exists(output_pdf_path):
            app.logger.error(f"[OCR]OCR output missing: {output_pdf_path}")
            combined_output = (result.stdout or "") + "\n" + (result.stderr or "")
            return jsonify({
                "status": "error",
                "message": "OCR did not produce an output file.",
                "details": combined_output.strip()
            }), 500

        with open(output_pdf_path, 'rb') as output_handle:
            pdf_bytes = output_handle.read()

        from io import BytesIO
        return send_file(
            BytesIO(pdf_bytes),
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )

    except FileNotFoundError:
        return jsonify({
            "status": "error",
            "message": "OCR tool not found. Please install ocrmypdf and tesseract (see scripts/install_ubuntu_deps.sh)."
        }), 500
    except Exception as e:
        app.logger.error(f"[OCR]Unexpected error in ocr_pdf_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

    finally:
        try:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[OCR]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[OCR]Could not clean up temporary files: {str(e)}")


@app.route('/edit_pdf', methods=['POST'])
def edit_pdf_route():
    """Process a single PDF file with reordering, deletion, and rotation edits"""
    session_id = str(uuid.uuid4())[:8]
    temp_dir = None
    base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'

    try:
        if 'pdf_file' not in request.files:
            return jsonify({"status": "error", "message": "No PDF file provided"}), 400

        pdf_file = request.files['pdf_file']
        if not pdf_file or pdf_file.filename == '':
            return jsonify({"status": "error", "message": "No PDF file selected"}), 400

        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "File must be a PDF"}), 400

        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"[PE]Created temp directory: {temp_dir}")

        input_pdf_path = os.path.join(temp_dir, secure_filename(pdf_file.filename))
        pdf_file.save(input_pdf_path)
        app.logger.info(f"[PE]Saved uploaded PDF to: {input_pdf_path}")

        import json
        edits_json = request.form.get('edits_json', '{}')
        try:
            edits = json.loads(edits_json)
        except Exception as e:
            app.logger.error(f"[PE]Invalid edits JSON: {str(e)}")
            return jsonify({"status": "error", "message": "Invalid edit data"}), 400

        page_order = edits.get('page_order', [])
        rotations = edits.get('rotations', {})

        if not isinstance(page_order, list) or not page_order:
            return jsonify({"status": "error", "message": "No page order supplied"}), 400

        # Normalize rotations keys to int
        try:
            rotations_map = {int(k): int(v) for k, v in rotations.items()}
        except Exception:
            return jsonify({"status": "error", "message": "Invalid rotation data"}), 400

        from pikepdf import Pdf

        with Pdf.open(input_pdf_path) as src_pdf:
            total_pages = len(src_pdf.pages)
            if any((not isinstance(p, int)) for p in page_order):
                return jsonify({"status": "error", "message": "Invalid page order"}), 400

            # Enforce unique page numbers within range
            if len(set(page_order)) != len(page_order):
                return jsonify({"status": "error", "message": "Duplicate pages in order"}), 400

            for page_num in page_order:
                if page_num < 1 or page_num > total_pages:
                    return jsonify({"status": "error", "message": "Page out of range"}), 400

            for page_num, rotation in rotations_map.items():
                if page_num < 1 or page_num > total_pages:
                    return jsonify({"status": "error", "message": "Rotation page out of range"}), 400
                if rotation % 90 != 0:
                    return jsonify({"status": "error", "message": "Rotation must be a multiple of 90"}), 400

            output_filename = request.form.get('output_filename', '').strip()
            if not output_filename:
                base_name = os.path.splitext(pdf_file.filename)[0]
                output_filename = f"{base_name}_edited.pdf"
            if not output_filename.lower().endswith('.pdf'):
                output_filename += '.pdf'

            output_pdf_path = os.path.join(temp_dir, secure_filename(output_filename))

            edited_pdf = Pdf.new()
            for page_num in page_order:
                page = src_pdf.pages[page_num - 1]
                rotation = rotations_map.get(page_num, 0)
                if rotation:
                    current_rotation = int(page.get('/Rotate', 0))
                    page.Rotate = (current_rotation + rotation) % 360
                edited_pdf.pages.append(page)

            edited_pdf.save(output_pdf_path)
            app.logger.info(f"[PE]Saved edited PDF to: {output_pdf_path}")

        return send_file(
            output_pdf_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        app.logger.error(f"[PE]Unexpected error in edit_pdf_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

    finally:
        try:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[PE]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[PE]Could not clean up temporary files: {str(e)}")


@app.route('/version_compare')
def version_compare():
    """Display the PDF version comparison tool interface"""
    return render_template('version_compare_tool.html')


@app.route('/compare_pdfs_route', methods=['POST'])
def compare_pdfs_route():
    """Process two PDF files and generate comparison report"""
    session_id = str(uuid.uuid4())[:8]
    temp_dir = None
    base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'

    try:
        # Validate file uploads
        if 'pdf_file_1' not in request.files or 'pdf_file_2' not in request.files:
            return jsonify({"status": "error", "message": "Two PDF files are required"}), 400

        pdf_file_1 = request.files['pdf_file_1']
        pdf_file_2 = request.files['pdf_file_2']

        if pdf_file_1.filename == '' or pdf_file_2.filename == '':
            return jsonify({"status": "error", "message": "Both files must be selected"}), 400

        if not (pdf_file_1.filename.lower().endswith('.pdf') and pdf_file_2.filename.lower().endswith('.pdf')):
            return jsonify({"status": "error", "message": "Both files must be PDFs"}), 400

        # Create temporary directory
        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"[VC]Created temp directory: {temp_dir}")

        # Set up logging
        logs_path = os.path.join(logs_dir, f'version_compare_{session_id}.log')
        session_file_handler = RotatingFileHandler(
            logs_path, maxBytes=100*1024*1024, backupCount=3, encoding='utf-8'
        )
        session_file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-[VC]: %(message)s')
        session_file_handler.setFormatter(formatter)
        app.logger.addHandler(session_file_handler)

        # Save uploaded PDFs
        pdf1_path = os.path.join(temp_dir, secure_filename(pdf_file_1.filename))
        pdf2_path = os.path.join(temp_dir, secure_filename(pdf_file_2.filename))

        pdf_file_1.save(pdf1_path)
        pdf_file_2.save(pdf2_path)

        app.logger.info(f"[VC]Saved PDFs: {pdf_file_1.filename}, {pdf_file_2.filename}")

        # Get comparison options
        ignore_whitespace = request.form.get('ignore_whitespace') == 'on'

        # Early exit check: if files are identical
        import filecmp
        if filecmp.cmp(pdf1_path, pdf2_path, shallow=False):
            app.logger.info(f"[VC]Files are byte-for-byte identical")
            return jsonify({
                "status": "success",
                "message": "The files are identical (byte-for-byte match). No differences found."
            })

        # Perform text comparison
        app.logger.info(f"[VC]Starting text comparison (ignore_whitespace={ignore_whitespace})...")
        text_results = buntool.compare_pdfs_text(pdf1_path, pdf2_path, ignore_whitespace)

        # Perform structural comparison
        app.logger.info(f"[VC]Starting structural comparison...")
        structure_results = buntool.compare_pdfs_structure(pdf1_path, pdf2_path)

        # Generate HTML report
        report_filename = f'comparison_report_{session_id}.html'
        report_path = os.path.join(temp_dir, report_filename)

        app.logger.info(f"[VC]Generating HTML report...")
        buntool.generate_comparison_html(text_results, structure_results, report_path)

        if not os.path.exists(report_path):
            return jsonify({"status": "error", "message": "Error generating comparison report"}), 500

        app.logger.info(f"[VC]Report generated successfully. Sending to client...")

        # Send HTML file to client
        return send_file(
            report_path,
            as_attachment=True,
            download_name=report_filename,
            mimetype='text/html'
        )

    except Exception as e:
        app.logger.error(f"[VC]Unexpected error in compare_pdfs_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

    finally:
        # Clean up temporary files
        try:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[VC]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[VC]Could not clean up temporary files: {str(e)}")


@app.route('/metadata_cleaner')
def metadata_cleaner():
    """Display the PDF metadata cleaner tool interface"""
    return render_template('metadata_cleaner_tool.html')


@app.route('/clean_metadata_route', methods=['POST'])
def clean_metadata_route():
    """Process PDF file and remove privacy-sensitive metadata"""
    session_id = str(uuid.uuid4())[:8]
    temp_dir = None
    base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'

    try:
        # Validate file upload
        if 'pdf_file' not in request.files:
            return jsonify({"status": "error", "message": "No PDF file provided"}), 400

        pdf_file = request.files['pdf_file']

        if pdf_file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400

        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "File must be a PDF"}), 400

        # Create temporary directory
        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"[MC]Created temp directory: {temp_dir}")

        # Set up logging
        logs_path = os.path.join(logs_dir, f'metadata_cleaner_{session_id}.log')
        session_file_handler = RotatingFileHandler(
            logs_path, maxBytes=100*1024*1024, backupCount=3, encoding='utf-8'
        )
        session_file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-[MC]: %(message)s')
        session_file_handler.setFormatter(formatter)
        app.logger.addHandler(session_file_handler)

        # Save uploaded PDF
        input_pdf_path = os.path.join(temp_dir, secure_filename(pdf_file.filename))
        pdf_file.save(input_pdf_path)

        app.logger.info(f"[MC]Saved PDF: {pdf_file.filename}")

        # Get cleaning options from form
        options = {
            'remove_metadata': request.form.get('remove_metadata') == 'on',
            'remove_xmp': request.form.get('remove_xmp') == 'on',
            'remove_annotations': request.form.get('remove_annotations') == 'on',
            'remove_bookmarks': request.form.get('remove_bookmarks') == 'on',
            'anonymize_dates': request.form.get('anonymize_dates') == 'on'
        }

        app.logger.info(f"[MC]Cleaning options: {options}")

        # Generate output filename
        original_name = os.path.splitext(secure_filename(pdf_file.filename))[0]
        output_filename = f"{original_name}_cleaned.pdf"
        output_pdf_path = os.path.join(temp_dir, output_filename)

        # Clean metadata
        app.logger.info(f"[MC]Starting metadata cleaning...")
        result = buntool.clean_pdf_metadata(input_pdf_path, output_pdf_path, options)

        if not result['success']:
            return jsonify({"status": "error", "message": result['message']}), 500

        if not os.path.exists(output_pdf_path):
            return jsonify({"status": "error", "message": "Error generating cleaned PDF"}), 500

        app.logger.info(f"[MC]Metadata cleaned successfully: {result['message']}")

        # Send cleaned PDF to client
        return send_file(
            output_pdf_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        app.logger.error(f"[MC]Unexpected error in clean_metadata_route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

    finally:
        # Clean up temporary files
        try:
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                app.logger.debug(f"[MC]Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            app.logger.warning(f"[MC]Could not clean up temporary files: {str(e)}")


@app.route('/create_bundle', methods=['GET', 'POST'])
def create_bundle():
    if request.method == 'GET':
        return render_template('index.html')

    timestamp = buntool.datetime.now().strftime('%Y%m%d_%H%M%S')
    session_id = str(uuid.uuid4())[:8]
    user_agent = request.headers.get('User-Agent')
    app.logger.debug(f"******************APP HEARS A CALL******************")
    app.logger.debug(f"New session ID: {session_id} {user_agent}")
    # check if csv has been passed:

    # check whether input files are actually povided:
    if 'files' not in request.files:
        app.logger.error(f"Cannot create bundle: No files found in form submission")
        return jsonify({"status": "error", "message": "No files found. Please add files and try again."})

    try:
        # Create temporary working directory in /tmp/tempfiles/{session_id}:
        base_dir = tempfile.gettempdir() if is_running_in_lambda() else '.'
        temp_dir = os.path.join(base_dir, 'tempfiles', session_id)
        os.makedirs(temp_dir, exist_ok=True)
        app.logger.debug(f"Temporary directory created: {temp_dir}")

        # Add RotatingFileHandler for session-specific logging
        logs_path = os.path.join(logs_dir, f'buntool_{session_id}.log')
        session_file_handler = RotatingFileHandler(
            logs_path,
            maxBytes=100*1024*1024,  # 100MB limit
            backupCount=3,            # Keep 3 backup files
            encoding='utf-8'
        )
        session_file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-[APP]: %(message)s')
        session_file_handler.setFormatter(formatter)
        app.logger.addHandler(session_file_handler)

        # Get form data
        # Ingest csv index
        app.logger.debug(f"Ingesting form information...")
        if request.files.get('csv_index'):
            app.logger.info(f"..index file found in form submission")
            app.logger.info(f"..index data: {request.files.get('csv_index')}")
        else:
            app.logger.info(f"..No CSV index found.")

        # ingest other form data:
        bundle_title = request.form.get('bundle_title', 'Bundle') if request.form.get('bundle_title') else 'Bundle'
        case_name = request.form.get('case_name')
        claim_no = request.form.get('claim_no')
        page_num_align = request.form.get('page_num_align')
        footer_font = request.form.get('footer_font')
        index_font = request.form.get('index_font')
        page_num_style = request.form.get('page_num_style')
        footer_prefix = request.form.get('footer_prefix')
        confidential_bool = request.form.get('confidential_bool')
        date_setting = request.form.get('date_setting')
        roman_for_preface = bool(strtobool(request.form.get('roman_for_preface')))
        # Custom alphanumeric numbering parameters
        custom_alpha_prefix = request.form.get('custom_alpha_prefix', '')
        custom_alpha_reset = request.form.get('custom_alpha_reset', 'none')
        custom_alpha_reset_interval = request.form.get('custom_alpha_reset_interval', '20')
        # Page range mapping
        use_page_range_mapping = request.form.get('use_page_range_mapping', 'off') == 'on'
        page_range_mapping_input = request.form.get('page_range_mapping_input', '') if use_page_range_mapping else ''
        case_details = [bundle_title, claim_no, case_name]
        zip_bool = True  # option not implemented for GUI control.
        bookmark_setting = request.form.get('bookmark_setting')

        output_file = get_output_filename(bundle_title, case_name, timestamp, footer_prefix)
        app.logger.debug(f"generated output filename: {output_file}")

        # Save uploaded files
        app.logger.debug(f"Gathering uploaded files...")
        files = request.files.getlist('files')
        # check whether files exceed max allowed overall size of MAX_CONTENT_LENGTH:
        total_size = sum([f.content_length for f in files])
        if total_size > app.config['MAX_CONTENT_LENGTH']:
            app.logger.error(
                f"Total size of files exceeds maximum allowed size: {total_size} > {app.config['MAX_CONTENT_LENGTH']}")
            return jsonify({"status": "error",
                            "message": f"Total size of files exceeds maximum allowed size: {total_size} > {app.config['MAX_CONTENT_LENGTH']}"})
        app.logger.debug(f"....{files}")
        input_files = []
        filename_mappings = {}
        for file in files:
            app.logger.debug(f"..Processing {file.filename}")
            if file.filename:
                secure_name = secure_filename(file.filename)
                filename_mappings[file.filename] = secure_name
                # app.logger.debug(f"[{session_id}-{timestamp}-APP]--filename_mappings: {filename_mappings}")
                filepath = save_uploaded_file(file, temp_dir, secure_name)
                if filepath:
                    input_files.append(filepath)
            else:
                app.logger.error(f"..No filename found for {file}")
            if not os.path.exists(filepath):
                app.logger.error(f"File not found at: {filepath}")
            else:
                app.logger.info(f"..File saved to: {filepath}")

        # Save coversheet if provided
        secure_coversheet_filename = None
        if 'coversheet' in request.files and request.files['coversheet'].filename != '':
            app.logger.debug(f"Coversheet found in form submission")
            cover_file = request.files['coversheet']
            # if cover_file and cover_file.filename:
            # Generate a secure and unique filename for coversheet
            secure_coversheet_filename = secure_filename(f'coversheet_{session_id}_{timestamp}.pdf')
            coversheet_filepath = save_uploaded_file(cover_file, temp_dir, secure_coversheet_filename)
            app.logger.debug(f"Coversheet path: {coversheet_filepath}")
        else:
            app.logger.debug(f"No coversheet found in form submission")

        # Save CSV index
        saved_csv_path = ""
        if 'csv_index' in request.files:
            app.logger.debug(f"CSV index found in form submission: {request.files['csv_index']}")
            csv_file = request.files['csv_index']
            if csv_file and csv_file.filename:
                secure_csv_filename = secure_filename(f'index_{session_id}_{timestamp}.csv')
                saved_csv_path = save_uploaded_file(csv_file, temp_dir, secure_csv_filename)
                # if secure_csv_path:
                # permanent_csv_path = os.path.join(temp_dir, secure_csv_filename)
                sanitised_filenames_index_csv = synchronise_csv_index(saved_csv_path, filename_mappings)
        else:
            app.logger.debug(f"No CSV index found in form submission")
            sanitised_filenames_index_csv = None
        if not os.path.exists(saved_csv_path):
            app.logger.error(f"CSV file not found at: {saved_csv_path}")
            return jsonify(
                {"status": "error", "message": f"Index data did not upload correctly. Session code: {session_id}"}), 400
        else:
            app.logger.debug(f"CSV saved to: {saved_csv_path}")

        # Create bundle - main function call
        try:
            app.logger.info(f"Calling buntool.create_bundle with params:")
            app.logger.info(f"....input_files: {input_files}")
            app.logger.info(f"....output_file: {output_file}")
            app.logger.info(f"....secure_coversheet_filename: {secure_coversheet_filename}")
            app.logger.info(f"....sanitised_filenames_index_csv: {sanitised_filenames_index_csv}")
            app.logger.info(f"....bundle_config elements:")
            app.logger.info(f"........timestamp: {timestamp}")
            app.logger.info(f"........case_details: {case_details}")
            app.logger.info(f"........confidential_bool: {confidential_bool}")
            app.logger.info(f"........zip_bool: {zip_bool}")
            app.logger.info(f"........session_id: {session_id}")
            app.logger.info(f"........user_agent: {user_agent}")
            app.logger.info(f"........page_num_align: {page_num_align}")
            app.logger.info(f"........index_font: {index_font}")
            app.logger.info(f"........footer_font: {footer_font}")
            app.logger.info(f"........page_num_style: {page_num_style}")
            app.logger.info(f"........footer_prefix: {footer_prefix}")
            app.logger.info(f"........date_setting: {date_setting}")
            app.logger.info(f"........roman_for_preface: {roman_for_preface}")
            app.logger.info(f"........custom_alpha_prefix: {custom_alpha_prefix}")
            app.logger.info(f"........custom_alpha_reset: {custom_alpha_reset}")
            app.logger.info(f"........custom_alpha_reset_interval: {custom_alpha_reset_interval}")
            if use_page_range_mapping:
                app.logger.info(f"........page_range_mapping: ENABLED")
                app.logger.debug(f"........page_range_mapping_input: {page_range_mapping_input[:100]}")
            app.logger.info(f"........temp_dir: {temp_dir}")
            app.logger.info(f"........logs_dir: {logs_dir}")
            app.logger.info(f"........bookmark_setting: {bookmark_setting}")
            # Create BundleConfig instance
            bundle_config = buntool.BundleConfig(
                timestamp=timestamp,
                case_details=case_details,
                csv_string=None,
                confidential_bool=confidential_bool,
                zip_bool=zip_bool,
                session_id=session_id,
                user_agent=user_agent,
                page_num_align=page_num_align,
                index_font=index_font,
                footer_font=footer_font,
                page_num_style=page_num_style,
                footer_prefix=footer_prefix,
                date_setting=date_setting,
                roman_for_preface=roman_for_preface,
                temp_dir=temp_dir,
                logs_dir=logs_dir,
                bookmark_setting=bookmark_setting,
                custom_alpha_prefix=custom_alpha_prefix,
                custom_alpha_reset=custom_alpha_reset,
                custom_alpha_reset_interval=custom_alpha_reset_interval,
                page_range_mapping_string=page_range_mapping_input
            )

            received_output_file, zip_file_path = buntool.create_bundle(
                input_files,
                output_file,
                secure_coversheet_filename,
                sanitised_filenames_index_csv,
                bundle_config
            )

            # Copy both files to bundles folder
            if os.path.exists(received_output_file):
                final_output_path = os.path.join(BUNDLES_DIR, os.path.basename(received_output_file))
                shutil.copy2(received_output_file, final_output_path)
                app.logger.debug(f"Copied final PDF to: {final_output_path}")
            else:
                app.logger.error(f"PDF file not found at: {received_output_file}")
                return jsonify({"status": "error",
                                "message": f"Error preparing PDF file for download. Session code: {session_id}"}), 500

            if os.path.exists(zip_file_path):
                final_zip_path = os.path.join(BUNDLES_DIR, os.path.basename(zip_file_path))
                shutil.copy2(zip_file_path, final_zip_path)
                app.logger.debug(f"Copied final ZIP to: {final_zip_path}")
            else:
                app.logger.error(f"ZIP file not found at: {zip_file_path}")
                return jsonify(
                    {"status": "error", "message": f"Error creating ZIP archive. Session code: {session_id}"}), 500

            return jsonify({
                "status": "success",
                "message": "Bundle created successfully!",
                "bundle_path": final_output_path,
                "zip_path": final_zip_path
            })

        except Exception as e:
            app.logger.error(f"Fatal Error creating bundle: {str(e)}")
            return jsonify(
                {"status": "error", "message": "Fatal error creating bundle. Session code: {session_id}"}), 500

    except Exception as e:
        app.logger.error(f"Fatal Error in processing bundle: {str(e)}")
        return jsonify(
            {"status": "error", "message": f"Fatal error in creating bundle. Session code: {session_id}"}), 500

    finally:
        # Remove the session FileHandler to prevent duplicate logs
        if session_file_handler and session_file_handler in app.logger.handlers:
            app.logger.removeHandler(session_file_handler)

        # try:
        #     # Upload logs to s3:
        #     # As mentioned in the frontend, logs are always uploaded to s3, and the
        #     # only private info they contain are is user agent and index
        #     # data (basically, filenames and titles):
        #     logsurl = upload_to_s3(logs_path, f'logs/{os.path.basename(logs_path)}')
        #     # By contrast, the zip file has all the input files and the output bundle
        #     # itself. It almost certainly contains private data.
        #     # In the /dev/ instance it's uploaded to s3 for testing purposes
        #     # and regularly cleaned out.It is disabled in stable version by commenting
        #     # out the following lin, but is left uncommented here for tranparency:
        #     #upload_to_s3(final_zip_path, f'bundles/{os.path.basename(final_zip_path)}')
        #     app.logger.debug(f"Upload to s3 successful: {logsurl}")
        # except Exception as e:
        #     app.logger.error(f"Error uploading logs or zip to s3: {str(e)}")
        #     pass


@app.route('/download/bundle', methods=['GET'])
def download_bundle():
    bundle_path = request.args.get('path')
    if not bundle_path:
        return jsonify({"status": "error", "message": f"Download Error: Bundle download path could not be found."}), 400

    absolute_path = os.path.abspath(bundle_path)
    if not os.path.exists(absolute_path):
        return jsonify(
            {"status": "error", "message": f"Download Error: bundle does not exist in expected location."}), 404

    return send_file(absolute_path, as_attachment=True)


@app.route('/download/zip', methods=['GET'])
def download_zip():
    zip_path = request.args.get('path')
    if not zip_path:
        return jsonify({"status": "error", "message": f"Download Error: Zip download path could not be found."}), 400

    absolute_path = os.path.abspath(zip_path)
    if not os.path.exists(absolute_path):
        return jsonify({"status": "error", "message": f"Download Error: zip does not exist in expected location."}), 404

    return send_file(absolute_path, as_attachment=True)


@app.route('/TOOLS.md')
def serve_tools_documentation():
    """Serve the TOOLS.md documentation file."""
    tools_md_path = os.path.join(os.path.dirname(__file__), 'TOOLS.md')
    if os.path.exists(tools_md_path):
        return send_file(tools_md_path, mimetype='text/markdown')
    else:
        return "Documentation not found", 404


if __name__ == '__main__':
    app.logger.debug(f"APP - Server started on port 7001 -- Hello.")
    serve(app, host='0.0.0.0', port=7001, threads=4, connection_limit=100, channel_timeout=120)
