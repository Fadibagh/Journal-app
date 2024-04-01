from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

@app.route('/')
def home():
    return render_template('rate-my-code.html')

@app.route('/get-rating', methods=['POST'])
def get_rating():
    content = request.json
    user_code = content.get('user_code')

    if not user_code:
        return jsonify({"error": "No code topic provided"}), 400
    
    messages = [
        {"role": "system", "content": "You are an expert at rating code"},
        {"role": "system", "content": "For the code you are given, rate it based on Readability, Style and Structure, Robustness and Error Handling."},
        {"role": "system", "content": "In your reply, give the rating for each subject out of a 100 and give some comments on how it could be better."},
        {"role": "system", "content": "Keep it breif"},
        {"role": "user", "content": user_code}
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000
    )

    print(completion.usage.total_tokens)

    code_rating = str(completion.choices[0].message.content)

    return jsonify({"code_rating": code_rating})

if __name__ == '__main__':
    app.run(debug=True)