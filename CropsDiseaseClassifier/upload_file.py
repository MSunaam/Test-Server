import os
from werkzeug.utils import secure_filename

from RootUtils.allowed_file import allowed_file

def upload_image(request, appConfig)->str:
    if request.method != 'POST':
        return "Method not allowed. Please send a POST request.", ""
    
    if 'file' not in request.files:
        return "No file part", ""
    
    file = request.files['file']

    if file and allowed_file(file.filename, appConfig, request):
        filename = secure_filename(file.filename)
        file.save(os.path.join(appConfig['UPLOAD_FOLDER'], filename))
        return f"File uploaded successfully {filename}", filename
    else:
        return "File not allowed", ""