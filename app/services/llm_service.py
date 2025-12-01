from setting import settings
from langchain_openai import OpenAI


openai=OpenAI(
    model=settings.LLM_MODEL,
    temperature=settings.TEMPERATURE
    api=settings.OPENAI_API_KEY)


