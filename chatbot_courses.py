import os
import markdown
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re

# Configuration de l'API de Google Gemini
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', 'AIzaSyDJub1_OGii8k9a4c4XZT8_Ecqm7r6nhCE')
genai.configure(api_key=GOOGLE_API_KEY)

# Créer l'application Flask
app = Flask(__name__)
CORS(app)  # Activation de CORS pour les requêtes inter-domaines

# Fonction pour nettoyer et formater le texte
def clean_and_format_text(text):
    # Suppression des caractères spéciaux et formatage
    text = re.sub(r'[*#]', '', text)
    return text

# Fonction pour générer différents types de contenu
def generate_content(prompt_type, subject):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompts = {
        "cours": f"Génère un plan de cours détaillé pour '{subject}' avec des modules, objectifs et ressources.",
        "exercices": f"Crée 5 exercices progressifs pour un cours sur '{subject}'.",
        "quiz": f"Développe un quiz de 10 questions à choix multiples sur '{subject}'.",
        "resume": f"Rédige un résumé synthétique du sujet '{subject}'.",
        "projet": f"Propose un projet pratique pour approfondir les connaissances sur '{subject}'."
    }
    
    try:
        prompt = prompts.get(prompt_type, prompts["cours"])
        response = model.generate_content(prompt)
        
        # Conversion Markdown en HTML pour une meilleure lisibilité
        html_content = markdown.markdown(clean_and_format_text(response.text))
        return html_content
    except Exception as e:
        return f"Erreur lors de la génération du contenu : {e}"

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    subject = data.get('subject', '')
    prompt_type = data.get('type', 'cours')
    
    if not subject:
        return jsonify({"error": "Sujet manquant"}), 400
    
    content = generate_content(prompt_type, subject)
    return jsonify({"content": content})

if __name__ == "__main__":
    app.run(debug=True)