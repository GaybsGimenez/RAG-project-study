from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

from langchain.chains import LLMMathChain
from langchain.utilities import SerpAPIWrapper #faz buscas na internet
from langchain.agents import initialize_agent, Tool
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory #memória

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

llm = ChatOpenAI(
    model="gpt-3.5-turbo-16k",
    temperature=0.0,
    openai_api_key=openai_api_key,
    verbose=True,
)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
search = SerpAPIWrapper()

# array de objeto tool
tools = [
    Tool(
        name="Search", # obejto para pesquisa
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions", #descrição pra o O AGENTE
    ),
    Tool(
        name="Calculator", #objeto para calculos matematicos
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
    Tool(
        name="FooBar-DB", # objeto para rodar o banco de dados (agente rodar quando for necessário)
        func=db_chain.run,
        description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
    ),
]

# Setar a memória para ser um bot conversacional 
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

# Argumentos adcionais para o objeto AGENT 
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")], #substitui o agente do prompt pela memory setada acima
}

# criar o agente
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS, #escolhe melhor quais funções rodas (criado pela openai)
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

# conversação
while True:
    user_input = input("Enter your query or type 'exit' to quit: ")

    if user_input.lower() == "exit":
        break

    response = agent.run(user_input)

    print(response)
