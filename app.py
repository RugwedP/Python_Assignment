from flask import Flask, render_template, request, redirect, url_for
from s3_manager import S3Manager

app = Flask(__name__)
s3_helper = S3Manager(bucket_name='your-actual-bucket-name')

@app.route('/')
def index():
    prefix = request.args.get('prefix', '')
    files, folders = s3_helper.list_files(prefix)
    return render_template('index.html', files=files, folders=folders, current_path=prefix)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = request.form.get('path', '')
    if file:
        s3_helper.upload_file(file, path + file.filename)
    return redirect(url_for('index', prefix=path))

@app.route('/delete/<path:key>')
def delete(key):
    s3_helper.delete_object(key)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)