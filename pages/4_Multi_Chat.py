"""
4_Multi_Chat.py
--------------
Multi-agent chat page for the Vaccine Hesitancy Simulation app.
Allows the user to select multiple agent personas and receive responses from all selected agents at once.
"""

import os
import streamlit as st
from agent_profiles import PROFILES, format_profile
import asyncio
import csv

# Set the title of the page
st.title("🤝 Multi-Agent Chat")

# Sidebar: API Key input for OpenAI
# Get the OpenAI API key from the user and store it as an environment variable
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    st.warning("Please enter your OpenAI API Key in the sidebar to use the chat.")

# Sidebar: Multi-agent selection (checkboxes)
# Get the list of agent names and allow the user to select multiple agents
agent_names = [profile["name"] for profile in PROFILES]
selected_agents = st.sidebar.multiselect("Select agents to chat with", agent_names, default=agent_names[:2])

# Show persona details for selected agents in the sidebar
# Display the details of each selected agent in the sidebar
for agent_name in selected_agents:
    profile = next((p for p in PROFILES if p["name"] == agent_name), None)
    if profile:
        st.sidebar.markdown(f"---\n**{profile['name']}**")
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

# Display instructions for the user
st.write("Select one or more agents in the sidebar. Type a message and see how each persona responds!")

# User input (form prevents repeated submissions)
# Create a form to get user input and prevent repeated submissions
with st.form(key="multi_chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message and press Enter", key="multi_chat_input")
    submitted = st.form_submit_button("Send to All Agents")

# When user submits, send input to all selected agents and display their responses
# If the user submits the form, simulate conversations with all selected agents and display their responses
if submitted and user_input.strip() and api_key and selected_agents:
    # Define an asynchronous function to simulate conversations with all selected agents
    async def simulate_all():
        results = []
        for agent_name in selected_agents:
            profile = next((p for p in PROFILES if p["name"] == agent_name), None)
            if profile:
                # Create a placeholder for agent instance and run the conversation
                agent = None  # Placeholder for Agent instance
                result = None  # Placeholder for conversation result
                results.append((profile, result))
        return results

    # Run the simulation and display the results
    responses = asyncio.run(simulate_all())
    st.markdown("---")

    import csv
    import os
    csv_path = os.path.join(os.path.dirname(__file__), '../multi_chat_log.csv')
    # Prepare headers: Question, <Agent1> Rating, <Agent2> Rating, ...
    header = ["Question"]
    for profile, _ in responses:
        header.append(f"{profile['name']} Rating (1–10)")
    # Prepare row: question, <Agent1> rating, <Agent2> rating, ...
    row = [user_input]
    validation_msgs = []
    for profile, output in responses:
        lines = []  # Placeholder for conversation output
        rating = ''  # Placeholder for rating
        # Validate rating is an integer between 1 and 10
        try:
            rating_int = int(rating)
            if not (1 <= rating_int <= 10):
                validation_msgs.append(f"{profile['name']}: Invalid rating '{rating}' (should be 1–10)")
                rating = f"❌ {rating}"
        except Exception:
            if rating != '':
                validation_msgs.append(f"{profile['name']}: Invalid rating '{rating}' (not an integer)")
                rating = f"❌ {rating}"
        row.append(rating)
    # Always write header as first row, then append new row
    file_exists = os.path.isfile(csv_path)
    if not file_exists:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerow(row)
    else:
        # Check if header matches, if not, rewrite file with new header and keep only current row
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            existing_header = next(reader, None)
            existing_rows = list(reader)
        if existing_header != header:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerow(row)
        else:
            with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)

    for profile, output in responses:
        st.markdown(f"### {profile['name']}")
        st.markdown("<details><summary>Persona Details</summary>" +
                    "<br>".join([f"<b>{k.replace('_', ' ').capitalize()}</b>: {v}" for k, v in profile.items() if k not in ("name", "behavior_instruction")]) +
                    "</details>", unsafe_allow_html=True)
        lines = []  # Placeholder for conversation output
        rating = ''  # Placeholder for rating
        try:
            rating_int = int(rating)
            if not (1 <= rating_int <= 10):
                st.markdown(f"**Rating (1–10):** ❌ {rating} _(Invalid: should be 1–10)_")
            else:
                st.markdown(f"**Rating (1–10):** {rating}")
        except Exception:
            if rating != '':
                st.markdown(f"**Rating (1–10):** ❌ {rating} _(Invalid: not an integer)_")
            else:
                st.markdown(f"**Rating (1–10):** (No rating provided)")
        st.markdown("---")
    if validation_msgs:
        st.warning("\n".join(validation_msgs))

# --- Radar Charts Section ---
# (Removed visualization from Multi-Chat page; now only available on Visualization page)
