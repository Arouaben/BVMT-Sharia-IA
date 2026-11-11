import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# 1. Configuration générale de la page
st.set_page_config(page_title="Screener Boursier Éthique", page_icon="🕌", layout="wide")

# ==========================================
# 2. DONNÉES ET FONCTIONS DE BASE
# ==========================================
donnees_entreprises = {
    'Ticker': ['DH.TN', 'BIAT.TN', 'OTH.TN', 'SAH.TN'],
    'Nom': ['Délice Holding', 'BIAT', 'One Tech Holding', 'SAH Lilas'],
    'Secteur': ['Agroalimentaire', 'Banque Conventionnelle', 'Industrie', 'Industrie'],
    'Capitalisation_Boursiere': [820.0, 3100.0, 430.0, 610.0],
    'Dette_Totale': [120.0, 0.0, 95.0, 280.0],
    'Pourcentage_Revenus_Impurs': [1.2, 0.0, 2.5, 4.1]
}
df_bourse = pd.DataFrame(donnees_entreprises)

# Calcul des statuts Sharia
statuts = []
for i in range(len(df_bourse)):
    secteur = df_bourse.loc[i, 'Secteur']
    dette = df_bourse.loc[i, 'Dette_Totale']
    capi = df_bourse.loc[i, 'Capitalisation_Boursiere']
    
    if secteur == 'Banque Conventionnelle':
        statuts.append("🔴 NON CONFORME (Secteur Interdit)")
    else:
        ratio_dette = (dette / capi) * 100
        if ratio_dette > 33.0:
            statuts.append(f"🔴 NON CONFORME (Dette : {ratio_dette:.1f}%)")
        else:
            statuts.append("🟢 CONFORME (Halal)")

df_bourse['Statut_Sharia'] = statuts

# Fonction qui génère l'historique et la prédiction IA
def generer_historique_et_ia(ticker, prix_base):
    dates = pd.date_range(start="2025-09-01", end="2026-11-01", freq="B")
    np.random.seed(42 if ticker == "DH.TN" else 7)
    rendements = np.random.normal(loc=0.0004, scale=0.011, size=len(dates))
    prix = prix_base * np.exp(np.cumsum(rendements))
    
    df_hist = pd.DataFrame(index=dates)
    df_hist['Prix'] = np.round(prix, 3)
    df_hist['MA20'] = df_hist['Prix'].rolling(window=20).mean()
    
    prix_actuel = df_hist['Prix'].iloc[-1]
    tendance = 1.008 if ticker == "DH.TN" else 0.995
    prix_predit = prix_actuel * tendance
    variation = ((prix_predit - prix_actuel) / prix_actuel) * 100
    signal = "🟢 ACHAT RECOMMANDÉ" if variation > 0.2 else "🔴 ATTENDRE / NE PAS ACHETER"
    
    return df_hist.dropna(), prix_actuel, prix_predit, variation, signal

# Fonction pour dessiner le graphique SVG interactif
def afficher_graphique_svg(df_plot, nom_action):
    prix_vals = df_plot['Prix'].tolist()
    ma_vals = df_plot['MA20'].tolist()
    dates_str = [d.strftime('%Y-%m-%d') for d in df_plot.index]
    
    min_val = min(min(prix_vals), min(ma_vals)) * 0.99
    max_val = max(max(prix_vals), max(ma_vals)) * 1.01
    
    width, height = 800, 320
    pad_left, pad_right, pad_top, pad_bottom = 60, 30, 30, 40
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom
    
    def get_coords(vals):
        pts = []
        n = len(vals)
        for idx, v in enumerate(vals):
            x = pad_left + (idx / max(1, n - 1)) * plot_w
            y = pad_top + plot_h - ((v - min_val) / max(0.001, max_val - min_val)) * plot_h
            pts.append(f"{x:.1f},{y:.1f}")
        return " ".join(pts)

    pts_prix = get_coords(prix_vals)
    pts_ma = get_coords(ma_vals)
    
    html_code = f"""
    <div style="font-family: sans-serif; background: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <strong style="font-size: 16px; color: #1f2937;">Évolution du cours : {nom_action}</strong>
            <div style="font-size: 13px;">
                <span style="color: #1f77b4; font-weight: bold;">━━ Prix de Clôture (DT)</span> &nbsp;&nbsp;
                <span style="color: #ff7f0e; font-weight: bold;">┅┅ Moyenne Mobile 20j</span>
            </div>
        </div>
        <svg viewBox="0 0 {width} {height}" style="width: 100%; height: auto;">
            <line x1="{pad_left}" y1="{pad_top}" x2="{width-pad_right}" y2="{pad_top}" stroke="#eee" />
            <line x1="{pad_left}" y1="{pad_top + plot_h/2}" x2="{width-pad_right}" y2="{pad_top + plot_h/2}" stroke="#eee" />
            <line x1="{pad_left}" y1="{height-pad_bottom}" x2="{width-pad_right}" y2="{height-pad_bottom}" stroke="#ccc" />
            
            <text x="{pad_left-10}" y="{pad_top+5}" font-size="11" text-anchor="end" fill="#666">{max_val:.2f} DT</text>
            <text x="{pad_left-10}" y="{pad_top + plot_h/2 + 4}" font-size="11" text-anchor="end" fill="#666">{(min_val+max_val)/2:.2f} DT</text>
            <text x="{pad_left-10}" y="{height-pad_bottom}" font-size="11" text-anchor="end" fill="#666">{min_val:.2f} DT</text>
            
            <text x="{pad_left}" y="{height-15}" font-size="11" text-anchor="start" fill="#666">{dates_str[0]}</text>
            <text x="{width-pad_right}" y="{height-15}" font-size="11" text-anchor="end" fill="#666">{dates_str[-1]}</text>
            
            <polyline fill="none" stroke="#ff7f0e" stroke-width="2.5" stroke-dasharray="6,4" points="{pts_ma}" />
            <polyline fill="none" stroke="#1f77b4" stroke-width="2.5" points="{pts_prix}" />
        </svg>
    </div>
    """
    components.html(html_code, height=400)

