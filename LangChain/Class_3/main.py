from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate


from dotenv import load_dotenv
import os


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Criação do modelo de embedding
embeddings = OpenAIEmbeddings(
    openai_api_key=openai_api_key
)


# função para vetorizar texto
def create_vector_from_yt_url(video_url: str) -> FAISS: # recebe um obj do tipo strig e retorna um banco de dados vetorizado
    loader = YoutubeLoader.from_youtube_url(video_url, language="pt") 
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs, embeddings) # Gera embeddings de cada documentos
    return db


# função para responder as perguntas dos usuário
def get_response_from_query(db, query, k=4): # k = numero de documentos para o prompt k=4 documentos
    docs = db.similarity_search(query, k=k) # procura nos bd alguns documentos que tem a ver com a query que o usuário passou e traz apenas 4
    docs_page_content = " ".join([d.page_content for d in docs]) # docs_page_content traz tudo que vem do banco de dados em uma variável só 

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key,
    )

    chat_template = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                """Você é um assistente que responde perguntas sobre vídeos do youtube baseado
        na transcrição do vídeo.

        Responda a seguinte pergunta: {pergunta}
        Procurando nas seguintes transcrições: {docs}

        Use somente informação da transcrição para responder a pergunta. Se você não sabe, responda
        com "Eu não sei".

        Suas respostas devem ser bem detalhadas e verbosas.
        """,
            )
        ]
    )

    chain = LLMChain(llm=llm, prompt=chat_template, output_key="answer")

    response = chain({"pergunta": query, "docs": docs_page_content})

    return response, docs


if __name__ == "__main__":
    db = create_vector_from_yt_url("https://www.youtube.com/watch?v=2-Vjn7Ow1eg&ab_channel=EntreteniPop")
    response, docs = get_response_from_query(
        db, "O que é falado sobre Colin"
    )
    print(response)
