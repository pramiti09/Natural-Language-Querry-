#pip install pandas

import pandas as pd
import openai
import os
from sqlalchemy import create_engine
from sqlalchemy import text
import pyodbc

def db_query(table_name, nlp_text):
    server = '192.168.10.10' 
    database = 'Rhub_21Aug2022' 
    username = 'RodicAdmin' 
    password = 'Rinnovationhub@2021'  
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password, charset="utf8")
    cursor = cnxn.cursor()
    qh = "SELECT * FROM "
    sm=";"
    q=qh+table_name+sm
    df = cnxn.execute(q)
    #df = pd.read_sql(q, cnxn)
    os.environ['OPENAI_API_KEY'] = "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"
    def create_table_defination_prompt(df):
        prompt= '''### table with its properties: ##({})#'''.format(",".join(str(x) for x in df.columns))
        return prompt
    def combine_prompts(df, query_prompt):
        defination=create_table_defination_prompt(df)
        query_init_string=f"### a query to answer: {query_prompt}\nSelect"
        return defination+query_init_string
    openai.api_key = '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'
    response=openai.Completion.create(
    model="text-davinci-003",
    prompt=combine_prompts(df,nlp_text),
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["#", ";"])
    
    def handle_response(response):
        query=response["choices"][0]["text"]
        if query.startswith(" "):
            query="Select"+query
        return query
    
    cursor.execute(handle_response(response))
    for i in cursor:
        print(i)
