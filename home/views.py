import os

from flask import Blueprint, render_template, request, send_from_directory, send_file
from werkzeug.utils import secure_filename

from image_to_pdf import image_to_pdf
from optimize_pdf import optimize_pdf

home = Blueprint('home',__name__,template_folder='templates',static_folder='static',static_url_path='/static')

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/optimize')
def optimize():
    return render_template('optimize.html')

@home.route('/convert_image')
def convert_image():
    return  render_template('convert_to_image.html')


# ---------- optimizer des fichiers PDFs
@home.route('/optimize', methods=['POST'])
def optimize_PDF():
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


# -------- converter des images to pdf

# Définir les extensions d'images autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Fonction pour vérifier si l'extension du fichier est autorisée
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@home.route("/image_to_pdf", methods=['POST'])
def convert_to_pdf():
    # Vérifie si le fichier d'image a été inclus dans la requête
    if 'image_file' not in request.files:
        return "Aucune image sélectionnée", 400

    image_file = request.files['image_file']

    # Vérifie si un fichier a été sélectionné
    if image_file.filename == '':
        return "Aucune image sélectionnée", 400

    # Vérifie si le fichier est une image avec une extension autorisée
    if image_file and allowed_file(image_file.filename):
        # Sécurise le nom du fichier
        filename = secure_filename(image_file.filename)

        # Crée le répertoire temporaire s'il n'existe pas
        temp_directory = "temp"
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory)

        # Enregistre l'image dans un dossier temporaire
        temp_image_path = os.path.join(temp_directory ,filename)
        image_file.save(temp_image_path)

        # Appelle la fonction pour convertir l'image en PDF
        pdf_path = image_to_pdf(temp_image_path)

        # Supprime l'image temporaire
        os.remove(temp_image_path)

        # Retourne le fichier PDF généré en téléchargement
        pdf_directory = os.path.dirname(pdf_path)
        pdf_filename = os.path.basename(pdf_path)
        return send_from_directory(pdf_directory, pdf_filename, as_attachment=True)
    else:
        return "Format de fichier non pris en charge", 400