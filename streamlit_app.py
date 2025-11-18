import streamlit as st
import google.generativeai as genai

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

    # Configure Google Gemini
    genai.configure(api_key=google_api_key)
    
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

        # Generate a response using the Gemini API.
        try:
            # Initialize model for each request to avoid session issues
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(prompt)
            
            # Display and store the response
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            error_message = str(e)
            with st.chat_message("assistant"):
                if "ResourceExhausted" in error_message or "quota" in error_message.lower():
                    st.error("⚠️ Limite de uso da API atingido. Por favor, verifique sua quota no Google AI Studio ou tente novamente mais tarde.")
                elif "API key" in error_message:
                    st.error("⚠️ Erro com a chave API. Verifique se ela está correta e ativa.")
                else:
                    st.error(f"⚠️ Erro ao gerar resposta: {error_message}")
            # Remove a última mensagem do usuário se houve erro
            st.session_state.messages.pop()
