from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_ocr(pdf_file):
    images = convert_from_path(pdf_file)
    ocr_text = ""

    for page_num, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image)
        ocr_text += text

    return ocr_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('result', filename=filename))
    return render_template('index.html')

@app.route('/result/<filename>', methods=['GET', 'POST'])
def result(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    ocr_text = perform_ocr(file_path)

    if request.method == 'POST':
        search_query = request.form['search_query']
        search_result = search_word(ocr_text, search_query)
        return render_template('result.html', text=ocr_text, search_result=search_result, filename=filename)
    
    return render_template('result.html', text=ocr_text, search_result=None, filename=filename)

def search_word(ocr_text, search_query):
    lines = ocr_text.split('\n')

    for line in lines:
        if search_query in line:
            idx = line.find(search_query)
            return f"Text after '{search_query}': {line[idx + len(search_query):].strip()}"
    
    return f"'{search_query}' not found in the document."

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == "__main__":
    app.run(debug=True, port=8083)
