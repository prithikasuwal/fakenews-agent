"""
app.py
------
Streamlit multipage launcher for the Vaccine Hesitancy Simulation app.
Provides navigation and a welcome message.
"""
import streamlit as st

st.set_page_config(page_title="Vaccine Hesitancy Simulation", page_icon="🧠")
st.title("Vaccine Hesitancy Simulation")

st.markdown("""
Welcome! Use the sidebar to navigate between:
- **Chat**: Talk with the simulated agent.
- **Multi-Chat**: Send a message to multiple agents at once.
- **Agent Profile**: View the agent's persona.
- **About**: Learn more about this project.

Start by selecting a page from the sidebar.
""")
