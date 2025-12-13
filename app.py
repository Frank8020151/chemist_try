import flask
import openai
from flask import request, jsonify, render_template
from flask_cors import CORS

import Main
import tools

app = flask.Flask(__name__)


CORS(app)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data['query']

    result = Main.chat(query)

    return jsonify({
        'message': result,
    })


@app.route('/api/change_client', methods=['POST'])
def change_client():
    data = request.get_json()
    api_key = data['api_key']
    base_url = data['base_url']
    model_name = data['model_name']
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    Main.client = client
    tools.client2 = client
    Main.user_model_name = model_name
    tools.user_model_name = model_name
    return jsonify({
        'success': 'success',
    })


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8080)
