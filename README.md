# Chatbot Flask com Autenticação de Usuários

Este é um aplicativo web desenvolvido em Flask que combina autenticação de usuários com um chatbot baseado no modelo GPT-3.5-turbo da OpenAI. A aplicação permite o registro de usuários, login, gerenciamento de sessões e uma interface de chat interativa.

---

## Funcionalidades

- **Autenticação de Usuários**: Os usuários podem se registrar, fazer login e logout de forma segura, utilizando senhas protegidas com hashing via bcrypt.
- **Integração com Chatbot**: Após o login, os usuários podem interagir com o chatbot que utiliza a API da OpenAI.
- **Gerenciamento de Sessões**: Sessões são usadas para garantir que apenas usuários autenticados possam acessar o chatbot.
- **Banco de Dados com SQLAlchemy**: Gerenciamento de usuários e persistência de dados com PostgreSQL.

---

## Pré-requisitos

Certifique-se de que você tem os seguintes itens instalados:

- Python 3.9 ou superior
- PostgreSQL
- Um arquivo `.env` com as seguintes variáveis configuradas:
  - `FLASK_SECRET_KEY`: Chave secreta para a aplicação Flask.
  - `POSTGRES_URI`: URI de conexão ao banco de dados PostgreSQL.
  - `OPENAI_API_KEY`: Chave da API da OpenAI para acessar o GPT-3.5.

---

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```

2. Crie um ambiente virtual e ative-o:
    ```
    python -m venv venv
    source venv/bin/activate  # No Windows, use:          venv\Scripts\activate
    ```

3. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```

4. Configure o arquivo `.env` com as variáveis necessárias.

5. Crie o banco de dados e as tabelas:

    - Acesse o shell do Python:
        ```
        python
        ```
    - Execute os comandos:
        ```
        from app import db
        db.create_all()
        exit()
        ```

## Como Executar

1. Inicie o servidor Flask:
    ```
    python app.py
    ```

2. Acesse a aplicação no navegador:
    ```
    http://127.0.0.1:5000/
    ```

## Estrutura de Rotas

- `/`: Página inicial com links de login e cadastro.
- `/register`: Página de registro de novos usuários.
- `/login`: Página de login para usuários existentes.
- `/logout`: Rota para realizar logout e limpar a sessão.
- `/chat`: Página principal do chatbot (necessita de login).
- `/chat_api`: Endpoint para comunicação com o chatbot.

## Tecnologias Utilizadas

- **Backend**: Flask
- **Banco de Dados**: PostgreSQL com SQLAlchemy
- **Autenticação**: bcrypt para hashing de senhas
- **IA**: OpenAI GPT-3.5-turbo
- **Gerenciamento de Sessão**: Flask Sessions

## Observações

- Certifique-se de proteger o arquivo `.env` para evitar exposição de chaves sensíveis.

- Use `debug=False` em produção para maior segurança.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto é licenciado sob a licença `MIT.`