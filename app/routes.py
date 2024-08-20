from flask import Blueprint, request, render_template, redirect, flash
from .models import db, Data
from .utils import process_file
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def upload_file():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if file:
        result = process_file(file)
        if result['status'] == 'error':
            flash(result['message'])
        return redirect('/')
