import streamlit as st

st.title("👨🏻‍💻 Asistente virtual Adoptame 🐾")

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "firs_message" not in st.session_state:
    st.session_state.first_message= True

#Muestra historico de mensajes recorriendo un for

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Comprueba si es el primer mensaje
if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola, como puedo ayudarte?")

#Agrega los mensajes al historico
st.session_state.messages.append({"role": "assistant", "content": "Hola, como puedo ayudarte?"})
st.session_state.first_message= False

if prompt:= st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "content": prompt})
    with st.chat_message("assistant"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"assitant", "content": prompt})