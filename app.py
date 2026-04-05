from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv
load_dotenv()  # charge le .env automatiquement


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MISTRAL_API_KEY = os.environ.get('MISTRAL_API_KEY')

PROMPT_HISTORY = []  # garde en mémoire les réponses précédentes pour forcer la variété

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

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(silent=True) or {}
    count = data.get('count', 250)  # 20 par défaut

    prompt = (
        f'Je me prépare au test TOEIC. Génère exactement {count} paires de mots et expressions variés '
        f'(vocabulaire général, business, phrasal verbs, voyages, finance) '
        f'sous ce format exact : mot_anglais, traduction_française, mot_anglais, traduction_française, ... '
        f'Tout sur une seule ligne, séparé uniquement par des virgules. '
        f'Aucun texte avant ou après, aucune numérotation, aucune explication. '
        f'Fournir une version différente à chaque appel.'
    )

    response = requests.post(
        'https://api.mistral.ai/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {MISTRAL_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'mistral-small-latest',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.9,
            'max_tokens': min(count * 15, 8000)  # ~15 tokens par paire, max 8000
        }
    )

    if response.status_code != 200:
        return jsonify({'error': 'Mistral API error', 'details': response.text}), 500

    result = response.json()
    text = result['choices'][0]['message']['content'].strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    clean = lines[0] if lines else text
    items = [item.strip() for item in clean.split(',') if item.strip()]
    return jsonify({'items': items})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)