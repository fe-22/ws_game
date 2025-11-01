import streamlit as st
import random
import string

# Configuração da página para matching exato com seu HTML
st.set_page_config(
    page_title="🎮 Pedra, Papel e Tesoura - Multiplayer",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS para replicar exatamente seu template
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        overflow: hidden;
    }

    .header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 30px;
        text-align: center;
    }

    .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
    }

    .header p {
        font-size: 1.1em;
        opacity: 0.9;
    }

    .content {
        padding: 30px;
    }

    .tab-buttons {
        display: flex;
        margin-bottom: 30px;
        background: #f8f9fa;
        border-radius: 10px;
        padding: 5px;
    }

    .tab-btn {
        flex: 1;
        padding: 15px;
        border: none;
        background: none;
        font-size: 1.1em;
        font-weight: 600;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .tab-btn.active {
        background: #667eea;
        color: white;
    }

    .form-group {
        margin-bottom: 20px;
    }

    label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
        color: #333;
    }

    .stTextInput input, .stSelectbox select {
        width: 100%;
        padding: 12px;
        border: 2px solid #e9ecef !important;
        border-radius: 8px;
        font-size: 1em;
        transition: border-color 0.3s ease;
    }

    .stTextInput input:focus, .stSelectbox select:focus {
        outline: none;
        border-color: #667eea !important;
    }

    .custom-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1em;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        width: 100%;
        margin: 10px 0;
    }

    .custom-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    .btn-secondary {
        background: linear-gradient(135deg, #fd746c 0%, #ff9068 100%);
    }

    .game-id {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        border: 2px dashed #667eea;
    }

    .choice-buttons {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 20px 0;
    }

    .choice-btn {
        padding: 20px;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        background: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.1em;
        font-weight: 600;
        text-align: center;
    }

    .choice-btn:hover {
        border-color: #667eea;
        transform: translateY(-2px);
    }

    .choice-btn.selected {
        border-color: #667eea;
        background: #667eea;
        color: white;
    }

    .status-box {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        border-left: 4px solid #2196f3;
    }

    .success-box {
        background: #e8f5e8;
        border-left-color: #4caf50;
    }

    .error-box {
        background: #ffebee;
        border-left-color: #f44336;
    }

    .players-list {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .player-item {
        padding: 8px;
        margin: 5px 0;
        background: white;
        border-radius: 5px;
        border-left: 3px solid #667eea;
    }

    .footer {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        text-align: center;
        padding: 20px;
        margin-top: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .developer-info {
        font-size: 1.1em;
        margin-bottom: 10px;
    }

    .developer-info strong {
        color: #ff6b6b;
    }

    .contact-info {
        font-size: 0.9em;
        opacity: 0.8;
        margin-bottom: 5px;
    }

    .footer-links {
        margin-top: 10px;
    }

    .footer-links a {
        color: #667eea;
        text-decoration: none;
        margin: 0 10px;
        transition: color 0.3s ease;
    }

    .footer-links a:hover {
        color: #ff6b6b;
    }

    /* Remove Streamlit default styles */
    .main .block-container {
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Estado da sessão
if 'jogos' not in st.session_state:
    st.session_state.jogos = {}
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "home"
if 'selected_choice' not in st.session_state:
    st.session_state.selected_choice = None
if 'current_game_id' not in st.session_state:
    st.session_state.current_game_id = None

def gerar_id_jogo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def calcular_resultado(jogadas):
    if len(jogadas) < 2:
        return "Aguardando mais jogadores..."
    
    if all(j == list(jogadas.values())[0] for j in jogadas.values()):
        return "Empate! 🤝"
    
    jogadas_unicas = set(jogadas.values())
    
    if jogadas_unicas == {"pedra", "tesoura"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "pedra"][0]
        return f"🏆 {vencedor} venceu com Pedra! 🪨"
    elif jogadas_unicas == {"papel", "pedra"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "papel"][0]
        return f"🏆 {vencedor} venceu com Papel! 📄"
    elif jogadas_unicas == {"tesoura", "papel"}:
        vencedor = [nome for nome, escolha in jogadas.items() if escolha == "tesoura"][0]
        return f"🏆 {vencedor} venceu com Tesoura! ✂️"
    else:
        return "Escolhas diferentes - sem vencedor claro"

# Layout principal replicando seu HTML
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🎮 Pedra, Papel e Tesoura</h1>
    <p>Jogue com seus amigos em tempo real!</p>
</div>
""", unsafe_allow_html=True)

# Content
st.markdown('<div class="content">', unsafe_allow_html=True)

# Tab buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Início", use_container_width=True, key="tab_home"):
        st.session_state.current_tab = "home"
with col2:
    if st.button("🎯 Criar Jogo", use_container_width=True, key="tab_create"):
        st.session_state.current_tab = "create"
with col3:
    if st.button("👥 Jogar", use_container_width=True, key="tab_play"):
        st.session_state.current_tab = "play"

st.markdown("</div>", unsafe_allow_html=True)  # Close content

# Tab contents
if st.session_state.current_tab == "home":
    st.markdown("""
    <div class="content">
        <h2>Bem-vindo ao Jogo!</h2>
        <div class="status-box">
            <h3>🎯 Como Jogar:</h3>
            <ol style="margin-left: 20px; margin-top: 10px;">
                <li>Crie um jogo na aba 'Criar Jogo'</li>
                <li>Compartilhe o ID do jogo com amigos</li>
                <li>Entre na aba 'Jogar' para participar</li>
                <li>Escolha pedra, papel ou tesoura</li>
                <li>Veja quem venceu cada rodada!</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_tab == "create":
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.subheader("Criar Novo Jogo")
    
    jogadores_necessarios = st.selectbox(
        "Número de Jogadores:",
        [2, 3, 4],
        index=0,
        key="players_select"
    )
    
    if st.button("🎮 Criar Jogo", key="create_game", use_container_width=True):
        id_jogo = gerar_id_jogo()
        st.session_state.jogos[id_jogo] = {
            "jogadores": {},
            "jogadores_necessarios": jogadores_necessarios,
            "placar": {},
            "rodada_atual": 1,
            "jogando": True,
            "historico": []
        }
        st.session_state.current_game_id = id_jogo
        st.success("🎉 Jogo criado com sucesso!")
        
        st.markdown(f"""
        <div class="game-id">
            ID do Jogo: <span style="color: #667eea;">{id_jogo}</span>
        </div>
        <p>Compartilhe este ID com seus amigos!</p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_tab == "play":
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.subheader("Entrar no Jogo")
    
    game_code = st.text_input("ID do Jogo:", placeholder="Digite o ID do jogo", key="game_code")
    player_name = st.text_input("Seu Nome:", placeholder="Como quer ser chamado?", key="player_name")
    
    if st.button("🎯 Entrar no Jogo", key="join_game", use_container_width=True):
        if not game_code or not player_name:
            st.error("❌ Por favor, preencha todos os campos!")
        elif game_code not in st.session_state.jogos:
            st.error("❌ Jogo não encontrado! Verifique o ID")
        else:
            st.session_state.current_game_id = game_code
            st.success(f"✅ {player_name} entrou no jogo!")
    
    # Área do jogo
    if st.session_state.current_game_id and st.session_state.current_game_id in st.session_state.jogos:
        jogo = st.session_state.jogos[st.session_state.current_game_id]
        
        # Status do jogo
        st.markdown(f"""
        <div class="status-box">
            <strong>Rodada {jogo['rodada_atual']}</strong><br>
            Jogadores: {len(jogo['jogadores'])}/{jogo['jogadores_necessarios']}<br>
            Status: {'🟢 Jogo ativo' if jogo['jogando'] else '🔴 Jogo encerrado'}
        </div>
        """, unsafe_allow_html=True)
        
        # Botões de escolha
        st.markdown("<h4>Faça sua jogada:</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🪨 Pedra", use_container_width=True, key="choice_rock"):
                st.session_state.selected_choice = "pedra"
        with col2:
            if st.button("📄 Papel", use_container_width=True, key="choice_paper"):
                st.session_state.selected_choice = "papel"
        with col3:
            if st.button("✂️ Tesoura", use_container_width=True, key="choice_scissors"):
                st.session_state.selected_choice = "tesoura"
        
        # Processar jogada
        if st.session_state.selected_choice and player_name:
            jogo["jogadores"][player_name] = st.session_state.selected_choice
            
            if player_name not in jogo["placar"]:
                jogo["placar"][player_name] = 0
            
            # Verificar se todos jogaram
            if len(jogo["jogadores"]) >= jogo["jogadores_necessarios"]:
                resultado = calcular_resultado(jogo["jogadores"])
                st.balloons()
                
                st.markdown(f"""
                <div class="status-box success-box">
                    <h3>🎉 Resultado da Rodada!</h3>
                    <p><strong>{resultado}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Limpar para próxima rodada
                jogo["jogadores"] = {}
                jogo["rodada_atual"] += 1
                st.session_state.selected_choice = None
                st.rerun()
            else:
                faltantes = jogo['jogadores_necessarios'] - len(jogo['jogadores'])
                st.info(f"⏳ Aguardando {faltantes} jogador(es)...")
        
        # Lista de jogadores
        if jogo['jogadores']:
            st.markdown("<h4>Jogadores Conectados:</h4>", unsafe_allow_html=True)
            for jogador in jogo['jogadores']:
                st.markdown(f'<div class="player-item">{jogador}</div>', unsafe_allow_html=True)
        
        # Botão encerrar
        if st.button("⏹️ Encerrar Jogo", type="secondary", use_container_width=True):
            jogo["jogando"] = False
            st.success("Jogo encerrado!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <div class="developer-info">
            <strong>Desenvolvido por: Fthec</strong>
        </div>
        <div class="contact-info">
            📧 Email: fernandoalexthec@gmail.com | 📱 Telefone: (11) 98217-0425
        </div>
        <div class="contact-info">
            📅 Ano: 2025
        </div>
        <div class="footer-links">
            <a href="https://home-page-76ks.onrender.com/" target="_blank">Portfólio</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close container
st.markdown('</div>', unsafe_allow_html=True)  # Close main
