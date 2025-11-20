import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Importar módulos do projeto
from modules.workflow_manager import WorkflowManager, EstadoConversa
from modules import prompt_templates as prompts
from utils.validators import validar_tema, validar_metodologia
from utils.export_utils import gerar_pdf_cronograma, sanitizar_nome_arquivo

# Load environment variables from .env file
load_dotenv()


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def chamar_gemini(api_key: str, prompt_usuario: str, historico: list) -> str:
    """
    Chama a API do Gemini e retorna a resposta.
    
    Args:
        api_key: Chave da API do Google
        prompt_usuario: Prompt/mensagem do usuário
        historico: Histórico de mensagens anteriores
    
    Returns:
        Resposta do modelo ou mensagem de erro
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        
        # Adiciona prompt de sistema e contexto
        mensagens = [
            {"role": "user", "parts": [{"text": prompts.SYSTEM_PROMPT}]},
            {"role": "model", "parts": [{"text": "Entendido. Estou pronto para ajudar a criar cronogramas de estudo personalizados."}]}
        ]
        
        # Adiciona histórico
        for msg in historico:
            role = "model" if msg["role"] == "assistant" else "user"
            mensagens.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        # Adiciona mensagem atual
        mensagens.append({"role": "user", "parts": [{"text": prompt_usuario}]})
        
        data = {"contents": mensagens}
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if "candidates" in result and result["candidates"]:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "⚠️ Não foi possível obter uma resposta. Tente novamente."
    
    except requests.exceptions.Timeout:
        return "⚠️ A requisição demorou muito. Tente um tema mais específico ou um prazo menor."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "⚠️ Limite de uso da API atingido. Aguarde alguns minutos."
        elif e.response.status_code == 404:
            return "⚠️ Modelo não encontrado."
        else:
            return f"⚠️ Erro HTTP {e.response.status_code}"
    except Exception as e:
        return f"⚠️ Erro: {str(e)}"


def processar_mensagem_usuario(mensagem: str, api_key: str):
    """Processa mensagem do usuário com base no estado atual do workflow."""
    
    workflow = st.session_state.workflow
    estado_atual = workflow.get_estado()
    
    with st.chat_message("assistant"):
        # Estado INICIAL -> Coletar tema
        if estado_atual == EstadoConversa.INICIAL:
            workflow.processar_tema(mensagem)
            
            prompt = prompts.PROMPT_CONFIRMAR_TEMA.format(tema=mensagem)
            resposta = chamar_gemini(api_key, prompt, st.session_state.messages[-5:])
            
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        
        # Estado COLETANDO_TEMA -> mesma lógica
        elif estado_atual == EstadoConversa.COLETANDO_TEMA:
            workflow.processar_tema(mensagem)
            
            prompt = prompts.PROMPT_CONFIRMAR_TEMA.format(tema=mensagem)
            resposta = chamar_gemini(api_key, prompt, st.session_state.messages[-5:])
            
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        
        # Estado APRESENTANDO_METODOLOGIAS -> Processar escolha de metodologia
        elif estado_atual == EstadoConversa.APRESENTANDO_METODOLOGIAS:
            workflow.processar_metodologia(mensagem)
            
            dados = workflow.get_dados()
            prompt = prompts.PROMPT_COLETAR_PARAMETROS.format(
                tema=dados.tema,
                metodologia=dados.metodologia
            )
            resposta = chamar_gemini(api_key, prompt, st.session_state.messages[-5:])
            
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        
        # Estado COLETANDO_PARAMETROS -> Processar parâmetros
        elif estado_atual == EstadoConversa.COLETANDO_PARAMETROS:
            novo_estado, tipo_prompt, completo = workflow.processar_parametros(mensagem)
            
            if completo:
                # Tem todos os parâmetros, gerar cronograma
                dados = workflow.get_dados()
                
                st.info("⏳ Gerando seu cronograma personalizado... Isso pode levar alguns segundos.")
                
                prompt_cronograma = prompts.construir_prompt_cronograma(
                    tema=dados.tema,
                    metodologia=dados.metodologia,
                    tempo=dados.tempo_disponivel,
                    prazo=dados.prazo,
                    nivel=dados.nivel
                )
                
                cronograma = chamar_gemini(api_key, prompt_cronograma, [])
                
                workflow.cronograma_gerado(cronograma)
                
                st.markdown(cronograma)
                st.session_state.messages.append({"role": "assistant", "content": cronograma})
                
                # Perguntar feedback
                msg_feedback = "\n\n---\n\n✅ O que achou do cronograma? Está de acordo com suas expectativas?\n\nVocê pode aprovar (👍), solicitar ajustes específicos, ou pedir para refazer."
                st.markdown(msg_feedback)
                st.session_state.messages.append({"role": "assistant", "content": msg_feedback})
            else:
                # Ainda falta informações
                faltando = workflow.get_faltando_parametros()
                dados = workflow.get_dados()
                
                prompt_reforco = f"O usuário forneceu: '{mensagem}'\n\nAinda faltam: {', '.join(faltando)}\n\nTema: {dados.tema}\nMetodologia: {dados.metodologia}\n\nPergunte APENAS as informações que faltam de forma amigável."
                
                resposta = chamar_gemini(api_key, prompt_reforco, st.session_state.messages[-3:])
                
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
        
        # Estado APRESENTANDO_CRONOGRAMA ou COLETANDO_FEEDBACK -> Processar feedback
        elif estado_atual in [EstadoConversa.APRESENTANDO_CRONOGRAMA, EstadoConversa.COLETANDO_FEEDBACK]:
            novo_estado, tipo_acao = workflow.processar_feedback(mensagem)
            
            if tipo_acao == "feedback_positivo":
                resposta = "🎉 Ótimo! Seu cronograma está aprovado!\n\n📥 **Próximos passos:**\n- Salve este cronograma\n- Comece pelos primeiros tópicos\n- Mantenha consistência nos estudos\n\nQuer criar um novo cronograma de estudos?"
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            
            elif tipo_acao == "feedback_negativo_generico":
                resposta = "Entendo que não ficou como esperava. Pode me dizer especificamente o que gostaria de mudar?\n\nPor exemplo:\n- Prazo muito longo/curto?\n- Conteúdo muito básico/avançado?\n- Faltam exercícios práticos?\n- Outro aspecto?"
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            
            elif tipo_acao == "refinar_cronograma":
                st.info("⏳ Refinando o cronograma com base no seu feedback...")
                
                dados = workflow.get_dados()
                prompt_refinamento = prompts.PROMPT_PROCESSAR_FEEDBACK.format(
                    cronograma_anterior=dados.cronograma_atual,
                    feedback=mensagem
                )
                
                novo_cronograma = chamar_gemini(api_key, prompt_refinamento, [])
                
                workflow.cronograma_refinado(novo_cronograma)
                
                st.markdown("🔄 **Cronograma Atualizado:**\n\n" + novo_cronograma)
                st.session_state.messages.append({"role": "assistant", "content": novo_cronograma})
                
                msg_feedback = "\n\n---\n\nO que achou agora? Posso fazer mais algum ajuste?"
                st.markdown(msg_feedback)
                st.session_state.messages.append({"role": "assistant", "content": msg_feedback})
            
            else:  # pedir_esclarecimento
                resposta = "Não entendi bem o que você gostaria de mudar. Pode ser mais específico?\n\nPor exemplo: 'Reduzir para 6 semanas' ou 'Adicionar mais projetos práticos'"
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
        
        # Estado APROVADO -> Oferecer novo cronograma
        elif estado_atual == EstadoConversa.APROVADO:
            if any(palavra in mensagem.lower() for palavra in ['sim', 'quero', 'novo', 'outro']):
                workflow.resetar()
                st.session_state.messages = []
                st.rerun()
            else:
                resposta = "Obrigado por usar o Chatbot de Estudos! Bons estudos! 📚✨"
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
        
        st.rerun()


# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

# Configuração da página
st.set_page_config(
    page_title="Chatbot de Estudos Personalizados",
    page_icon="📚",
    layout="wide"
)

# Show title and description.
st.title("📚 Chatbot de Estudos Personalizados")
st.write(
    "Crie cronogramas de estudo personalizados com metodologias comprovadas de aprendizagem!"
)

# Get API key from environment variable or user input
# Try Streamlit secrets first (for Streamlit Cloud), then environment variable
try:
    google_api_key = st.secrets.get("GEMINI_API_KEY", "")
except:
    google_api_key = os.environ.get("GEMINI_API_KEY", "")

# If no API key in environment, ask user for input
if not google_api_key:
    google_api_key = st.text_input("Google API Key", type="password")
    if not google_api_key:
        st.info("Por favor, adicione sua chave API do Google para continuar (ou configure no arquivo .env)", icon="🗝️")
else:
    # Inicializar WorkflowManager e session state
    if "workflow" not in st.session_state:
        st.session_state.workflow = WorkflowManager()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Carregar histórico do localStorage na primeira execução
    if "historico_carregado" not in st.session_state:
        st.session_state.historico_carregado = False
    
    # Nota: A funcionalidade de localStorage com streamlit.components.v1.html
    # tem limitações. Uma alternativa mais robusta seria usar session_state
    # do Streamlit com query parameters ou cookies.
    # Por simplicidade, vamos focar no salvamento e reset manual.
    
    # Sidebar com informações de progresso
    with st.sidebar:
        st.header("📊 Progresso")
        progresso = st.session_state.workflow.get_progresso()
        st.progress(progresso["percentual"] / 100)
        st.write(f"**{progresso['descricao']}**")
        st.write(f"Etapa {progresso['etapa_atual']} de {progresso['total_etapas']}")
        
        st.divider()
        
        # Mostrar informações coletadas
        dados = st.session_state.workflow.get_dados()
        if dados.tema:
            st.write(f"📚 **Tema:** {dados.tema}")
        if dados.metodologia:
            st.write(f"🎯 **Metodologia:** {dados.metodologia}")
        if dados.tempo_disponivel:
            st.write(f"⏰ **Tempo:** {dados.tempo_disponivel}")
        if dados.prazo:
            st.write(f"📅 **Prazo:** {dados.prazo}")
        if dados.nivel:
            st.write(f"📊 **Nível:** {dados.nivel}")
        
        st.divider()
        
        # Botão de download do PDF (só aparece quando há cronograma)
        if dados.cronograma_atual:
            st.subheader("💾 Exportar Cronograma")
            
            # Gerar PDF
            try:
                pdf_bytes = gerar_pdf_cronograma(
                    tema=dados.tema or "Tema não definido",
                    metodologia=dados.metodologia or "Metodologia não definida",
                    cronograma=dados.cronograma_atual,
                    tempo=dados.tempo_disponivel or "",
                    prazo=dados.prazo or "",
                    nivel=dados.nivel or ""
                )
                
                # Nome do arquivo
                nome_arquivo = sanitizar_nome_arquivo(dados.tema or "cronograma")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_completo = f"cronograma_{nome_arquivo}_{timestamp}.pdf"
                
                # Botão de download
                st.download_button(
                    label="📥 Baixar PDF",
                    data=pdf_bytes,
                    file_name=nome_completo,
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success("✅ Cronograma pronto para download!")
                
            except Exception as e:
                st.error(f"❌ Erro ao gerar PDF: {str(e)}")
        
        st.divider()
        
        # Botão de ação
        if st.button("🔄 Nova Conversa", use_container_width=True):
            st.session_state.workflow.resetar()
            st.session_state.messages = []
            st.rerun()
    
    # Se primeira vez, enviar mensagem de boas-vindas
    if len(st.session_state.messages) == 0:
        mensagem_boas_vindas = chamar_gemini(
            google_api_key, 
            prompts.PROMPT_BOAS_VINDAS,
            []
        )
        st.session_state.messages.append({"role": "assistant", "content": mensagem_boas_vindas})

    # Display the existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process message based on current state
        processar_mensagem_usuario(prompt, google_api_key)


