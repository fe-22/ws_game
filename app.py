import streamlit as st
import random
import string

# Configuração da página
st.set_page_config(
    page_title="🎮 Pedra, Papel e Tesoura",
    page_icon="🎮",
    layout="wide"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF4B4B;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .game-card {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .winner {
        color: #00D26A;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .choice-btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        margin: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho bonito
st.markdown('<div class="main-header">🎮 Pedra, Papel e Tesoura Online</div>', unsafe_allow_html=True)

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
        return "Empate! 🤝"
    
    jogadas_unicas = set(jogadas.values())
    
    if jogadas_unicas == {"pedra", "tesoura"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "pedra"][0]
        return f"🏆 {vencedor} venceu com Pedra! 🪨 (quebrou tesoura ✂️)"
    elif jogadas_unicas == {"papel", "pedra"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "papel"][0]
        return f"🏆 {vencedor} venceu com Papel! 📄 (embrulhou pedra 🪨)"
    elif jogadas_unicas == {"tesoura", "papel"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "tesoura"][0]
        return f"🏆 {vencedor} venceu com Tesoura! ✂️ (cortou papel 📄)"
    else:
        return "Escolhas diferentes - sem vencedor claro"

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Início", "🎯 Criar Jogo", "🎮 Jogar", "📊 Status"])

with tab1:
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.header("Bem-vindo ao Jogo!")
    st.write("""
    ### Como jogar:
    1. **Crie um jogo** na aba "Criar Jogo"
    2. **Compartilhe o ID** com seus amigos
    3. **Faça suas jogadas** na aba "Jogar"
    4. **Acompanhe o placar** na aba "Status"
    
    ### Regras:
    - 🪨 Pedra quebra tesoura ✂️
    - 📄 Papel embrulha pedra 🪨  
    - ✂️ Tesoura corta papel 📄
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("Criar Novo Jogo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        jogadores_necessarios = st.number_input(
            "Número de jogadores", 
            min_value=2, 
            max_value=10, 
            value=2,
            help="Quantos jogadores são necessários para cada rodada"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🎯 Criar Novo Jogo", use_container_width=True):
            id_jogo = gerar_id_jogo()
            st.session_state.jogos[id_jogo] = {
                "jogadores": {},
                "jogadores_necessarios": jogadores_necessarios,
                "placar": {},
                "rodada_atual": 1,
                "jogando": True,
                "historico": []
            }
            st.success(f"🎉 Jogo criado com sucesso!")
            st.info(f"**ID do Jogo:** `{id_jogo}`")
            st.warning("⚠️ Compartilhe este ID com outros jogadores")

with tab3:
    st.header("Fazer Jogada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        id_jogo = st.text_input("ID do Jogo", placeholder="Digite o ID do jogo")
        jogador = st.text_input("Seu nome", placeholder="Como você quer ser chamado?")
    
    with col2:
        st.subheader("Sua escolha:")
        escolha = st.radio(
            "Escolha sua jogada:",
            ["pedra", "papel", "tesoura"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Ícones para as escolhas
        icons = {"pedra": "🪨", "papel": "📄", "tesoura": "✂️"}
        st.write(f"Você escolheu: **{escolha}** {icons[escolha]}")
    
    if st.button("🎮 Fazer Jogada", type="primary", use_container_width=True):
        if not id_jogo or not jogador:
            st.error("❌ Por favor, preencha o ID do jogo e seu nome")
        elif id_jogo not in st.session_state.jogos:
            st.error("❌ Jogo não encontrado! Verifique o ID")
        else:
            jogo = st.session_state.jogos[id_jogo]
            
            if not jogo["jogando"]:
                st.error("❌ Este jogo já foi encerrado.")
            else:
                # Registra jogada
                jogo["jogadores"][jogador] = escolha
                
                # Inicializa placar
                if jogador not in jogo["placar"]:
                    jogo["placar"][jogador] = 0
                
                # Verifica se todos jogaram
                if len(jogo["jogadores"]) >= jogo["jogadores_necessarios"]:
                    resultado = calcular_resultado(jogo["jogadores"])
                    st.balloons()
                    st.success(f"**Resultado da Rodada {jogo['rodada_atual']}:** {resultado}")
                    
                    # Atualiza placar para vencedor
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
                    
                    # Limpa para próxima rodada
                    jogo["jogadores"] = {}
                    jogo["rodada_atual"] += 1
                    
                    # Mostra placar atualizado
                    st.subheader("📊 Placar Atual:")
                    for jogador, pontos in jogo["placar"].items():
                        st.write(f"**{jogador}:** {pontos} ponto(s)")
                else:
                    faltantes = jogo['jogadores_necessarios'] - len(jogo['jogadores'])
                    st.info(f"⏳ Aguardando {faltantes} jogador(es)...")
                    st.write(f"**Jogadores conectados:** {list(jogo['jogadores'].keys())}")

with tab4:
    st.header("Status do Jogo")
    
    id_status = st.text_input("ID do Jogo para ver status", key="status_input")
    
    if st.button("🔍 Ver Status", use_container_width=True):
        if id_status and id_status in st.session_state.jogos:
            jogo = st.session_state.jogos[id_status]
            
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Informações do Jogo")
                st.write(f"**Rodada Atual:** {jogo['rodada_atual']}")
                st.write(f"**Status:** {'🟢 Jogando' if jogo['jogando'] else '🔴 Encerrado'}")
                st.write(f"**Jogadores Necessários:** {jogo['jogadores_necessarios']}")
                st.write(f"**Jogadores Conectados:** {len(jogo['jogadores'])}")
                
            with col2:
                st.subheader("🎯 Jogadores Atuais")
                if jogo['jogadores']:
                    for jogador in jogo['jogadores']:
                        st.write(f"• {jogador}")
                else:
                    st.write("Nenhum jogador conectado nesta rodada")
            
            st.subheader("🏆 Placar Geral")
            if jogo['placar']:
                for jogador, pontos in sorted(jogo['placar'].items(), key=lambda x: x[1], reverse=True):
                    st.write(f"**{jogador}:** {pontos} ponto(s)")
            else:
                st.write("Nenhum ponto marcado ainda")
            
            # Botão para encerrar jogo
            if jogo['jogando']:
                if st.button("🛑 Encerrar Jogo", type="secondary"):
                    jogo["jogando"] = False
                    st.success("Jogo encerrado com sucesso!")
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Jogo não encontrado! Verifique o ID")

# Rodapé
st.markdown("---")
st.markdown("🎮 Desenvolvido com Streamlit | Pedra, Papel e Tesoura Online")
