import streamlit as st
import json
import os
import base64
import time



# Configuração da página
st.set_page_config(page_title="Portal BI", layout="wide")

# Carregando dados dos setores
with open('configs/setores.json', 'r', encoding='utf-8') as f:
    setores = json.load(f)

# Inicializando session_state
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'setor_atual' not in st.session_state:
    st.session_state['setor_atual'] = ''
if 'admin_liberado' not in st.session_state:
    st.session_state['admin_liberado'] = []
if 'painel_selecionado' not in st.session_state:
    st.session_state['painel_selecionado'] = None

# === TELA DE SETOR (APÓS LOGIN) ===
def get_base64_image(image_path):
    """Converte imagem local para base64 para uso no HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Senha geral (acesso irrestrito a qualquer painel)
SENHA_GESTOR_GERAL = "#acessoGeral2735!"


def tela_login():
    logo_path = "assets/logo.png"  # Caminho da logo principal
    powerbi_logo_path = "assets/Power-BI-Logo.png"  # Caminho da logo do Power BI

    # Verifica se as logos existem
    if os.path.exists(logo_path) and os.path.exists(powerbi_logo_path):
        logo_base64 = get_base64_image(logo_path)
        powerbi_logo_base64 = get_base64_image(powerbi_logo_path)

        # Exibe a logo principal e o título com o gradiente de fundo
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #000000, #FFA500, #D4A011);
                padding: 8px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                width: 100%;
            '>
                <!-- Logo Principal -->
                <div style='display: flex; align-items: center;'>
                    <img src='data:image/png;base64,{logo_base64}' style='height: 80px; margin-right: 20px;' alt='Logo'>
                </div>
                <!-- Título Centralizado -->
                <div style='flex-grow: 1; text-align: center;'>
                    <h2 style='
                        margin: 0;
                        font-size: 42px;
                        font-family: "Arial Rounded MT Bold", Arial, sans-serif !important;
                        color: #FFE378;
                        padding-top: 48px;
                    '>PORTAL DE BUSINESS INTELLIGENCE</h2>
                </div>
                <!-- Logo Power BI no canto direito -->
                <div style='display: flex; align-items: center;'>
                    <img src='data:image/png;base64,{powerbi_logo_base64}' style='height: 90px;' alt='Logo Power BI'>
                </div>
            </div>
        """, unsafe_allow_html=True)


    # Resumo da ferramenta
    st.markdown(""" 
        <div style='margin-top: 10px; font-size:14px; color:#2E1900; font-family: "Open Sans", sans-serif;'>
        Este portal tem como objetivo centralizar os painéis de BI da organização, para o acesso organizado dos dados de cada setor. 
        Cada setor possui uma senha para garantir a segurança do acesso. Além disso, alguns painéis são restritos e exigem autenticação adicional, para que apenas usuários administrativos tenham permissão para visualizá-los.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")


    # Estilo para personalizar as opções do selectbox
    st.markdown("""
        <style>
            /* Personalizando o título do selectbox */
            .stSelectbox label {
                color: #241400 !important;
                font-size: 20px !important;
            }

            /* Estilizando o campo da selectbox */
            .stSelectbox border {
                color: #241400 !important;
                border: 2px solid #6B3B00 !important;  /* <-- Borda personalizada */
                border-radius: 6px !important;
                padding: 4px 8px !important;
            }

            /* Estilizando a área visível da selectbox com borda em todas as direções */
            div[data-baseweb="select"] {
                width: 99% !important;
                border-width: 1.5px !important;
                border-style: solid !important;
                border-color: #6B3B00 !important;
                border-radius: 6px !important;
                padding: 4px 8px !important;
                color: #241400 !important;
            }               

            /* Fundo das opções */
            .stSelectbox div[role="listbox"] {
                background-color: white !important;
            }

            /* Cor do texto das opções */
            .st-b6 {
                color: #703400 !important;
            }

            /* Campo de texto (text_input), incluindo senha */
            input[type="password"],
            input[type="text"] {
                width: 100% !important;
                border: 1.5px solid #6B3B00 !important;
                border-radius: 6px !important;
                padding: 10px !important;
                color: #241400 !important;
                font-size: 16px !important;
            }                

            /* Ajuste de cor de fallback para texto selecionado */
            .st-emotion-cache-1s2v671 {
                color: #241400 !important;
                padding: 0.25rem 1.5rem;
            }
                
            /* Estilo do botão "Entrar" */
            .stButton>button {
                background-color: green;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
            }
            /* Borda no botão de mostrar/ocultar senha */
            button[aria-label="Show password text"],
            button[title="Show password text"],
            button[aria-label="Hide password text"],
            button[title="Hide password text"] {
                border: 1.5px solid #6B3B00 !important;
                border-radius: 6px !important;
            }

            .stButton>button:hover {
                background-color: darkgreen;
            }
                
            .st-bb {
                background-color: rgb(240 242 246 / 0%);
            }                
            
            .stSelectbox label {
                color: #241400 !important;
                font-size: 20px !important;
                text-align: left !important;
            }

        </style>
    """, unsafe_allow_html=True)


    # Campos de login
    setor = st.selectbox("Selecione o tipo de  setor", list(setores.keys()))
    senha = st.text_input("Informe a senha do setor", type="password")


    # Botão e mensagem lado a lado
    col1, col2 = st.columns([1, 10])  # Ajuste os pesos conforme necessário

    with col1:
        login_btn = st.button("Entrar")

    with col2:
        if 'login_erro' in st.session_state and st.session_state['login_erro']:
            st.markdown("""
                <div style="background-color: rgba(219, 0, 0, 0.85); color: white; padding: 10px 16px; 
                            border-radius: 6px; font-weight: bold; font-size: 14px; width: 98%;">
                    🚫 Senha incorreta.
                </div>
            """, unsafe_allow_html=True)


    if login_btn:
        if senha == setores[setor]['senha']:
            # Login padrão por setor
            st.session_state['logado'] = True
            st.session_state['setor_atual'] = setor
            st.session_state['gestor_geral_autenticado'] = False  # <== não é gestor geral
            st.session_state['login_erro'] = False

            # Limpa estado antigo
            st.session_state['painel_pendente'] = None
            st.session_state['painel_avisado'] = False
            st.session_state['senha_restrita'] = ''

            st.rerun()

        elif senha == SENHA_GESTOR_GERAL:
            # Login como gestor geral
            st.session_state['logado'] = True
            st.session_state['setor_atual'] = setor  # ainda precisa escolher um setor
            st.session_state['gestor_geral_autenticado'] = True  # <== MARCA como gestor geral
            st.session_state['login_erro'] = False

            # Limpa estado antigo
            st.session_state['painel_pendente'] = None
            st.session_state['painel_avisado'] = False
            st.session_state['senha_restrita'] = ''

            st.rerun()

        else:
            st.session_state['login_erro'] = True

			

# === FUNÇÃO PARA EXIBIR O PAINEL (HTML LOCAL OU IFRAME) ===
def exibir_painel(painel):
    if 'iframe' in painel:
        # Painel Power BI ou outro via iframe
        st.components.v1.html(painel['iframe'], height=900, scrolling=True)
    elif 'arquivo' in painel:
        # Painel salvo em HTML local
        if os.path.exists(painel['arquivo']):
            with open(painel['arquivo'], 'r', encoding='utf-8') as f:
                html = f.read()
            st.components.v1.html(html, height=900, scrolling=True)
        else:
            st.warning("Arquivo do painel não encontrado.")
    else:
        st.error("Formato do painel inválido.")



# Função de logout
def logout():
    st.session_state['logado'] = False
    st.session_state['setor_atual'] = ''
    st.session_state['painel_selecionado'] = None
    st.session_state['admin_liberado'] = []
    st.session_state['boas_vindas_exibidas'] = False 
    st.session_state['login_erro'] = False

# Função para exibir a tela de seleção do setor após o login
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def tela_setor():
    setor_atual = st.session_state['setor_atual']

    if 'boas_vindas_exibidas' not in st.session_state:
        st.session_state['boas_vindas_exibidas'] = False


    if not st.session_state.get('painel_selecionado'):
        st.markdown(f"""
            <h1 style='
                text-align: center;
                font-weight: bold;
                font-size: 25px;
                color: rgb(194 144 6);
                margin: 0 !important;
                padding: 0 !important;
                line-height: 1.2 !important;
                font-family: sans-serif;
            '>
                Bem-vindo ao setor: {setor_atual}
            </h1>
        """, unsafe_allow_html=True)

        # ✅ Aviso para gestor geral
        if st.session_state.get("gestor_geral_autenticado"):
           st.success(f"🔐 Você está logado no setor {setor_atual} como Gestor Geral. Acesso total liberado.")
        else:
           st.success(f"Você está logado no setor: {setor_atual}")

    # === ESTILO PERSONALIZADO ORIGINAL COM AJUSTES DE TOPO ===
    st.markdown("""
        <style>   
                
            /* Altera a cor de fundo da área principal (onde os painéis aparecem) */
            main[data-testid="stAppViewContainer"] {
                background-color: #FFFDE7;  /* ⬅️ Escolha sua cor aqui */
            }         
                                   
            /* === ESTILO DA SIDEBAR === */
            section[data-testid="stSidebar"] {
                background-color: #ddbc5c6b !important;
            }


            /* Estilo geral para o botão de retração/expansão da sidebar */
            button[data-testid="stBaseButton-headerNoPadding"] {
                background-color: transparent !important; /* ou #E8E7E7 se quiser fundo igual */
                border: none !important;
                box-shadow: none !important;
                padding: 4px !important;
            }

            /* Estilo do ícone da setinha */
            button[data-testid="stBaseButton-headerNoPadding"] span[data-testid="stIconMaterial"] {
                color: #fdefd1 !important;  /* ou qualquer cor que contraste com o fundo */
                fill: #fdefd1 !important;
                font-size: 1.4rem !important;
            }               

            section[data-testid="stSidebar"] button {
                background-color: #001a25d6 !important;
                color: #fdefd1 !important;
                border-radius: 8px !important;
                border: none !important;
                font-size: 10px !important;
                padding: 0.12rem 1.7rem;
            }

            section[data-testid="stSidebar"] button:hover {
                background-color: #00425ed6 !important;
            }
                            
             
            /* === Fixar rodapé da sidebar === */
            #rodape-sidebar {
                position: absolute;
                bottom: 20px;
                width: 85%;
                left: 8%;
            }

                       
            section[data-testid="stSidebar"] {
                position: relative;  /* necessário para que 'absolute' funcione dentro */
                padding-bottom: 80px;  /* espaço para os botões não sobreporem */
            }
                         
            .linha-divisoria {
                border: 1px solid #A36E00;
                margin-top: 0px;
                margin-bottom: 10px;
            }

            /* === REMOVER ESPAÇAMENTO EXCESSIVO NO TOPO === */
            .block-container {
                /* Espaço interno no topo do conteúdo principal (ex: antes do título ou painel) */
                padding-top: 55px !important;

                /* Espaço externo acima do conteúdo principal (separação do topo da tela) */
                margin-top: 20px !important;

                /* Espaço interno à esquerda – controla a "borda" lateral interna do app */
                padding-left: 20px !important;

                /* Espaço interno à direita – controla a "borda" lateral interna do app */
                padding-right: 20px !important;

                /* Permite que o conteúdo use toda a largura disponível da tela */
                max-width: 95% !important;
            }

            .element-container {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }

            iframe {
                margin-top: 0x !important;
                padding-top: 0px !important;
                border: none !important;
                display: block;
            }

            h1 {
                margin-top: 0px !important;
                padding-top: 0px !important;
            }

            .stToast {
                margin-top: 0px !important;
            }
                
            .st-ct {
                padding-right: 1px;
            }
                
        </style>
    """, unsafe_allow_html=True)



    # === TÍTULO DA SIDEBAR ===
    setor_nome = st.session_state.get("setor_atual", "Painéis")
    st.sidebar.markdown(f"""
        <div style='
            font-weight: bold;
            font-size: 25px;
            color: rgb(189 145 0);
            text-align: left;
            padding-left: 20px;
            margin-bottom: 0px;
        '>
            Setor {setor_nome}
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr class='linha-divisoria'>", unsafe_allow_html=True)


    # Senhas para gestores de cada setor (painéis restritos)
    SENHAS_GESTORES = {
        "Comercial": "gestorcomercial578*",
        "Financeiro": "gestor658#financeiro",
        "Diretoria": "@gestor348diretoria",
        "Emissão": "@gestoremissao36d8",
        "Manutenção": "gestor1565#manuten",
        "Operação": "*gestor978operacao#",
        "Gerenciamento de Risco": "@gestoremissao36d8"
    }


    # Obtém o setor atual e seus painéis diretamente do JSON 
    setor_atual = st.session_state['setor_atual']
    paineis = setores[setor_atual].get('paineis', [])

    # === BOTÕES DOS PAINÉIS ===
    for painel in paineis:
        nome = painel['nome'].strip()
        if st.sidebar.button(nome, key=f"btn_{nome}"):
            # 🔄 Zera a flag do toast sempre que um painel for clicado
            st.session_state['toast_exibido'] = False

            if painel.get("restrito"):
                st.session_state['painel_pendente'] = painel
                st.session_state['painel_avisado'] = False
                st.rerun()
            else:
                # ✅ Mostra toast também para painéis não restritos
                st.toast(f"✅ Acesso ao painel '{nome}' liberado! Aguarde, carregando...")
                time.sleep(2.5)

                st.session_state['painel_selecionado'] = painel
                st.session_state['boas_vindas_exibidas'] = True
                st.session_state['painel_avisado'] = False
                st.session_state['painel_pendente'] = None
                st.session_state['toast_exibido'] = True  # Marca que já mostrou o toast
                st.rerun()

    # === CAMPO DE SENHA SE FOR PAINEL RESTRITO === 
    if 'painel_pendente' in st.session_state and st.session_state['painel_pendente']:
        painel = st.session_state['painel_pendente']
        nome_painel = painel['nome'].strip()

        # ✅ Se já autenticou como gestor geral, pula a senha
        if st.session_state.get('gestor_geral_autenticado', False):
            if not st.session_state.get("toast_exibido", False):
                st.toast(f"✅ Acesso ao painel '{nome_painel}' liberado! Aguarde, carregando...")
                time.sleep(2.5)
                st.session_state["toast_exibido"] = True

            st.session_state['painel_selecionado'] = painel
            st.session_state['boas_vindas_exibidas'] = True
            st.session_state['painel_avisado'] = False
            st.session_state['painel_pendente'] = None
            st.rerun()

        else:
            st.sidebar.markdown(f"🔒 Painel **{nome_painel}** requer autenticação")
            senha_input = st.sidebar.text_input("Digite a senha:", type="password", key="senha_restrita")
            acessar = st.sidebar.button("Acessar Painel📈📉📊")

            if not st.session_state.get('painel_avisado', False) and not acessar:
                st.toast(f"⚠️ Painel '{nome_painel}' requer autenticação. Deslize a tela para baixo e insira a senha.")
                time.sleep(2)
                st.session_state['painel_avisado'] = True

            if acessar:
                setor_painel = painel.get("setor", st.session_state.get("setor_atual"))
                senha_gestor = SENHAS_GESTORES.get(setor_painel)

                if senha_input == senha_gestor or senha_input == SENHA_GESTOR_GERAL:
                    if senha_input == SENHA_GESTOR_GERAL:
                        st.session_state['gestor_geral_autenticado'] = True

                    if not st.session_state.get("toast_exibido", False):
                        st.toast(f"✅ Acesso ao painel '{nome_painel}' liberado! Aguarde, carregando...")
                        time.sleep(2.5)
                        st.session_state["toast_exibido"] = True

                    st.session_state['painel_selecionado'] = painel
                    st.session_state['boas_vindas_exibidas'] = True
                    st.session_state['painel_avisado'] = False
                    st.session_state['painel_pendente'] = None
                    st.rerun()
                else:
                    st.sidebar.markdown("""
                        <div style="background-color: rgba(219, 0, 0, 0.75); color: white; padding: 10px 16px; 
                                    border-radius: 6px; font-weight: bold; font-size: 14px; width: 100%;">
                            🚫 Senha incorreta.
                        </div>
                    """, unsafe_allow_html=True)




    # === RODAPÉ DA SIDEBAR ===
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)    
    # Botões "Sair" e "Voltar" no rodapé da sidebar
    sair_col, voltar_col = st.sidebar.columns([2, 2])  # botão "Voltar" menor e mais à direita

    with sair_col:
        if st.button("Sair"):
            logout()
            st.rerun()

    with voltar_col:
        if st.button("Voltar", key="voltar_btn"):
            st.session_state['painel_selecionado'] = ''
            st.session_state['boas_vindas_exibidas'] = False
            st.session_state['painel_pendente'] = None
            st.rerun()

    # === EXIBIÇÃO DO PAINEL SELECIONADO ===
    if 'painel_avisado' not in st.session_state:
        st.session_state['painel_avisado'] = False

    if st.session_state.get('painel_selecionado'):
        painel = st.session_state['painel_selecionado']

        if not st.session_state['painel_avisado']:
            st.toast(f"Carregando painel: {painel['nome']}...", icon="✅")
            st.session_state['painel_avisado'] = True
            st.rerun()

        # Exibir painel a partir do arquivo HTML local
        if os.path.exists(painel['arquivo']):
            with open(painel['arquivo'], 'r', encoding='utf-8') as f:
                html = f.read()
            st.components.v1.html(html, height=900, scrolling=True)
        else:
            st.error("Arquivo HTML do painel não encontrado.")
    else:
        st.info("Selecione um painel na barra lateral para visualizar aqui.")
        st.session_state['painel_avisado'] = False


# Verifica se o usuário está logado
if 'logado' in st.session_state and st.session_state['logado']:
    tela_setor()
else:
    tela_login()



