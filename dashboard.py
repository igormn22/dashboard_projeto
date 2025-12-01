import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(page_title="Violência Doméstica & Impunidade Judicial", layout="wide", initial_sidebar_state="collapsed")

PRIMARY = "#0f6b66"
ACCENT = "#ff6b4a"
SECOND = "#3a4f9c"
TEXT = "#0b2b36"
MUTED = "#6b7b80"
PLOT_TEXT = "#ffffff"

H_LARGE = 520
H_MED = 380

# ---------------------------------------------------
#  CSS — TÍTULO SEM COR DE FUNDO (AJUSTADO)
# ---------------------------------------------------
st.markdown(f"""
<style>
.header-band {{
  width:100%;
  background: none !important;   /* sem cor */
  padding: 0;                    /* sem altura extra */
  box-shadow: none !important;   /* sem sombra */
  position: static;              /* sem sticky */
  display:flex;
  align-items:center;
  justify-content:center;
}}
.header-title {{
  color: {TEXT} !important;
  font-size:30px;
  font-weight:900;
  letter-spacing:0.6px;
  margin:10px 0 20px 0;
  text-align:center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}}
.block-container {{ padding-top: 20px; padding-left:18px; padding-right:18px; background: linear-gradient(180deg, #f8fbfb 0%, #ffffff 100%); }}
.card {{
  background: white;
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 8px 22px rgba(11,43,54,0.06);
  margin-bottom: 18px;
}}
.chart-title {{ font-weight:700; color:{TEXT}; margin-bottom:10px; font-size:15px; }}
[data-testid="stSidebar"] {{ display: none; }}
</style>
""", unsafe_allow_html=True)

# TÍTULO — AGORA SEM FUNDO
st.markdown("<div class='header-band'><h1 class='header-title'>Violência Doméstica & Impunidade Judicial</h1></div>", unsafe_allow_html=True)
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)


# ---------------------------------------------------
# CARREGAMENTO DOS DADOS
# ---------------------------------------------------
csv_data = """UF,Ano,Total_2022,Total_2023,Taxa_2022,Taxa_2023,Variacao_Percentual,Registros_Violencia_Domestica_SINESP,Taxa_100mil_Mulheres_SINESP,Feminicidios_SSP,Chamadas_180_Total,Medidas_Protetivas_Concedidas,Atendimentos_Saude_Violencia,Processos_Ajuizados_CNJ,Condenacoes_CNJ,Arquivamentos_CNJ,Indice_Impunidade,Populacao_Feminina_Estimada,Delegacias_Especializadas_Mulher,PIB_per_Capita_R$,IDH_Estadual
Brasil,2023,235915,258941,225.7,247.7,9.8,258941,247.7,1467,1123450,382115,598230,168400,45230,39170,5.72,107400000,1365,41200,0.765
Acre,2023,817,1105,197.02,266.47,35.3,1105,266.47,12,8420,1640,2590,620,180,120,6.14,430000,18,23800,0.710
Alagoas,2023,2013,2400,123.48,147.22,19.2,2400,147.22,52,23100,3980,6200,1340,310,210,7.74,1660000,46,18200,0.684
Amapá,2023,1164,968,315.24,262.16,-16.8,968,262.16,9,5670,1280,2010,480,95,85,10.19,430000,15,26100,0.708
Amazonas,2023,3284,3564,166.21,180.38,8.53,3564,180.38,41,30210,5240,7890,2100,520,380,6.85,2060000,52,29900,0.700
Bahia,2023,14919,14499,204.20,198.45,-2.82,14499,198.45,135,98500,18600,32400,8700,1700,1450,8.53,7450000,132,21400,0.714
Ceará,2023,772,503,17.02,11.09,-34.84,503,11.09,66,44200,8030,15700,260,60,55,8.38,4610000,101,23600,0.734
Distrito Federal,2023,3362,3525,227.99,239.05,4.85,3525,239.05,18,27100,5300,9500,2500,720,430,4.90,1520000,38,85000,0.824
Espírito Santo,2023,2254,2455,114.79,125.02,8.92,2455,125.02,37,19400,4100,7800,1500,430,290,5.71,2080000,57,39500,0.772
Goiás,2023,5158,5225,143.69,145.56,1.30,5225,145.56,59,36900,7130,13900,3400,860,570,6.07,3570000,89,36100,0.769
Maranhão,2023,2225,1900,64.5,55.1,-14.6,1900,55.1,61,55300,6400,11300,950,190,170,10.00,3690000,74,15600,0.687
Mato Grosso,2023,11415,10540,628.09,579.95,-7.7,10540,579.95,44,18700,3900,7400,5100,820,760,12.85,1790000,44,51200,0.774
Mato Grosso do Sul,2023,3412,2837,243.63,202.57,-16.85,2837,202.57,28,13300,2700,5200,1400,260,240,10.91,1460000,33,48700,0.766
Minas Gerais,2023,22014,24000,209.17,228.04,9.02,24000,228.04,121,154000,29800,51000,15000,3400,2200,7.06,10600000,220,36200,0.787
Pará,2023,9957,10465,244.74,257.23,5.10,10465,257.23,83,67400,9100,17400,4800,900,810,11.63,4280000,92,20300,0.698
Paraíba,2023,1001,1192,48.69,57.98,19.08,1192,57.98,29,17650,3050,6200,620,150,135,7.95,2040000,49,21000,0.722
Paraná,2023,17777,23886,303.00,407.12,34.36,23886,407.12,98,73100,15600,32500,13200,2900,2300,8.23,5850000,165,42500,0.792
Pernambuco,2023,9338,10121,197.10,213.63,8.39,10121,213.63,107,88400,12000,21100,5200,990,890,10.23,5050000,118,24200,0.719
Piauí,2023,1319,1529,78.95,91.52,15.92,1529,91.52,22,15600,2990,5300,700,160,145,9.56,1630000,41,19700,0.703
Rio de Janeiro,2023,25413,27148,299.77,320.24,6.9,27148,320.24,143,169000,27600,43200,16400,3100,2700,8.76,8700000,190,45800,0.800
Rio Grande do Norte,2023,2777,3145,162.97,184.57,13.25,3145,184.57,26,22100,3800,7800,1700,350,310,8.99,1770000,44,22600,0.728
Rio Grande do Sul,2023,18207,19862,323.55,352.96,9.09,19862,352.96,94,81000,13900,29200,12000,2300,2000,8.64,5650000,150,46300,0.787
Rondônia,2023,3653,4132,460.53,520.92,13.11,4132,520.92,19,9200,2140,4100,1900,290,260,14.25,920000,28,31200,0.735
Roraima,2023,1274,1500,402.76,474.21,17.7,1500,474.21,11,4600,980,2100,670,120,110,12.50,300000,12,28300,0.707
Santa Catarina,2023,16531,17035,428.35,441.41,3.05,17035,441.41,55,52000,9500,24300,9800,2100,1800,8.11,3800000,120,48700,0.808
São Paulo,2023,52672,61991,228.86,269.35,17.69,61991,269.35,221,247000,51200,78400,41000,8200,7100,7.56,23000000,280,58000,0.826
Sergipe,2023,1203,1162,104.41,100.85,-3.41,1162,100.85,14,8700,1480,2600,540,95,85,12.23,1180000,29,21800,0.702
Tocantins,2023,1984,2252,263.06,298.60,13.51,2252,298.60,17,7100,1290,3300,1180,210,195,10.72,820000,22,28900,0.742
"""

