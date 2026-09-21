import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from app.chain import executar_chatbot
from app.memory_manager import memoria_buffer
import tiktoken


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("OLLAMA_API_KEY")


def contar_tokens(texto:str, modelo:str='gpt-4') -> int:
    enc = tiktoken.encoding_for_model(modelo)
    return len(enc.encode(texto))

@app.route("/")
def index():
    session["historico"] = []
    memoria_buffer.clear()
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

        memoria_buffer.clear()
        for msg in historico:
            if msg["role"] == "user":
                memoria_buffer.chat_memory.add_user_message(msg["content"])
            elif msg["role"] == "assistant":
                memoria_buffer.chat_memory.add_ai_message(msg["content"])

        resultado_chatbot = executar_chatbot(mensagem_usuario)
        
        resposta_ia = getattr(resultado_chatbot, 'resposta_final', str(resultado_chatbot))
        
        tokens_pergunta = contar_tokens(mensagem_usuario)
        tokens_resposta = contar_tokens(resposta_ia)
        

        historico.append({"role": "user", "content": mensagem_usuario})
        historico.append({"role": "assistant", "content": resposta_ia})
        session["historico"] = historico
        
        return jsonify({
            "resposta": resposta_ia,
            "tokens_pergunta": tokens_pergunta,
            "tokens_resposta": tokens_resposta
        })

    except Exception as e:
        print(f"Erro na requisição: {e}")
        return jsonify({"resposta": "Desculpe, ocorreu um erro ao processar sua resposta no Ollama."}), 500

if __name__ == "__main__":
    app.run(debug=True)