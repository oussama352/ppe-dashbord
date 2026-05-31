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
post_f = [15,15,16,13,16,14,17,15,13,12,16,14,11,15,16,13]
pre_g  = [6,8,5,7,7,5,8,6,6,7,9,7,8,6,8,7]
post_g = [14,16,12,14,15,12,16,13,13,14,17,14,16,12,15,13]

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
    filtre_genre  = st.selectbox("Genre",  ["Tous", "Filles", "Garçons"])
    filtre_niveau = st.selectbox("Niveau (post-test)", ["Tous", "Maîtrise", "En cours", "Difficultés"])
    st.markdown("---")
    st.markdown("### 📋 Infos séance")
    st.info("📅 Séance de soutien pédagogique  \n👥 6 groupes collaboratifs  \n🧠 Guidage progressif  \n✅ Correction collective")
    st.caption("Projet Professionnel Étudiant · Formation initiale enseignants")

df_filtered = df.copy()
if filtre_genre  != "Tous": df_filtered = df_filtered[df_filtered["Genre"]  == filtre_genre]
if filtre_niveau != "Tous": df_filtered = df_filtered[df_filtered["Niveau"] == filtre_niveau]

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

tabs = st.tabs(["📊 Vue Globale","⚖️ Filles vs Garçons","🎯 Compétences","👥 Suivi Élèves","📈 Simulation","📋 Rapport PDF"])

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

# ══ TAB 2 ════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Comparaison Filles / Garçons</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        means = df.groupby("Genre")[["Pré-test","Post-test"]].mean().reset_index()
        fig = px.bar(means.melt(id_vars="Genre",var_name="Test",value_name="Score"), x="Test",y="Score",color="Genre",barmode="group",color_discrete_map=COLOR_MAP,title="Score moyen /20")
        fig.update_layout(height=300,plot_bgcolor="white",paper_bgcolor="white",margin=dict(t=40,b=10,l=0,r=0),yaxis=dict(range=[0,20]))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        prog_genre = df.groupby("Genre")["Prog %"].mean().reset_index()
        fig2 = px.bar(prog_genre,x="Genre",y="Prog %",color="Genre",color_discrete_map=COLOR_MAP,title="Taux de progression (%)")
        fig2.update_layout(height=300,plot_bgcolor="white",paper_bgcolor="white",margin=dict(t=40,b=10,l=0,r=0),showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    fig3 = px.box(df,x="Genre",y="Post-test",color="Genre",points="all",hover_name="Nom",color_discrete_map=COLOR_MAP,title="Distribution des scores post-test")
    fig3.add_hline(y=14,line_dash="dot",line_color="#2E9E6B",annotation_text="Seuil maîtrise")
    fig3.update_layout(height=350,plot_bgcolor="white",paper_bgcolor="white",margin=dict(t=40,b=10,l=0,r=0),showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
    comps_short = ["Axes","Variations","Comparaison","Conclusions"]
    fig4 = go.Figure()
    fig4.add_trace(go.Scatterpolar(r=post_comp_f+[post_comp_f[0]],theta=comps_short+[comps_short[0]],fill='toself',name='Filles',line_color='#E04E39',fillcolor='rgba(224,78,57,0.15)'))
    fig4.add_trace(go.Scatterpolar(r=post_comp_g+[post_comp_g[0]],theta=comps_short+[comps_short[0]],fill='toself',name='Garçons',line_color='#1B6CA8',fillcolor='rgba(27,108,168,0.15)'))
    fig4.update_layout(polar=dict(radialaxis=dict(range=[0,100])),height=380,paper_bgcolor="white",margin=dict(t=30,b=30,l=30,r=30))
    st.plotly_chart(fig4, use_container_width=True)

# ══ TAB 3 ════════════════════════════════════════════════════════════════════
with tabs[2]:
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

# ══ TAB 4 ════════════════════════════════════════════════════════════════════
with tabs[3]:
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
with tabs[4]:
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
with tabs[5]:
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
