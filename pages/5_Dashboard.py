"""
5_Dashboard.py
-----------------
Dashboard page for radar charts in the Vaccine Hesitancy Simulation app.
Displays all radar charts (real, fake, fact, opinion, combined) for agent ratings.
"""
import streamlit as st
import visualization_utils
import os
from agent_profiles import PROFILES
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF
import base64
import io

st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Dashboard")

df = pd.read_csv('multi_chat_log_profession.csv')
professions = df.columns[1:]

# --- Agent Occupation Filter ---
all_occupations = sorted(list(set([p['occupation'] for p in PROFILES])))
def get_profiles_by_occupation(selected_occupations):
    return [p for p in PROFILES if p['occupation'] in selected_occupations]

selected_occupation = st.selectbox(
    'Select agent occupation to display:',
    all_occupations
)

filtered_profiles = get_profiles_by_occupation([selected_occupation])

# --- Split layout for persona and ratings ---
left_col, right_col = st.columns(2)

with left_col:
    st.header('Agent Persona')
    for profile in filtered_profiles:
        st.subheader(profile['occupation'])
        st.markdown(f"**Name:** {profile['name']}")
        persona_info = "\n".join([
            f"**{k.replace('_', ' ').capitalize()}**: {v}" for k, v in profile.items() if k not in ("name", "behavior_instruction", "occupation")
        ])
        st.markdown(persona_info)
        if "personality_traits" in profile:
            st.markdown("**Personality Traits:**")
            if isinstance(profile["personality_traits"], (list, tuple)):
                for trait in profile["personality_traits"]:
                    st.markdown(f"- {trait}")
            else:
                st.markdown(profile["personality_traits"])

with right_col:
    st.header('Question Ratings for Selected Agent')
    agent_col_name = selected_occupation
    if agent_col_name in professions:
        for i, question in enumerate(['Real', 'Fake', 'Fact', 'Opinion']):
            rating = df.loc[df['Question'].str.lower() == question.lower(), agent_col_name].values[0]
            st.metric(label=f"{question} Question", value=rating)
    else:
        st.warning('No rating data available for this occupation.')

# --- Agent Radar Charts Section (below split) ---
st.header('Agent Radar Charts')
options = ['Real', 'Fake', 'Fact', 'Opinion']
selected = st.multiselect(
    'Select question type(s) to display:',
    options,
    default=['Real']
)
if set(selected) == set(options):
    selected = ['Combined']
radar_charts = {
    'Real': ('multi_chat_log_profession_real.png', 'Real'),
    'Fake': ('multi_chat_log_profession_fake.png', 'Fake'),
    'Fact': ('multi_chat_log_profession_fact.png', 'Fact'),
    'Opinion': ('multi_chat_log_profession_opinion.png', 'Opinion'),
    'Combined': ('multi_chat_log_profession_combined.png', 'Combined'),
}
st.markdown("""
This section presents radar charts for agent ratings on different question types (real, fake, fact, opinion), as well as a combined chart. Each chart uses a distinct color for clarity.
""")
if 'Combined' in selected and len(selected) == 1:
    file, title = radar_charts['Combined']
    st.subheader(f'{title} Question')
    st.image(file, caption=f'{title} Question', use_container_width=True)
elif len(selected) == 1:
    file, title = radar_charts[selected[0]]
    st.subheader(f'{title} Question')
    st.image(file, caption=f'{title} Question', use_container_width=True)
elif len(selected) > 1:
    combined_path = 'multi_chat_log_profession_custom_combined.png'
    visualization_utils.plot_combined_radar(selected, 'multi_chat_log_profession.csv', combined_path)
    st.subheader(f"Combined Radar Chart: {', '.join(selected)}")
    st.image(combined_path, caption=f"Combined: {', '.join(selected)}", use_container_width=True)

