from flask import Flask, request, render_template, send_file, abort, after_this_request
import os
import shutil
import zipfile
from datetime import datetime
from func import process_files_in_folder

app = Flask(__name__)

# 配置输出文件夹和archives文件夹
OUTPUT_FOLDER = 'outputs'
ARCHIVES_FOLDER = 'archives'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['ARCHIVES_FOLDER'] = ARCHIVES_FOLDER

# 如果输出文件夹不存在，则创建它
if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

# 如果archives文件夹不存在，则创建它
if not os.path.exists(app.config['ARCHIVES_FOLDER']):
    os.makedirs(app.config['ARCHIVES_FOLDER'])

@app.route('/')
def index():
    # 渲染主页
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 为上传文件创建一个唯一的子文件夹
    upload_folder = os.path.join(app.config['OUTPUT_FOLDER'], datetime.now().strftime("%Y%m%d_%H%M%S"))
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # 检查请求中是否包含文件
    if 'files[]' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('files[]')
    if files:
        for file in files:
            if file.filename == '':
                return 'No selected file'
            if file:
                # 保存每个上传的文件
                filename = file.filename
                file_path = os.path.join(upload_folder, filename)
                print(f"Saving file to: {file_path}")  # 打印保存文件的路径
                file.save(file_path)
        
        # 处理上传的文件
        output_file_name = process_files_in_folder(folder_path=upload_folder, output_folder=app.config['OUTPUT_FOLDER'])
        
        # 返回处理后的文件作为附件
        return send_file(os.path.join(app.config['OUTPUT_FOLDER'], output_file_name), as_attachment=True)
    else:
        return 'File not allowed'

@app.route('/clear_outputs')
def clear_outputs():
    # 清理输出文件夹中的内容
    for file_name in os.listdir(app.config['OUTPUT_FOLDER']):
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return 'Outputs folder cleared successfully!'

def get_all_files(folder):
    # 递归获取文件夹中的所有文件
    file_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_paths.append(os.path.relpath(os.path.join(root, file), start=folder))
    return file_paths

def get_subfolders_with_files(folder):
    # 获取文件夹中的所有子文件夹及其文件
    subfolders = {}
    for root, dirs, files in os.walk(folder):
        subfolder_name = os.path.relpath(root, folder)
        files_in_subfolder = [file for file in files]
        subfolders[subfolder_name] = files_in_subfolder
    return subfolders

@app.route('/archives')
def show_archives():
    # 获取 archives 文件夹中的所有子文件夹及其文件列表
    subfolders_with_files = {}
    for root, dirs, files in os.walk(app.config['ARCHIVES_FOLDER']):
        # 获取子文件夹相对路径
        subfolder_name = os.path.relpath(root, app.config['ARCHIVES_FOLDER'])
        # 将子文件夹的文件列表添加到字典中
        subfolders_with_files[subfolder_name] = [file for file in files if not file.startswith('.')]  # 排除隐藏文件
    print(subfolders_with_files)
    return render_template('archives.html', subfolders_with_files=subfolders_with_files)




@app.route('/download/<path:filename>')
def download_file(filename):
    base_path = app.config['ARCHIVES_FOLDER']
    target_path = os.path.join(base_path, filename)
    
    # 检查路径安全性
    if not os.path.commonpath([base_path, target_path]) == base_path:
        abort(404)
    
    try:
        return send_file(target_path, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/download_folder/<path:foldername>')
def download_folder(foldername):
    base_path = app.config['ARCHIVES_FOLDER']
    target_path = os.path.join(base_path, foldername)
    
    # 检查路径安全性
    if not os.path.commonpath([base_path, target_path]) == base_path:
        abort(404)

    # 创建一个临时 ZIP 文件
    archive_name = os.path.join(app.config['OUTPUT_FOLDER'], f"{foldername}")
    shutil.make_archive(archive_name, 'zip', target_path)
    
    # 返回 ZIP 文件作为附件
    return send_file(f"{archive_name}.zip", as_attachment=True, download_name=f"{foldername}.zip")

@app.route('/download_archive', methods=['POST'])
def download_archive():
    selected_files = request.form.getlist('file')
    print(selected_files)
    
    if not selected_files:
        return "No files selected"

    zip_folder = os.path.join(app.config['OUTPUT_FOLDER'], 'selected_files')
    os.makedirs(zip_folder, exist_ok=True)

    # 将选中的文件复制到临时文件夹中
    for filename in selected_files:
        source_path = os.path.join(app.config['ARCHIVES_FOLDER'], filename)
        print(source_path)
        dest_path = os.path.join(zip_folder, filename)
        print(dest_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # 复制文件
        try:
            shutil.copy(source_path, dest_path)
            print(f"File copied successfully: {filename}")
        except Exception as e:
            print(f"Failed to copy file: {filename}. Error: {e}")

    # 创建一个 ZIP 文件
    zip_filename = os.path.join(app.config['OUTPUT_FOLDER'], 'selected_files.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(zip_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, zip_folder)
                zipf.write(file_path, arcname=arcname)
    
    @after_this_request
    def remove_temp_files(response):
        shutil.rmtree(zip_folder)
        return response
    
    # 提供 ZIP 文件的下载链接
    return send_file(zip_filename,as_attachment=True, download_name='selected_files.zip')

if __name__ == '__main__':
    app.run(debug=True)

