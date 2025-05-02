"""
2_Agent_Profile.py
------------------
Displays the currently selected agent's persona details and personality traits.
"""
import streamlit as st
from agent_profiles import PROFILES

# Set the title of the page
st.title("🧑‍💼 Agent Profile")

# Add a selectbox to choose an agent by name
agent_names = [p['name'] for p in PROFILES]
selected_name = st.selectbox("Select agent", agent_names)
profile = next(p for p in PROFILES if p['name'] == selected_name)

# Display the current persona details
st.header("Current Persona")
# Show all profile fields except behavior_instruction
for k, v in profile.items():
    if k not in ("behavior_instruction"):
        # Format the key-value pair as a markdown string
        st.markdown(f"**{k.replace('_', ' ').capitalize()}:** {v}")

# Display Personality Traits if present
if 'personality_traits' in profile:
    st.subheader("Personality Traits")
    if isinstance(profile['personality_traits'], (list, tuple)):
        for trait in profile['personality_traits']:
            st.markdown(f"- {trait}")
    else:
        st.markdown(profile['personality_traits'])

# Provide information on how to edit the agent
st.info("To edit the agent, please modify agent_profiles.py directly. (Live editing UI can be added in the future.)")
