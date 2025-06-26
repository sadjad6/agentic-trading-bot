from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph
from data_models.models import AgentState
from toolkit.tools import tavilytool, retriever_tool, financials_tool, stock_analysis_tool, technical_analysis_tool
from utils.model_loaders import ModelLoader
from prompt_library.prompt import router_prompt

class GraphBuilder:
    def __init__(self):
        self.model_loader = ModelLoader()

    def build(self):
        llm = self.model_loader.load_llm()
        tools = [retriever_tool, financials_tool, tavilytool, stock_analysis_tool, technical_analysis_tool]
        llm_with_tools = llm.bind_tools(tools)

        def agent(state: AgentState):
            messages = state["messages"]
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}

        def tool_node(state: AgentState):
            messages = state["messages"]
            last_message = messages[-1]
            tool_calls = last_message.tool_calls
            
            if not tool_calls:
                return {"messages": messages}

            responses = []
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_to_call = {tool.name: tool for tool in tools}[tool_name]
                observation = tool_to_call.invoke(tool_call["args"])
                responses.append(AIMessage(content=str(observation), tool_call_id=tool_call["id"]))
            
            return {"messages": responses}

        def router(state: AgentState):
            messages = state["messages"]
            question = messages[-1].content
            
            router_chain = router_prompt | llm.bind(tools=tools)
            response = router_chain.invoke({"question": question})
            
            if "tool_calls" in response.additional_kwargs:
                return "tools"
            else:
                return "agent"

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent)
        workflow.add_node("tools", tool_node)
        
        workflow.set_entry_point("agent")
        workflow.add_conditional_edge(
            "agent",
            router,
            {"tools": "tools", "agent": "agent"}
        )
        workflow.add_edge("tools", "agent")

        return workflow.compile()