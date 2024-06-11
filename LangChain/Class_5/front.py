"""
import streamlit as st

from agent import handle_chat

if "history" not in st.session_state:
    st.session_state["history"] = []

st.title("AI Chatbot")


def send_message():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        response = handle_chat(user_message)
        st.session_state["history"].append(("You", user_message))
        st.session_state["history"].append(("AI", response))
        st.session_state.user_input = ""


user_input = st.text_input(
    "Enter your message:", key="user_input", on_change=send_message
)


send_button = st.button("Send")

if send_button and st.session_state.user_input:
    send_message()

for idx, (user, message) in enumerate(reversed(st.session_state["history"])):
    if user == "You":
        st.text_area(f"You: {idx}", message, key=f"msg{idx}u", disabled=True)
    else:
        st.text_area(f"AI: {idx}", message, key=f"msg{idx}b", disabled=True)

st.markdown("---")

"""

import streamlit as st

from agent import handle_chat # importar a função handle_chat do agete.py

# verificar a memória se não tiver nada, iniciar com IA CHAT BOT
if "history" not in st.session_state:
    st.session_state["history"] = [] 

st.title("AI ChatBot")

# deifnir a função para envio de msg
def send_message():
    if st.session_state.user_input:
        user_message = st.session_state
        response = handle_chat(user_message)
        st.session_state["history"].append(("You", user_message))
        st.session_state["history"].append(("AI", response))
        st.session_state.user_input = ""
        
user_input =  st.text_input(
    "Enter your message: ", key="user_input", on_change=send_message #sempre que mudar o input, ele chama a função sand_message
)

#função do botão de Enviar
send_button = st.button("Send")

if send_button and st.session_state.user_input:
    send_button()

# buscar os dados que estão no history, enumerar e mostrar na tela o array invertido (pra ficcar com o historico correto)    
for idx, (user, message) in enumerate(reversed(st.session_state["history"])):
    if user == "You":
        st.text_area(f"You: {idx}", message, key=f"msg{idx}u", distabled=True) # area de texto que não pode ser editada, apenas vizualizada
    else:
        st.text_area(f"AI: {idx}", message, key=f"msg{idx}u", distabled=True)
        
st.markdown("---")