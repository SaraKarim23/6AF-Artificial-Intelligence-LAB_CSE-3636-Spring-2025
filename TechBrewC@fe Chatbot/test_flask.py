from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = "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"  # Replace this with your actual API key

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_id = data.get('user_id', 'anonymous')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are TechBrew Cafe's helpful assistant. Greet users and assist with menu, coffee info, BMI suggestions."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
