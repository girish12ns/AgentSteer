from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from service_llm import chatgpt_openai
from prompt import GENERATOR_PROMPT
from tools import sales_data_tool,load_bullet_texts,quadrant_query_tool
from ollama_client import ollama_model
from prompt import GLM_GENERATOR_PROMPT, GLM_REFLECTOR_PROMPT, GLM_CURATOR_PROMPT


generator = create_agent(chatgpt_openai, tools=[sales_data_tool,quadrant_query_tool],system_prompt=GLM_GENERATOR_PROMPT)

