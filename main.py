# main.py
from flask import Flask, request, send_file, jsonify
import tempfile
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "📝 LibreOffice DOCX to PDF Converter is running."

@app.route('/convert', methods=['POST'])
def convert_docx_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    docx_file = request.files['file']
    if not docx_file.filename.endswith('.docx'):
        return jsonify({"error": "Only .docx files are supported"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, 'input.docx')
        output_path = os.path.join(temp_dir, 'input.pdf')

        docx_file.save(input_path)

        try:
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', temp_dir,
                input_path
            ], check=True)

            return send_file(output_path, as_attachment=True, download_name='converted.pdf')
        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Conversion failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
