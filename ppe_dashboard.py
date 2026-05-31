import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# ── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PPE – Remédiation Immunologie 3AC",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans Arabic', sans-serif; }

.main { background-color: #F8F9FB; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F4C75 0%, #1B6CA8 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label { color: rgba(255,255,255,0.85) !important; }

.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    border-left: 4px solid #1B6CA8;
    margin-bottom: 8px;
}
.kpi-card.green { border-left-color: #2E9E6B; }
.kpi-card.orange { border-left-color: #E87C35; }
.kpi-card.purple { border-left-color: #7C5CBF; }

.kpi-value { font-size: 2rem; font-weight: 600; color: #1a1a2e; margin: 0; }
.kpi-label { font-size: 0.78rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.kpi-delta { font-size: 0.82rem; margin-top: 4px; }
.delta-up { color: #2E9E6B; }
.delta-down { color: #E04E39; }

.section-header {
    font-size: 1rem; font-weight: 600; color: #1a1a2e;
    border-bottom: 2px solid #E5E7EB;
    padding-bottom: 8px; margin-bottom: 16px; margin-top: 8px;
}

.insight-box {
    background: #EEF4FF; border-radius: 10px;
    border-left: 4px solid #1B6CA8;
    padding: 14px 18px; font-size: 0.88rem;
    color: #374151; line-height: 1.7;
}
.insight-box b { color: #1B6CA8; }

.badge-maitrise { background:#D1FAE5; color:#065F46; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:500; }
.badge-cours    { background:#FEF3C7; color:#92400E; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:500; }
.badge-diff     { background:#FEE2E2; color:#991B1B; padding:3px 10px; border-radius:20px; font-size:0.78rem; font-weight:500; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #F3F4F6; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 500; color: #6B7280; }
.stTabs [aria-selected="true"] { background: white !important; color: #1B6CA8 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
random.seed(42)

prenoms_filles = ["Amina","Fatima","Nadia","Sara","Houda","Zineb","Maryam","Hajar",
                  "Layla","Rim","Chaimae","Samira","Loubna","Hiba","Asma","Siham"]
prenoms_garcons = ["Khalid","Youssef","Hassan","Amine","Mehdi","Bilal","Adil","Omar",
                   "Soufiane","Othmane","Ilias","Anass","Hamza","Saad","Rayan","Zakaria"]

pre_f  = [5,7,8,6,8,6,9,7,6,5,8,6,5,7,8,6]
post_f = [15,15,16,13,16,14,17,15,13,12,16,14,11,15,16,13]
pre_g  = [6,8,5,7,7,5,8,6,6,7,9,7,8,6,8,7]
post_g = [14,16,12,14,15,12,16,13,13,14,17,14,16,12,15,13]

df_f = pd.DataFrame({"Nom": prenoms_filles, "Genre": " (Filles)",
                     "Pré-test": pre_f, "Post-test": post_f})
df_g = pd.DataFrame({"Nom": prenoms_garcons, "Genre": " (Garçons)",
                     "Pré-test": pre_g, "Post-test": post_g})
df = pd.concat([df_f, df_g], ignore_index=True)
df["Progression"] = df["Post-test"] - df["Pré-test"]
df["Prog %"] = (df["Progression"] / df["Pré-test"] * 100).round(1)

def get_niveau(s):
    if s > 14: return "Maîtrise"
    if s >= 10: return "En cours"
    return "Difficultés"

df["Niveau"] = df["Post-test"].apply(get_niveau)

competences = ["Lecture des axes","Compréhension des variations","Comparaison de courbes","Formulation de conclusions"]
pre_comp  = [24, 32, 45, 42]
post_comp = [83, 74, 68, 58]
df_comp = pd.DataFrame({"Compétence": competences, "Pré-test": pre_comp, "Post-test": post_comp})
df_comp["Progression"] = df_comp["Post-test"] - df_comp["Pré-test"]

pre_comp_f = [26,35,46,45]; post_comp_f = [86,76,70,62]
pre_comp_g = [22,29,44,39]; post_comp_g = [80,72,66,54]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 PPE – CRMEF")
    st.markdown("**Remédiation Immunologie**  \n3ème Année Collège · 3AC")
    st.markdown("---")
    st.markdown("### ⚙️ Filtres")
    filtre_genre = st.selectbox("Genre", ["Tous", " (Filles)", " (Garçons)"])
    filtre_niveau = st.selectbox("Niveau (post-test)", ["Tous", "Maîtrise", "En cours", "Difficultés"])
    st.markdown("---")
    st.markdown("### 📋 Infos séance")
    st.info("📅 Séance de soutien pédagogique  \n👥 6 groupes collaboratifs  \n🧠 Guidage progressif  \n✅ Correction collective")
    st.markdown("---")
    st.caption("Projet Professionnel Étudiant · Formation initiale enseignants")

# ── Filter data ───────────────────────────────────────────────────────────────
df_filtered = df.copy()
if filtre_genre != "Tous":
    df_filtered = df_filtered[df_filtered["Genre"] == filtre_genre]
if filtre_niveau != "Tous":
    df_filtered = df_filtered[df_filtered["Niveau"] == filtre_niveau]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🔬 Tableau de bord – Projet Professionnel de l'Étudiant")
st.markdown("**Remédiation des difficultés en lecture des graphes immunologiques** · 3AC · CRMEF")
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">👥 Effectif total</div>
        <div class="kpi-value">{len(df_filtered)}</div>
        <div class="kpi-delta">sur 32 élèves</div>
    </div>""", unsafe_allow_html=True)

with k2:
    moy_pre = df_filtered["Pré-test"].mean()
    st.markdown(f"""<div class="kpi-card orange">
        <div class="kpi-label">📉 Moy. Pré-test</div>
        <div class="kpi-value">{moy_pre:.1f}/20</div>
        <div class="kpi-delta delta-down">Avant remédiation</div>
    </div>""", unsafe_allow_html=True)

with k3:
    moy_post = df_filtered["Post-test"].mean()
    st.markdown(f"""<div class="kpi-card green">
        <div class="kpi-label">📈 Moy. Post-test</div>
        <div class="kpi-value">{moy_post:.1f}/20</div>
        <div class="kpi-delta delta-up">Après remédiation</div>
    </div>""", unsafe_allow_html=True)

with k4:
    prog_moy = df_filtered["Progression"].mean()
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">🚀 Progression moy.</div>
        <div class="kpi-value">+{prog_moy:.1f} pts</div>
        <div class="kpi-delta delta-up">↑ amélioration nette</div>
    </div>""", unsafe_allow_html=True)

with k5:
    n_maitrise = len(df_filtered[df_filtered["Niveau"] == "Maîtrise"])
    pct = int(n_maitrise / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
    st.markdown(f"""<div class="kpi-card purple">
        <div class="kpi-label">🏆 Taux de maîtrise</div>
        <div class="kpi-value">{pct}%</div>
        <div class="kpi-delta delta-up">{n_maitrise} élèves</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Vue Globale",
    "⚖️ Filles vs garçon",
    "🎯 Compétences",
    "👥 Suivi Élèves",
    "📈 Simulation",
    "📋 Rapport"
])

# ═══════════════════════════ TAB 1 : VUE GLOBALE ════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Évolution globale pré-test → post-test</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])

    with c1:
        # Grouped bar: pre vs post by student
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Pré-test", x=df_filtered["Nom"], y=df_filtered["Pré-test"],
                             marker_color="#93C5FD", marker_line_width=0))
        fig.add_trace(go.Bar(name="Post-test", x=df_filtered["Nom"], y=df_filtered["Post-test"],
                             marker_color="#1B6CA8", marker_line_width=0))
        fig.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maîtrise (14/20)")
        fig.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Seuil validé (10/20)")
        fig.update_layout(barmode="group", height=320, margin=dict(t=20,b=20,l=0,r=0),
                          plot_bgcolor="white", paper_bgcolor="white",
                          legend=dict(orientation="h", y=1.1),
                          yaxis=dict(range=[0,20], title="Score /20"),
                          font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Donut niveaux
        niv_counts = df_filtered["Niveau"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=niv_counts.index, values=niv_counts.values,
            hole=0.55,
            marker=dict(colors=["#2E9E6B","#E87C35","#E04E39"]),
            textinfo="label+percent"
        ))
        fig2.update_layout(height=320, margin=dict(t=30,b=10,l=10,r=10),
                           paper_bgcolor="white",
                           annotations=[dict(text=f"{len(df_filtered)}<br>élèves", x=0.5, y=0.5, font_size=14, showarrow=False)],
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter plot progression individuelle
    st.markdown('<div class="section-header">Progression individuelle (scatter)</div>', unsafe_allow_html=True)
    fig3 = px.scatter(df_filtered, x="Pré-test", y="Post-test", color="Genre", hover_name="Nom",
                      size="Progression", size_max=18,
                      color_discrete_map={"Bnat (Filles)":"#D4537E","Drari (Garçons)":"#1B6CA8"},
                      labels={"Pré-test":"Score Pré-test /20","Post-test":"Score Post-test /20"})
    fig3.add_shape(type="line", x0=0, y0=0, x1=20, y1=20, line=dict(dash="dash", color="gray", width=1))
    fig3.add_annotation(x=9, y=8.5, text="Ligne d'égalité", showarrow=False, font=dict(size=10, color="gray"))
    fig3.update_layout(height=350, margin=dict(t=10,b=10,l=0,r=0),
                       plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""<div class="insight-box">
    <b>🔍 Observation clé :</b> Tous les élèves se situent <b>au-dessus de la ligne d'égalité</b>, confirmant une progression
    universelle après la séance de remédiation. La majorité a dépassé le <b>seuil de maîtrise (14/20)</b>.
    Les stratégies de <b>guidage progressif</b> et de <b>correction collective</b> ont eu un impact significatif,
    notamment sur la lecture des axes (+59 pts de taux de maîtrise collectif).
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════ TAB 2 : BNAT VS DRARI ══════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Comparaison filles / garçons</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        means = df.groupby("Genre")[["Pré-test","Post-test"]].mean().reset_index()
        fig = px.bar(means.melt(id_vars="Genre", var_name="Test", value_name="Score"),
                     x="Test", y="Score", color="Genre", barmode="group",
                     color_discrete_map={"Bnat (Filles)":"#D4537E","Drari (Garçons)":"#1B6CA8"},
                     title="Score moyen /20 — Pré vs Post test")
        fig.update_layout(height=300, plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(t=40,b=10,l=0,r=0), yaxis=dict(range=[0,20]))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        prog_genre = df.groupby("Genre")["Prog %"].mean().reset_index()
        fig2 = px.bar(prog_genre, x="Genre", y="Prog %", color="Genre",
                      color_discrete_map={"Bnat (Filles)":"#D4537E","Drari (Garçons)":"#1B6CA8"},
                      title="Taux de progression moyen (%)")
        fig2.update_layout(height=300, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=40,b=10,l=0,r=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Box plot distribution
    fig3 = px.box(df, x="Genre", y="Post-test", color="Genre", points="all",
                  hover_name="Nom",
                  color_discrete_map={"Bnat (Filles)":"#D4537E","Drari (Garçons)":"#1B6CA8"},
                  title="Distribution des scores post-test par genre")
    fig3.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maîtrise")
    fig3.update_layout(height=350, plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(t=40,b=10,l=0,r=0), showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    # Comp par genre radar
    st.markdown('<div class="section-header">Profil de compétences par genre (post-test)</div>', unsafe_allow_html=True)
    comps_short = ["Axes","Variations","Comparaison","Conclusions"]
    fig4 = go.Figure()
    fig4.add_trace(go.Scatterpolar(r=post_comp_f+[post_comp_f[0]], theta=comps_short+[comps_short[0]],
                                   fill='toself', name='Bnat', line_color='#D4537E',
                                   fillcolor='rgba(212,83,126,0.15)'))
    fig4.add_trace(go.Scatterpolar(r=post_comp_g+[post_comp_g[0]], theta=comps_short+[comps_short[0]],
                                   fill='toself', name='Drari', line_color='#1B6CA8',
                                   fillcolor='rgba(27,108,168,0.15)'))
    fig4.update_layout(polar=dict(radialaxis=dict(range=[0,100])),
                       height=380, paper_bgcolor="white",
                       margin=dict(t=30,b=30,l=30,r=30))
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════ TAB 3 : COMPÉTENCES ════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Analyse par compétence ciblée</div>', unsafe_allow_html=True)

    # Progress bars
    cols = st.columns(4)
    colors = ["#1B6CA8","#2E9E6B","#E87C35","#7C5CBF"]
    for i, (comp, pre, post) in enumerate(zip(competences, pre_comp, post_comp)):
        with cols[i]:
            delta = post - pre
            st.metric(label=f"{'🔵' if i==0 else '🟢' if i==1 else '🟠' if i==2 else '🟣'} {comp}",
                      value=f"{post}%", delta=f"+{delta}pts depuis pré-test")
            st.progress(post/100)

    st.markdown("")

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Pré-test", y=competences, x=pre_comp, orientation='h',
                             marker_color="#93C5FD", marker_line_width=0))
        fig.add_trace(go.Bar(name="Post-test", y=competences, x=post_comp, orientation='h',
                             marker_color="#1B6CA8", marker_line_width=0))
        fig.update_layout(barmode="group", height=300, plot_bgcolor="white",
                          paper_bgcolor="white", margin=dict(t=20,b=10,l=0,r=0),
                          xaxis=dict(range=[0,100], title="Taux de maîtrise (%)"),
                          legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Waterfall chart — gain par compétence
        fig2 = go.Figure(go.Waterfall(
            name="Gain", orientation="v",
            x=["Axes","Variations","Comparaison","Conclusions"],
            y=[59, 42, 23, 16],
            connector=dict(line=dict(color="rgb(63, 63, 63)")),
            increasing=dict(marker=dict(color="#2E9E6B")),
            text=["+59%","+42%","+23%","+16%"],
            textposition="outside"
        ))
        fig2.update_layout(title="Gain de maîtrise par compétence (%)",
                           height=300, plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=40,b=10,l=0,r=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Heatmap compétences x genre
    st.markdown('<div class="section-header">Carte thermique — maîtrise par compétence et genre</div>', unsafe_allow_html=True)
    heatmap_data = pd.DataFrame({
        "Fille": post_comp_f,
        "Garçon": post_comp_g
    }, index=competences)
    fig3 = px.imshow(heatmap_data, text_auto=True, aspect="auto",
                     color_continuous_scale="Blues",
                     labels=dict(color="Taux %"),
                     title="Taux de maîtrise post-test (%)")
    fig3.update_layout(height=300, margin=dict(t=40,b=10,l=0,r=0), paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════ TAB 4 : SUIVI ÉLÈVES ════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Tableau de suivi individuel</div>', unsafe_allow_html=True)

    # Search
    search = st.text_input("🔍 Rechercher un élève", placeholder="Tapez un prénom...")
    df_show = df_filtered.copy()
    if search:
        df_show = df_show[df_show["Nom"].str.contains(search, case=False)]

    # Style the dataframe
    def color_niveau(val):
        if val == "Maîtrise": return "background-color: #D1FAE5; color: #065F46"
        if val == "En cours": return "background-color: #FEF3C7; color: #92400E"
        return "background-color: #FEE2E2; color: #991B1B"

    def color_prog(val):
        return "color: #2E9E6B; font-weight: 600" if val > 0 else "color: #E04E39"

    st.dataframe(
        df_show[["Nom","Genre","Pré-test","Post-test","Progression","Prog %","Niveau"]].style
            .map(color_niveau, subset=["Niveau"])
            .map(color_prog, subset=["Progression"])
            .format({"Prog %": "{:.1f}%", "Progression": "+{:.0f} pts"}),
        use_container_width=True, height=450
    )

    st.markdown(f"**{len(df_show)} élève(s) affichés**")

    # Download CSV
    csv = df_show.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Télécharger les données (CSV)", csv, "eleves_ppe.csv", "text/csv")

# ═══════════════════════════ TAB 5 : SIMULATION ══════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">🎮 Simulation pédagogique interactive</div>', unsafe_allow_html=True)
    st.markdown("*Testez l'impact de différentes stratégies pédagogiques sur les résultats*")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("#### ⚙️ Paramètres")
        intensite_guidage = st.slider("Intensité du guidage progressif", 0, 100, 70, step=5)
        travail_groupe = st.slider("Travail en groupes (%)", 0, 100, 60, step=5)
        correction_coll = st.slider("Correction collective (%)", 0, 100, 80, step=5)
        nb_seances = st.slider("Nombre de séances de soutien", 1, 5, 1)
        st.markdown("---")
        st.info(f"**Score estimé moyen :** {min(20, 6.9 + (intensite_guidage*0.05 + travail_groupe*0.03 + correction_coll*0.04)/10 * nb_seances):.1f}/20")

    with c2:
        base = 6.9
        score_simul = []
        for s in range(1, nb_seances+2):
            gain = (intensite_guidage*0.05 + travail_groupe*0.03 + correction_coll*0.04) / 10
            score = min(20, base + gain * s)
            score_simul.append(round(score, 1))

        seances = [f"S{i}" if i > 0 else "Pré" for i in range(nb_seances+1)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=seances, y=score_simul, mode="lines+markers",
                                 line=dict(color="#1B6CA8", width=3),
                                 marker=dict(size=10, color="#1B6CA8"),
                                 fill="tozeroy", fillcolor="rgba(27,108,168,0.1)",
                                 name="Score simulé"))
        fig.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Maîtrise (14/20)")
        fig.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Validé (10/20)")
        fig.update_layout(height=380, plot_bgcolor="white", paper_bgcolor="white",
                          yaxis=dict(range=[0,20], title="Score moyen /20"),
                          xaxis_title="Séances", margin=dict(t=20,b=20,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    # Recommandations automatiques
    st.markdown('<div class="section-header">💡 Recommandations automatiques</div>', unsafe_allow_html=True)
    recs = []
    if intensite_guidage < 50:
        recs.append("⚠️ Augmentez l'intensité du guidage progressif pour mieux soutenir les élèves en difficulté.")
    if travail_groupe < 50:
        recs.append("⚠️ Le travail en groupes favorise l'entraide et la co-construction du savoir — à renforcer.")
    if correction_coll < 60:
        recs.append("⚠️ La correction collective renforce la métacognition et la révision des erreurs.")
    if nb_seances < 2:
        recs.append("💡 Une 2ème séance de soutien permettrait de consolider les acquis, surtout pour les conclusions.")
    if not recs:
        recs.append("✅ Excellent dispositif ! Vos stratégies couvrent toutes les dimensions de la remédiation efficace.")
    for r in recs:
        st.markdown(f"- {r}")

# ═══════════════════════════ TAB 6 : RAPPORT ════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">📋 Synthèse automatique du PPE</div>', unsafe_allow_html=True)

    moy_pre_tot = df["Pré-test"].mean()
    moy_post_tot = df["Post-test"].mean()
    n_maitrise_tot = len(df[df["Niveau"]=="Maîtrise"])
    n_diff_tot = len(df[df["Niveau"]=="Difficultés"])

    rapport = f"""
## Rapport de synthèse — PPE Immunologie 3AC

### 1. Contexte
Ce projet professionnel s'inscrit dans le cadre de la formation initiale des enseignants au **CRMEF**.
Il porte sur la **remédiation des difficultés** rencontrées par les élèves de 3AC dans l'interprétation
des graphes en immunologie.

### 2. Diagnostic initial
- **Effectif concerné :** 32 élèves (16 filles, 16 garçons)
- **Score moyen pré-test :** {moy_pre_tot:.1f}/20
- **Difficultés majeures identifiées :**
  - Lecture des axes (76% des élèves en difficulté)
  - Compréhension des variations (68%)
  - Formulation de conclusions scientifiques (42%)

### 3. Dispositif de remédiation
La séance de soutien s'est appuyée sur trois stratégies complémentaires :
- **Guidage progressif** : décomposition des tâches de lecture graphique
- **Travail en groupes** : 6 groupes hétérogènes favorisant la co-construction
- **Correction collective** : verbalisation des démarches et des erreurs

### 4. Résultats observés
- **Score moyen post-test :** {moy_post_tot:.1f}/20
- **Progression moyenne :** +{moy_post_tot-moy_pre_tot:.1f} points
- **Élèves en maîtrise (>14/20) :** {n_maitrise_tot}/32 ({int(n_maitrise_tot/32*100)}%)
- **Élèves encore en difficulté :** {n_diff_tot}/32

### 5. Analyse par genre
| | Pré-test | Post-test | Progression |
|---|---|---|---|
| 
 (Filles) | {pd.concat([df_f])['Pré-test'].mean():.1f}/20 | {pd.concat([df_f])['Post-test'].mean():.1f}/20 | +{pd.concat([df_f])['Post-test'].mean()-pd.concat([df_f])['Pré-test'].mean():.1f} pts |
|  (Garçons) | {pd.concat([df_g])['Pré-test'].mean():.1f}/20 | {pd.concat([df_g])['Post-test'].mean():.1f}/20 | +{pd.concat([df_g])['Post-test'].mean()-pd.concat([df_g])['Pré-test'].mean():.1f} pts |

### 6. Compétence la plus améliorée
📈 **Lecture des axes** : de 24% → 83% de maîtrise (+59 points)

### 7. Compétence à consolider
⚠️ **Formulation de conclusions** : 58% de maîtrise — nécessite des séances supplémentaires

### 8. Recommandations pédagogiques
1. Prévoir une 2ème séance focalisée sur la **formulation de conclusions argumentées**
2. Utiliser des supports visuels progressifs (courbes annotées, fléchage des variations)
3. Intégrer l'évaluation formative continue pour suivre la progression individuelle
4. Valoriser les productions des groupes lors de la correction collective
    """

    st.markdown(rapport)
    st.download_button("⬇️ Télécharger le rapport (MD)", rapport.encode(), "rapport_ppe.md", "text/markdown")
