from flask import Flask, request, send_file, send_from_directory
import subprocess
import os
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
import uuid
import os

from flask_cors import CORS



app = Flask(__name__, static_folder='static')

CORS(app)  # Enables CORS globally


@app.before_request
def block_prefetch():
    if request.headers.get('Purpose') == 'prefetch':
        return '', 403

from flask import render_template

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/claims-tatva')
def claims_tatva():
    return render_template('claims-tatva.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sw.js')
def serve_sw():
    return send_from_directory('.', 'sw.js')

ROBOTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'robots.txt')
with open(ROBOTS_PATH, encoding='utf-8') as f:
    ROBOTS_CONTENT = f.read()

@app.route('/robots.txt')
def serve_robots():
    from flask import Response
    response = Response(ROBOTS_CONTENT, mimetype='text/plain')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

from flask import Response
import os

@app.route('/sitemap.xml')
def serve_sitemap():
    try:
        file_path = os.path.join(app.static_folder, 'site-index.xml')
        if not os.path.exists(file_path):
            return "Sitemap file not found", 404
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype="application/xml")
    except Exception as e:
        return f"Error serving sitemap: {e}", 500




@app.route('/compress', methods=['POST'])
def compress_pdf():
    uploaded_file = request.files.get('pdf')
    if not uploaded_file:
        return "No file uploaded", 400

    # Debug logging
    print("User-Agent:", request.headers.get('User-Agent'))
    print("File name:", uploaded_file.filename)
    print("File size (bytes):", len(uploaded_file.read()))
    uploaded_file.seek(0)  # Reset pointer

    input_path = 'input.pdf'
    output_path = 'compressed.pdf'
    uploaded_file.save(input_path)

    try:
        # Open PDF with PyMuPDF
        doc = fitz.open(input_path)

        # Save compressed PDF, preserving metadata and images
        doc.save(output_path, deflate=True, clean=True)
        doc.close()

        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"compressed-{uploaded_file.filename}"
        )

    except Exception as e:
        print(e)
        return "Compression failed", 500

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)


@app.route('/3ctool')
def serve_3ctool():
    return render_template('3ctool/index.html')

@app.route('/gpstool')
def serve_gpstool():
    return render_template('gpstool/index.html')


@app.route("/pdf2excel", methods=["POST"])
def pdf_to_excel():
    file = request.files.get("pdf")
    password = request.form.get("password") or None
    mode = request.form.get("mode")  # "consolidated" or "separate"

    if not file:
        return "No PDF uploaded", 400

    temp_pdf = f"/tmp/{uuid.uuid4()}.pdf"
    output_xlsx = f"/tmp/{uuid.uuid4()}.xlsx"
    file.save(temp_pdf)

    try:
        with pdfplumber.open(temp_pdf, password=password) as pdf:
            all_tables = []
            header = None

            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    if mode == "consolidated":
                        if header is None:
                            header = table[0]
                        all_tables.extend(table[1:])
                    else:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        all_tables.append(df)

        if mode == "consolidated":
            df = pd.DataFrame(all_tables, columns=header)
            df.to_excel(output_xlsx, index=False)
        else:
            with pd.ExcelWriter(output_xlsx) as writer:
                for i, df in enumerate(all_tables):
                    df.to_excel(writer, sheet_name=f"Page{i+1}", index=False)

        return send_file(output_xlsx, as_attachment=True, download_name="output.xlsx")

    except Exception as e:
        return f"❌ Error: {str(e)}", 500
    finally:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
        if os.path.exists(output_xlsx):
            os.remove(output_xlsx)
   

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)