from flask import Flask, request, send_file, send_from_directory
import subprocess
import os



app = Flask(__name__, static_folder='static')



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

 # 🔍 Debug logging starts here
    print("User-Agent:", request.headers.get('User-Agent'))
    print("File name:", uploaded_file.filename)
    print("File size (bytes):", len(uploaded_file.read()))
    uploaded_file.seek(0)  # Reset file pointer after reading


    input_path = 'input.pdf'
    output_path = 'compressed.pdf'
    uploaded_file.save(input_path)

    try:
        subprocess.run([
            'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET', '-dBATCH',
            f'-sOutputFile={output_path}', input_path
        ], check=True)
        return send_file(output_path, as_attachment=True, mimetype='application/pdf')
    except Exception as e:
        print(e)
        return "Compression failed", 500
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

@app.route('/3ctool')
def serve_3ctool():
    return render_template('3ctool/index.html')

@app.route('/gpstool')
def serve_gpstool():
    return render_template('gpstool/index.html')


   

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)