import browser_use
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
import sys
sys.stdout.reconfigure(encoding='utf-8')
import logging
logging.basicConfig(level=logging.DEBUG)  # Define o nível de log para DEBUG
from flask import Flask, request, jsonify

app = Flask(__name__)

load_dotenv()

class Noticia(BaseModel):
    titulo: str
    imagem: str


class Noticias(BaseModel):
    noticias: list[Noticia]


controller = Controller(output_model=Noticias)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'


@app.route('/test', methods=['GET'])
def test():
    async def main():
        task = """
    Log in using the email: 'jpaulo@gmail.com' and password 'jpa2024' and bring me the updated URL
    """
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="AIzaSyArTog-quWD9Tqf-CkkFAq_-UOZfK1FTtA")
        initial_actions = [
            {'open_tab': {'url': 'https://akin-lis-app-web.vercel.app/akin/schedule/new'}}
        ]
    
        agent = Agent(
            task=task,
            controller=controller,
            initial_actions=initial_actions,
            llm=llm,
            message_context="This is a platform that contains a user email field and password to log in"
           
    
        )
    
        history = await agent.run()  # Certifique-se de que isto esteja dentro de uma função assíncrona
        result = history.final_result()
        print(history)
        for step in history.steps:
            return jsonify(f"Step {step['number']}: {step['action']} - Status: {step['status']}")
    
        
    
    # Esta linha é usada para iniciar a função assíncrona 'main'
    asyncio.run(main())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

