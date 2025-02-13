import os
import google.generativeai as genai
from flask import Flask, request, jsonify,render_template
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini AI API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Flask App
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json()
        user_question = data.get("question", "").strip()

        if not user_question:
            return jsonify({"error": "Please provide a question"}), 400

        # AI-Based Cyber Law Classification
        classification_prompt = (
            f"Determine whether the following question is related to Cyber Law or not. "
            f"Answer with only 'YES' or 'NO'.\n\n"
            f"Question: {user_question}"
        )
        
        classification_response = model.generate_content(classification_prompt).text.strip()

        # Check AI's classification response
        if classification_response.upper() != "YES":
            return jsonify({"error": "This question is not related to Cyber Law. Please ask a relevant question."}), 400

        # Generate response from AI for Cyber Law related question
        response = model.generate_content(user_question)
        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
