"""
4_Multi_Chat.py
--------------
Multi-agent chat page for the Vaccine Hesitancy Simulation app.
Allows the user to select multiple agent personas and receive responses from all selected agents at once.
"""

import os
import streamlit as st
from agent_profiles import PROFILES, format_profile
from agents import Agent, Runner
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
                # Create an agent instance and run the conversation
                agent = Agent(name=profile["name"], instructions=format_profile(profile))
                result = await Runner.run(agent, user_input + "\n(As this character, reply on the first line ONLY with a single number from 1 to 5 (where 1 means you are least likely and 5 means you are most likely to agree, comply, or react positively to the question, based on your beliefs, biases, and background). On the next line(s), explain your reasoning or thoughts in character. Do NOT break character.)")
                results.append((profile, result.final_output))
        return results

    # Run the simulation and display the results
    responses = asyncio.run(simulate_all())
    st.markdown("---")

    import csv
    import os
    csv_path = os.path.join(os.path.dirname(__file__), '../multi_chat_log.csv')
    # Prepare headers: Question, <Agent1> Rating, <Agent2> Rating, ...
    header = ['Question']
    for profile, _ in responses:
        header.append(f"{profile['name']} Rating")
    # Prepare row: question, <Agent1> rating, <Agent2> rating, ...
    row = [user_input]
    for profile, output in responses:
        lines = [l for l in output.strip().split('\n') if l.strip()]
        rating = lines[0] if lines else ''
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
        st.markdown(f"**Rating:** {output}")
        st.markdown("---")