df = pd.read_csv(StringIO(csv_data))

# ajustes numéricos
for c in [
    "Total_2022","Total_2023","Taxa_100mil_Mulheres_SINESP","Feminicidios_SSP",
    "Processos_Ajuizados_CNJ","Condenacoes_CNJ","Arquivamentos_CNJ","Indice_Impunidade",
    "Medidas_Protetivas_Concedidas","Atendimentos_Saude_Violencia",
    "Chamadas_180_Total","Variacao_Percentual"
]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

# novos indicadores
df["Taxa_Condenacao"] = df.apply(lambda r: r["Condenacoes_CNJ"] / r["Processos_Ajuizados_CNJ"] if r["Processos_Ajuizados_CNJ"]>0 else 0, axis=1)
df["Arquivamentos_prop"] = df.apply(lambda r: r["Arquivamentos_CNJ"] / r["Processos_Ajuizados_CNJ"] if r["Processos_Ajuizados_CNJ"]>0 else 0, axis=1)
df["Feminicidios_por_100k"] = df.apply(lambda r: r["Feminicidios_SSP"] / r["Populacao_Feminina_Estimada"] * 100000 if r["Populacao_Feminina_Estimada"]>0 else 0, axis=1)

df = df[df["Ano"]==2023].copy()

# ---------------------------------------------------
# Layout padrão para gráficos
# ---------------------------------------------------
def standard_layout(fig, height, left_margin=220):
    fig.update_layout(
        template="plotly",
        plot_bgcolor="#061014",
        paper_bgcolor="#061014",
        font=dict(color=PLOT_TEXT, family="Segoe UI, Roboto, Arial"),
        margin=dict(l=left_margin, r=24, t=36, b=24),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        hoverlabel=dict(bgcolor="white", font_color="#071617")
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False, automargin=True)
    return fig


# ---------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------

col1, col2, col3 = st.columns([1.2, 1.0, 1.0])

