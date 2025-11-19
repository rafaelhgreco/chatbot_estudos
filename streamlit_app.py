import streamlit as st
import requests
import json

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "Este é um chatbot simples que usa o modelo Gemini do Google para gerar respostas. "
    "Para usar este app, você precisa fornecer uma API key do Google, que você pode obter [aqui](https://aistudio.google.com/app/apikey). "
)

# Ask user for their Google API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
google_api_key = st.text_input("Google API Key", type="password")
if not google_api_key:
    st.info("Por favor, adicione sua chave API do Google para continuar.", icon="🗝️")
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
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={google_api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            
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
