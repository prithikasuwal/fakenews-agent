"""
1_Chat.py
---------
Single-agent chat page for the Vaccine Hesitancy Simulation app.
Allows the user to select an agent persona, chat in character, and view persona details.
"""

import os
import streamlit as st
from agent_profiles import PROFILES, format_profile
import asyncio
import pandas as pd
from data_loader import load_articles_dataset, categorize_articles
from news_classifier import predict_article_type
from retrieval_utils import get_top_k_similar_articles

# Function to reset chat history and input box
# Called when user clicks the New Chat button
def reset_chat():
    """
    Resets the chat history and input box.
    """
    st.session_state["chat_history"] = []
    st.session_state["chat_input"] = ""
    st.session_state["selected_agent"] = st.session_state.get("selected_agent", 0)

# Sidebar: API Key input for OpenAI
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if api_key:
    # Set API key as environment variable
    os.environ["OPENAI_API_KEY"] = api_key
else:
    # Display warning if API key is not provided
    st.warning("Please enter your OpenAI API Key in the sidebar to use the chat.")

# Sidebar: Agent selector (dropdown)
agent_names = [profile["name"] for profile in PROFILES]
selected_agent = st.sidebar.selectbox("Choose an agent persona", agent_names, key="selected_agent")

# Reset chat when agent changes
if "last_agent" not in st.session_state:
    # Initialize last agent if not present in session state
    st.session_state["last_agent"] = selected_agent
if selected_agent != st.session_state["last_agent"]:
    # Reset chat history and input box when agent changes
    st.session_state["chat_history"] = []
    st.session_state["chat_input"] = ""
    st.session_state["last_agent"] = selected_agent

# Button to start a fresh new chat
st.sidebar.button(" New Chat", on_click=reset_chat)

# Load and categorize articles dataset
try:
    articles_df = load_articles_dataset()
    article_categories = categorize_articles(articles_df, label_column="Type")
    article_labels = articles_df['Type'].unique().tolist()
    # Prepare a background context with all articles for the agent (not shown to user)
    if articles_df is not None:
        all_articles_context = "Here is background information from recent articles (for your reference only, do not mention directly):\n"
        for _, row in articles_df.iterrows():
            all_articles_context += f"- [{row['Type']}] {row['Article Name']} ({row['Site Name']})\n"
    else:
        all_articles_context = ""
except Exception as e:
    articles_df = None
    article_categories = None
    article_labels = []
    all_articles_context = ""
    st.warning(f"Could not load articles dataset: {e}")

st.title(" Vaccine Hesitancy Chat")
# Find the profile for the selected agent
profile = next((p for p in PROFILES if p["name"] == selected_agent), PROFILES[0])

# Initialize chat history in session state if not present
if "chat_history" not in st.session_state:
    # Initialize chat history as an empty list
    st.session_state["chat_history"] = []

# Display chat history (alternating user/agent messages)
for idx, msg in enumerate(st.session_state["chat_history"]):
    if msg["role"] == "user":
        # Display user message
        st.markdown(f"**You:** {msg['content']}")
        # Add a horizontal line after the user message if next is agent
        if idx + 1 < len(st.session_state["chat_history"]) and st.session_state["chat_history"][idx + 1]["role"] == "agent":
            st.markdown("---")
    else:
        # Display agent reply as plain scale 1 to 10 answer
        st.markdown(f"**{profile['name']} (Scale 1–10, 1 = least likely, 10 = most likely):**\n{msg['content']}")

# User input for next message (in a form to prevent looping)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message and press Enter", key="chat_input")
    submitted = st.form_submit_button("Send")

# When user submits a message, append it and get agent's reply
if submitted and user_input.strip() and api_key:
    # Append user message to chat history
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    with st.spinner(f"{profile['name']} is typing..."):
        # Simulate chat with agent
        async def simulate_chat():
            """
            Simulates a chat with the agent, always including article background context.
            """
            conversation = ""
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "user":
                    conversation += f"User: {msg['content']}\n"
                else:
                    conversation += f"{profile['name']}: {msg['content']}\n"
            # Always include all articles as background context
            prompt = conversation + all_articles_context + f"{profile['name']} (As this character, reply on the first line ONLY with a single number from 1 to 10 (where 1 means you are least likely and 10 means you are most likely to agree, comply, or react positively to the question, based on your beliefs, background, and characteristics). On the next line(s), explain your reasoning or thoughts in character. Your explanation MUST clearly justify the number you chose and should not contradict it. Double-check for consistency. Do NOT break character.)"
            # Removed Agent and Runner references
            # agent = Agent(name=profile["name"], instructions=format_profile(profile))
            # result = await Runner.run(agent, prompt)
            # For now, just return a placeholder response
            return "5\nThis is a placeholder response."
        agent_reply = asyncio.run(simulate_chat())
    # Append agent reply to chat history
    st.session_state["chat_history"].append({"role": "agent", "content": agent_reply})
    # Rerun the app to display updated chat history
    st.rerun()

# Show persona details in sidebar (always visible)
st.sidebar.markdown("**Persona Details:**")
st.sidebar.markdown(
    "<br>".join([
        f"<b>{k.replace('_', ' ').capitalize()}</b>: {v}"
        for k, v in profile.items() if k not in ("name", "behavior_instruction")
    ]),
    unsafe_allow_html=True,
)
st.sidebar.markdown("**Behavior:**")
if "behavior_instruction" in profile:
    st.sidebar.code(profile["behavior_instruction"], language="markdown")
else:
    st.sidebar.markdown("_No specific behavior instructions for this persona._")
