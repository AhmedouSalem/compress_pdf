from flask import Flask, render_template, request, send_from_directory
import os
from optimize_pdf import optimize_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    if 'pdf_file' not in request.files:
        return "Aucun fichier PDF sélectionné", 400

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return "Aucun fichier PDF sélectionné", 400

    # Enregistre temporairement le fichier PDF
    temp_path = 'temp.pdf'
    pdf_file.save(temp_path)

    # Optimise le fichier PDF
    output_path = optimize_pdf(temp_path)

    # Supprime le fichier temporaire
    os.remove(temp_path)
    
    # Retourne le fichier optimisé en téléchargement
    return send_from_directory('.', output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
