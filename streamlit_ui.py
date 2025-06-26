import streamlit as st
import requests
from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="📈 Advanced Stock Market Agentic Chatbot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Advanced Stock Market Agentic Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_stock" not in st.session_state:
    st.session_state.current_stock = ""

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Quick Stock Analysis")
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., NIFTY50)")
    
    if stock_symbol:
        st.session_state.current_stock = stock_symbol
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Basic Analysis", "Technical Analysis", "Both"]
        )
        
        if st.button("Analyze"):
            prompt = f"""
            Analyze {stock_symbol} with the following requirements:
            1. Use stock_analysis_tool for basic metrics
            2. Use technical_analysis_tool for technical indicators
            3. Provide a comprehensive analysis and trading recommendation
            """
            
            try:
                response = requests.post(f"{BASE_URL}/query", json={"question": prompt})
                
                if response.status_code == 200:
                    with st.expander("Analysis Results", expanded=True):
                        st.markdown(response.json().get("answer", "No analysis returned."))
                else:
                    st.error("❌ Analysis failed: " + response.text)
            except Exception as e:
                raise TradingBotException(e, sys)
    
    # Document Upload Section
    st.header("📄 Upload Documents")
    st.markdown("Upload **stock market PDFs or DOCX** to create knowledge base.")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx"], accept_multiple_files=True)
    
    if st.button("Upload and Ingest"):
        if uploaded_files:
            files = []
            for f in uploaded_files:
                file_data = f.read()
                if not file_data:
                    continue
                files.append(("files", (getattr(f, "name", "file.pdf"), file_data, f.type)))

            if files:
                try:
                    with st.spinner("Uploading and processing files..."):
                        response = requests.post(f"{BASE_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success("✅ Files uploaded and processed successfully!")
                        else:
                            st.error("❌ Upload failed: " + response.text)
                except Exception as e:
                    raise TradingBotException(e, sys)
            else:
                st.warning("Some files were empty or unreadable.")

with col1:
    # Chat interface
    st.header("💬 Chat")
    
    # Display chat messages
    for chat in st.session_state.messages:
        if chat["role"] == "user":
            st.markdown(f"**🧑 You:** {chat['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {chat['content']}")
    
    # Chat input box
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message", placeholder="e.g. Tell me about NIFTY 50")
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input.strip():
        try:
            # If current_stock is set, include it in the context
            if st.session_state.current_stock:
                user_input = f"Context: Currently analyzing {st.session_state.current_stock}. User question: {user_input}"
            
            # Show user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Show thinking spinner while backend processes
            with st.spinner("Bot is thinking..."):
                payload = {"question": user_input}
                response = requests.post(f"{BASE_URL}/query", json=payload)

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                st.session_state.messages.append({"role": "bot", "content": answer})
                st.rerun()
            else:
                st.error("❌ Bot failed to respond: " + response.text)

        except Exception as e:
            raise TradingBotException(e, sys)

# Add a footer with helpful information
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><small>💡 Tips:
    - Use the Quick Stock Analysis panel for instant stock insights
    - Upload relevant documents to enhance the bot's knowledge
    - Ask questions about specific stocks, technical analysis, or market trends
    </small></p>
</div>
""", unsafe_allow_html=True)
