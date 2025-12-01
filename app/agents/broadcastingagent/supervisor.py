from typing import List, Optional, Literal
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage, trim_messages
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Optional,TypedDict
from generator import generator
from reflector import reflection_agent
from curator import curator_agent
from service_llm import openai





class State(MessagesState):
    next: str




def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = ["FINISH"] + members


    system_prompt = (
    "You are a Supervisor Agent that manages a sequential workflow using these workers: "
    f"{members}.\n\n"

    "Your ONLY responsibility is to route the user query through the following steps "
    "IN THIS EXACT ORDER:\n"
    "1. generator →\n"
    "3. reflector →\n"
    "4. curator\n\n"

    "RULES:\n"
    "- ALWAYS start with the generator.\n"
    "- NEVER skip a worker.\n"
    "- The output of each worker becomes the input to the next.\n"
    "- When a worker completes its task, you must route to the next worker.\n"
    "- After curator finishes, return the final result.\n"
    "- Do not do any worker's job yourself — only delegate.\n\n"

    "Your job: Track which worker has finished and ensure the sequence continues correctly.\n"
    )

    
    
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options]


    
    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    return supervisor_node



def Data_validator_node(state: State) -> Command[Literal["supervisor"]]:
    import time
    start = time.time()
    result = generator.invoke(state)


    print("Generator Result:", result['messages'][-1].content)
    end = time.time()
    
    print("Execution time:", end - start, "seconds")


    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="generator")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )


def error_analayst_node(state: State) -> Command[Literal["supervisor"]]:
    result = reflection_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="reflector")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )


def know_management_node(state: State) -> Command[Literal["supervisor"]]:
    result = curator_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="curator")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )

supervisor_agent = make_supervisor_node(chatgpt_openai, ["generator", "reflector","curator"])


data_analyst=StateGraph(State)
data_analyst.add_node("supervisor", supervisor_agent)
data_analyst.add_node("generator", Data_validator_node)
data_analyst.add_node("reflector", error_analayst_node)
data_analyst.add_node("curator", know_management_node)

data_analyst.add_edge(START, "supervisor")
research_graph = data_analyst.compile()