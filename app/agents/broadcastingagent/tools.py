from langchain.tools import tool
import json
from quadrant import ask


@tool
def sales_data_tool(last_year:str,present_year:str) -> str:
    """
    A tool to fetch sales data based on the query.
    """
    if present_year > last_year:
        return "Sales have increased compared to last year."
    elif present_year < last_year:
        return "Sales have decreased compared to last year."
    
    
@tool   
def load_bullet_texts() -> str:
   
    """Load the JSON file and return all bullet 'content' strings."""

    json_path = r"ace_react\playbook.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    bullets = data.get("bullets", {})
    contents = [entry.get("content", "") for entry in bullets.values()]
    return contents


@tool
def quadrant_query_tool(query: str, limit: int = 5) -> str:
    """
    this playbook tool  return the relevant results.
    """
    return ask(query, limit)
   
  
    