# --- Custom Agent Persona Report ---
st.header('Custom Agent Persona Report')
selected_profile_name = st.selectbox('Select agent to generate profile card:', [p['name'] for p in PROFILES])
profile = next((p for p in PROFILES if p['name'] == selected_profile_name), None)
if profile:
    st.subheader(f"Profile Card: {profile['name']}")
    st.markdown(f"**Occupation:** {profile.get('occupation', 'N/A')}")
    st.markdown(f"**Age:** {profile.get('age', 'N/A')}")
    st.markdown(f"**Gender:** {profile.get('gender', 'N/A')}")
    st.markdown(f"**Education Level:** {profile.get('education_level', 'N/A')}")
    st.markdown(f"**Location Type:** {profile.get('location_type', 'N/A')}")
    st.markdown(f"**Socioeconomic Status:** {profile.get('socioeconomic_status', 'N/A')}")
    st.markdown(f"**Marital Status:** {profile.get('marital_status', 'N/A')}")
    st.markdown(f"**Primary News Source:** {profile.get('primary_news_source', 'N/A')}")
    # Show personality traits if present
    if 'personality_traits' in profile:
        st.markdown('**Personality Traits:**')
        if isinstance(profile['personality_traits'], (list, tuple)):
            for trait in profile['personality_traits']:
                st.markdown(f"- {trait}")
        else:
            st.markdown(profile['personality_traits'])
    # Show ratings
    st.markdown('**Ratings:**')
    ratings = {}
    for q in ['Real', 'Fake', 'Fact', 'Opinion']:
        occ = profile.get('occupation')
        try:
            val = df.loc[df['Question'].str.lower() == q.lower(), occ].values[0]
        except:
            val = 'N/A'
        ratings[q] = val
    st.table(pd.DataFrame([ratings]))
    # Downloadable profile card as PDF only
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'Agent Profile Card: {profile["name"]}', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Occupation: {profile.get("occupation", "N/A")}', ln=True)
    pdf.cell(0, 10, f'Age: {profile.get("age", "N/A")}', ln=True)
    pdf.cell(0, 10, f'Gender: {profile.get("gender", "N/A")}', ln=True)
    pdf.cell(0, 10, f'Education Level: {profile.get("education_level", "N/A")}', ln=True)
    pdf.cell(0, 10, f'Location Type: {profile.get("location_type", "N/A")}', ln=True)
    pdf.cell(0, 10, f'Socioeconomic Status: {profile.get("socioeconomic_status", "N/A")}', ln=True)
    pdf.cell(0, 10, f'Marital Status: {profile.get("marital_status", "N/A")}', ln=True)
    pdf.cell(0, 10, f'Primary News Source: {profile.get("primary_news_source", "N/A")}', ln=True)
    # Add personality traits
    if 'personality_traits' in profile:
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Personality Traits:', ln=True)
        pdf.set_font('Arial', '', 11)
        if isinstance(profile['personality_traits'], (list, tuple)):
            for trait in profile['personality_traits']:
                pdf.multi_cell(0, 8, f'- {trait}')
        else:
            pdf.multi_cell(0, 8, str(profile['personality_traits']))
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Ratings:', ln=True)
    pdf.set_font('Arial', '', 11)
    for q in ['Real', 'Fake', 'Fact', 'Opinion']:
        pdf.cell(0, 8, f'{q}: {ratings[q]}', ln=True)
    pdf_output = pdf.output(dest='S').encode('latin1')
    b64_pdf = base64.b64encode(pdf_output).decode()
    pdf_href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{profile["name"].replace(" ", "_")}_profile_card.pdf">Download Profile Card (PDF)</a>'
    st.markdown(pdf_href, unsafe_allow_html=True)

# --- Demographic Filter & Bar Chart ---
def get_age_group(age):
    try:
        age = int(age)
        if age < 25:
            return '<25'
        elif age < 35:
            return '25-34'
        elif age < 45:
            return '35-44'
        elif age < 55:
            return '45-54'
        else:
            return '55+'
    except:
        return 'Unknown'

demographic_fields = ['gender', 'location_type', 'education_level', 'socioeconomic_status', 'marital_status', 'age_group', 'primary_news_source']
demo_options = [f for f in demographic_fields if f != 'age_group' or any('age' in p for p in PROFILES)]

# Prepare age_group for all profiles
enriched_profiles = []
for p in PROFILES:
    p = p.copy()
    if 'age' in p:
        p['age_group'] = get_age_group(p['age'])
    else:
        p['age_group'] = 'Unknown'
    enriched_profiles.append(p)

demographic = st.selectbox('Filter by demographic:', ['None'] + demographic_fields)
demographic_values = []
if demographic != 'None':
    demographic_values = sorted(list(set([str(p.get(demographic, 'Unknown')) for p in enriched_profiles])))
    selected_demo = st.selectbox(f'Select {demographic.replace("_", " ")}:', demographic_values)
    filtered_professions = [p['occupation'] for p in enriched_profiles if str(p.get(demographic, 'Unknown')) == selected_demo]
else:
    filtered_professions = professions

st.header('Average Ratings by Question Type')
ratings_data = []
for q in ['Real', 'Fake', 'Fact', 'Opinion']:
    values = [df.loc[df['Question'].str.lower() == q.lower(), prof].values[0]
              for prof in professions if prof in filtered_professions and len(df.loc[df['Question'].str.lower() == q.lower(), prof].values) > 0]
    if values:
        ratings_data.append({'Question': q, 'Average Rating': sum(values)/len(values)})
if ratings_data:
    fig = go.Figure([go.Bar(x=[d['Question'] for d in ratings_data], y=[d['Average Rating'] for d in ratings_data],
                            marker_color=['green','coral','orange','blue'])])
    fig.update_layout(title=f'Average Ratings by Question Type' + (f' ({selected_demo})' if demographic != 'None' else ''),
                      xaxis_title='Question Type', yaxis_title='Average Rating', yaxis_range=[0,10])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info('No data to display for the selected demographic filter.')