with col1:
    st.markdown("<div class='card'><div class='chart-title'>Denúncias — Total 2023</div></div>", unsafe_allow_html=True)
    db = df.sort_values("Total_2023", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=db["Total_2023"], y=db["UF"], orientation="h", marker=dict(color=PRIMARY)))
    scale = db["Total_2023"].max()/max(1,db["Taxa_100mil_Mulheres_SINESP"].max())
    fig.add_trace(go.Scatter(x=db["Taxa_100mil_Mulheres_SINESP"]*scale, y=db["UF"], mode="markers",
                             marker=dict(color=ACCENT, size=9)))
    fig = standard_layout(fig, H_LARGE, left_margin=240)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<div class='card'><div class='chart-title'>Atuação de Serviços — Chamadas, Saúde e Medidas (Top 8)</div></div>", unsafe_allow_html=True)
    df["resp_sum"] = df[["Medidas_Protetivas_Concedidas","Atendimentos_Saude_Violencia","Chamadas_180_Total"]].sum(axis=1)
    top8 = df.sort_values("resp_sum", ascending=False).head(8).set_index("UF")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(y=top8.index, x=top8["Chamadas_180_Total"], orientation="h", name="Chamadas 180"))
    fig2.add_trace(go.Bar(y=top8.index, x=top8["Atendimentos_Saude_Violencia"], orientation="h", name="Atendimentos"))
    fig2.add_trace(go.Bar(y=top8.index, x=top8["Medidas_Protetivas_Concedidas"], orientation="h", name="Medidas protetivas"))
    fig2 = standard_layout(fig2, H_LARGE, left_margin=240)
    fig2.update_layout(barmode="stack", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.markdown("<div class='card'><div class='chart-title'>Condenações x Arquivamentos — Top 10</div></div>", unsafe_allow_html=True)
    top10 = df.sort_values("Processos_Ajuizados_CNJ", ascending=False).head(10).set_index("UF")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(y=top10.index, x=top10["Condenacoes_CNJ"], orientation="h", name="Condenações"))
    fig3.add_trace(go.Bar(y=top10.index, x=top10["Arquivamentos_CNJ"], orientation="h", name="Arquivamentos"))
    scale2 = top10["Condenacoes_CNJ"].max() if top10["Condenacoes_CNJ"].max()>0 else 1
    fig3.add_trace(go.Scatter(y=top10.index, x=top10["Taxa_Condenacao"]*scale2, mode="lines+markers", name="Taxa condenação"))
    fig3 = standard_layout(fig3, H_LARGE, left_margin=240)
    fig3.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)


r1, r2, r3 = st.columns([1.2, 1.0, 1.0])

with r1:
    st.markdown("<div class='card'><div class='chart-title'>Variação % (2022 → 2023)</div></div>", unsafe_allow_html=True)
    df_var = df.sort_values("Variacao_Percentual")
    colors = [ACCENT if v < 0 else PRIMARY for v in df_var["Variacao_Percentual"]]
    fig4 = go.Figure(go.Bar(x=df_var["Variacao_Percentual"], y=df_var["UF"], orientation="h", marker_color=colors))
    fig4.add_vline(x=0)
    fig4 = standard_layout(fig4, H_MED, left_margin=240)
    fig4.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig4, use_container_width=True)

with r2:
    st.markdown("<div class='card'><div class='chart-title'>Taxa por 100k mulheres — Top 15</div></div>", unsafe_allow_html=True)
    top15 = df.sort_values("Taxa_100mil_Mulheres_SINESP", ascending=False).head(15)
    fig5 = go.Figure()
    for _, row in top15.iterrows():
        fig5.add_shape(type="line", x0=0, x1=row["Taxa_100mil_Mulheres_SINESP"], y0=row["UF"], y1=row["UF"], line=dict(width=6))
    fig5.add_trace(go.Scatter(x=top15["Taxa_100mil_Mulheres_SINESP"], y=top15["UF"], mode="markers"))
    med = df["Taxa_100mil_Mulheres_SINESP"].median()
    fig5.add_vline(x=med)
    fig5 = standard_layout(fig5, H_MED, left_margin=240)
    fig5.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig5, use_container_width=True)

with r3:
    st.markdown("<div class='card'><div class='chart-title'>Índice de Impunidade — distribuição por UF</div></div>", unsafe_allow_html=True)
    idx = df[["UF","Indice_Impunidade"]].sort_values("Indice_Impunidade")
    q1, q2, q3 = np.percentile(idx["Indice_Impunidade"], [25,50,75])
    def qc(v):
        if v <= q1: return "#cdeee8"
        if v <= q2: return "#9fe6dd"
        if v <= q3: return "#58d2c2"
        return PRIMARY
    colors = [qc(v) for v in idx["Indice_Impunidade"]]
    fig6 = go.Figure(go.Bar(x=idx["Indice_Impunidade"], y=idx["UF"], orientation="h", marker_color=colors))
    med_imp = idx["Indice_Impunidade"].median()
    fig6.add_vline(x=med_imp)
    fig6 = standard_layout(fig6, H_MED, left_margin=240)
    fig6.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig6, use_container_width=True)
