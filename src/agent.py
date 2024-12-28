from typing_extensions import TypedDict
from langgraph.graph import END, START, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from typing import Annotated, Literal, Optional
from langgraph.graph.message import add_messages
from prompt_templates import DETECT_LANGUAGE_PROMPT, TRANSLATE_USER_QUERY_PROMPT
from schemas import Filter


class State(TypedDict):
    messages: Annotated[list, add_messages]
    lang: str
    translated_message: str
    filter: Optional[Filter]


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


def should_translate(state: State) -> Literal["translate", END]:
    lang = state["lang"]
    if lang == "de":
        return END
    return "translate"


async def translate(state: State):
    llm = create_llm()
    prompt_template = PromptTemplate.from_template(TRANSLATE_USER_QUERY_PROMPT)
    chain = prompt_template | llm
    res = await chain.ainvoke(
        {"message": state["messages"][-1].content, "lang": state["lang"]}
    )
    return {"translated_message": res.content}


graph_workflow = StateGraph(State)
graph_workflow.add_node("chatbot", chatbot)
graph_workflow.add_node("language", language)
graph_workflow.add_node("translate", translate)

graph_workflow.add_edge(START, "language")
graph_workflow.add_conditional_edges("language", should_translate)
graph_workflow.add_edge("language", END)
graph_workflow.add_edge("translate", END)
agent = graph_workflow.compile()
