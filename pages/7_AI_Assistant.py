
import streamlit as st
from ai.analytics_agent import answer_dataset_question

st.title("🤖 AI Data Analyst Assistant")
st.caption("Ask questions and get AI-powered insights from your dataset.")

# Check dataset
df = st.session_state.get("working_df")

if df is None:
    st.warning("Please upload a dataset first from Data Import.")
    st.stop()

# Dataset overview
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", f"{len(df):,}")

with col2:
    st.metric("Total Columns", len(df.columns))

with col3:
    st.metric("Missing Values", f"{df.isnull().sum().sum():,}")

st.divider()

# Initialize chat history
if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []

# Clear chat
if st.button("🗑️ Clear Chat"):
    st.session_state.ai_chat_history = []
    st.rerun()

# Suggested questions
st.subheader("💡 Suggested Questions")

suggestions = [
    "Give me an overview of this dataset.",
    "Which numerical columns have the highest average?",
    "Are there missing values or duplicate records?",
    "Explain the customer spending patterns."
]

for question in suggestions:
    if st.button(question, key=f"suggest_{question}"):
        st.session_state.pending_ai_question = question

# Display previous messages
for message in st.session_state.ai_chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_question = st.chat_input("Ask anything about your dataset...")

if "pending_ai_question" in st.session_state:
    user_question = st.session_state.pop("pending_ai_question")

if user_question:
    st.session_state.ai_chat_history.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your dataset..."):
            answer = answer_dataset_question(df, user_question)
            st.markdown(answer)

    st.session_state.ai_chat_history.append({
        "role": "assistant",
        "content": answer
    })
