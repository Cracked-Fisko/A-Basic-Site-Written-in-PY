from flask import Flask, render_template, send_file, request, abort, jsonify
import os
import zipfile

app = Flask(__name__, static_folder='static')

# Define the folder paths
DROP_FOLDER = 'C:/dropper'
TEMP_FOLDER = 'C:/temp'

# Ensure the temp directory exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dropper')
def dropper():
    files = []
    for root, dirs, file_names in os.walk(DROP_FOLDER):
        for file_name in file_names:
            relative_path = os.path.relpath(os.path.join(root, file_name), DROP_FOLDER)
            files.append(relative_path)
    return render_template('dropper.html', files=files)

@app.route('/download/<path:filename>')
def download(filename):
    file_path = os.path.join(DROP_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        abort(404)

@app.route('/download_selected', methods=['POST'])
def download_selected():
    selected_files = request.form.getlist('files')
    zip_filename = 'selected_files.zip'
    zip_filepath = os.path.join(TEMP_FOLDER, zip_filename)

    # Create the zip file
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in selected_files:
            full_path = os.path.join(DROP_FOLDER, file)
            if os.path.isfile(full_path):
                zipf.write(full_path, arcname=os.path.basename(full_path))

    # Send the zip file to the user
    response = send_file(zip_filepath, as_attachment=True, download_name=zip_filename)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)