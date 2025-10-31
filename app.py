from flask import Flask, jsonify, request, render_template
import random
import string
import streamlit as st
import pandas as pd

st.title("Your App Title")
st.write("Your content here")

app = Flask(__name__)

# Estrutura de dados para armazenar jogos
jogos = {}

def gerar_id_jogo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def calcular_resultado(jogadas):
    """Calcula o resultado do jogo pedra, papel, tesoura"""
    if len(jogadas) < 2:
        return "Aguardando mais jogadores..."
    
    if all(j == jogadas[0] for j in jogadas):
        return "Empate!"
    
    # Lógica do jogo
    jogadas_unicas = set(jogadas)
    
    if jogadas_unicas == {"pedra", "tesoura"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "pedra"][0]
        return f"{vencedor} venceu com Pedra! 🪨 (quebrou tesoura)"
    elif jogadas_unicas == {"papel", "pedra"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "papel"][0]
        return f"{vencedor} venceu com Papel! 📄 (embrulhou pedra)"
    elif jogadas_unicas == {"tesoura", "papel"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "tesoura"][0]
        return f"{vencedor} venceu com Tesoura! ✂️ (cortou papel)"
    else:
        return "Escolhas diferentes - sem vencedor claro"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/criar_jogo', methods=['POST'])
def criar_jogo():
    data = request.get_json()
    jogadores_necessarios = int(data.get("jogadores_necessarios", 2))

    id_jogo = gerar_id_jogo()
    
    # Inicializa o jogo
    jogos[id_jogo] = {
        "jogadores": {},
        "jogadores_necessarios": jogadores_necessarios,
        "placar": {},
        "rodada_atual": 1,
        "jogando": True,
        "historico": []
    }

    return jsonify({
        "success": True,
        "mensagem": "Jogo criado com sucesso!",
        "id_jogo": id_jogo
    })

@app.route('/jogar/<id_jogo>', methods=['POST'])
def jogar(id_jogo):
    data = request.get_json()
    jogador = data.get("jogador")
    escolha = data.get("escolha")

    if id_jogo not in jogos:
        return jsonify({"success": False, "erro": "Jogo não encontrado."}), 404

    jogo = jogos[id_jogo]

    if not jogo["jogando"]:
        return jsonify({"success": False, "mensagem": "O jogo já foi encerrado."})

    # Registra jogada
    jogo["jogadores"][jogador] = escolha

    # Inicializa placar do jogador se ainda não existir
    if jogador not in jogo["placar"]:
        jogo["placar"][jogador] = 0

    # Verifica status atual
    jogadores_faltantes = jogo["jogadores_necessarios"] - len(jogo["jogadores"])
    
    if jogadores_faltantes > 0:
        return jsonify({
            "success": True,
            "status": "aguardando",
            "mensagem": f"Aguardando {jogadores_faltantes} jogador(es)...",
            "jogadores_conectados": list(jogo["jogadores"].keys()),
            "rodada": jogo["rodada_atual"]
        })

    # Todos jogaram -> calcular resultado
    resultado = calcular_resultado(jogo["jogadores"])

    # Atualiza placar para o vencedor
    if "venceu" in resultado:
        for nome in jogo["jogadores"]:
            if nome in resultado:
                jogo["placar"][nome] += 1

    # Adiciona ao histórico
    jogo["historico"].append({
        "rodada": jogo["rodada_atual"],
        "jogadas": jogo["jogadores"].copy(),
        "resultado": resultado
    })

    # Prepara resposta
    response_data = {
        "success": True,
        "status": "resultado",
        "resultado": resultado,
        "placar": jogo["placar"],
        "rodada": jogo["rodada_atual"],
        "jogadores": list(jogo["jogadores"].keys())
    }

    # Limpa jogadas para próxima rodada
    jogo["jogadores"] = {}
    jogo["rodada_atual"] += 1

    return jsonify(response_data)

@app.route('/status/<id_jogo>')
def status_jogo(id_jogo):
    if id_jogo not in jogos:
        return jsonify({"success": False, "erro": "Jogo não encontrado."}), 404

    jogo = jogos[id_jogo]
    
    return jsonify({
        "success": True,
        "jogando": jogo["jogando"],
        "jogadores_conectados": list(jogo["jogadores"].keys()),
        "jogadores_necessarios": jogo["jogadores_necessarios"],
        "rodada": jogo["rodada_atual"],
        "placar": jogo["placar"]
    })

@app.route('/encerrar_jogo/<id_jogo>', methods=['POST'])
def encerrar_jogo(id_jogo):
    if id_jogo not in jogos:
        return jsonify({"success": False, "erro": "Jogo não encontrado."}), 404

    jogo = jogos[id_jogo]
    placar_final = jogo.get("placar", {})
    jogo["jogando"] = False

    return jsonify({
        "success": True,
        "mensagem": "Jogo encerrado!",
        "placar_final": placar_final
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)