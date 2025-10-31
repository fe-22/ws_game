from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Estrutura de dados para armazenar jogos
jogos = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/criar_jogo', methods=['POST'])
def criar_jogo():
    data = request.get_json()
    id_jogo = data.get("id_jogo")
    jogadores_necessarios = int(data.get("jogadores_necessarios", 2))

    # Inicializa o jogo com placar e rodada
    jogos[id_jogo] = {
        "jogadores": {},             # escolhas da rodada atual
        "jogadores_necessarios": jogadores_necessarios,
        "placar": {},                # inicializa placar
        "rodada_atual": 1,
        "jogando": True
    }

    return jsonify({
        "mensagem": "Jogo criado com sucesso!",
        "id_jogo": id_jogo,
        "link_convite": f"http://127.0.0.1:8501/?jogo={id_jogo}"
    })


@app.route('/jogar/<id_jogo>/<jogador>', methods=['POST'])
def jogar(id_jogo, jogador):
    data = request.get_json()
    escolha = data.get("escolha")

    if id_jogo not in jogos:
        return jsonify({"erro": "Jogo não encontrado."}), 404

    jogo = jogos[id_jogo]

    if not jogo["jogando"]:
        return jsonify({"mensagem": "O jogo já foi encerrado."})

    # Registra jogada
    jogo["jogadores"][jogador] = escolha

    # Inicializa placar do jogador se ainda não existir
    if jogador not in jogo["placar"]:
        jogo["placar"][jogador] = 0

    # Espera todos jogarem
    if len(jogo["jogadores"]) < jogo["jogadores_necessarios"]:
        return jsonify({"mensagem": "Aguardando outros jogadores..."})

    # Todos jogaram -> calcular resultado da rodada
    jogadas = list(jogo["jogadores"].values())
    resultado = calcular_resultado(jogadas)

    # Atualiza placar
    for nome, jog in jogo["jogadores"].items():
        if resultado.startswith(nome):
            jogo["placar"][nome] += 1

    # Limpa jogadas para próxima rodada
    jogo["jogadores"] = {}
    jogo["rodada_atual"] += 1

    return jsonify({
        "resultado_rodada": resultado,
        "placar": jogo["placar"],
        "rodada": jogo["rodada_atual"]
    })


def calcular_resultado(jogadas):
    """Função simples para comparar jogadas"""
    if all(j == jogadas[0] for j in jogadas):
        return "Empate!"

    # Lógica de pedra, papel, tesoura
    if "pedra" in jogadas and "tesoura" in jogadas and "papel" not in jogadas:
        return "Pedra venceu!"
    elif "papel" in jogadas and "pedra" in jogadas and "tesoura" not in jogadas:
        return "Papel venceu!"
    elif "tesoura" in jogadas and "papel" in jogadas and "pedra" not in jogadas:
        return "Tesoura venceu!"
    else:
        return "Resultado indefinido."


@app.route('/encerrar_jogo/<id_jogo>', methods=['POST'])
def encerrar_jogo(id_jogo):
    if id_jogo not in jogos:
        return jsonify({"erro": "Jogo não encontrado."}), 404

    jogo = jogos[id_jogo]
    placar_final = jogo.get("placar", {})
    del jogos[id_jogo]

    return jsonify({
        "mensagem": "Jogo encerrado!",
        "placar_final": placar_final
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
