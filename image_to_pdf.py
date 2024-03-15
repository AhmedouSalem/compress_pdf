from PDFNetPython3.PDFNetPython import PDFNet, PDFDoc, ElementBuilder, ElementWriter, Image, SDFDoc
import os

def image_to_pdf(image_path):
    # Initialise PDFNet avec une clé de licence
    PDFNet.Initialize("demo:1708430225314:7f5bef2c030000000049212c4ef225c03dd7b573fab542d49426d99b8f")

    # Crée un nouveau document PDF
    doc = PDFDoc()

    # Crée un objet ElementBuilder pour construire de nouveaux éléments
    f = ElementBuilder()

    # Crée un objet ElementWriter pour écrire des éléments dans le document
    writer = ElementWriter()

    # Crée une nouvelle page dans le document
    page = doc.PageCreate()

    # Commence l'écriture sur cette page
    writer.Begin(page)

    # Charge l'image à partir du chemin spécifié
    img = Image.Create(doc.GetSDFDoc(), image_path)

    # Récupère les dimensions de l'image
    width = img.GetImageWidth()
    height = img.GetImageHeight()

    # Calcule les coordonnées pour centrer l'image au milieu du PDF
    page_width = 612  # Largeur de la page par défaut
    page_height = 792  # Hauteur de la page par défaut
    left_margin = (page_width - width / 2) / 2
    bottom_margin = (page_height - height / 2) / 2

    # Crée un élément d'image à partir de l'image chargée
    element = f.CreateImage(img, left_margin, bottom_margin, width / 2, height / 2)

    # Ajoute l'élément d'image à la page
    writer.WritePlacedElement(element)

    # Termine l'écriture sur la page
    writer.End()

    # Ajoute la page au document
    doc.PagePushBack(page)

    # Crée le chemin de sortie pour le fichier PDF
    output_pdf_path = os.path.join(os.path.splitext(os.path.basename(image_path))[0] + "_RIMPDF.pdf")

    # Sauvegarde le document PDF avec l'image ajoutée
    doc.Save(output_pdf_path, SDFDoc.e_linearized)

    # Ferme le document
    doc.Close()

    # Termine PDFNet
    PDFNet.Terminate()

    # Retourne le chemin du fichier PDF généré
    return output_pdf_path