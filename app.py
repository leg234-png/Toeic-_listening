from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_listening', methods=['POST'])
def upload_listening():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    content = file.read().decode('utf-8')
    items = [item.strip() for item in content.split(',') if item.strip()]
    return jsonify({'items': items})

@app.route('/upload_brain', methods=['POST'])
def upload_brain():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    content = file.read().decode('utf-8')
    stories = [story.strip() for story in content.split('|') if story.strip()]
    return jsonify({'stories': stories})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
