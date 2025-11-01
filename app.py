import streamlit as st
import random
import string

st.title("🎮 Jogo Pedra, Papel e Tesoura")
st.write("Crie e participe de jogos online!")

# Estrutura de dados para armazenar jogos
if 'jogos' not in st.session_state:
    st.session_state.jogos = {}

def gerar_id_jogo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def calcular_resultado(jogadas):
    """Calcula o resultado do jogo pedra, papel, tesoura"""
    if len(jogadas) < 2:
        return "Aguardando mais jogadores..."
    
    if all(j == list(jogadas.values())[0] for j in jogadas.values()):
        return "Empate!"
    
    # Lógica do jogo
    jogadas_unicas = set(jogadas.values())
    
    if jogadas_unicas == {"pedra", "tesoura"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "pedra"][0]
        return f"{vencedor} venceu com Pedra! 🪨"
    elif jogadas_unicas == {"papel", "pedra"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "papel"][0]
        return f"{vencedor} venceu com Papel! 📄"
    elif jogadas_unicas == {"tesoura", "papel"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "tesoura"][0]
        return f"{vencedor} venceu com Tesoura! ✂️"
    else:
        return "Escolhas diferentes - sem vencedor claro"

# Interface Streamlit
tab1, tab2, tab3 = st.tabs(["Criar Jogo", "Jogar", "Status"])

with tab1:
    st.header("Criar Novo Jogo")
    jogadores_necessarios = st.number_input("Jogadores necessários", min_value=2, max_value=10, value=2)
    
    if st.button("Criar Jogo"):
        id_jogo = gerar_id_jogo()
        st.session_state.jogos[id_jogo] = {
            "jogadores": {},
            "jogadores_necessarios": jogadores_necessarios,
            "placar": {},
            "rodada_atual": 1,
            "jogando": True,
            "historico": []
        }
        st.success(f"Jogo criado! ID: **{id_jogo}**")
        st.info("Compartilhe este ID com outros jogadores")

with tab2:
    st.header("Fazer Jogada")
    id_jogo = st.text_input("ID do Jogo")
    jogador = st.text_input("Seu nome")
    escolha = st.selectbox("Sua escolha", ["pedra", "papel", "tesoura"])
    
    if st.button("Jogar"):
        if id_jogo and id_jogo in st.session_state.jogos:
            jogo = st.session_state.jogos[id_jogo]
            
            if not jogo["jogando"]:
                st.error("Este jogo já foi encerrado.")
            elif jogador:
                # Registra jogada
                jogo["jogadores"][jogador] = escolha
                
                # Inicializa placar
                if jogador not in jogo["placar"]:
                    jogo["placar"][jogador] = 0
                
                # Verifica se todos jogaram
                if len(jogo["jogadores"]) >= jogo["jogadores_necessarios"]:
                    resultado = calcular_resultado(jogo["jogadores"])
                    st.success(f"Resultado: {resultado}")
                    
                    # Atualiza placar para vencedor
                    if "venceu" in resultado:
                        for nome in jogo["jogadores"]:
                            if nome in resultado:
                                jogo["placar"][nome] += 1
                    
                    # Limpa para próxima rodada
                    jogo["jogadores"] = {}
                    jogo["rodada_atual"] += 1
                else:
                    faltantes = jogo['jogadores_necessarios'] - len(jogo['jogadores'])
                    st.info(f"Aguardando {faltantes} jogador(es)...")
                    st.write(f"Jogadores atuais: {list(jogo['jogadores'].keys())}")
            else:
                st.error("Digite seu nome!")
        else:
            st.error("Jogo não encontrado!")

with tab3:
    st.header("Status do Jogo")
    id_status = st.text_input("ID do Jogo para ver status", key="status_input")
    
    if st.button("Ver Status"):
        if id_status and id_status in st.session_state.jogos:
            jogo = st.session_state.jogos[id_status]
            st.write(f"**Rodada:** {jogo['rodada_atual']}")
            st.write(f"**Jogadores conectados:** {list(jogo['jogadores'].keys())}")
            st.write(f"**Placar:** {jogo['placar']}")
            st.write(f"**Status:** {'Jogando' if jogo['jogando'] else 'Encerrado'}")
            
            if st.button("Encerrar Jogo"):
                jogo["jogando"] = False
                st.success("Jogo encerrado!")
        else:
            st.error("Jogo não encontrado!")
