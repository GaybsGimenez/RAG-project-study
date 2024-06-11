from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")

# definir função de definição da LLM
def generate_company_name():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key,
    )
    # Array com 2 objetos, SystemMessage e HumanMessage
    company_name = llm(
        [
            SystemMessage( #define a personalidade do bot
                content="Você é um assistente IA que sempre responde em Português do Brasil"
            ),
            HumanMessage( # prompt 
                content="Gere 5 ideias de nomes para empresas no segmento Pets"
            ),
        ]
    )

    return company_name


if __name__ == "__main__":
    print(generate_company_name())
