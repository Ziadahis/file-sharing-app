from flask import Flask, request, render_template, redirect, url_for, flash
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# AWS S3 setup
S3_BUCKET = 'your-s3-bucket-name'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt'}

s3 = boto3.client('s3')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, S3_BUCKET, filename)
            download_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
            return render_template('success.html', filename=filename, url=download_url)
        else:
            flash('File type not allowed')
            return redirect(request.url)
    
    return render_template('index.html')
