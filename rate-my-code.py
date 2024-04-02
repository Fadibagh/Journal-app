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
        {"role": "system", "content": "You are an expert at rating python code"},
        {"role": "system", "content": "For the code you are given, rate it based on Readability, Style and Structure, Robustness, and Error Handling."},
        {"role": "system", "content": "In your reply, give the rating for each subject out of a 100 and give some comments on how it could be better."},
        {"role": "system", "content": "Keep it breif"},
        {"role": "system", "content": "Try to be inline with relevant up-to-date practices"},
        {"role": "system", "content": "Leave an empty line after each section for better readability"},
        {"role": "system", "content": "Give a possible improvements section at the end."},
        {"role": "user", "content": user_code}
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000
    )

    print(completion.usage.total_tokens)

    code_rating = str(completion.choices[0].message.content)

    return jsonify({"code_rating": code_rating})

if __name__ == '__main__':
    app.run()