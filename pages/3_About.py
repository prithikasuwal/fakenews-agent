import streamlit as st

st.title("About This Project")

st.markdown("""
### Vaccine Hesitancy Simulation

This app simulates a conversation with a persona who is hesitant about vaccines. You can chat with the agent, review their persona details, and use this tool for research, empathy-building, or educational purposes.

**Pages:**
- **Chat:** Have a back-and-forth conversation with the simulated agent.
- **Agent Profile:** View the current persona's traits and behavioral instructions.
- **About:** Learn more about the app and its purpose.

---

**Built with:**
- [Streamlit](https://streamlit.io/)
- OpenAI API (via your API key)

**To modify the agent's behavior or persona, edit `agent_profiles.py`.**

*Created by [Your Name or Team], 2025.*
""")
