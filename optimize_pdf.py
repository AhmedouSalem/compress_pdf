import os

from PDFNetPython3.PDFNetPython import PDFDoc, PDFNet, Optimizer, ImageSettings, SDFDoc, OptimizerSettings

def optimize_pdf(input_path):
    # Initialise PDFNet avec la clé de licence
    PDFNet.Initialize("demo:1708272182326:7f5e798b03000000009058fad3adf9127f6ad41aacb37b78fb48bd1258")

    # Charge le document PDF à partir du chemin d'entrée
    doc = PDFDoc(input_path)
    doc.InitSecurityHandler()
    Optimizer.Optimize(doc)
    
    # Initialise les paramètres d'optimisation pour les images
    image_settings = ImageSettings()
    
    # compression jpeg de mauvaise qualité
    image_settings.SetCompressionMode(ImageSettings.e_jpeg)
    image_settings.SetQuality(1)
    
    # Définissez le dpi de sortie sur la résolution d'écran standard
    image_settings.SetImageDPI(144,96)
    
    # cette option recompressera les images non compressées avec
    # compression jpeg et utiliser le résultat si la nouvelle image
    # est plus petit.
    image_settings.ForceRecompression(True)
    
    """cette option n'est pas couramment utilisée car elle peut
    peut potentiellement conduire à des fichiers plus volumineux. Il devrait être activé
    seulement si la compression de sortie spécifiée doit être appliquée
    à chaque image d'un type donné quelle que soit la taille de l'image de sortie """
    # image_settings.ForceChanges(True)

    opt_settings = OptimizerSettings()
    opt_settings.SetColorImageSettings(image_settings)
    opt_settings.SetGrayscaleImageSettings(image_settings)

    # Applique les paramètres d'optimisation au document
    Optimizer.Optimize(doc, opt_settings)
    
    # Sauvegarde le document optimisé
    # Obtenez le nom du fichier d'entrée sans le chemin d'accès
    input_filename = os.path.basename(input_path)

    # Créez le chemin de sortie en concaténant le nom du fichier d'entrée avec "_optimized.pdf"
    output_filename = input_filename.split('.')[0] + "_optimized.pdf"
    output_path = os.path.join(os.path.dirname(input_path), output_filename)
    doc.Save(output_path, SDFDoc.e_linearized)
    doc.Close()

    # Termine PDFNet
    PDFNet.Terminate()

    return output_path