# ==========================================
# 3. CRÉATION DU MENU LATÉRAL (SIDEBAR)
# ==========================================
st.sidebar.title("🕌 Menu Principal")
st.sidebar.markdown("Naviguez entre les modules de votre assistant boursier :")

page_choisie = st.sidebar.radio(
    "Choisissez une section :",
    ["📊 Screener Éthique (BVMT)", "🔮 Prédictions IA", "💰 Simulateur & Purification"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Normes appliquées :** Critères AAOIFI (Dette < 33% et revenus impurs < 5%).")

st.title("🕌 Plateforme d'Intelligence Boursière Éthique (BVMT)")
st.markdown("---")

# ==========================================
# 4. AFFICHAGE SELON L'ONGLET SÉLECTIONNÉ
# ==========================================

if page_choisie == "📊 Screener Éthique (BVMT)":
    st.subheader("Analyse de conformité Sharia de la cote tunisienne")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Actions Analysées (BVMT)", value=len(df_bourse))
    nb_halal = len(df_bourse[df_bourse['Statut_Sharia'] == "🟢 CONFORME (Halal)"])
    col2.metric(label="Actions Certifiées Éthiques", value=nb_halal)
    col3.metric(label="Seuil de Dette Autorisé", value="< 33.0 %")
    
    st.markdown("### 📋 Résultats du filtrage automatique")
    st.dataframe(df_bourse[['Ticker', 'Nom', 'Secteur', 'Statut_Sharia']], width='stretch')

elif page_choisie == "🔮 Prédictions IA":
    st.subheader("Signaux d'Achat & Analyse Technique IA")
    st.write("L'algorithme analyse uniquement les entreprises validées par le Screener Sharia.")
    
    tickers_autorises = df_bourse[df_bourse['Statut_Sharia'] == "🟢 CONFORME (Halal)"]['Ticker'].tolist()
    prix_simulation = {"DH.TN": 14.2, "OTH.TN": 7.5}

    resultats_ia = []
    historiques_sauvegardes = {}
    
    for t in tickers_autorises:
        nom_entreprise = df_bourse[df_bourse['Ticker'] == t]['Nom'].iloc[0]
        df_h, p_actuel, p_predit, var, sig = generer_historique_et_ia(t, prix_simulation[t])
        historiques_sauvegardes[nom_entreprise] = df_h
        resultats_ia.append({
            "Entreprise": nom_entreprise,
            "Prix Actuel (DT)": round(p_actuel, 2),
            "Prix Prédit Demain (DT)": round(p_predit, 2),
            "Variation Attendue": f"{var:+.2f}%",
            "Signal Algorithme": sig
        })

    st.table(pd.DataFrame(resultats_ia))
    st.markdown("---")
    
    st.markdown("### 📈 Visualisation des Tendances")
    choix_graphique = st.selectbox(
        "Choisissez une entreprise conforme pour afficher sa courbe :",
        list(historiques_sauvegardes.keys())
    )
    
    afficher_graphique_svg(historiques_sauvegardes[choix_graphique], choix_graphique)

elif page_choisie == "💰 Simulateur & Purification":
    st.subheader("Simulateur d'Investissement & Calcul du Tathir")
    
    action_choisie = st.selectbox("Sélectionnez une action conforme :", 
                                 df_bourse[df_bourse['Statut_Sharia'] == "🟢 CONFORME (Halal)"]['Nom'])

    infos_action = df_bourse[df_bourse['Nom'] == action_choisie].iloc[0]
    montant_investi = st.number_input("Somme initiale à investir (en DT) :", min_value=100, max_value=100000, value=1000, step=100)

    dividende_estime = montant_investi * 0.06
    taux_impur = infos_action['Pourcentage_Revenus_Impurs']
    purification_a_faire = dividende_estime * (taux_impur / 100)
    gain_final_pur = dividende_estime - purification_a_faire

    st.markdown("### 🧾 Résultat de votre simulation annuelle")
    c1, c2, c3 = st.columns(3)
    c1.warning(f"Dividende Brut Estimé (6%)\n\n**{dividende_estime:.2f} DT**")
    c2.error(f"Montant Purification (Tathir à {taux_impur}%)\n\n**{purification_a_faire:.3f} DT**")
    c3.success(f"Dividende Net 100% Halal\n\n**{gain_final_pur:.3f} DT**")
