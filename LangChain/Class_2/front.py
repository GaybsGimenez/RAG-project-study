import langchain_helper as la
import streamlit as st # biblioteca em python para monstar scripts de interfase 


st.set_page_config(layout="wide") # st.set_page_config(layout="wide"): Configura a página do aplicativo Streamlit para usar um layout amplo, permitindo que a interface utilize a largura total da janela do navegador.
st.title("Gerador de Nomes de Empresas")
segmento = st.sidebar.text_area(label="Qual é o segmento da sua empresa?")

# vericifcar se existe o segmento que o usuário digitar no campo de texto
if segmento:
    response = la.generate_company_name(segmento)

    st.text(response["company_name"])
