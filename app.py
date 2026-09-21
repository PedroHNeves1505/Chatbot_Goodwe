import os
from flask import Flask, render_template, request, jsonify, session
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "chave_secreta_para_desenvolvimento_hca_g2")

api_key_groq = os.environ.get("GROQ_API_KEY")

if not api_key_groq:
    raise ValueError("ERRO: A variável GROQ_API_KEY não foi encontrada. Verifique se o arquivo .env está configurado corretamente.")

client = Groq(api_key=api_key_groq)



@app.route("/")
def index():
    session["historico"] = []
    return render_template("index.html")

@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    try:
        data = request.get_json()
        mensagem_usuario = data.get("mensagem", "")
        
        if not mensagem_usuario:
            return jsonify({"resposta": "Por favor, digite uma mensagem válida."}), 400

        if "historico" not in session:
            session["historico"] = []
        
        historico = session["historico"]

        messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in historico:
            messages_payload.append({"role": msg["role"], "content": msg["content"]})

        messages_payload.append({"role": "user", "content": mensagem_usuario})

        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages_payload, 
            temperature=0.3, 
            max_tokens=512
        )
        
        resposta_ia = chat_completion.choices[0].message.content
    
        historico.append({"role": "user", "content": mensagem_usuario})
        historico.append({"role": "assistant", "content": resposta_ia})
        session["historico"] = historico
        
        return jsonify({"resposta": resposta_ia})

    except Exception as e:
        print(f"Erro na requisição: {e}")
        return jsonify({"resposta": "Desculpe, ocorreu um erro ao processar sua resposta na API do Groq."}), 500

if __name__ == "__main__":
    app.run(debug=True)