import streamlit as st
import random
import string

# Configuração da página
st.set_page_config(
    page_title="🎮 Pedra, Papel e Tesoura - Multiplayer",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS ajustado - Header menor e melhorias
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 10px;
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
        padding: 20px;
        text-align: center;
    }

    .header h1 {
        font-size: 1.8em;
        margin-bottom: 5px;
    }

    .header p {
        font-size: 0.9em;
        opacity: 0.9;
    }

    .content {
        padding: 20px;
    }

    .form-group {
        margin-bottom: 15px;
    }

    label {
        display: block;
        margin-bottom: 5px;
        font-weight: 600;
        color: #333;
        font-size: 0.9em;
    }

    .stTextInput input, .stSelectbox select {
        width: 100%;
        padding: 10px;
        border: 2px solid #e9ecef !important;
        border-radius: 8px;
        font-size: 0.9em;
    }

    .custom-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        font-size: 1em;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        width: 100%;
        margin: 8px 0;
    }

    .btn-secondary {
        background: linear-gradient(135deg, #fd746c 0%, #ff9068 100%);
    }

    .game-id {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        margin: 15px 0;
        text-align: center;
        font-size: 1em;
        font-weight: bold;
        border: 2px dashed #667eea;
    }

    .share-link {
        background: #e3f2fd;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
        font-size: 0.85em;
    }

    .choice-buttons {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin: 15px 0;
    }

    .choice-btn {
        padding: 15px;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        background: white;
        font-size: 1em;
        font-weight: 600;
        text-align: center;
    }

    .status-box {
        background: #e3f2fd;
        padding: 12px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #2196f3;
        font-size: 0.9em;
    }

    .success-box {
        background: #e8f5e8;
        border-left-color: #4caf50;
    }

    .players-list {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        font-size: 0.9em;
    }

    .player-item {
        padding: 6px;
        margin: 3px 0;
        background: white;
        border-radius: 5px;
        border-left: 3px solid #667eea;
    }

    .footer {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        text-align: center;
        padding: 15px;
        margin-top: 15px;
        border-radius: 10px;
        font-size: 0.8em;
    }

    /* Remove espaçamento excessivo do Streamlit */
    .main .block-container {
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs mais compactas */
    .stButton button {
        margin: 2px;
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

# Layout principal
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="container">', unsafe_allow_html=True)

# Header compacto
st.markdown("""
<div class="header">
    <h1>🎮 Pedra, Papel e Tesoura</h1>
    <p>Jogue com seus amigos em tempo real!</p>
</div>
""", unsafe_allow_html=True)

# Content
st.markdown('<div class="content">', unsafe_allow_html=True)

# Tabs compactas
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

# Tab contents
if st.session_state.current_tab == "home":
    st.subheader("Bem-vindo ao Jogo!")
    st.markdown("""
    <div class="status-box">
        <h4>🎯 Como Jogar:</h4>
        <ol style="margin-left: 20px; margin-top: 8px; font-size: 0.9em;">
            <li><strong>Crie um jogo</strong> na aba 'Criar Jogo'</li>
            <li><strong>Compartilhe o link</strong> com amigos</li>
            <li><strong>Entre no jogo</strong> na aba 'Jogar'</li>
            <li><strong>Escolha</strong> pedra, papel ou tesoura</li>
            <li><strong>Veja quem venceu</strong> cada rodada!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_tab == "create":
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
        st.session_state.current_tab = "play"  # Vai direto para jogar
        
        st.success("🎉 Jogo criado com sucesso!")
        
        # Mostra ID do jogo e link para compartilhar
        st.markdown(f"""
        <div class="game-id">
            🆔 ID do Jogo: <span style="color: #667eea; font-size: 1.1em;">{id_jogo}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Link para compartilhar
        app_url = "https://wsgame-c5a7wrr3a7rs6ufcehbdtw.streamlit.app"
        share_message = f"🎮 Entre no meu jogo de Pedra, Papel e Tesoura! ID: {id_jogo} - Acesse: {app_url}"
        
        st.markdown(f"""
        <div class="share-link">
            <strong>📤 Compartilhe com amigos:</strong><br>
            <div style="background: white; padding: 8px; border-radius: 5px; margin: 8px 0; font-size: 0.8em;">
                {share_message}
            </div>
            <button onclick="navigator.clipboard.writeText('{share_message}')" style="background: #667eea; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 0.8em;">
                📋 Copiar Link
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 Agora vá para a aba 'Jogar' para começar!")

elif st.session_state.current_tab == "play":
    st.subheader("Entrar no Jogo")
    
    # Se já tem um jogo criado, mostra o ID atual
    if st.session_state.current_game_id:
        st.markdown(f"""
        <div class="status-box">
            <strong>Jogo Ativo:</strong> {st.session_state.current_game_id}
        </div>
        """, unsafe_allow_html=True)
    
    game_code = st.text_input("ID do Jogo:", placeholder="Digite o ID do jogo", key="game_code")
    player_name = st.text_input("Seu Nome:", placeholder="Como quer ser chamado?", key="player_name")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Entrar no Jogo", key="join_game", use_container_width=True):
            if not game_code or not player_name:
                st.error("❌ Preencha todos os campos!")
            elif game_code not in st.session_state.jogos:
                st.error("❌ Jogo não encontrado!")
            else:
                st.session_state.current_game_id = game_code
                st.success(f"✅ {player_name} entrou no jogo!")
                st.rerun()
    
    with col2:
        if st.button("🆕 Criar Novo Jogo", key="create_from_play", use_container_width=True):
            st.session_state.current_tab = "create"
            st.rerun()
    
    # Área do jogo
    if st.session_state.current_game_id and st.session_state.current_game_id in st.session_state.jogos:
        jogo = st.session_state.jogos[st.session_state.current_game_id]
        player_name = st.session_state.get('player_name', player_name)
        
        # Status do jogo
        st.markdown(f"""
        <div class="status-box">
            <strong>Rodada {jogo['rodada_atual']}</strong> | 
            Jogadores: {len(jogo['jogadores'])}/{jogo['jogadores_necessarios']} |
            Status: {'🟢 Ativo' if jogo['jogando'] else '🔴 Encerrado'}
        </div>
        """, unsafe_allow_html=True)
        
        # Botões de escolha
        st.markdown("<h4>Faça sua jogada:</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rock_clicked = st.button("🪨 Pedra", use_container_width=True, key="choice_rock")
            if rock_clicked:
                st.session_state.selected_choice = "pedra"
        with col2:
            paper_clicked = st.button("📄 Papel", use_container_width=True, key="choice_paper")
            if paper_clicked:
                st.session_state.selected_choice = "papel"
        with col3:
            scissors_clicked = st.button("✂️ Tesoura", use_container_width=True, key="choice_scissors")
            if scissors_clicked:
                st.session_state.selected_choice = "tesoura"
        
        # Mostra escolha atual
        if st.session_state.selected_choice:
            st.info(f"🎯 Sua escolha: {st.session_state.selected_choice}")
        
        # Processar jogada
        if st.session_state.selected_choice and player_name and jogo["jogando"]:
            jogo["jogadores"][player_name] = st.session_state.selected_choice
            
            if player_name not in jogo["placar"]:
                jogo["placar"][player_name] = 0
            
            # Verificar se todos jogaram
            if len(jogo["jogadores"]) >= jogo["jogadores_necessarios"]:
                resultado = calcular_resultado(jogo["jogadores"])
                st.balloons()
                
                st.markdown(f"""
                <div class="status-box success-box">
                    <h4>🎉 Resultado da Rodada {jogo['rodada_atual']}!</h4>
                    <p><strong>{resultado}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Atualizar placar para vencedor
                if "venceu" in resultado:
                    for nome in jogo["jogadores"]:
                        if nome in resultado:
                            jogo["placar"][nome] += 1
                
                # Limpar para próxima rodada
                jogo["jogadores"] = {}
                jogo["rodada_atual"] += 1
                st.session_state.selected_choice = None
                st.rerun()
            else:
                faltantes = jogo['jogadores_necessarios'] - len(jogo['jogadores'])
                st.info(f"⏳ Aguardando {faltantes} jogador(es)...")
        
        # Lista de jogadores conectados
        if jogo['jogadores']:
            st.markdown("<h5>Jogadores Conectados:</h5>", unsafe_allow_html=True)
            for jogador, escolha in jogo['jogadores'].items():
                emoji = {"pedra": "🪨", "papel": "📄", "tesoura": "✂️"}.get(escolha, "❓")
                st.markdown(f'<div class="player-item">{emoji} {jogador} - {escolha}</div>', unsafe_allow_html=True)
        
        # Placar
        if jogo['placar']:
            st.markdown("<h5>🏆 Placar:</h5>", unsafe_allow_html=True)
            for jogador, pontos in sorted(jogo['placar'].items(), key=lambda x: x[1], reverse=True):
                st.markdown(f'<div class="player-item">{jogador}: {pontos} ponto(s)</div>', unsafe_allow_html=True)
        
        # Botão encerrar
        if st.button("⏹️ Encerrar Jogo", type="secondary", use_container_width=True):
            jogo["jogando"] = False
            st.success("Jogo encerrado!")
            st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <div style="font-size: 0.8em;">
        <strong>Desenvolvido por: Fthec</strong><br>
        📧 fernandoalexthec@gmail.com | 📱 (11) 98217-0425<br>
        📅 2025 | <a href="https://home-page-76ks.onrender.com/" target="_blank" style="color: #667eea;">Portfólio</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close content
st.markdown('</div>', unsafe_allow_html=True)  # Close container
st.markdown('</div>', unsafe_allow_html=True)  # Close main
