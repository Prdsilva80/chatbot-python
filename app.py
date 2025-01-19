import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave API do ambiente
chave_api = os.getenv("OPENAI_API_KEY")
openai.api_key = chave_api

app = Flask(__name__)

# Função para enviar a mensagem ao chatbot
def enviar_mensagem(mensagem, lista_mensagens=[]):
    lista_mensagens.append({"role": "user", "content": mensagem})
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=lista_mensagens,
    )
    return resposta["choices"][0]["message"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    lista_mensagens = []
    response = enviar_mensagem(user_message, lista_mensagens)
    return jsonify({"response": response["content"]})

if __name__ == "__main__":
    app.run(debug=True)
