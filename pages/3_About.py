import streamlit as st

st.title("About This Project")

st.markdown("""
### Vaccine Hesitancy Simulation & Agent Dashboard

This interactive web app enables users to:
- **Chat** with simulated agent personas, each with unique backgrounds and beliefs about vaccines.
- **Explore agent profiles**: Review detailed demographic, behavioral, and attitudinal information for each persona.
- **Analyze agent responses**: Use the Dashboard to visualize and compare how different agent types rate real, fake, fact, and opinion questions.
- **Generate reports**: Download detailed agent profile cards as PDFs for research, presentations, or educational use.

**Key Features:**
- Dynamic radar and bar charts for agent ratings by occupation and demographic filters (age, gender, education, news source, etc.).
- Persona cards with demographic, behavioral, and attitudinal data.
- Custom report generation and export.

**Use Cases:**
- Vaccine hesitancy research and education
- Empathy-building and scenario training
- Data-driven communication strategy development

**Pages:**
- **Chat**: Converse with a simulated agent.
- **Agent Profile**: View a persona's traits and instructions.
- **Dashboard**: Visualize, filter, and download agent data and reports.
- **About**: Learn about the app and its features.

---

**Built with:**
- [Streamlit](https://streamlit.io/)
- OpenAI API (via your API key)
- Plotly, pandas, fpdf

**To modify the agent's behavior, persona, or demographic data, edit `agent_profiles.py`.**

*Created by Prithika Suwal, 2025.*
""")
