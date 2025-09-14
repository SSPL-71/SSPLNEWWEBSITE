from flask import Flask, request, send_file, send_from_directory
import subprocess
import os

app = Flask(__name__, static_folder='.', static_url_path='')


@app.before_request
def block_prefetch():
    if request.headers.get('Purpose') == 'prefetch':
        return '', 403

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('.', 'sw.js')

@app.route('/robots.txt')
def serve_robots():
    import os
    from flask import Response
    root_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_dir, 'robots.txt')) as f:
        content = f.read()
    response = Response(content, mimetype='text/plain')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

from flask import send_file

@app.route('/site-index.xml')
def serve_sitemap():
    import os
    root_dir = os.path.dirname(os.path.abspath(__file__))
    sitemap_path = os.path.join(root_dir, 'site-index.xml')

    return send_file(
        sitemap_path,
        mimetype='application/xml',
        as_attachment=False
    )


@app.route('/compress', methods=['POST'])
def compress_pdf():
    uploaded_file = request.files.get('pdf')
    if not uploaded_file:
        return "No file uploaded", 400

@app.route('/3ctool')
def serve_3ctool():
    return send_from_directory('3ctool', 'index.html')

@app.route('/gpstool')
def serve_gpstool():
    return send_from_directory('gpstool', 'index.html')

 # 🔍 Logging diagnostics
    print("User-Agent:", request.headers.get('User-Agent'))
    print("Received file:", uploaded_file.filename)
    print("Content-Type:", uploaded_file.content_type)
    print("Content Length:", request.content_length)
    print("Form field name:", 'pdf' in request.files)


    input_path = 'input.pdf'
    output_path = 'compressed.pdf'
    uploaded_file.save(input_path)

    try:
        subprocess.run([
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/ebook',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_path}',
            input_path
        ], check=True)

        return send_file(output_path, as_attachment=True)
    except subprocess.CalledProcessError:
        return "Compression failed", 500
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)