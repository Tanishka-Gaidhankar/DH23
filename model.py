import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from flask import Flask, request, jsonify
import google.generativeai as genai

from transformers import AutoTokenizer, AutoModel

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("markusbayer/CySecBERT")

# Load the model
model = AutoModel.from_pretrained("markusbayer/CySecBERT")


genai.configure(api_key="AIzaSyAKeanOwPuWnxlpu8IqxO6eRgNa00XTaGg")

app = Flask(_name_)



def classify_query(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()

    classes = ["Data Privacy", "Cyber Crime", "Intellectual Property", "Regulatory Compliance"]
    return classes[prediction]

def generate_response(query, category):
    prompt = f"You are an expert in {category} law. Answer the following question professionally:\n\n{query}"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


def chat():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    category = classify_query(user_input)
    response = generate_response(user_input, category)

    return jsonify({"category": category, "response": response})

if _name_ == "_main_":
    app.run(debug=True)