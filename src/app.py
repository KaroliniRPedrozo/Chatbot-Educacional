import streamlit as st
import google.generativeai as genai
import os
import json
import PyPDF2
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image

# Carrega as variáveis de ambiente
load_dotenv(dotenv_path="../.env") 
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

PASTA_CHATS = "conversas_salvas"
if not os.path.exists(PASTA_CHATS):
    os.makedirs(PASTA_CHATS)

# 1. Configuração da página 
st.set_page_config(page_title="Alexandri.ia", page_icon="🏛️", layout="centered")

# --- CSS ORIGINAL (COM ADIÇÃO DE FONTE MAIOR NO CHAT) ---
st.markdown("""
    <style>
    /* ---> NOVO: Aumentar a fonte das mensagens do chat <--- */
    [data-testid="stChatMessageContent"] p, 
    [data-testid="stChatMessageContent"] li, 
    [data-testid="stChatMessageContent"] span {
        font-size: 20px !important; /* Tamanho da letra */
        line-height: 1.6 !important; /* Espaçamento entre as linhas */
    }

    /* Estilo do Botão Primário (Novo Chat) */
    button[kind="primary"] {
        background-color: #1E88E5 !important;
        border-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: 0.3s !important;
        font-size: 20px !important;
    }
    button[kind="primary"]:hover {
        background-color: #1565C0 !important;
        border-color: #1565C0 !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(30, 136, 229, 0.4) !important;
        font-size: 20px !important;
    }
    
    /* Arredondamento dos botões de histórico */
    button[kind="secondary"] {
        border-radius: 8px !important;
        font-size: 20px !important;
    }

    /* Tamanho ideal para os avatares no chat */
    .stChatAvatar {
        width: 48px !important;
        height: 48px !important;
    }
    </style>
""", unsafe_allow_html=True)

instrucao_sistema = """Você é um professor especialista estritamente em História e Geografia. 
Suas respostas devem ser curtas, didáticas e adequadas para estudantes."""

modelo = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=instrucao_sistema
)

# --- CABEÇALHO PRINCIPAL DA PÁGINA ---
try:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.image("assets/logo.png", use_container_width=True)
except FileNotFoundError:
    st.markdown("<h1 style='text-align: center;'>🏛️ Alexandri.ia</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style='width: 100%; text-align: center; margin-top: -15px;'>
        <h4 style='color: #78909C; display: inline-block; margin: 0;'>Seu Tutor Especialista em História e Geografia</h4>
    </div>
""", unsafe_allow_html=True)
st.divider()

texto_base = ""

# --- BARRA LATERAL ---
with st.sidebar:
    
    try:
        st.image("assets/logo.png", use_container_width=True)
    except FileNotFoundError:
        pass 
    
    st.write("") 

    if st.button("Novo Chat", type="primary", use_container_width=True):
        st.session_state.sessao_chat = modelo.start_chat(history=[])
        st.session_state.id_conversa_atual = datetime.now().strftime("%Y%m%d%H%M%S")
        st.rerun()

    st.write("---")

    st.markdown("### 🕰️ Histórico")
    
    if os.path.exists(PASTA_CHATS):
        arquivos_salvos = sorted(os.listdir(PASTA_CHATS), reverse=True)
        if arquivos_salvos:
            for arquivo in arquivos_salvos:
                try:
                    titulo_exibicao = arquivo.split("_", 1)[1].replace(".json", "")
                except IndexError:
                    titulo_exibicao = arquivo
                if st.button(f"💬 {titulo_exibicao}", key=arquivo, use_container_width=True):
                    with open(os.path.join(PASTA_CHATS, arquivo), "r", encoding="utf-8") as f:
                        st.session_state.sessao_chat = modelo.start_chat(history=json.load(f))
                    st.session_state.id_conversa_atual = arquivo.split("_")[0]
                    st.rerun()
        else:
            st.caption("Nenhuma conversa salva ainda.")
        
    st.write("---")

    st.markdown("### 🛠️ Ferramentas")
    
    with st.expander("📎 Anexar Material de Estudo", expanded=False):
        arquivo_up = st.file_uploader("Arquivo", type=["txt", "pdf"], label_visibility="collapsed")
        if arquivo_up is not None:
            try:
                if arquivo_up.name.endswith(".txt"):
                    texto_base = arquivo_up.read().decode("utf-8")
                elif arquivo_up.name.endswith(".pdf"):
                    leitor = PyPDF2.PdfReader(arquivo_up)
                    for pagina in leitor.pages:
                        texto_base += pagina.extract_text() + "\n"
                st.success("Arquivo lido!")
            except Exception as e:
                st.error(f"Erro ao ler: {e}")

    with st.expander("🎯 Modo Quiz", expanded=False):
        iniciar_quiz = st.button("Fazer uma Pergunta", use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True) 
    st.markdown("<center><small>👩‍💻 Desenvolvido por Karolini</small></center>", unsafe_allow_html=True)

# --- LÓGICA PRINCIPAL DO CHAT ---
if "sessao_chat" not in st.session_state:
    st.session_state.sessao_chat = modelo.start_chat(history=[])
    st.session_state.id_conversa_atual = datetime.now().strftime("%Y%m%d%H%M%S")

try:
    avatar_bot = Image.open("assets/logo2.png")
except Exception:
    avatar_bot = "🏛️"

def salvar_conversa_atual():
    if len(st.session_state.sessao_chat.history) > 0:
        primeira_msg = st.session_state.sessao_chat.history[0].parts[0].text[:30]
        titulo_limpo = "".join(x for x in primeira_msg if x.isalnum() or x in " ").strip()
        nome_arquivo = f"{st.session_state.id_conversa_atual}_{titulo_limpo or 'chat'}.json"
        caminho = os.path.join(PASTA_CHATS, nome_arquivo)
        historico_formatado = [{"role": msg.role, "parts": [msg.parts[0].text]} for msg in st.session_state.sessao_chat.history]
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(historico_formatado, f, ensure_ascii=False, indent=4)

if iniciar_quiz:
    comando_quiz = "Mande uma pergunta de múltipla escolha de História ou Geografia para testar meus conhecimentos."
    with st.spinner("Preparando a pergunta..."):
        resposta = st.session_state.sessao_chat.send_message(comando_quiz)
        salvar_conversa_atual()

for mensagem in st.session_state.sessao_chat.history:
    if "Mande uma pergunta de múltipla escolha" in mensagem.parts[0].text and mensagem.role == "user":
        continue
    papel = "user" if mensagem.role == "user" else "assistant"
    icone_atual = "👩‍💻" if papel == "user" else avatar_bot
    
    with st.chat_message(papel, avatar=icone_atual):
        st.markdown(mensagem.parts[0].text)

if prompt := st.chat_input("Digite sua dúvida (ou 'sair' para encerrar)"):
    if prompt.strip().lower() == 'sair':
        st.warning("Conversa encerrada.")
        st.stop()

    with st.chat_message("user", avatar="👩‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=avatar_bot):
        try:
            with st.spinner("Consultando os pergaminhos..."):
                prompt_enviado = f"Considere este texto como base:\n{texto_base}\n\nAgora responda: {prompt}" if texto_base else prompt
                resposta = st.session_state.sessao_chat.send_message(prompt_enviado)
            st.markdown(resposta.text)
            salvar_conversa_atual()
        except Exception as e:
            st.error(f"Erro: {e}")