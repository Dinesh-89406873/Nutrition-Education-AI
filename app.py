import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()
app = Flask(__name__, static_folder="static")
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
client = genai.Client(api_key=API_KEY) if API_KEY else None

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Please enter your question."}), 400
    if client is None:
        return jsonify({"error": "GEMINI_API_KEY is missing in .env"}), 500
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{SYSTEM_PROMPT}\n\nUser Question:\n{message}"
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print(e)
        return jsonify({"error": "Unable to generate AI response."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
