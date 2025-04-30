"""
1_Chat.py
---------
Single-agent chat page for the Vaccine Hesitancy Simulation app.
Allows the user to select an agent persona, chat in character, and view persona details.
"""

import os
import streamlit as st
from agent_profiles import PROFILES, format_profile
from agents import Agent, Runner
import asyncio

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
        # Display agent message
        st.markdown(f"**{profile['name']}:** {msg['content']}")

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
            Simulates a chat with the agent.
            """
            # Build conversation history for context
            conversation = ""
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "user":
                    conversation += f"User: {msg['content']}\n"
                else:
                    conversation += f"{profile['name']}: {msg['content']}\n"
            prompt = conversation + f"{profile['name']} (reply in character):"
            agent = Agent(name=profile["name"], instructions=format_profile(profile))
            result = await Runner.run(agent, prompt)
            return result.final_output
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
st.sidebar.code(profile["behavior_instruction"], language="markdown")
