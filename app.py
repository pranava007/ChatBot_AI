from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama runs on this port

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Ollama Chatbot is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Send request to Ollama model
        payload = {
            "model": "mistral",  # Change the model if needed
            "prompt": user_input,
            "stream": False  # Set to True if you want streaming responses
        }

        response = requests.post(OLLAMA_API_URL, json=payload)
        response_data = response.json()

        return jsonify({"response": response_data["response"]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
