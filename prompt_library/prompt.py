from langchain_core.prompts import ChatPromptTemplate

router_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert at routing a user question to a vectorstore or web search. Use the vectorstore for questions about stock market analysis, financial statements, and company-specific information. For all other questions, use web search."),
        ("human", "{question}"),
    ]
)