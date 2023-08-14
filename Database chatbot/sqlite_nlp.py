#pip install pandas

import pandas as pd
import openai
import os

df=pd.read_csv("D:\\chatbot_with_nlq(version 1)\\sales_data_sample.csv",encoding="latin1")
from sqlalchemy import create_engine
from sqlalchemy import text

'''This program connects to sqlite . To connect to microsoft sql server uncomment the following code , fill in the information and delete the sqllite code(engine formation)
We will be using pymssql driver for ms sql server 
uncomment the following code

from sqlalchemy import URL

url_object = URL.create(
    "mssql+pymssql",
    username="",
    password="",  # plain (unescaped) text
    host="",
    database="",
)

from sqlalchemy import create_engine

engine = create_engine(url_object)'''

#coment the following line to conect to mssql

temp_db=create_engine('sqlite:///:memory:', echo=True)
#we push all the data into sales table

'''if we wish to work with already created database we do not have to these steps. We can directly 
connect to database after creating and implementing the model '''

data= df.to_sql(name="Sales", con=temp_db)

#openai.api_key=os.getenv("YOUR API KEY") this line gave an error. so instead we used the below code
#skip above 3 steps inorder to work with already created database 
os.environ['OPENAI_API_KEY'] = "YOUR API KEY"

#inform gpt about sql table
def create_table_defination_prompt(df):
    prompt= '''### table with its properties: ##Sales({})#'''.format(",".join(str(x) for x in df.columns))
    return prompt
print(create_table_defination_prompt(df))
#get natural language request
def prompt_input():
    nlp_text=input("Enter query:")
    return nlp_text
nlp_text=prompt_input()
def combine_prompts(df, query_prompt):
    defination=create_table_defination_prompt(df)
    query_init_string=f"### a query to answer: {query_prompt}\nSelect"
    return defination+query_init_string
combine_prompts(df, nlp_text)

openai.api_key = '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'
response=openai.Completion.create(
    model="text-davinci-003",
    prompt=combine_prompts(df,nlp_text),
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["#", ";"]
)

#building s function to parse the response
def handle_response(response):
    query=response["choices"][0]["text"]
    if query.startswith(" "):
        query="Select"+query
    return query
handle_response(response)
#passing this into the database
with temp_db.connect() as conn:
    result=conn.execute(text(handle_response(response)))
print(result.all())

