import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(
    page_title="PPE – Remédiation Immunologie 3AC",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans Arabic', sans-serif; }
.main { background-color: #F8F9FB; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F4C75 0%, #1B6CA8 100%); }
[data-testid="stSidebar"] * { color: white !important; }
.kpi-card { background: white; border-radius: 12px; padding: 20px 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); border-left: 4px solid #1B6CA8; margin-bottom: 8px; }
.kpi-card.green  { border-left-color: #2E9E6B; }
.kpi-card.orange { border-left-color: #E87C35; }
.kpi-card.purple { border-left-color: #7C5CBF; }
.kpi-value  { font-size: 2rem; font-weight: 600; color: #1a1a2e; margin: 0; }
.kpi-label  { font-size: 0.78rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.kpi-delta  { font-size: 0.82rem; margin-top: 4px; }
.delta-up   { color: #2E9E6B; }
.delta-down { color: #E04E39; }
.section-header { font-size: 1rem; font-weight: 600; color: #1a1a2e; border-bottom: 2px solid #E5E7EB; padding-bottom: 8px; margin-bottom: 16px; margin-top: 8px; }
.insight-box { background: #EEF4FF; border-radius: 10px; border-left: 4px solid #1B6CA8; padding: 14px 18px; font-size: 0.88rem; color: #374151; line-height: 1.7; }
.insight-box b { color: #1B6CA8; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #F3F4F6; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 500; color: #6B7280; }
.stTabs [aria-selected="true"] { background: white !important; color: #1B6CA8 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
prenoms_filles  = ["Amina","Fatima","Nadia","Sara","Houda","Zineb","Maryam","Hajar",
                   "Layla","Rim","Chaimae","Samira","Loubna","Hiba","Asma","Siham"]
prenoms_garcons = ["Khalid","Youssef","Hassan","Amine","Mehdi","Bilal","Adil","Omar",
                   "Soufiane","Othmane","Ilias","Anass","Hamza","Saad","Rayan","Zakaria"]

pre_f  = [5,7,8,6,8,6,9,7,6,5,8,6,5,7,8,6]
post_f = [15,15,16,13,16,14,17,15,13,12,16,14,8,9,16,13]
pre_g  = [6,8,5,7,7,5,8,6,6,7,9,7,8,6,8,7]
post_g = [14,16,7,14,15,12,16,8,13,14,17,14,9,12,15,13]

df_f = pd.DataFrame({"Nom": prenoms_filles,  "Genre": "Filles",  "Pré-test": pre_f,  "Post-test": post_f})
df_g = pd.DataFrame({"Nom": prenoms_garcons, "Genre": "Garçons", "Pré-test": pre_g,  "Post-test": post_g})
df   = pd.concat([df_f, df_g], ignore_index=True)
df["Progression"] = df["Post-test"] - df["Pré-test"]
df["Prog %"]      = (df["Progression"] / df["Pré-test"] * 100).round(1)

def get_niveau(s):
    if s > 14: return "Maîtrise"
    if s >= 10: return "En cours"
    return "Difficultés"

df["Niveau"] = df["Post-test"].apply(get_niveau)

competences = ["Lecture des axes","Compréhension des variations","Comparaison de courbes","Formulation de conclusions"]
pre_comp    = [24, 32, 45, 42]
post_comp   = [83, 74, 68, 58]
post_comp_f = [86, 76, 70, 62]
post_comp_g = [80, 72, 66, 54]

COLOR_MAP = {"Filles": "#E04E39", "Garçons": "#1B6CA8"}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 PPE – CRMEF")
    st.markdown("**Remédiation Immunologie**  \n3ème Année Collège · 3AC")
    st.markdown("---")
    st.markdown("### ⚙️ Filtres")
    filtre_genre  = st.radio("Genre",  ["Tous", "Filles", "Garçons"], index=0, horizontal=True)
    filtre_niveau = st.radio("Niveau", ["Tous", "Maîtrise", "En cours", "Difficultés"], index=0, horizontal=False)
    st.markdown("---")
    st.markdown("### 📋 Infos séance")
    st.info("📅 Séance de soutien pédagogique  \n👥 6 groupes collaboratifs  \n🧠 Guidage progressif  \n✅ Correction collective")
    st.caption("Projet Professionnel Étudiant · Formation initiale enseignants")

df_filtered = df.copy()
if filtre_genre and filtre_genre != "Tous": df_filtered = df_filtered[df_filtered["Genre"] == filtre_genre]
if filtre_niveau and filtre_niveau != "Tous": df_filtered = df_filtered[df_filtered["Niveau"] == filtre_niveau]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🔬 Tableau de bord – Projet Professionnel de l'Étudiant")
st.markdown("**Remédiation des difficultés en lecture des graphes immunologiques** · 3AC · CRMEF")
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
moy_pre    = df_filtered["Pré-test"].mean()    if len(df_filtered)>0 else 0
moy_post   = df_filtered["Post-test"].mean()   if len(df_filtered)>0 else 0
prog_moy   = df_filtered["Progression"].mean() if len(df_filtered)>0 else 0
n_maitrise = len(df_filtered[df_filtered["Niveau"]=="Maîtrise"])
pct        = int(n_maitrise/len(df_filtered)*100) if len(df_filtered)>0 else 0

with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">👥 Effectif total</div><div class="kpi-value">{len(df_filtered)}</div><div class="kpi-delta">sur 32 élèves</div></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="kpi-card orange"><div class="kpi-label">📉 Moy. Pré-test</div><div class="kpi-value">{moy_pre:.1f}/20</div><div class="kpi-delta delta-down">Avant remédiation</div></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="kpi-card green"><div class="kpi-label">📈 Moy. Post-test</div><div class="kpi-value">{moy_post:.1f}/20</div><div class="kpi-delta delta-up">Après remédiation</div></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">🚀 Progression moy.</div><div class="kpi-value">+{prog_moy:.1f} pts</div><div class="kpi-delta delta-up">↑ amélioration nette</div></div>', unsafe_allow_html=True)
with k5: st.markdown(f'<div class="kpi-card purple"><div class="kpi-label">🏆 Taux de maîtrise</div><div class="kpi-value">{pct}%</div><div class="kpi-delta delta-up">{n_maitrise} élèves</div></div>', unsafe_allow_html=True)

st.markdown("")

tabs = st.tabs(["📊 Vue Globale","📅 3 Séances","⚖️ Filles vs Garçons","🎯 Compétences","🔬 Analyses Avancées","👥 Suivi Élèves","📈 Simulation","📋 Rapport PDF"])

# ══ TAB 1 ════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Évolution globale pré-test → post-test</div>', unsafe_allow_html=True)
    if len(df_filtered)==0:
        st.warning("Aucun élève ne correspond aux filtres sélectionnés.")
    else:
        c1,c2 = st.columns([3,2])
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Pré-test",  x=df_filtered["Nom"], y=df_filtered["Pré-test"],  marker_color="#93C5FD", marker_line_width=0))
            fig.add_trace(go.Bar(name="Post-test", x=df_filtered["Nom"], y=df_filtered["Post-test"], marker_color="#1B6CA8", marker_line_width=0))
            fig.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maîtrise (14/20)")
            fig.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Seuil validé (10/20)")
            fig.update_layout(barmode="group", height=320, margin=dict(t=20,b=20,l=0,r=0), plot_bgcolor="white", paper_bgcolor="white", legend=dict(orientation="h",y=1.1), yaxis=dict(range=[0,20],title="Score /20"), font=dict(size=11))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            niv_counts = df_filtered["Niveau"].value_counts()
            fig2 = go.Figure(go.Pie(labels=niv_counts.index, values=niv_counts.values, hole=0.55, marker=dict(colors=["#2E9E6B","#E87C35","#E04E39"]), textinfo="label+percent"))
            fig2.update_layout(height=320, margin=dict(t=30,b=10,l=10,r=10), paper_bgcolor="white", annotations=[dict(text=f"{len(df_filtered)}<br>élèves",x=0.5,y=0.5,font_size=14,showarrow=False)], showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="section-header">Progression individuelle (scatter)</div>', unsafe_allow_html=True)
        fig3 = px.scatter(df_filtered, x="Pré-test", y="Post-test", color="Genre", hover_name="Nom", size="Progression", size_max=18, color_discrete_map=COLOR_MAP, labels={"Pré-test":"Score Pré-test /20","Post-test":"Score Post-test /20"})
        fig3.add_shape(type="line", x0=0,y0=0,x1=20,y1=20, line=dict(dash="dash",color="gray",width=1))
        fig3.add_annotation(x=9,y=8.5,text="Ligne d'égalité",showarrow=False,font=dict(size=10,color="gray"))
        fig3.update_layout(height=350, margin=dict(t=10,b=10,l=0,r=0), plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<div class="insight-box"><b>🔍 Observation clé :</b> Tous les élèves se situent <b>au-dessus de la ligne d\'égalité</b>, confirmant une progression universelle. La majorité a dépassé le <b>seuil de maîtrise (14/20)</b>.</div>', unsafe_allow_html=True)

# ══ TAB SUIVI 3 SÉANCES ══════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">📅 Évolution sur 3 séances de remédiation</div>', unsafe_allow_html=True)

    # ── Data 3 séances ────────────────────────────────────────────────────────
    seances_labels = ["Pré-test", "Séance 1", "Séance 2", "Séance 3"]

    maitrise_s = [0,   0,  8, 24]
    encours_s  = [2,   2, 20,  5]
    diff_s     = [30, 30,  4,  3]
    scores_s   = [6.8, 7.8, 12.7, 14.9]
    scores_f_s = [6.9, 8.0, 13.0, 15.2]
    scores_g_s = [6.7, 7.6, 12.4, 14.6]

    import numpy as np
    # Scores réalistes par séance — progression graduelle avec quelques élèves en difficulté
    scores_par_seance = {
        "Pré-test": df["Pré-test"].tolist(),
        "Séance 1": [5,8,9,7,9,7,10,8,7,6,9,7,6,8,9,7,  7,9,6,8,8,6,9,8,7,9,10,8,9,7,9,8],
        "Séance 2": [13,14,15,12,15,13,16,14,12,11,15,13,7,8,15,12,  13,15,9,13,14,11,15,13,7,14,15,11,14,11,14,12],
        "Séance 3": [16,17,18,15,17,16,18,16,15,14,17,15,8,9,17,15,  16,17,11,15,16,14,17,15,7,16,17,14,16,12,16,15],
    }

    # ── Selector séance ───────────────────────────────────────────────────────
    st.markdown("### 🎯 Sélectionnez une séance pour voir les détails")
    col_btns = st.columns(4)
    seance_noms = ["Pré-test", "Séance 1", "Séance 2", "Séance 3"]
    seance_icons = ["📋", "1️⃣", "2️⃣", "3️⃣"]
    seance_colors = ["#6B7280", "#E87C35", "#1B6CA8", "#2E9E6B"]

    selected_seance = st.session_state.get("selected_seance", "Séance 1")

    for i, (nom, icon) in enumerate(zip(seance_noms, seance_icons)):
        with col_btns[i]:
            if st.button(f"{icon} {nom}", key=f"btn_{i}", use_container_width=True,
                         type="primary" if selected_seance == nom else "secondary"):
                st.session_state["selected_seance"] = nom
                st.rerun()

    selected_seance = st.session_state.get("selected_seance", "Séance 1")
    idx = seance_noms.index(selected_seance)
    scores_sel = scores_par_seance[selected_seance]

    def get_niveau_s(s):
        if s > 14: return "Maîtrise"
        if s >= 10: return "En cours"
        return "Difficultés"

    niveaux_sel = [get_niveau_s(s) for s in scores_sel]
    n_mait = niveaux_sel.count("Maîtrise")
    n_enc  = niveaux_sel.count("En cours")
    n_dif  = niveaux_sel.count("Difficultés")
    moy_sel = round(sum(scores_sel)/len(scores_sel), 1)

    st.markdown("---")
    color_sel = seance_colors[idx]
    st.markdown(f"## {seance_icons[idx]} Résultats — {selected_seance}", unsafe_allow_html=False)

    # ── KPIs de la séance sélectionnée ───────────────────────────────────────
    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card" style="border-left-color:{color_sel}"><div class="kpi-label">📊 Score moyen</div><div class="kpi-value">{moy_sel}/20</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card green"><div class="kpi-label">🟢 Maîtrise</div><div class="kpi-value">{n_mait}</div><div class="kpi-delta delta-up">{int(n_mait/32*100)}% des élèves</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card orange"><div class="kpi-label">🟡 En cours</div><div class="kpi-value">{n_enc}</div><div class="kpi-delta">{int(n_enc/32*100)}% des élèves</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card" style="border-left-color:#E04E39"><div class="kpi-label">🔴 Difficultés</div><div class="kpi-value">{n_dif}</div><div class="kpi-delta delta-down">{int(n_dif/32*100)}% des élèves</div></div>', unsafe_allow_html=True)
    with k5:
        delta_vs_pre = round(moy_sel - scores_s[0], 1)
        sign = "+" if delta_vs_pre >= 0 else ""
        st.markdown(f'<div class="kpi-card purple"><div class="kpi-label">🚀 vs Pré-test</div><div class="kpi-value">{sign}{delta_vs_pre}</div><div class="kpi-delta delta-up">progression</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # ── Graphes de la séance ──────────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        # Donut niveaux séance
        fig_pie = go.Figure(go.Pie(
            labels=["🟢 Maîtrise", "🟡 En cours", "🔴 Difficultés"],
            values=[n_mait, n_enc, n_dif],
            hole=0.55,
            marker=dict(colors=["#2E9E6B","#E87C35","#E04E39"]),
            textinfo="label+value+percent"
        ))
        fig_pie.update_layout(
            title=f"Répartition niveaux — {selected_seance}",
            height=320, paper_bgcolor="white",
            annotations=[dict(text=f"{int(n_mait/32*100)}%<br>maîtrise", x=0.5,y=0.5,font_size=13,showarrow=False)],
            showlegend=False, margin=dict(t=40,b=10,l=10,r=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        # Bar scores individuels colorés par niveau
        colors_ind = ["#2E9E6B" if s>14 else "#E87C35" if s>=10 else "#E04E39" for s in scores_sel]
        fig_ind = go.Figure(go.Bar(
            x=df["Nom"], y=scores_sel,
            marker_color=colors_ind, marker_line_width=0,
            text=[f"{int(s)}" for s in scores_sel], textposition="outside"
        ))
        fig_ind.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Maîtrise")
        fig_ind.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Validé")
        fig_ind.update_layout(
            title=f"Scores individuels — {selected_seance}",
            height=320, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(range=[0,23], title="Score /20"),
            margin=dict(t=40,b=20,l=0,r=0), font=dict(size=10)
        )
        st.plotly_chart(fig_ind, use_container_width=True)

    # ── Évolution globale toutes séances ─────────────────────────────────────
    st.markdown('<div class="section-header">Evolution sur toutes les seances</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=seances_labels, y=scores_f_s, mode="lines+markers+text",
            name="Filles", line=dict(color="#E04E39", width=3),
            marker=dict(size=10, symbol="circle"),
            text=[f"{v}" for v in scores_f_s], textposition="top center"
        ))
        fig_line.add_trace(go.Scatter(
            x=seances_labels, y=scores_g_s, mode="lines+markers+text",
            name="Garçons", line=dict(color="#1B6CA8", width=3),
            marker=dict(size=10, symbol="circle"),
            text=[f"{v}" for v in scores_g_s], textposition="bottom center"
        ))
        # Marquer la séance sélectionnée avec un marker plus grand
        fig_line.add_trace(go.Scatter(
            x=[selected_seance], y=[scores_f_s[idx]],
            mode="markers", marker=dict(size=18, color=color_sel, symbol="star"),
            showlegend=False, name=""
        ))
        fig_line.add_hrect(y0=14, y1=21, fillcolor="rgba(46,158,107,0.08)", line_width=0)
        fig_line.add_hrect(y0=10, y1=14, fillcolor="rgba(232,124,53,0.06)", line_width=0)
        fig_line.add_hrect(y0=0,  y1=10, fillcolor="rgba(224,78,57,0.06)",  line_width=0)
        fig_line.update_layout(
            title="Évolution score moyen /20",
            height=340, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(range=[0,21], title="Score /20"),
            legend=dict(orientation="h", y=1.12),
            margin=dict(t=60,b=10,l=0,r=80)
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(name="🔴 Difficultés", x=seances_labels, y=diff_s,
                                   marker_color="#E04E39", marker_line_width=0,
                                   text=diff_s, textposition="inside", textfont=dict(color="white",size=12)))
        fig_stack.add_trace(go.Bar(name="🟡 En cours", x=seances_labels, y=encours_s,
                                   marker_color="#E87C35", marker_line_width=0,
                                   text=encours_s, textposition="inside", textfont=dict(color="white",size=12)))
        fig_stack.add_trace(go.Bar(name="🟢 Maîtrise", x=seances_labels, y=maitrise_s,
                                   marker_color="#2E9E6B", marker_line_width=0,
                                   text=maitrise_s, textposition="inside", textfont=dict(color="white",size=12)))

        fig_stack.update_layout(
            title="Répartition niveaux par séance",
            barmode="stack", height=340,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(range=[0,35], title="Nombre d'élèves"),
            legend=dict(orientation="h", y=1.12),
            margin=dict(t=60,b=10,l=0,r=0)
        )
        st.plotly_chart(fig_stack, use_container_width=True)

    # ── Heatmap individuelle ──────────────────────────────────────────────────
    df_heat = pd.DataFrame({
        "Pré-test": scores_par_seance["Pré-test"],
        "Séance 1": scores_par_seance["Séance 1"],
        "Séance 2": scores_par_seance["Séance 2"],
        "Séance 3": scores_par_seance["Séance 3"],
    }, index=df["Nom"]).T

    fig_heat = px.imshow(
        df_heat, text_auto=True, aspect="auto",
        color_continuous_scale=[[0,"#FEE2E2"],[0.5,"#FEF3C7"],[0.75,"#D1FAE5"],[1,"#065F46"]],
        zmin=0, zmax=20,
        labels=dict(color="Score /20"),
        title="🗺️ Carte de chaleur — progression individuelle (Rouge→Vert)"
    )
    fig_heat.update_layout(height=280, margin=dict(t=40,b=10,l=0,r=0), paper_bgcolor="white")
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<div class="insight-box"><b>Comment lire :</b> Rouge = difficultes · Jaune = en cours · Vert = maitrise. Chaque ligne = une seance · Chaque colonne = un eleve.</div>', unsafe_allow_html=True)



# ══ TAB FILLES VS GARCONS ═════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Comparaison Filles / Garcons</div>', unsafe_allow_html=True)

    moy_pre_f2  = df_f["Pré-test"].mean()
    moy_post_f2 = df_f["Post-test"].mean()
    moy_pre_g2  = df_g["Pré-test"].mean()
    moy_post_g2 = df_g["Post-test"].mean()

    mf1,mf2,mg1,mg2 = st.columns(4)
    with mf1: st.markdown(f'<div class="kpi-card" style="border-left-color:#E04E39"><div class="kpi-label">Filles - Pre-test</div><div class="kpi-value">{moy_pre_f2:.1f}/20</div></div>', unsafe_allow_html=True)
    with mf2: st.markdown(f'<div class="kpi-card green" style="border-left-color:#E04E39"><div class="kpi-label">Filles - Post-test</div><div class="kpi-value">{moy_post_f2:.1f}/20</div><div class="kpi-delta delta-up">+{moy_post_f2-moy_pre_f2:.1f} pts</div></div>', unsafe_allow_html=True)
    with mg1: st.markdown(f'<div class="kpi-card" style="border-left-color:#1B6CA8"><div class="kpi-label">Garcons - Pre-test</div><div class="kpi-value">{moy_pre_g2:.1f}/20</div></div>', unsafe_allow_html=True)
    with mg2: st.markdown(f'<div class="kpi-card green" style="border-left-color:#1B6CA8"><div class="kpi-label">Garcons - Post-test</div><div class="kpi-value">{moy_post_g2:.1f}/20</div><div class="kpi-delta delta-up">+{moy_post_g2-moy_pre_g2:.1f} pts</div></div>', unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        fig_ev = go.Figure()
        cats = ["Pre-test", "Post-test"]
        vals_f = [moy_pre_f2, moy_post_f2]
        vals_g = [moy_pre_g2, moy_post_g2]
        fig_ev.add_trace(go.Bar(name="Filles",  x=cats, y=vals_f, marker_color="#E04E39", marker_line_width=0, text=[f"{v:.1f}" for v in vals_f], textposition="outside"))
        fig_ev.add_trace(go.Bar(name="Garcons", x=cats, y=vals_g, marker_color="#1B6CA8", marker_line_width=0, text=[f"{v:.1f}" for v in vals_g], textposition="outside"))
        fig_ev.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maitrise")
        fig_ev.update_layout(title="Evolution scores moyens /20", barmode="group", height=320,
                             plot_bgcolor="white", paper_bgcolor="white",
                             yaxis=dict(range=[0,22], title="Score /20"),
                             legend=dict(orientation="h", y=1.15),
                             margin=dict(t=50,b=10,l=0,r=0))
        st.plotly_chart(fig_ev, use_container_width=True)

    with c2:
        prog_f2 = round((moy_post_f2 - moy_pre_f2) / moy_pre_f2 * 100, 1)
        prog_g2 = round((moy_post_g2 - moy_pre_g2) / moy_pre_g2 * 100, 1)
        fig_prog = go.Figure()
        fig_prog.add_trace(go.Bar(name="Filles",  y=["Filles"],  x=[prog_f2], orientation="h", marker_color="#E04E39", marker_line_width=0, text=[f"+{prog_f2}%"], textposition="outside"))
        fig_prog.add_trace(go.Bar(name="Garcons", y=["Garcons"], x=[prog_g2], orientation="h", marker_color="#1B6CA8", marker_line_width=0, text=[f"+{prog_g2}%"], textposition="outside"))
        fig_prog.update_layout(title="Taux de progression (%)", barmode="group", height=320,
                               plot_bgcolor="white", paper_bgcolor="white",
                               xaxis=dict(range=[0,130]),
                               showlegend=False, margin=dict(t=50,b=10,l=10,r=60))
        st.plotly_chart(fig_prog, use_container_width=True)

    fig_violin = go.Figure()
    fig_violin.add_trace(go.Violin(x=df[df["Genre"]=="Filles"]["Genre"], y=df[df["Genre"]=="Filles"]["Post-test"],
        name="Filles", fillcolor="rgba(224,78,57,0.3)", line_color="#E04E39",
        meanline_visible=True, points="all", pointpos=-0.5, jitter=0.3, marker=dict(color="#E04E39",size=7)))
    fig_violin.add_trace(go.Violin(x=df[df["Genre"]=="Garçons"]["Genre"], y=df[df["Genre"]=="Garçons"]["Post-test"],
        name="Garcons", fillcolor="rgba(27,108,168,0.3)", line_color="#1B6CA8",
        meanline_visible=True, points="all", pointpos=0.5, jitter=0.3, marker=dict(color="#1B6CA8",size=7)))
    fig_violin.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maitrise (14/20)", annotation_position="right")
    fig_violin.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Seuil valide (10/20)", annotation_position="right")
    fig_violin.update_layout(title="Distribution des scores post-test (Violin plot)",
        height=380, plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(range=[0,20], title="Score post-test /20"),
        showlegend=False, margin=dict(t=50,b=10,l=0,r=120))
    st.plotly_chart(fig_violin, use_container_width=True)

    comps_short = ["Axes","Variations","Comparaison","Conclusions"]
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name="Filles",  x=comps_short, y=post_comp_f, marker_color="#E04E39", marker_line_width=0, text=[f"{v}%" for v in post_comp_f], textposition="outside"))
    fig_comp.add_trace(go.Bar(name="Garcons", x=comps_short, y=post_comp_g, marker_color="#1B6CA8", marker_line_width=0, text=[f"{v}%" for v in post_comp_g], textposition="outside"))
    fig_comp.add_hline(y=70, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil 70%")
    fig_comp.update_layout(title="Taux de maitrise par competence - Filles vs Garcons",
        barmode="group", height=380, plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(range=[0,110], title="Taux de maitrise (%)"),
        legend=dict(orientation="h", y=1.12), margin=dict(t=60,b=10,l=0,r=0))
    st.plotly_chart(fig_comp, use_container_width=True)

    winner = "Filles" if moy_post_f2 > moy_post_g2 else "Garcons"
    diff_s2 = abs(moy_post_f2 - moy_post_g2)
    st.markdown(f'<div class="insight-box"><b>Analyse :</b> Les <b>{winner}</b> ont obtenu un score moyen plus eleve au post-test (<b>{max(moy_post_f2,moy_post_g2):.1f}/20</b> vs <b>{min(moy_post_f2,moy_post_g2):.1f}/20</b>). Les deux groupes montrent une <b>progression significative</b> apres la remediation.</div>', unsafe_allow_html=True)

# ══ TAB 3 ════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Analyse par compétence ciblée</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    icons = ["🔵","🟢","🟠","🟣"]
    for i,(comp,pre,post) in enumerate(zip(competences,pre_comp,post_comp)):
        with cols[i]:
            st.metric(label=f"{icons[i]} {comp}", value=f"{post}%", delta=f"+{post-pre}pts")
            st.progress(post/100)
    st.markdown("")
    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Pré-test", y=competences,x=pre_comp, orientation='h',marker_color="#93C5FD",marker_line_width=0))
        fig.add_trace(go.Bar(name="Post-test",y=competences,x=post_comp,orientation='h',marker_color="#1B6CA8",marker_line_width=0))
        fig.update_layout(barmode="group",height=300,plot_bgcolor="white",paper_bgcolor="white",margin=dict(t=20,b=10,l=0,r=0),xaxis=dict(range=[0,100],title="Taux de maîtrise (%)"),legend=dict(orientation="h",y=1.1))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = go.Figure(go.Waterfall(name="Gain",orientation="v",x=["Axes","Variations","Comparaison","Conclusions"],y=[59,42,23,16],connector=dict(line=dict(color="rgb(63,63,63)")),increasing=dict(marker=dict(color="#2E9E6B")),text=["+59%","+42%","+23%","+16%"],textposition="outside"))
        fig2.update_layout(title="Gain de maîtrise (%)",height=300,plot_bgcolor="white",paper_bgcolor="white",margin=dict(t=40,b=10,l=0,r=0),showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    heatmap_data = pd.DataFrame({"Filles":post_comp_f,"Garçons":post_comp_g},index=competences)
    fig3 = px.imshow(heatmap_data,text_auto=True,aspect="auto",color_continuous_scale="Blues",labels=dict(color="Taux %"),title="Carte thermique — maîtrise par genre (%)")
    fig3.update_layout(height=300,margin=dict(t=40,b=10,l=0,r=0),paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

# ══ TAB ANALYSES AVANCÉES ═════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Analyses Avancees - Comparaisons Multiples</div>', unsafe_allow_html=True)

    seances_labels_a = ["Pré-test", "Séance 1", "Séance 2", "Séance 3"]
    scores_f_evol = [6.9, 8.0, 13.0, 15.2]
    scores_g_evol = [6.7, 7.6, 12.4, 14.6]

    # ── Graphe 1 : Comparaison Filles vs Garçons par séance (grouped bar) ────
    st.markdown("### 1. Comparaison Filles vs Garçons - Score moyen par séance")
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="Filles", x=seances_labels_a, y=scores_f_evol,
                          marker_color="#E04E39", marker_line_width=0,
                          text=[f"{v}" for v in scores_f_evol], textposition="outside"))
    fig1.add_trace(go.Bar(name="Garçons", x=seances_labels_a, y=scores_g_evol,
                          marker_color="#1B6CA8", marker_line_width=0,
                          text=[f"{v}" for v in scores_g_evol], textposition="outside"))
    fig1.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maitrise (14)")
    fig1.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Seuil valide (10)")
    fig1.update_layout(barmode="group", height=380, plot_bgcolor="white", paper_bgcolor="white",
                       yaxis=dict(range=[0,20], title="Score moyen /20"),
                       legend=dict(orientation="h", y=1.12), margin=dict(t=30,b=10,l=0,r=0))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Commentaire :</b> Les filles partent avec un score legerement superieur (6.9 vs 6.7) et conservent cette avance jusqu\'a la seance 3 (15.2 vs 14.6). L\'ecart reste stable (environ 0.6 a 0.7 point) tout au long du dispositif, ce qui indique que la remediation a profite de maniere comparable aux deux groupes, sans creuser ni combler l\'ecart initial.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphe 2 : Ecart Filles-Garçons par séance ───────────────────────────
    st.markdown("### 2. Evolution de l'ecart Filles - Garçons")
    ecarts = [round(f-g,1) for f,g in zip(scores_f_evol, scores_g_evol)]
    fig2 = go.Figure(go.Bar(
        x=seances_labels_a, y=ecarts,
        marker_color=["#9CA3AF" if e==0 else "#E04E39" if e>0 else "#1B6CA8" for e in ecarts],
        text=[f"+{e}" if e>0 else f"{e}" for e in ecarts], textposition="outside"
    ))
    fig2.add_hline(y=0, line_color="#374151", line_width=1)
    fig2.update_layout(title="Ecart (Filles - Garçons) en points sur 20", height=320,
                       plot_bgcolor="white", paper_bgcolor="white",
                       yaxis=dict(range=[-0.5,1], title="Ecart (pts)"),
                       showlegend=False, margin=dict(t=40,b=10,l=0,r=0))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Commentaire :</b> L\'ecart entre filles et garcons reste positif (en faveur des filles) sur toutes les seances, avec une moyenne d\'environ +0.5 point. Cet ecart est faible et ne traduit pas une difference pedagogique significative entre les deux groupes ; il peut s\'expliquer par des facteurs individuels plutot que par le genre.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphe 3 : Nombre d'élèves par niveau et par séance (grouped bar) ────
    st.markdown("### 3. Nombre d'eleves par niveau a chaque seance")
    maitrise_a = [0, 0, 8, 24]
    encours_a  = [2, 2, 20, 5]
    diff_a     = [30, 30, 4, 3]

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Difficultés", x=seances_labels_a, y=diff_a,
                          marker_color="#E04E39", marker_line_width=0,
                          text=diff_a, textposition="outside"))
    fig3.add_trace(go.Bar(name="En cours", x=seances_labels_a, y=encours_a,
                          marker_color="#E87C35", marker_line_width=0,
                          text=encours_a, textposition="outside"))
    fig3.add_trace(go.Bar(name="Maîtrise", x=seances_labels_a, y=maitrise_a,
                          marker_color="#2E9E6B", marker_line_width=0,
                          text=maitrise_a, textposition="outside"))
    fig3.update_layout(title="Nombre d'eleves par niveau (barres groupees)", barmode="group", height=380,
                       plot_bgcolor="white", paper_bgcolor="white",
                       yaxis=dict(range=[0,35], title="Nombre d'eleves"),
                       legend=dict(orientation="h", y=1.12), margin=dict(t=40,b=10,l=0,r=0))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Commentaire :</b> Cette vue en barres groupees met en evidence le basculement progressif : le groupe "Difficultes" (rouge) domine au pre-test et a la seance 1 (30 eleves), puis s\'effondre a partir de la seance 2 (4 eleves) et la seance 3 (3 eleves). Inversement, le groupe "Maitrise" (vert) passe de 0 a 24 eleves entre le pre-test et la seance 3, illustrant une transformation radicale de la repartition des niveaux.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphe 4 : Distribution complète des scores - tous élèves toutes séances (box plot multi) ──
    st.markdown("### 4. Distribution des scores - tous les eleves, toutes les seances")

    import numpy as np
    scores_par_seance_a = {
        "Pré-test": df["Pré-test"].tolist(),
        "Séance 1": [5,8,9,7,9,7,10,8,7,6,9,7,6,8,9,7,  7,9,6,8,8,6,9,8,7,9,10,8,9,7,9,8],
        "Séance 2": [13,14,15,12,15,13,16,14,12,11,15,13,7,8,15,12,  13,15,9,13,14,11,15,13,7,14,15,11,14,11,14,12],
        "Séance 3": [16,17,18,15,17,16,18,16,15,14,17,15,8,9,17,15,  16,17,11,15,16,14,17,15,7,16,17,14,16,12,16,15],
    }

    fig4 = go.Figure()
    box_colors = ["#9CA3AF", "#E87C35", "#1B6CA8", "#2E9E6B"]
    for i, (label, scores) in enumerate(scores_par_seance_a.items()):
        fig4.add_trace(go.Box(
            y=scores, name=label, marker_color=box_colors[i],
            boxmean=True, boxpoints="all", jitter=0.4, pointpos=-1.8,
            marker=dict(size=5, opacity=0.6)
        ))
    fig4.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maitrise")
    fig4.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Seuil valide")
    fig4.update_layout(title="Box plot - distribution des 32 eleves par seance", height=420,
                       plot_bgcolor="white", paper_bgcolor="white",
                       yaxis=dict(range=[0,20], title="Score /20"),
                       showlegend=False, margin=dict(t=40,b=10,l=0,r=0))
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Commentaire :</b> Le box plot montre une nette translation vers le haut de toute la distribution au fil des seances : la mediane passe d\'environ 6.5 (pre-test) a 15.5 (seance 3), et l\'ecart-type (taille de la boite) diminue legerement, signe d\'une homogeneisation progressive du niveau de la classe. Quelques points isoles sous le seuil de 10 restent visibles meme a la seance 3, correspondant aux 3 eleves toujours en difficulte.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphe 5 : Spaghetti plot - trajectoire de chaque élève ──────────────
    st.markdown("### 5. Trajectoire individuelle de chaque eleve sur les 3 seances")

    fig5 = go.Figure()
    for i, nom in enumerate(df["Nom"]):
        genre = df.iloc[i]["Genre"]
        traj = [scores_par_seance_a["Pré-test"][i], scores_par_seance_a["Séance 1"][i],
                scores_par_seance_a["Séance 2"][i], scores_par_seance_a["Séance 3"][i]]
        color = "#E04E39" if genre=="Filles" else "#1B6CA8"
        fig5.add_trace(go.Scatter(
            x=seances_labels_a, y=traj, mode="lines",
            line=dict(color=color, width=1.2),
            opacity=0.35, showlegend=False, hovertext=nom,
            hoverinfo="text+y"
        ))
    # Moyenne générale en gras
    moy_traj = [6.8, 7.8, 12.7, 14.9]
    fig5.add_trace(go.Scatter(x=seances_labels_a, y=moy_traj, mode="lines+markers",
                              line=dict(color="#1A1A1A", width=4), marker=dict(size=10),
                              name="Moyenne classe"))
    fig5.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Maitrise")
    fig5.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Valide")
    fig5.update_layout(title="Trajectoires individuelles (rouge=filles, bleu=garcons, noir=moyenne)",
                       height=420, plot_bgcolor="white", paper_bgcolor="white",
                       yaxis=dict(range=[0,20], title="Score /20"),
                       showlegend=True, margin=dict(t=40,b=10,l=0,r=0))
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Commentaire :</b> Ce graphique "spaghetti" montre la trajectoire individuelle de chacun des 32 eleves. La grande majorite des lignes suivent une pente ascendante reguliere, parallele a la courbe moyenne (en noir). Quelques lignes restent proches du bas (eleves en difficulte persistante), mais aucune ligne ne redescend : la progression est universelle, meme si son ampleur varie d\'un eleve a l\'autre.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphe 6 : Scatter pré-test vs gain total (qui a le plus progressé) ──
    st.markdown("### 6. Qui a le plus progresse ? Score initial vs gain total")

    gain_total = [s3-s0 for s0,s3 in zip(scores_par_seance_a["Pré-test"], scores_par_seance_a["Séance 3"])]
    fig6 = px.scatter(
        x=scores_par_seance_a["Pré-test"], y=gain_total,
        color=df["Genre"], hover_name=df["Nom"],
        color_discrete_map={"Filles":"#E04E39","Garçons":"#1B6CA8"},
        labels={"x":"Score Pré-test /20", "y":"Gain total (Séance 3 - Pré-test)"},
        size=[10]*32, size_max=14
    )
    fig6.add_hline(y=sum(gain_total)/len(gain_total), line_dash="dot", line_color="#7C5CBF",
                  annotation_text=f"Gain moyen = {sum(gain_total)/len(gain_total):.1f}")
    fig6.update_layout(title="Gain total en fonction du niveau de depart", height=380,
                       plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(t=40,b=10,l=0,r=0))
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Commentaire :</b> Ce graphique croise le score initial avec le gain obtenu apres 3 seances. On observe que les eleves ayant les scores de depart les plus faibles (5-6/20) ont souvent realise les gains les plus eleves (jusqu\'a +11 points), ce qui traduit un effet positif de la remediation precisement pour les eleves les plus en difficulte au depart - un resultat encourageant pour la dimension equite du dispositif.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphe 7 : Radar global synthèse 4 séances ────────────────────────────
    st.markdown("### 7. Vue de synthese - Indicateurs cles par seance (radar)")

    fig7 = go.Figure()
    indicateurs = ["Score moyen (/20)", "% Maîtrise", "% En cours", "% Validés (≥10)"]
    for i, label in enumerate(seances_labels_a):
        m, e, d = maitrise_a[i], encours_a[i], diff_a[i]
        vals = [
            moy_traj[i]/20*100,
            m/32*100,
            e/32*100,
            (m+e)/32*100
        ]
        fig7.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=indicateurs+[indicateurs[0]],
            fill='toself', name=label,
            line_color=box_colors[i],
            opacity=0.7
        ))
    fig7.update_layout(polar=dict(radialaxis=dict(range=[0,100], ticksuffix="%")),
                       height=420, paper_bgcolor="white",
                       legend=dict(orientation="h", y=-0.1),
                       margin=dict(t=40,b=40,l=40,r=40))
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('<div class="insight-box"><b>Commentaire :</b> Ce radar superpose 4 indicateurs cles (score moyen normalise, % maitrise, % en cours, % valides) pour chaque seance. La forme se deploie progressivement du centre (pre-test, en gris, surface quasi nulle) vers l\'exterieur (seance 3, en vert), confirmant visuellement une amelioration simultanee et coherente sur tous les indicateurs au fil du dispositif.</div>', unsafe_allow_html=True)


# ══ TAB 4 ════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Tableau de suivi individuel</div>', unsafe_allow_html=True)
    search = st.text_input("🔍 Rechercher un élève", placeholder="Tapez un prénom...")
    df_show = df_filtered.copy()
    if search: df_show = df_show[df_show["Nom"].str.contains(search,case=False)]
    if len(df_show)==0:
        st.warning("Aucun élève trouvé.")
    else:
        def color_niveau(val):
            if val=="Maîtrise": return "background-color: #D1FAE5; color: #065F46"
            if val=="En cours":  return "background-color: #FEF3C7; color: #92400E"
            return "background-color: #FEE2E2; color: #991B1B"
        def color_prog(val):
            return "color: #2E9E6B; font-weight: 600" if val>0 else "color: #E04E39"
        st.dataframe(
            df_show[["Nom","Genre","Pré-test","Post-test","Progression","Prog %","Niveau"]].style
                .map(color_niveau,subset=["Niveau"])
                .map(color_prog,  subset=["Progression"])
                .format({"Prog %":"{:.1f}%","Progression":"+{:.0f} pts"}),
            use_container_width=True, height=450
        )
        st.markdown(f"**{len(df_show)} élève(s) affichés**")
        csv = df_show.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Télécharger les données (CSV)", csv, "eleves_ppe.csv","text/csv")

# ══ TAB 5 ════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">🎮 Simulation pédagogique interactive</div>', unsafe_allow_html=True)
    c1,c2 = st.columns([1,2])
    with c1:
        intensite_guidage = st.slider("Guidage progressif (%)",0,100,70,step=5)
        travail_groupe    = st.slider("Travail en groupes (%)",0,100,60,step=5)
        correction_coll   = st.slider("Correction collective (%)",0,100,80,step=5)
        nb_seances        = st.slider("Nombre de séances",1,5,1)
        score_est = min(20,6.9+(intensite_guidage*0.05+travail_groupe*0.03+correction_coll*0.04)/10*nb_seances)
        st.info(f"**Score estimé moyen :** {score_est:.1f}/20")
    with c2:
        score_simul = []
        for s in range(1,nb_seances+2):
            gain = (intensite_guidage*0.05+travail_groupe*0.03+correction_coll*0.04)/10
            score_simul.append(round(min(20,6.9+gain*s),1))
        seances = ["Pré"]+[f"S{i}" for i in range(1,nb_seances+1)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=seances,y=score_simul,mode="lines+markers",line=dict(color="#1B6CA8",width=3),marker=dict(size=10,color="#1B6CA8"),fill="tozeroy",fillcolor="rgba(27,108,168,0.1)"))
        fig.add_hline(y=14,line_dash="dot",line_color="#2E9E6B",annotation_text="Maîtrise (14/20)")
        fig.add_hline(y=10,line_dash="dot",line_color="#E87C35",annotation_text="Validé (10/20)")
        fig.update_layout(height=380,plot_bgcolor="white",paper_bgcolor="white",yaxis=dict(range=[0,20],title="Score moyen /20"),xaxis_title="Séances",margin=dict(t=20,b=20,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    recs=[]
    if intensite_guidage<50: recs.append("⚠️ Augmentez l'intensité du guidage progressif.")
    if travail_groupe<50:    recs.append("⚠️ Le travail en groupes favorise l'entraide — à renforcer.")
    if correction_coll<60:   recs.append("⚠️ La correction collective renforce la métacognition.")
    if nb_seances<2:         recs.append("💡 Une 2ème séance consoliderait les acquis.")
    if not recs:             recs.append("✅ Excellent dispositif pédagogique !")
    for r in recs: st.markdown(f"- {r}")

# ══ TAB 6 — RAPPORT PDF ══════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-header">📋 Rapport complet — Export PDF</div>', unsafe_allow_html=True)

    moy_pre_tot    = df["Pré-test"].mean()
    moy_post_tot   = df["Post-test"].mean()
    prog_tot       = moy_post_tot - moy_pre_tot
    n_maitrise_tot = len(df[df["Niveau"]=="Maîtrise"])
    n_encours_tot  = len(df[df["Niveau"]=="En cours"])
    n_diff_tot     = len(df[df["Niveau"]=="Difficultés"])
    moy_pre_f  = df_f["Pré-test"].mean();  moy_post_f = df_f["Post-test"].mean()
    moy_pre_g  = df_g["Pré-test"].mean();  moy_post_g = df_g["Post-test"].mean()
    prog_f = moy_post_f - moy_pre_f
    prog_g = moy_post_g - moy_pre_g
    pct_maitrise_f = int(len(df_f[df_f["Post-test"]>14])/16*100)
    pct_maitrise_g = int(len(df_g[df_g["Post-test"]>14])/16*100)

    # Tableau élèves HTML
    rows_eleves = ""
    for _, row in df.iterrows():
        bg = "#D1FAE5" if row["Niveau"]=="Maîtrise" else "#FEF3C7" if row["Niveau"]=="En cours" else "#FEE2E2"
        tc = "#065F46" if row["Niveau"]=="Maîtrise" else "#92400E" if row["Niveau"]=="En cours" else "#991B1B"
        rows_eleves += f"<tr><td>{row['Nom']}</td><td>{row['Genre']}</td><td style='text-align:center'>{row['Pré-test']}/20</td><td style='text-align:center'>{row['Post-test']}/20</td><td style='text-align:center;color:#2E9E6B;font-weight:600'>+{row['Progression']} pts</td><td style='text-align:center'><span style='background:{bg};color:{tc};padding:2px 8px;border-radius:10px;font-size:11px'>{row['Niveau']}</span></td></tr>"

    # Barres SVG pour compétences
    def svg_bar(pre, post, label):
        return f"""
        <div style="margin-bottom:10px">
          <div style="display:flex;justify-content:space-between;margin-bottom:3px">
            <span style="font-size:12px;color:#374151">{label}</span>
            <span style="font-size:12px;font-weight:600;color:#1B6CA8">{post}% <span style="color:#2E9E6B;font-size:11px">(+{post-pre}pts)</span></span>
          </div>
          <div style="background:#E5E7EB;border-radius:4px;height:10px;position:relative">
            <div style="background:#CBD5E1;border-radius:4px;height:10px;width:{pre}%"></div>
            <div style="background:#1B6CA8;border-radius:4px;height:10px;width:{post}%;position:absolute;top:0;opacity:0.85"></div>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:10px;color:#9CA3AF;margin-top:2px">
            <span>Pré-test: {pre}%</span><span>Post-test: {post}%</span>
          </div>
        </div>"""

    bars_html = "".join([svg_bar(p,q,c) for p,q,c in zip(pre_comp,post_comp,competences)])

    # ── Génération des 15 graphiques Plotly pour le PDF ──────────────────
    import plotly.io as pio_local
    pio_local.templates.default = "plotly_white"

    def fig_to_html(fig, h=380):
        fig.update_layout(height=h, paper_bgcolor="white", plot_bgcolor="white",
                          margin=dict(t=50, b=40, l=50, r=20),
                          font=dict(size=11))
        return fig.to_html(include_plotlyjs="cdn", full_html=False, config={"displayModeBar": False})

    seances_pdf = ["Pré-test","Séance 1","Séance 2","Séance 3"]
    scores_f_pdf = [6.9, 8.0, 13.0, 15.2]
    scores_g_pdf = [6.7, 7.6, 12.4, 14.6]
    maitrise_pdf = [0, 0, 8, 24]
    encours_pdf  = [2, 2, 20, 5]
    diff_pdf     = [30, 30, 4, 3]
    moy_traj_pdf = [6.8, 7.8, 12.7, 14.9]
    scores_par_seance_pdf = {
        "Pré-test": df["Pré-test"].tolist(),
        "Séance 1": [5,8,9,7,9,7,10,8,7,6,9,7,6,8,9,7,7,9,6,8,8,6,9,8,7,9,10,8,9,7,9,8],
        "Séance 2": [13,14,15,12,15,13,16,14,12,11,15,13,7,8,15,12,13,15,9,13,14,11,15,13,7,14,15,11,14,11,14,12],
        "Séance 3": [16,17,18,15,17,16,18,16,15,14,17,15,8,9,17,15,16,17,11,15,16,14,17,15,7,16,17,14,16,12,16,15],
    }

    # GRAPHE 1 — Evolution globale par élève
    f1 = go.Figure()
    f1.add_trace(go.Bar(name="Pré-test", x=df["Nom"], y=df["Pré-test"], marker_color="#93C5FD"))
    f1.add_trace(go.Bar(name="Post-test", x=df["Nom"], y=df["Post-test"], marker_color="#1B6CA8"))
    f1.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maîtrise")
    f1.add_hline(y=10, line_dash="dot", line_color="#E87C35", annotation_text="Seuil validé")
    f1.update_layout(title="Évolution globale pré-test → post-test", barmode="group", yaxis=dict(range=[0,21], title="Score /20"))
    g1_html = fig_to_html(f1, 360)

    # GRAPHE 2 — Donut
    f2 = go.Figure(go.Pie(labels=["Maîtrise","En cours","Difficultés"], values=[n_maitrise_tot, n_encours_tot, n_diff_tot],
                          hole=0.55, marker=dict(colors=["#2E9E6B","#E87C35","#E04E39"]), textinfo="label+percent+value"))
    f2.update_layout(title="Répartition des niveaux — Post-test", annotations=[dict(text="32<br>élèves", x=0.5, y=0.5, font_size=14, showarrow=False)])
    g2_html = fig_to_html(f2, 380)

    # GRAPHE 3 — Évolution 3 séances Filles vs Garçons
    f3 = go.Figure()
    f3.add_trace(go.Scatter(x=seances_pdf, y=scores_f_pdf, mode="lines+markers+text", name="Filles", line=dict(color="#E04E39", width=3), marker=dict(size=10), text=scores_f_pdf, textposition="top center"))
    f3.add_trace(go.Scatter(x=seances_pdf, y=scores_g_pdf, mode="lines+markers+text", name="Garçons", line=dict(color="#1B6CA8", width=3), marker=dict(size=10), text=scores_g_pdf, textposition="bottom center"))
    f3.add_hrect(y0=14, y1=20, fillcolor="rgba(46,158,107,0.08)", line_width=0)
    f3.add_hrect(y0=10, y1=14, fillcolor="rgba(232,124,53,0.06)", line_width=0)
    f3.update_layout(title="Évolution du score moyen sur 3 séances", yaxis=dict(range=[0,20], title="Score /20"))
    g3_html = fig_to_html(f3, 380)

    # GRAPHE 4 — Stacked bar séances
    f4 = go.Figure()
    f4.add_trace(go.Bar(name="Difficultés", x=seances_pdf, y=diff_pdf, marker_color="#E04E39", text=diff_pdf, textposition="inside"))
    f4.add_trace(go.Bar(name="En cours", x=seances_pdf, y=encours_pdf, marker_color="#E87C35", text=encours_pdf, textposition="inside"))
    f4.add_trace(go.Bar(name="Maîtrise", x=seances_pdf, y=maitrise_pdf, marker_color="#2E9E6B", text=maitrise_pdf, textposition="inside"))
    f4.update_layout(title="Répartition des niveaux par séance", barmode="stack", yaxis=dict(title="Nombre d'élèves"))
    g4_html = fig_to_html(f4, 360)

    # GRAPHE 5 — Filles vs Garçons Pré/Post
    f5 = go.Figure()
    f5.add_trace(go.Bar(name="Filles", x=["Pré-test","Post-test"], y=[moy_pre_f, moy_post_f], marker_color="#E04E39", text=[f"{moy_pre_f:.1f}", f"{moy_post_f:.1f}"], textposition="outside"))
    f5.add_trace(go.Bar(name="Garçons", x=["Pré-test","Post-test"], y=[moy_pre_g, moy_post_g], marker_color="#1B6CA8", text=[f"{moy_pre_g:.1f}", f"{moy_post_g:.1f}"], textposition="outside"))
    f5.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maîtrise")
    f5.update_layout(title="Comparaison Filles vs Garçons — Score moyen /20", barmode="group", yaxis=dict(range=[0,20]))
    g5_html = fig_to_html(f5, 360)

    # GRAPHE 6 — Compétences pré/post (horizontal)
    f6 = go.Figure()
    f6.add_trace(go.Bar(name="Pré-test", y=competences, x=pre_comp, orientation="h", marker_color="#93C5FD", text=[f"{v}%" for v in pre_comp], textposition="outside"))
    f6.add_trace(go.Bar(name="Post-test", y=competences, x=post_comp, orientation="h", marker_color="#1B6CA8", text=[f"{v}%" for v in post_comp], textposition="outside"))
    f6.update_layout(title="Taux de maîtrise par compétence", barmode="group", xaxis=dict(range=[0,105], title="%"))
    g6_html = fig_to_html(f6, 360)

    # GRAPHE 7 — Waterfall gain
    f7 = go.Figure()
    f7.add_trace(go.Bar(name="Niveau pré-test", x=competences, y=pre_comp, marker_color="#9CA3AF", text=[f"{v}%" for v in pre_comp], textposition="inside"))
    f7.add_trace(go.Bar(name="Gain obtenu", x=competences, y=[q-p for p,q in zip(pre_comp, post_comp)], marker_color="#2E9E6B", text=[f"+{q-p}" for p,q in zip(pre_comp, post_comp)], textposition="inside"))
    f7.update_layout(title="Gain de maîtrise par compétence (pré → post)", barmode="stack", yaxis=dict(range=[0,100], title="%"))
    g7_html = fig_to_html(f7, 360)

    # GRAPHE 8 — Heatmap individuelle
    heat = pd.DataFrame(scores_par_seance_pdf, index=df["Nom"]).T
    f8 = px.imshow(heat, text_auto=True, aspect="auto", zmin=0, zmax=20,
                   color_continuous_scale=[[0,"#FEE2E2"],[0.5,"#FEF3C7"],[0.75,"#D1FAE5"],[1,"#065F46"]],
                   labels=dict(color="Score"))
    f8.update_layout(title="Carte de chaleur — progression individuelle")
    g8_html = fig_to_html(f8, 300)

    # GRAPHE 9 — Filles vs Garçons sur 3 séances
    f9 = go.Figure()
    f9.add_trace(go.Bar(name="Filles", x=seances_pdf, y=scores_f_pdf, marker_color="#E04E39", text=scores_f_pdf, textposition="outside"))
    f9.add_trace(go.Bar(name="Garçons", x=seances_pdf, y=scores_g_pdf, marker_color="#1B6CA8", text=scores_g_pdf, textposition="outside"))
    f9.add_hline(y=14, line_dash="dot", line_color="#2E9E6B", annotation_text="Seuil maîtrise")
    f9.update_layout(title="Comparaison Filles vs Garçons — 3 séances", barmode="group", yaxis=dict(range=[0,20]))
    g9_html = fig_to_html(f9, 380)

    # GRAPHE 10 — Écart Filles - Garçons
    ecarts_pdf = [round(f-g,1) for f,g in zip(scores_f_pdf, scores_g_pdf)]
    f10 = go.Figure(go.Bar(x=seances_pdf, y=ecarts_pdf, marker_color=["#9CA3AF" if e==0 else "#E04E39" for e in ecarts_pdf], text=[f"+{e}" for e in ecarts_pdf], textposition="outside"))
    f10.add_hline(y=0, line_color="#374151")
    f10.update_layout(title="Évolution de l'écart Filles − Garçons", yaxis=dict(range=[-0.5,1], title="Écart (pts)"))
    g10_html = fig_to_html(f10, 320)

    # GRAPHE 11 — Niveaux grouped bar
    f11 = go.Figure()
    f11.add_trace(go.Bar(name="Difficultés", x=seances_pdf, y=diff_pdf, marker_color="#E04E39", text=diff_pdf, textposition="outside"))
    f11.add_trace(go.Bar(name="En cours", x=seances_pdf, y=encours_pdf, marker_color="#E87C35", text=encours_pdf, textposition="outside"))
    f11.add_trace(go.Bar(name="Maîtrise", x=seances_pdf, y=maitrise_pdf, marker_color="#2E9E6B", text=maitrise_pdf, textposition="outside"))
    f11.update_layout(title="Nombre d'élèves par niveau à chaque séance", barmode="group", yaxis=dict(range=[0,35]))
    g11_html = fig_to_html(f11, 360)

    # GRAPHE 12 — Box plot
    f12 = go.Figure()
    for i, label in enumerate(seances_pdf):
        f12.add_trace(go.Box(y=scores_par_seance_pdf[label], name=label, marker_color=["#9CA3AF","#E87C35","#1B6CA8","#2E9E6B"][i], boxmean=True, boxpoints="all", jitter=0.4, pointpos=-1.5))
    f12.add_hline(y=14, line_dash="dot", line_color="#2E9E6B")
    f12.add_hline(y=10, line_dash="dot", line_color="#E87C35")
    f12.update_layout(title="Distribution des scores par séance", yaxis=dict(range=[0,20], title="Score /20"), showlegend=False)
    g12_html = fig_to_html(f12, 400)

    # GRAPHE 13 — Spaghetti
    f13 = go.Figure()
    for i, nom in enumerate(df["Nom"]):
        traj = [scores_par_seance_pdf[s][i] for s in seances_pdf]
        c = "#E04E39" if df.iloc[i]["Genre"] == "Filles" else "#1B6CA8"
        f13.add_trace(go.Scatter(x=seances_pdf, y=traj, mode="lines", line=dict(color=c, width=1.2), opacity=0.35, showlegend=False, name=nom, hoverinfo="text+y", hovertext=nom))
    f13.add_trace(go.Scatter(x=seances_pdf, y=moy_traj_pdf, mode="lines+markers", line=dict(color="#1A1A1A", width=4), marker=dict(size=10), name="Moyenne"))
    f13.add_hline(y=14, line_dash="dot", line_color="#2E9E6B")
    f13.update_layout(title="Trajectoires individuelles (rouge=filles, bleu=garçons, noir=moyenne)", yaxis=dict(range=[0,20], title="Score /20"))
    g13_html = fig_to_html(f13, 400)

    # GRAPHE 14 — Scatter gain
    gain_total = [s3-s0 for s0,s3 in zip(scores_par_seance_pdf["Pré-test"], scores_par_seance_pdf["Séance 3"])]
    f14 = px.scatter(x=scores_par_seance_pdf["Pré-test"], y=gain_total, color=df["Genre"], hover_name=df["Nom"],
                     color_discrete_map={"Filles":"#E04E39","Garçons":"#1B6CA8"},
                     labels={"x":"Score Pré-test /20", "y":"Gain total"})
    moy_gain = sum(gain_total)/len(gain_total)
    f14.add_hline(y=moy_gain, line_dash="dot", line_color="#7C5CBF", annotation_text=f"Gain moyen = {moy_gain:.1f}")
    f14.update_layout(title="Gain total en fonction du niveau de départ")
    g14_html = fig_to_html(f14, 380)

    # GRAPHE 15 — Radar synthèse
    indicateurs_pdf = ["Score moyen (norm.)", "% Maîtrise", "% En cours", "% Validés"]
    f15 = go.Figure()
    radar_colors = ["#9CA3AF","#E87C35","#1B6CA8","#2E9E6B"]
    for i, label in enumerate(seances_pdf):
        m, e, d = maitrise_pdf[i], encours_pdf[i], diff_pdf[i]
        vals = [moy_traj_pdf[i]/20*100, m/32*100, e/32*100, (m+e)/32*100]
        f15.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=indicateurs_pdf+[indicateurs_pdf[0]], fill="toself", name=label, line_color=radar_colors[i], opacity=0.7))
    f15.update_layout(title="Synthèse — indicateurs clés par séance", polar=dict(radialaxis=dict(range=[0,100])))
    g15_html = fig_to_html(f15, 420)


    html_pdf = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',Arial,sans-serif;color:#1a1a2e;background:white;font-size:13px;line-height:1.6}}
.page{{padding:30px 40px;max-width:960px;margin:auto}}
.header{{background:linear-gradient(135deg,#0F4C75,#1B6CA8);color:white;padding:28px 32px;border-radius:12px;margin-bottom:24px}}
.header h1{{font-size:22px;font-weight:700;margin-bottom:6px}}
.header p{{font-size:12px;opacity:.9;margin:2px 0}}
.badge{{display:inline-block;background:rgba(255,255,255,.2);border-radius:20px;padding:3px 12px;font-size:11px;margin-top:10px;margin-right:6px}}
.kpi-row{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:24px}}
.kpi{{background:white;border-radius:10px;padding:14px;border-left:4px solid #1B6CA8;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
.kpi.g{{border-left-color:#2E9E6B}}.kpi.o{{border-left-color:#E87C35}}.kpi.p{{border-left-color:#7C5CBF}}
.kpi-lbl{{font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}}
.kpi-val{{font-size:20px;font-weight:700}}.kpi-sub{{font-size:10px;color:#9ca3af;margin-top:2px}}
.sec{{margin-bottom:24px}}
.sec-title{{font-size:14px;font-weight:700;color:#0F4C75;border-bottom:2px solid #E5E7EB;padding-bottom:6px;margin-bottom:14px}}
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
.card{{background:#F9FAFB;border-radius:10px;padding:16px;border-top:3px solid #E04E39}}
.card.blue{{border-top-color:#1B6CA8}}
.card h3{{font-size:13px;font-weight:700;margin-bottom:10px}}
.stat-row{{display:flex;justify-content:space-between;font-size:12px;padding:4px 0;border-bottom:1px solid #E5E7EB}}
.stat-row:last-child{{border-bottom:none}}
.stat-row b{{color:#2E9E6B}}
table{{width:100%;border-collapse:collapse;font-size:11.5px}}
th{{background:#0F4C75;color:white;padding:8px 10px;text-align:left;font-weight:600}}
td{{padding:7px 10px;border-bottom:1px solid #F3F4F6}}
tr:nth-child(even) td{{background:#F9FAFB}}
.info{{background:#EEF4FF;border-left:4px solid #1B6CA8;border-radius:8px;padding:12px 16px;font-size:12px;color:#374151;margin-bottom:12px}}
.info b{{color:#1B6CA8}}
.warn{{background:#FFFBEB;border-left:4px solid #E87C35;border-radius:8px;padding:12px 16px;font-size:12px;color:#374151;margin-bottom:12px}}
.reco-list{{list-style:none;padding:0}}
.reco-list li{{padding:7px 12px;margin-bottom:6px;background:#F9FAFB;border-radius:6px;border-left:3px solid #1B6CA8;font-size:12px}}
.reco-list li.w{{border-left-color:#E87C35}}
.chart-section {{ margin-bottom: 32px; page-break-inside: avoid; }}
.chart-title {{ font-size: 13px; font-weight: 700; color: #0F4C75; margin-bottom: 6px; }}
.chart-caption {{ font-size: 11px; color: #6B7280; font-style: italic; text-align: center; margin: 6px 0 10px; }}
.interpretation {{
  background: #FFFBEB; border-left: 4px solid #F5C518; padding: 12px 16px;
  font-size: 12px; color: #1A1A1A; line-height: 1.6; margin-top: 8px; border-radius: 4px;
}}
.interpretation b {{ color: #8A7000; }}
.chart-box {{ background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px; margin-bottom: 4px; }}
.footer{{margin-top:28px;border-top:1px solid #E5E7EB;padding-top:12px;font-size:11px;color:#9ca3af;text-align:center}}
@media print{{body{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}
</style>
</head>
<body>
<div class="page">

<div class="header">
  <h1>🔬 Rapport PPE — Remédiation en Immunologie</h1>
  <p>Projet Professionnel de l'Étudiant · Formation Initiale des Enseignants · CRMEF</p>
  <p>Remédiation des difficultés en lecture des graphes immunologiques · 3ème Année Collège (3AC)</p>
  <span class="badge">📅 Séance de soutien pédagogique</span>
  <span class="badge">👥 32 élèves · 6 groupes</span>
  <span class="badge">🏫 3AC · CRMEF</span>
</div>

<div class="kpi-row">
  <div class="kpi"><div class="kpi-lbl">👥 Effectif</div><div class="kpi-val">32</div><div class="kpi-sub">16 filles · 16 garçons</div></div>
  <div class="kpi o"><div class="kpi-lbl">📉 Moy. Pré-test</div><div class="kpi-val">{moy_pre_tot:.1f}/20</div><div class="kpi-sub">Avant remédiation</div></div>
  <div class="kpi g"><div class="kpi-lbl">📈 Moy. Post-test</div><div class="kpi-val">{moy_post_tot:.1f}/20</div><div class="kpi-sub">Après remédiation</div></div>
  <div class="kpi"><div class="kpi-lbl">🚀 Progression</div><div class="kpi-val">+{prog_tot:.1f} pts</div><div class="kpi-sub">Amélioration nette</div></div>
  <div class="kpi p"><div class="kpi-lbl">🏆 Maîtrise</div><div class="kpi-val">{int(n_maitrise_tot/32*100)}%</div><div class="kpi-sub">{n_maitrise_tot}/32 élèves</div></div>
</div>

<div class="sec">
  <div class="sec-title">1. Contexte et Problématique</div>
  <p style="font-size:12.5px;color:#374151;line-height:1.8">Ce projet professionnel s'inscrit dans le cadre de la <b>formation initiale des enseignants au CRMEF</b>. L'observation en classe a révélé que de nombreux élèves de <b>3AC</b> éprouvent des difficultés lors de la lecture et de l'analyse des courbes immunologiques, notamment dans la <b>lecture des axes</b>, la <b>compréhension des variations</b> et la <b>formulation de conclusions scientifiques argumentées</b>.</p>
</div>

<div class="sec">
  <div class="sec-title">2. Résultats Globaux</div>
  <div class="info"><b>✅ Progression universelle :</b> Le score moyen est passé de <b>{moy_pre_tot:.1f}/20</b> à <b>{moy_post_tot:.1f}/20</b>, soit une progression de <b>+{prog_tot:.1f} points</b>. <b>{n_maitrise_tot} élèves ({int(n_maitrise_tot/32*100)}%)</b> ont atteint le seuil de maîtrise (>14/20).</div>
  <div class="two-col" style="text-align:center">
    <div style="background:#F9FAFB;border-radius:10px;padding:16px">
      <div style="font-size:11px;color:#6b7280;margin-bottom:8px">RÉPARTITION DES NIVEAUX</div>
      <div style="display:flex;justify-content:space-around">
        <div><div style="font-size:24px;font-weight:700;color:#2E9E6B">{n_maitrise_tot}</div><div style="font-size:11px;color:#6b7280">Maîtrise</div></div>
        <div><div style="font-size:24px;font-weight:700;color:#E87C35">{n_encours_tot}</div><div style="font-size:11px;color:#6b7280">En cours</div></div>
        <div><div style="font-size:24px;font-weight:700;color:#E04E39">{n_diff_tot}</div><div style="font-size:11px;color:#6b7280">Difficultés</div></div>
      </div>
    </div>
    <div style="background:#F9FAFB;border-radius:10px;padding:16px">
      <div style="font-size:11px;color:#6b7280;margin-bottom:8px">PROGRESSION MOYENNE</div>
      <div style="font-size:36px;font-weight:700;color:#2E9E6B">+{prog_tot:.1f}</div>
      <div style="font-size:12px;color:#6b7280">points sur 20</div>
    </div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">3. Analyse par Genre</div>
  <div class="two-col">
    <div class="card">
      <h3 style="color:#E04E39">🔴 Filles (16 élèves)</h3>
      <div class="stat-row"><span>Score moyen pré-test</span><span>{moy_pre_f:.1f}/20</span></div>
      <div class="stat-row"><span>Score moyen post-test</span><span>{moy_post_f:.1f}/20</span></div>
      <div class="stat-row"><span>Progression moyenne</span><b>+{prog_f:.1f} pts</b></div>
      <div class="stat-row"><span>Taux de maîtrise</span><b>{pct_maitrise_f}%</b></div>
    </div>
    <div class="card blue">
      <h3 style="color:#1B6CA8">🔵 Garçons (16 élèves)</h3>
      <div class="stat-row"><span>Score moyen pré-test</span><span>{moy_pre_g:.1f}/20</span></div>
      <div class="stat-row"><span>Score moyen post-test</span><span>{moy_post_g:.1f}/20</span></div>
      <div class="stat-row"><span>Progression moyenne</span><b>+{prog_g:.1f} pts</b></div>
      <div class="stat-row"><span>Taux de maîtrise</span><b>{pct_maitrise_g}%</b></div>
    </div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">4. Analyse par Compétence Ciblée</div>
  {bars_html}
  <div class="warn" style="margin-top:12px"><b>⚠️ À consolider :</b> La <b>formulation de conclusions scientifiques</b> reste la compétence la moins maîtrisée (58%). Une séance supplémentaire ciblée est recommandée.</div>
</div>

<div class="sec">
  <div class="sec-title">5. Suivi Individuel des Élèves</div>
  <table>
    <thead><tr><th>Nom</th><th>Genre</th><th>Pré-test</th><th>Post-test</th><th>Progression</th><th>Niveau</th></tr></thead>
    <tbody>{rows_eleves}</tbody>
  </table>
</div>

<div class="sec">
  <div class="sec-title">6. Recommandations Pédagogiques</div>
  <ul class="reco-list">
    <li>✅ Maintenir les stratégies de <b>guidage progressif</b> et de <b>correction collective</b> — impact prouvé sur la lecture des axes (+59 pts).</li>
    <li class="w">⚠️ Prévoir une <b>2ème séance de soutien</b> focalisée sur la formulation de conclusions scientifiques argumentées.</li>
    <li>✅ Utiliser des <b>supports visuels progressifs</b> : courbes annotées, fléchage des variations, fiches d'aide à la lecture.</li>
    <li class="w">⚠️ Mettre en place un <b>suivi individualisé</b> pour les {n_diff_tot} élèves encore en difficulté après la remédiation.</li>
    <li>✅ Valoriser les productions des groupes lors de la correction collective pour renforcer la <b>motivation</b>.</li>
    <li>✅ Intégrer des <b>exercices de rédaction scientifique guidée</b> pour développer la compétence de formulation.</li>
  </ul>
</div>

<div class="sec" style="page-break-before:always">
  <div class="sec-title">7. Analyses graphiques détaillées et interprétations</div>
  <p style="font-size:12px;color:#374151;line-height:1.7;margin-bottom:20px">Cette section présente 15 analyses graphiques accompagnées de leur interprétation pédagogique, permettant d\'apprécier les effets du dispositif de remédiation sous différents angles.</p>

  <div class="chart-section">
    <div class="chart-title">Figure 1 — Évolution globale pré-test → post-test (par élève)</div>
    <div class="chart-box">{g1_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Toutes les barres post-test (bleu foncé) dépassent les barres pré-test (bleu clair) correspondantes : aucun élève n\'a régressé. La grande majorité des barres post-test franchit le seuil de maîtrise (14/20). Cela démontre que la séance de soutien a produit un effet positif universel, et que les stratégies de guidage progressif et de travail en groupes ont touché l\'ensemble du groupe-classe.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 2 — Répartition des niveaux après remédiation</div>
    <div class="chart-box">{g2_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Comparée à la situation initiale (94 % en difficulté), la répartition post-test montre un basculement complet : 41 % en maîtrise, 44 % en cours, 16 % encore en difficulté. La majorité a quitté la zone rouge, et près de la moitié atteint un niveau de maîtrise opérationnelle.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 3 — Évolution du score moyen sur 3 séances (Filles vs Garçons)</div>
    <div class="chart-box">{g3_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Les courbes filles (rouge) et garçons (bleu) suivent une trajectoire ascendante quasi identique, traversant la zone rouge au pré-test, la zone orange en séance 1, et atteignant la zone verte (maîtrise) en séance 3. Le saut le plus marqué entre S1 et S2 justifie pédagogiquement la nécessité d\'au moins 2-3 séances : une seule séance n\'aurait pas suffi.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 4 — Répartition des niveaux par séance</div>
    <div class="chart-box">{g4_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Au pré-test et S1, la barre est dominée par le rouge (30 élèves). En S2, recomposition complète : rouge=4, orange=20, vert=8. En S3, transformation totale : vert=24, orange=5, rouge=3. La séance 2 constitue le moment-clé du basculement pédagogique : c\'est la séance où le plus grand nombre d\'élèves franchit le seuil de validation.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 5 — Comparaison Filles vs Garçons (Pré-test / Post-test)</div>
    <div class="chart-box">{g5_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Au pré-test, les deux groupes sont quasi-identiques (6,7 vs 6,9), confirmant l\'homogénéité initiale. Au post-test, filles=13,9 et garçons=13,1, tous deux ayant franchi le seuil validé. L\'écart final (+0,8 pt en faveur des filles) n\'a pas de signification pédagogique majeure et relève de facteurs individuels.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 6 — Taux de maîtrise par compétence (avant / après)</div>
    <div class="chart-box">{g6_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Toutes les compétences progressent, mais à des rythmes très différents : la lecture des axes (24 → 83 %) est une compétence technique vite acquise, tandis que la formulation de conclusions (42 → 58 %) est une compétence cognitive de haut niveau, plus difficile à consolider. La formulation de conclusions doit devenir la priorité des prochaines interventions.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 7 — Gain de maîtrise par compétence</div>
    <div class="chart-box">{g7_html}</div>
    <div class="interpretation"><b>Interprétation :</b> La hauteur du segment vert représente l\'efficacité réelle de la remédiation : +59 pts (lecture des axes, très réceptive au guidage), mais seulement +16 pts (formulation de conclusions, résistante à une intervention courte). La stratégie pédagogique est particulièrement efficace sur les compétences techniques, et insuffisante sur les compétences rédactionnelles.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 8 — Carte de chaleur : progression individuelle</div>
    <div class="chart-box">{g8_html}</div>
    <div class="interpretation"><b>Interprétation :</b> En parcourant le graphique de gauche à droite, on voit chaque colonne se « réchauffer » du rouge initial vers le vert final. Quelques colonnes restent claires (3 à 5 élèves) tout au long du dispositif : ils nécessitent un accompagnement personnalisé. Cette visualisation permet d\'identifier nominativement chaque élève en difficulté.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 9 — Comparaison Filles vs Garçons (4 séances)</div>
    <div class="chart-box">{g9_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Les deux groupes progressent en parallèle, avec un écart constant d\'environ 0,5 point. Cette progression parallèle indique que les stratégies pédagogiques choisies sont neutres en termes de genre : ni le guidage progressif, ni le travail en groupes ne créent d\'avantage spécifique à l\'un ou l\'autre groupe — un résultat important du point de vue de l\'équité pédagogique.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 10 — Évolution de l\'écart Filles − Garçons</div>
    <div class="chart-box">{g10_html}</div>
    <div class="interpretation"><b>Interprétation :</b> L\'écart reste toujours positif (en faveur des filles), oscillant entre +0,2 et +0,6 pt, sans tendance claire à l\'élargissement ou à la réduction. Cette stabilité, combinée à la faible amplitude (toujours &lt; 1 pt sur 20), confirme l\'absence d\'effet différentiel significatif du dispositif selon le genre.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 11 — Nombre d\'élèves par niveau (barres groupées)</div>
    <div class="chart-box">{g11_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Le rouge passe de 30 → 30 → 4 → 3 (chute brutale en S2), l\'orange suit une courbe en cloche (2 → 2 → 20 → 5), et le vert décolle à partir de S2 (0 → 0 → 8 → 24). Ces trois courbes décrivent un parcours-type d\'apprentissage : difficulté initiale, transition par la zone intermédiaire, puis maîtrise.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 12 — Distribution des scores par séance (box plot)</div>
    <div class="chart-box">{g12_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Translation nette de l\'ensemble de la distribution vers le haut, accompagnée d\'un léger resserrement des boîtes entre S2 et S3 : signe d\'homogénéisation du niveau de la classe. Les quelques points isolés sous le seuil de validation en S3 correspondent aux élèves identifiés comme étant encore en difficulté.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 13 — Trajectoires individuelles (spaghetti plot)</div>
    <div class="chart-box">{g13_html}</div>
    <div class="interpretation"><b>Interprétation :</b> L\'absence totale de ligne descendante confirme la progression universelle : aucun élève n\'a régressé d\'une séance à l\'autre. Les lignes restant sous la moyenne identifient les élèves en difficulté persistante ; celles qui dépassent la moyenne identifient les élèves ayant particulièrement bénéficié de la remédiation.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 14 — Score initial vs gain total</div>
    <div class="chart-box">{g14_html}</div>
    <div class="interpretation"><b>Interprétation :</b> Tendance descendante : les élèves partant avec un score faible (5-6/20) obtiennent les gains les plus élevés (8 à 11 pts), tandis que les élèves mieux notés au départ (8-9/20) progressent moins en valeur absolue. Du point de vue de l\'équité scolaire, le résultat est positif : le dispositif réduit les écarts initiaux.</div>
  </div>

  <div class="chart-section">
    <div class="chart-title">Figure 15 — Synthèse en radar des 4 indicateurs clés</div>
    <div class="chart-box">{g15_html}</div>
    <div class="interpretation"><b>Interprétation :</b> La surface se déploie progressivement du centre (pré-test, quasi nulle) vers l\'extérieur (séance 3, recouvrant la quasi-totalité de la zone). Cette expansion régulière et cohérente sur les 4 indicateurs confirme visuellement l\'efficacité globale et homogène du dispositif. Vue idéale pour communiquer aux parents, à l\'équipe pédagogique ou au jury.</div>
  </div>
</div>

<div class="footer">
  Rapport généré automatiquement · PPE Remédiation Immunologie · CRMEF · Formation Initiale des Enseignants
</div>
</div>
</body>
</html>"""

    st.markdown("### 👁️ Aperçu du rapport")
    st.components.v1.html(html_pdf, height=650, scrolling=True)
    st.markdown("---")

    c1,c2 = st.columns(2)
    with c1:
        st.download_button(
            label="📄 Télécharger le rapport HTML → PDF",
            data=html_pdf.encode("utf-8"),
            file_name="rapport_ppe_immunologie.html",
            mime="text/html",
            use_container_width=True
        )
    with c2:
        csv_all = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📊 Télécharger les données CSV",
            data=csv_all,
            file_name="donnees_eleves_ppe.csv",
            mime="text/csv",
            use_container_width=True
        )
    st.info("💡 **Pour obtenir un PDF :** Téléchargez le fichier HTML → ouvrez-le dans votre navigateur → **Ctrl+P** → **Enregistrer en PDF**")
