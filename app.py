from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    uploaded_file = request.files.get('pdf')
    if not uploaded_file:
        return "No file uploaded", 400

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
    app.run(host='0.0.0.0', port=10000)