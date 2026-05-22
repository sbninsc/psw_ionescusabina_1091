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

# 1.dezv apl struct multipagina
st.set_page_config(page_title="Delta Airlines",page_icon="✈️",layout="wide",initial_sidebar_state="expanded")

st.title("✈️Delta Airlines - Analiză Operațională ")
st.markdown("### Proiect Pachete Software")

st.info("""
**Context Economic (Obiectiv Strategic):** Analiza performanței zborurilor organizației Delta Air Lines 
în vederea optimizării rutelor, gestionării eficiente a motivelor de întârziere (DelayReason) 
și fundamentării deciziilor manageriale privind alocarea flotei pentru reducerea costurilor operaționale.
""")

st.header("📥 Citire Date")

#3. import fisier
df = pd.read_csv('esantion_delta.csv')

st.success(f"✅ Fișierul 'esantion_delta.csv' a fost importat cu succes!")
st.write(f"Volumul total de date identificat: **{len(df):,} înregistrări (zboruri)**.")


st.write("Previzualizare primele 5 rânduri din jurnalul de zbor brut:")
st.dataframe(df.head(5), use_container_width=True)

st.markdown("---")
st.markdown("💡 **Ghid de navigare:** Utilizați meniul lateral din stânga pentru a explora paginile dedicate statisticilor descriptive sau modelelor predictive avansate.")