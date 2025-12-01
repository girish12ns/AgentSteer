from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from service_llm import chatgpt_openai
from prompt import REFLECTOR_PROMPT
from tools import sales_data_tool,load_bullet_texts,quadrant_query_tool
from ollama_client import ollama_model
from prompt import GLM_GENERATOR_PROMPT, GLM_REFLECTOR_PROMPT, GLM_CURATOR_PROMPT


reflection_agent = create_agent(chatgpt_openai,system_prompt=GLM_REFLECTOR_PROMPT)

