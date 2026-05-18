from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

# 1. Model we use
groq_api_key=os.getenv('GROQ_API_KEY')
model = ChatGroq(model="groq/compound",groq_api_key=groq_api_key)

# 2. Create prompt template

system_template = "Translate the follow into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system',system_template),
    ('user','{text}')
])

# 3. Output parser

parser = StrOutputParser()

## create chain
chain = prompt_template|model|parser

## Creating fast api app
app = FastAPI(title="Langchain server",
              version="1.0",
              description="A simple language translation server using Langchain , runnable and interfaces")

## Adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8080)