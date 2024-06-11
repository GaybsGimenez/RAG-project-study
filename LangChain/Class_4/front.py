"""
import streamlit as st
import langchain_helper as lch
import textwrap

st.title("Assistente do Youtube!")

with st.sidebar:
    with st.form(key="my_form"):
        youtube_url = st.sidebar.text_area(label="URL do Vídeo", max_chars=50)
        query = st.sidebar.text_area(
            label="Me pergunte sobre algo do vídeo!", max_chars=50, key="query"
        )
        submit_button = st.form_submit_button(label="Enviar")

if query and youtube_url:
    db = lch.create_vector_from_yt_url(youtube_url)
    response, docs = lch.get_response_from_query(db, query)
    st.subheader("Resposta:")
    st.text(textwrap.fill(response["answer"], width=85))
    
"""

import streamlit as st # criar a interface com pytho
import langchain_helper as lch
import textwrap # para não deixar texto estourar a tela

st.title("Assistente do Youtube!")

with st.sidebar:
    with st.form(key="my_form"):
        youtube_url = st.sidebar.text_area(
            label="URL do Vídeo", 
            max_chars=100
            )
        query = st.sidebar.text_area(
            label="Me pergunte sobre algo do vídeo!",
            max_chars=100,
            key="query"
        )
        submit_button = st.form_submit_button(
            label="Enviar"
            )
        
# verificar se a query e a url existem
if query and youtube_url:
    db = lch.create_vector_from_yt_url(youtube_url)
    response, docs = lch.get_response_from_query(db, query)
    st.subheader("Resposta: ")
    st.text(textwrap.fill(response["answer"],width=85))