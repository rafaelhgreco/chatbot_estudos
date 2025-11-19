import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "Este é um chatbot simples que usa o modelo Gemini do Google para gerar respostas. "
)

# Get API key from environment variable or user input
google_api_key = os.environ.get("GEMINI_API_KEY", "")

# If no API key in environment, ask user for input
if not google_api_key:
    google_api_key = st.text_input("Google API Key", type="password")
    if not google_api_key:
        st.info("Por favor, adicione sua chave API do Google para continuar (ou configure no arquivo .env)", icon="🗝️")
else:

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Como posso ajudar?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the Gemini API via REST
        try:
            # Using the specific model version requested by the user
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={google_api_key}"
            headers = {"Content-Type": "application/json"}
            
            # Prepare conversational history for the API
            gemini_history = []
            for msg in st.session_state.messages:
                # Map role 'assistant' to 'model' for the Gemini API
                role = "model" if msg["role"] == "assistant" else "user"
                gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

            data = {"contents": gemini_history}
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            # Check if 'candidates' key exists and is not empty
            if "candidates" in result and result["candidates"]:
                ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                ai_response = "⚠️ Não foi possível obter uma resposta do modelo. A resposta pode ter sido bloqueada por segurança."

            # Display and store the response
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except requests.exceptions.HTTPError as e:
            with st.chat_message("assistant"):
                if e.response.status_code == 429:
                    st.error("⚠️ Limite de uso da API atingido. Por favor, aguarde alguns minutos ou verifique sua quota no Google AI Studio.")
                elif e.response.status_code == 404:
                    st.error("⚠️ Modelo não encontrado. Tentando modelo alternativo...")
                elif e.response.status_code == 400:
                    st.error("⚠️ Erro na requisição. Verifique sua chave API.")
                else:
                    st.error(f"⚠️ Erro HTTP {e.response.status_code}: {e.response.text}")
            st.session_state.messages.pop()
            
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"⚠️ Erro ao gerar resposta: {str(e)}")
            st.session_state.messages.pop()
