import streamlit as st
import pandas as pd

st.markdown("""
    <style>
        /* titlu */
        h1 {
            color: #E03A3E !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 700 !important;
        }
        /* subtitlu */
        h2, h3 {
            color: #003262 !important;
            font-family: 'Segoe UI', sans-serif !important;
            font-weight: 600 !important;
        }
        /* rotunjire colturi */
        .stDataFrame {
            border: 1px solid #e6e9ef;
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Statistici Delta", layout="wide")
st.title("📊 Statistici și filtrare")

df = pd.read_csv('esantion_delta.csv')

#2. widget
st.header("1. Filtrare Interactivă după Aeroport")
aeroport_ales = st.selectbox("Selectați Aeroportul de Origine (Origin):", sorted(df['Origin'].unique()))

#filtrare
df_filtrat = df[df['Origin'] == aeroport_ales].copy()

#4.tratare val lipsa
st.header("2. Curățarea Datelor (Tratarea Valorilor Lipsă)")
nule_inainte = df_filtrat['DelayReason'].isnull().sum()

df_filtrat['DelayReason'] = df_filtrat['DelayReason'].fillna('Fără întârziere')
nule_dupa = df_filtrat['DelayReason'].isnull().sum()

st.write(f"Valori lipsă în coloana `DelayReason` înainte de tratare: `{nule_inainte}`")
st.success(
    f"Tratare finalizată! Valori lipsă rămase în `DelayReason`: `{nule_dupa}` (Înlocuite cu succes cu textul 'Fără întârziere')")

#11. metrici specifice
st.header("3. Metricile Specifice ale Hub-ului de Plecare")
col1, col2, col3 = st.columns(3)

total_zboruri = len(df_filtrat)
medie_intarziere = df_filtrat['DelayMinutes'].mean()
total_anulate = df_filtrat['Cancelled'].sum()

col1.metric(label="Total Zboruri Operate", value=f"{total_zboruri:,}")
col2.metric(label="Întârziere Medie Globală", value=f"{medie_intarziere:.2f} min")
col3.metric(label="Zboruri Anulate", value=int(total_anulate))

col_stanga, col_dreapta = st.columns(2)

with col_stanga:
    #6. prelucrari statistice
    st.markdown("### 📈 Agregare Date pe Destinații (`groupby`)")
    st.write("Top 5 destinații și indicatorii lor de timp agregați:")

    statistici_dest = df_filtrat.groupby('Destination').agg(
        Numar_Zboruri=('FlightID', 'count'),
        Medie_Intarziere_Min=('DelayMinutes', 'mean'),
        Distanta_Medie_Mile=('Distance', 'mean')
    ).reset_index().sort_values(by='Numar_Zboruri', ascending=False)

    st.dataframe(statistici_dest.head(5), use_container_width=True, hide_index=True)

with col_dreapta:
    #7. loc si iloc
    st.markdown("### 🔍 Tehnici de Accesare Structurală (`loc` & `iloc`)")

    # fol .loc pt a selecta zborurile diverted
    st.write("Filtrare cu `.loc` (Zboruri deviate / Diverted = True):")
    zboruri_deviate = df_filtrat.loc[df_filtrat['Diverted'] == True, ['FlightNumber', 'Destination', 'AircraftType']]
    st.dataframe(zboruri_deviate.head(3), use_container_width=True)

    st.write("Extragere pozițională cu `.iloc` (Primele 3 rânduri și 4 coloane structurale):")
    felie_structurala = df_filtrat.iloc[0:3, 0:4]
    st.dataframe(felie_structurala, use_container_width=True)

