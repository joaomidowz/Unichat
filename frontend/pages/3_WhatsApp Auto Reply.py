import streamlit as st
import requests

st.title("Configurar Resposta Automática")

# URL do servidor Node.js
API_URL = "http://localhost:3001"

# Formulário para configuração de resposta automática
with st.form("auto_response_form"):
    trigger_message = st.text_input("Mensagem para acionar a resposta", label_visibility="visible")
    response_message = st.text_input("Resposta automática", label_visibility="visible")

    # Botão para enviar configuração
    submitted = st.form_submit_button("Configurar Resposta")

    if submitted:
        if trigger_message and response_message:
            try:
                response = requests.post(f"{API_URL}/auto-message", json={
                    "triggerMessage": trigger_message,
                    "responseMessage": response_message
                })
                if response.status_code == 200:
                    st.success("Resposta automática configurada com sucesso!")
                else:
                    st.error(
                        f"Erro ao configurar a resposta automática. Status code: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro de conexão com o servidor: {e}")
        else:
            st.error("Por favor, preencha todos os campos.")

# Seção para exibir as respostas automáticas configuradas
st.header("Respostas Automáticas Configuradas")

# Requisição para obter todas as respostas automáticas configuradas
try:
    response = requests.get(f"{API_URL}/get-auto-responses")
    if response.status_code == 200:
        auto_responses = response.json()

        # Exibe cada resposta em um "card" com botão de remoção
        for trigger, reply in auto_responses.items():
            with st.container():
                st.markdown(f"**Mensagem gatilho:** {trigger}")
                st.markdown(f"**Resposta:** {reply}")

                # Add a Remove button
                remove_button = st.button(f"Remover '{trigger}'", key=trigger)

                if remove_button:
                    # Send DELETE request to remove the auto-response
                    try:
                        delete_response = requests.delete(f"{API_URL}/delete-auto-response",
                                                          json={"triggerMessage": trigger})
                        if delete_response.status_code == 200:
                            st.success(f"Resposta automática para '{trigger}' removida com sucesso!")
                        else:
                            st.error(
                                f"Erro ao remover a resposta automática. Status code: {delete_response.status_code} - {delete_response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro de conexão com o servidor: {e}")

                st.markdown("---")  # Linha divisória entre cards
    else:
        st.error(f"Erro ao carregar as respostas automáticas. Status code: {response.status_code} - {response.text}")
except requests.exceptions.RequestException as e:
    st.error(f"Erro de conexão com o servidor: {e}")
