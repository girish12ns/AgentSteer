from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from service_llm import chatgpt_openai
from tools import quadrant_query_tool
from ollama_client import ollama_model

from prompt import CURATOR_PROMPT
from prompt import GLM_GENERATOR_PROMPT, GLM_REFLECTOR_PROMPT, GLM_CURATOR_PROMPT


curator_agent = create_agent(chatgpt_openai,system_prompt=GLM_CURATOR_PROMPT)
