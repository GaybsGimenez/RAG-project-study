from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage # interagir com o modelo de linguagem OpenAI e definir tipos de mensagens.

from langchain.prompts import ChatPromptTemplate # criar templates de prompts e definir cadeias de execução (chains) com modelos de linguagem
from langchain.chains import LLMChain

from dotenv import load_dotenv # para carregar variáveis de ambiente de um arquivo .env
import os #  para acessar variáveis de ambiente

# Carrega as variáveis de ambiente do arquivo .env para que possam ser usadas no script.
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")


def generate_company_name(segmento):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key,
    )
    
    # template de prompt - array com dois objetos
    chat_template = ChatPromptTemplate.from_messages( # ChatPromptTemplate.from_messages cria um template de prompt para o chat.
        [
            (
                "system",
                "Você é um assistente IA que sempre responde em português do Brasil",
            ),
            ("human", "Gere 5 ideas de nomes para empresas no segmento {segmento}"),
        ]
    )

    # Criando a Cadeia de Execução (Chain)
    company_names_chain = LLMChain( # LLMChain: Define uma cadeia de execução que liga o modelo de linguagem (llm) ao template de prompt (prompt=chat_template).
        llm=llm, prompt=chat_template, output_key="company_name" #output_key="company_name": Define a chave de saída da cadeia, que é onde a resposta do modelo será armazenada.
    )

    response = company_names_chain({"segmento": segmento})

    return response


if __name__ == "__main__":
    print(generate_company_name("imobiliária"))
