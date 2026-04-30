from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

app = Flask(__name__)

# .env file load karein
load_dotenv()

# Ab hum Groq ki key read kar rahe hain
groq_api_key = os.getenv("GROQ_API_KEY")

# OpenAI client ko Groq ke URL aur key ke sath setup karein
client = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question") or request.form.get("question")
    
    if not question:
        return jsonify({"response": "Error: Question nahi mila. Kripya dobara try karein."}), 400

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Groq ka superfast Llama 3 model
        messages=[
            {"role": "system", "content": "Act like a helpful personal assistant"},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=512
    )
        
    answer = response.choices[0].message.content.strip()
    return jsonify({"response": answer}), 200

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    email_text = data.get("email") or request.form.get("email")
    
    if not email_text:
         return jsonify({"response": "Error: Email text nahi mila."}), 400

    prompt = f"summarize the following email in 2-3 sentences: {email_text}"
        
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Groq ka model
        messages=[
            {"role": "system", "content": "Act like an expert email assistant"},                
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=512
    )
        
    summary = response.choices[0].message.content.strip()
    return jsonify({"response": summary}), 200

if __name__ == "__main__":
    app.run(debug=True)