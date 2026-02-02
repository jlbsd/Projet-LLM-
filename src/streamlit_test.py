import streamlit as st
from test_agent import poser_question

# 1. Initialisation
if "messages" not in st.session_state: 
    st.session_state.messages = []

st.title(" Jumelle de Jade")  #Titre à changer si besoin

# 2. Afficher l'historique
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 3. Saisie utilisateur
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse du modèle
    with st.chat_message("assistant"): 
        response = poser_question(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

