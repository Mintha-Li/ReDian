from flask import Flask, request, render_template, send_file
from func import process_files_in_folder
import os
from datetime import datetime

app = Flask(__name__)

OUTPUT_FOLDER = 'outputs'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    upload_folder = os.path.join(app.config['OUTPUT_FOLDER'], datetime.now().strftime("%Y%m%d_%H%M%S"))
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    if 'files[]' not in request.files:
        return 'No file part'
    files = request.files.getlist('files[]')
    if files:
        for file in files:
            if file.filename == '':
                return 'No selected file'
            if file:
                filename = file.filename
                file_path = os.path.join(upload_folder, filename)
                print(f"Saving file to: {file_path}")  # 添加这行
                file.save(file_path)
        # Process the uploaded files
        output_file_name = process_files_in_folder(folder_path=upload_folder,
                                                   output_folder=app.config['OUTPUT_FOLDER'])
        return send_file(os.path.join(app.config['OUTPUT_FOLDER'], output_file_name), as_attachment=True)
    else:
        return 'File not allowed'

@app.route('/clear_outputs')
def clear_outputs():
    # 清理 outputs 文件夹中的内容
    for file_name in os.listdir(app.config['OUTPUT_FOLDER']):
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return 'Outputs folder cleared successfully!'

if __name__ == '__main__':
    app.run(debug=True)
