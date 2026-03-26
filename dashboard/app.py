import streamlit as st
import psycopg2
import psycopg2.extras
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME", "job_market"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "admin123")
    )

@st.cache_data
def load_data():
    conn = get_db()
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

df = load_data()

st.title("📊 Job Market Dashboard")
st.markdown("Analyse du marché de l'emploi en temps réel")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Offres", len(df))
col2.metric("Entreprises", df['company'].nunique())
col3.metric("Localisations", df['location'].nunique())
col4.metric("Sources", df['source'].nunique())

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Offres par source")
    fig = px.pie(df, names='source', title='Distribution par source')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 entreprises")
    top_companies = df['company'].value_counts().head(10).reset_index()
    top_companies.columns = ['company', 'count']
    fig = px.bar(top_companies, x='count', y='company', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 localisations")
    top_locations = df['location'].value_counts().head(10).reset_index()
    top_locations.columns = ['location', 'count']
    fig = px.bar(top_locations, x='count', y='location', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Salaires (Adzuna)")
    df_salary = df.dropna(subset=['salary_min', 'salary_max'])
    if not df_salary.empty:
        fig = px.scatter(df_salary, x='salary_min', y='salary_max',
                        hover_data=['title', 'company', 'location'],
                        title='Distribution des salaires')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas de données de salaires disponibles")

st.divider()

st.subheader("🏆 Top métiers par nombre d'offres")
top_jobs = df['title'].value_counts().head(15).reset_index()
top_jobs.columns = ['title', 'count']
fig = px.bar(top_jobs, x='count', y='title', orientation='h',
             color='count', color_continuous_scale='Blues',
             title='Top 15 intitulés de poste')
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Recommandation
st.subheader("🔍 Recommandation d'emplois")
col1, col2 = st.columns(2)
with col1:
    skills_input = st.text_input("Tes compétences (séparées par des virgules)", "python, sql, data")
with col2:
    location_input = st.text_input("Localisation (optionnel)", "")

if st.button("Trouver des offres"):
    skill_list = [s.strip().lower() for s in skills_input.split(",")]
    filtered = df.copy()
    
    mask = pd.Series([False] * len(filtered))
    for skill in skill_list:
        mask |= filtered['title'].str.lower().str.contains(skill, na=False)
        mask |= filtered['description'].str.lower().str.contains(skill, na=False)
    filtered = filtered[mask]
    
    if location_input:
        filtered = filtered[filtered['location'].str.lower().str.contains(location_input.lower(), na=False)]
    
    st.write(f"**{len(filtered)} offres trouvées**")
    if not filtered.empty:
        st.dataframe(filtered[['title', 'company', 'location', 'source', 'url']].head(20))

st.divider()

# Table complète
st.subheader("📋 Toutes les offres")
source_filter = st.selectbox("Filtrer par source", ["Toutes"] + list(df['source'].unique()))
if source_filter != "Toutes":
    df_filtered = df[df['source'] == source_filter]
else:
    df_filtered = df

st.dataframe(df_filtered[['title', 'company', 'location', 'source', 'url']].head(50))