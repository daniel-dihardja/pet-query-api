from typing_extensions import TypedDict
from langgraph.graph import END, START, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from typing import Annotated
from langgraph.graph.message import add_messages
from prompt_templates import DETECT_LANGUAGE_PROMPT


class State(TypedDict):
    messages: Annotated[list, add_messages]
    lang: str


def create_llm():
    return ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")


def chatbot(state: State):
    llm = create_llm()
    return {"messages": [llm.invoke(state["messages"])]}


def language(state: State):
    llm = create_llm()
    prompt_template = PromptTemplate.from_template(DETECT_LANGUAGE_PROMPT)
    chain = prompt_template | llm
    language = chain.invoke({"message": state["messages"][-1]})
    return {"lang": language}


graph_workflow = StateGraph(State)
graph_workflow.add_node("chatbot", chatbot)
graph_workflow.add_node("language", language)
graph_workflow.add_edge(START, "language")
graph_workflow.add_edge("language", END)
agent = graph_workflow.compile()
