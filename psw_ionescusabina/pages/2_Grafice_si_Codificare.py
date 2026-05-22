import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import statsmodels.api as sm

st.markdown("""
    <style>
        /* titlul pag */
        h1 {
            color: #E03A3E !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 700 !important;
        }
        /* subtitluri*/
        h2, h3 {
            color: #003262 !important;
            font-family: 'Segoe UI', sans-serif !important;
            font-weight: 600 !important;
        }
        /* rotunjire colturi tabele */
        .stDataFrame {
            border: 1px solid #e6e9ef;
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Modele Delta", layout="wide")
st.title("📈 Grafice și Algoritmi Predictivi")

df = pd.read_csv('esantion_delta.csv')

# esantion
df_ml = df.head(5000).copy()


#5. codificare var
st.header("1. Pregătirea Datelor prin Codificare (Label Encoding)")
st.write("Transformăm caracteristica text `AircraftType` într-o variabilă numerică unică:")

le_avion = LabelEncoder()
df_ml['AircraftType_Codificat'] = le_avion.fit_transform(df_ml['AircraftType'].astype(str))

le_dest = LabelEncoder()
df_ml['Destination_Codificat'] = le_dest.fit_transform(df_ml['Destination'].astype(str))

st.dataframe(df_ml[['AircraftType', 'AircraftType_Codificat', 'Destination', 'Destination_Codificat']].drop_duplicates().head(5), use_container_width=True)


#8.plotly pt grafice
st.header("2. Analiză Vizuală Dinamică (Plotly Scatter Chart)")

#2.widget
filtru_distanta = st.slider(
    "Filtrează interactiv graficul după distanță zbor:",
    int(df_ml['Distance'].min()),
    int(df_ml['Distance'].max()),
    (int(df_ml['Distance'].min()), int(df_ml['Distance'].max()))
)

# filtrarea datelor pentru grafic pe baza sliderului
df_grafic = df_ml[(df_ml['Distance'] >= filtru_distanta[0]) & (df_ml['Distance'] <= filtru_distanta[1])]

fig = px.scatter(
    df_grafic,
    x='Distance',
    y='DelayMinutes',
    color='AircraftType',
    title="Grafic Interactiv: Relația dintre Distanță și Minutele de Întârziere",
    labels={'Distance': 'Distanță (Mile)', 'DelayMinutes': 'Întârziere (Minute)'}
)
st.plotly_chart(fig, use_container_width=True)


#9. scikit-learn pt clusterizare
st.header("3. Segmentarea Zborurilor cu Scikit-Learn (K-Means)")
st.write("Grupăm zborurile în 3 segmente operaționale distincte în funcție de `Distance` și `DelayMinutes`:")

st.markdown("""
<div style="background-color: #f0f4f8; padding: 15px; border-radius: 8px; border-left: 5px solid #003262; margin-top: 15px;">
    <h4 style="margin-top:0; color: #003262;">💡 Ghid de Interpretare Economică a Clusterelor</h4>
    <p>Algoritmul <b>K-Means</b> a segmentat automat cele 5,000 de zboruri Delta în 3 grupuri distincte, utilizând ca axe matematice două criterii operaționale esențiale:</p>
    <ul>
        <li><b>Distanța zborului (Distance):</b> Pentru a separa rutele scurt-curier (regionale) de cele lung-curier (transcontinentale).</li>
        <li><b>Amplitudinea întârzierii (DelayMinutes):</b> Pentru a izola zborurile punctuale de cele care generează pierderi financiare severe.</li>
    </ul>
    <p><b>Cum interpretăm cele 3 profile determinate în tabelul de mai sus:</b></p>
    <ol>
        <li><b>Zboruri Regionale Standard:</b> Clusterul caracterizat prin distanță medie mică și minute de întârziere minime. Reprezintă nucleul stabil și predictibil al operațiunilor zilnice Delta.</li>
        <li><b>Zboruri Transcontinentale Eficiente:</b> Clusterul cu distanță medie mare, dar cu un nivel scăzut de întârzieri. Demonstrează că rutele lungi sunt bine optimizate și nu acumulează decalaje orare din cauza distanței.</li>
        <li><b>Zboruri Critice (Zona de Risc):</b> Clusterul care înregistrează cele mai mari valori în coloana <i>DelayMinutes</i>, indiferent de lungimea rutei. Aceasta este grupa problematică pe care managementul Delta Air Lines trebuie să o monitorizeze, penalitățile și costurile cu compensațiile pasagerilor fiind concentrate aici.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

X_clusters = df_ml[['Distance', 'DelayMinutes']]
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_ml['Cluster'] = kmeans.fit_predict(X_clusters)

rezumat_clustere = df_ml.groupby('Cluster')[['Distance', 'DelayMinutes']].mean().reset_index()
st.write("Caracteristicile medii ale clusterelor identificate:")
st.dataframe(rezumat_clustere, use_container_width=True)

#8. plotly grafic cluster
st.subheader("📊 Structura și Ponderea Clusterelor Identificate")

proportie_clustere = df_ml['Cluster'].value_counts().reset_index()
proportie_clustere.columns = ['Cluster', 'Numar_Zboruri']
proportie_clustere['Cluster'] = proportie_clustere['Cluster'].map({
    0: 'Cluster 0 (Regionale Standard)',
    1: 'Cluster 1 (Transcontinentale)',
    2: 'Cluster 2 (Zona de Risc/Întârzieri)'
})

fig_pie = px.pie(
    proportie_clustere,
    values='Numar_Zboruri',
    names='Cluster',
    title="Ponderea Zborurilor Delta în Profilele Operaționale determinate de K-Means",
    color_discrete_sequence=['#003262', '#1f77b4', '#E03A3E'] # Bleumarin, Albastru deschis și Roșul de risc
)
st.plotly_chart(fig_pie, use_container_width=True)


#10. regresie cu statmodels
st.header("4. Model de Regresie Multiplă cu Statsmodels")
st.write("Analizăm impactul predictorilor `Distance` și `Destination_Codificat` asupra variabilei țintă `DelayMinutes`:")

Y = df_ml['DelayMinutes']
X = df_ml[['Distance', 'Destination_Codificat']]
X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()


#11. metrici specifice
st.subheader("Metrici Specifice rezultate din Regresie:")
col_m1, col_m2 = st.columns(2)

col_m1.metric(label="R-squared (Coeficientul de determinare)", value=f"{model.rsquared:.4f}")
col_m2.metric(label="F-statistic (Valoarea p a modelului)", value=f"{model.f_pvalue:.4f}")

with st.expander("📄 Vezi raportul matematic complet (Sumar OLS)"):
    st.text(model.summary().as_text())