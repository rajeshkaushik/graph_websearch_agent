from langchain_openai import ChatOpenAI, AzureChatOpenAI
from utils.helper_functions import load_config
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
load_config(config_path)

from dotenv import dotenv_values

config = dotenv_values(".env")

def get_open_ai(temperature=0, model='gpt-3.5-turbo'):

    llm = ChatOpenAI(
    model=model,
    temperature = temperature,
    )
    return llm

def get_open_ai_json(temperature=0, model='gpt-3.5-turbo'):
    #import ipdb; ipdb.set_trace()
    llm = AzureChatOpenAI(
        model=model,
        temperature = temperature,
        model_kwargs={"response_format": {"type": "json_object"}},
        api_key=config.get("AZURE_OPENAI_API_KEY"),
        api_version=config.get("OPENAI_API_VERSION"),
        azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=config.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    )
    return llm
