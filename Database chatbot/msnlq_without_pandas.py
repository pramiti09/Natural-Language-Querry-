from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
def db_query(table_name, nlp_text):
    server = 'SERVER' 
    database = 'DATABASE NAME' 
    username = 'USERNAME' 
    password = 'PASSWORD'  
    os.environ['OPENAI_API_KEY'] = "YOUR API KEY"
    db = SQLDatabase.from_uri(f"mssql+pyodbc://{username}:{password}@{server}/{database}")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", )
    toolkit = SQLDatabaseToolkit(db=db,llm=llm)
    agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
    )
    agent_executor.run(f"Describe the {table_name} related table and how they are related")
    return agent_executor.run(nlp_text)


db_query('ContractIssue,'Give all issue dates')
