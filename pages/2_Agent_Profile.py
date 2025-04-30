"""
2_Agent_Profile.py
------------------
Displays the currently selected agent's persona details and behavior instructions.
"""
import streamlit as st
from agent_profiles import PROFILES

# Set the title of the page
st.title("🧑‍💼 Agent Profile")
# Select the first agent profile
profile = PROFILES[0]

# Display the current persona details
st.header("Current Persona")
# Show all profile fields except behavior_instruction
for k, v in profile.items():
    if k not in ("behavior_instruction"):
        # Format the key-value pair as a markdown string
        st.markdown(f"**{k.replace('_', ' ').capitalize()}:** {v}")

# Display the behavior instructions
st.subheader("Behavior Instructions")
# Display the behavior instructions as a code block
st.code(profile["behavior_instruction"], language="markdown")

# Provide information on how to edit the agent
st.info("To edit the agent, please modify agent_profiles.py directly. (Live editing UI can be added in the future.)")
