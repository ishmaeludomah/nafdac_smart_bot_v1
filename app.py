from flask import Flask, render_template, request, jsonify, session
import os
import google.generativeai as genai
from dotenv import load_dotenv
from markdown import markdown
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key"  # required for session
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model name (Gemini Free Tier)
MODEL_NAME = "models/gemini-2.5-flash"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')

    # Initialize conversation history if it doesn't exist
    if 'history' not in session:
        session['history'] = []

    # Add user's new message to the history
    session['history'].append({"role": "user", "content": user_input})

    # Build conversation context for Gemini
    conversation = ""
    for msg in session['history']:
        if msg['role'] == "user":
            conversation += f"User: {msg['content']}\n"
        else:
            conversation += f"NAFDAC SmartBot: {msg['content']}\n"

    # Create Gemini model
    model = genai.GenerativeModel(MODEL_NAME)

    try:
        # Generate response with full context
        response = model.generate_content(
            f"You are NAFDAC SmartBot, the official assistant for the National Agency for Food and Drug Administration and Control. "
            f"Be polite, professional, and concise.\n"
            f"Here is the ongoing conversation:\n{conversation}\n"
            f"Continue the conversation appropriately."
        )

        bot_reply = response.text.strip() if response.text else "I couldn’t generate a reply at the moment."

        # Save bot response to history
        session['history'].append({"role": "assistant", "content": bot_reply})

        # Convert Markdown to HTML for formatting
        bot_reply_html = markdown(bot_reply)

        return jsonify({'reply': bot_reply_html})

    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"})


@app.route('/reset', methods=['POST'])
def reset_chat():
    session.pop('history', None)
    return jsonify({'message': 'Chat reset successfully.'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
