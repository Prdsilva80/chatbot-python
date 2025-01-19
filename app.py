import os
import openai
import bcrypt
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Secret para sessões

# Configuração do banco de dados (NeonDB) via URI completa
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Configurar chave da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

#################################################
#                   MODELOS                     #
#################################################

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Para criar as tabelas pela primeira vez:
#   python
#   >>> from app import db
#   >>> db.create_all()


#################################################
#                 FUNÇÃO DE IA                  #
#################################################

def enviar_mensagem(mensagem, lista_mensagens=[]):
    """
    Envia uma mensagem ao modelo GPT-3.5-turbo com base
    em uma lista de mensagens de contexto.
    """
    lista_mensagens.append({"role": "user", "content": mensagem})
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=lista_mensagens,
    )
    return resposta["choices"][0]["message"]


#################################################
#                   ROTAS                       #
#################################################

@app.route("/")
def home():
    """
    Página inicial simples com links de login/cadastro,
    ou exibe o chatbot caso queira personalizar.
    """
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Rota de cadastro de novos usuários.
    """
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Verificar se o usuário já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Esse email já está registrado."

        # Hash da senha com bcrypt
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Criar novo usuário e salvar no DB
        new_user = User(
            name=name,
            email=email,
            password=hashed_pw.decode("utf-8")  # Armazenamos em formato texto, mas já hasheado
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Rota de login. Cria uma sessão para o usuário com credenciais corretas.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password").encode("utf-8")

        user = User.query.filter_by(email=email).first()
        if user:
            # Verificar hash da senha
            if bcrypt.checkpw(password, user.password.encode("utf-8")):
                # Salva info do usuário na sessão
                session["user_id"] = user.id
                session["user_name"] = user.name
                return redirect(url_for("chat_page"))
            else:
                return "Senha incorreta."
        else:
            return "Usuário não encontrado."
    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Rota de logout. Limpa a sessão.
    """
    session.clear()
    return redirect(url_for("home"))


@app.route("/chat")
def chat_page():
    """
    Página do chatbot. Somente usuários logados podem acessar.
    """
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html")


@app.route("/chat_api", methods=["POST"])
def chat_api():
    """
    Endpoint que recebe a mensagem do cliente e retorna a resposta da IA.
    Protegido para exigir login.
    """
    if "user_id" not in session:
        return jsonify({"error": "Usuário não autenticado"}), 403

    user_message = request.form.get("message")
    lista_mensagens = []
    resposta = enviar_mensagem(user_message, lista_mensagens)

    return jsonify({"response": resposta["content"]})


#################################################
#            EXECUÇÃO DO SERVIDOR              #
#################################################

if __name__ == "__main__":
    app.run(debug=True)
