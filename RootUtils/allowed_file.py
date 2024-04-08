def allowed_file(filename,appConfig,request):
    # Check filename and file size
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in appConfig["ALLOWED_EXTENSIONS"] and \
              request.content_length < appConfig['ALLOWED_SIZE']