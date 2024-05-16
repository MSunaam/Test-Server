def allowed_file_crops(filename,appConfig,request):
    # Check filename and file size
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in appConfig["ALLOWED_EXTENSIONS_CROPS"] and \
              request.content_length < appConfig['ALLOWED_SIZE']
              
              
def allowed_file_hash(filename,appConfig,request):
    # Check filename and file size
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in appConfig["ALLOWED_EXTENSIONS_HASH"] and \
              request.content_length < appConfig['ALLOWED_SIZE']