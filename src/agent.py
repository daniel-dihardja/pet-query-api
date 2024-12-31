import json
from typing import Annotated, Optional
from typing_extensions import TypedDict

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from vector_search import PetVectorSearch

from prompt_templates import (
    DETECT_LANGUAGE_PROMPT,
    EXTRACT_FILTER_VALUES_PROMPT,
    TRANSLATE_USER_QUERY_PROMPT,
)
from schemas import Filter, Pet


class State(TypedDict):
    messages: Annotated[list, add_messages]
    lang: str
    translated_message: str
    filter: Optional[Filter]
    pets: Optional[list[Pet]]


def create_llm():
    return ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")


async def chatbot(state: State):
    llm = create_llm()
    res = await llm.ainvoke(state["messages"])
    return {"messages": [res]}


async def language(state: State):
    llm = create_llm()
    prompt_template = PromptTemplate.from_template(DETECT_LANGUAGE_PROMPT)
    chain = prompt_template | llm
    res = await chain.ainvoke({"message": state["messages"][-1]})
    return {"lang": res.content}


async def translate(state: State):
    # Check if the language is "de" (German)
    if state["lang"] == "de":
        # Return the untranslated message as it's already in the target language
        return {"translated_message": state["messages"][-1].content}

    # Otherwise, proceed with translation using the API
    llm = create_llm()
    prompt_template = PromptTemplate.from_template(TRANSLATE_USER_QUERY_PROMPT)
    chain = prompt_template | llm
    res = await chain.ainvoke(
        {"message": state["messages"][-1].content, "lang": state["lang"]}
    )
    return {"translated_message": res.content}


async def extract_filter_values(state: State) -> dict[str, dict[str, str | None]]:
    llm = create_llm()
    prompt_template = PromptTemplate.from_template(EXTRACT_FILTER_VALUES_PROMPT)
    chain = prompt_template | llm
    res = await chain.ainvoke({"message": state["translated_message"]})
    return {"filter": parse_json_response(res.content)}


def parse_json_response(response: str):
    """
    Parses a JSON response string.
    Returns the parsed JSON object if successful, otherwise a fallback value.
    """
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return "Invalid JSON"


async def vector_query(state: State):
    query = state["translated_message"]
    filter_obj = state["filter"]
    vs = PetVectorSearch()
    pets = await vs.search_pets(query, filter_obj)
    return {"pets": pets}


graph_workflow = StateGraph(State)
graph_workflow.add_node("chatbot", chatbot)
graph_workflow.add_node("language", language)
graph_workflow.add_node("translate", translate)
graph_workflow.add_node("extract_filter_values", extract_filter_values)
graph_workflow.add_node("vector_query", vector_query)

graph_workflow.add_edge(START, "language")
graph_workflow.add_edge("language", "translate")
graph_workflow.add_edge("translate", "extract_filter_values")
graph_workflow.add_edge("extract_filter_values", "vector_query")
graph_workflow.add_edge("vector_query", END)

agent = graph_workflow.compile()
