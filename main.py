import streamlit as st
import plotly.express as px
from seeders.importar_csv import importar_csv

dados = importar_csv("seeders/dados_car.csv")

st.set_page_config(page_title="IntegraCAR - Dashboard", page_icon="logo_total_semfundo.png", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
            
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        color: #2373B7;
        font-weight: 600;
    }

    /* Selectbox - borda quando ativo/focado */
    [data-baseweb="select"] > div:focus-within {
        border-color: #2373B7 !important;
        box-shadow: 0 0 0 1px #2373B7 !important;
    }

    /* Botões */
    [data-testid="baseButton-secondary"] {
        background-color: #2373B7;
        color: white;
        border: none;
        transition: background-color 0.3s, color 0.3s;
    }
            
    [data-testid="baseButton-secondary"]:hover {
        background-color: #8BB7C5;
        color: black;
        border: none;
    }

    /* Botão quando clicado/ativo */
    [data-testid="baseButton-secondary"]:active {
        border: 2px solid #2373B7 !important;
        background-color: #1a5a8f;
        transform: scale(0.98);
    }

    /* Download button */
    [data-testid="baseButton-primary"] {
        background-color: #EB9CB4;
        color: white;
        border: none;
    }

    [data-testid="baseButton-primary"]:hover {
        background-color: #d88ba1;
        border: none;
    }

    [data-testid="baseButton-primary"]:active {
        border: 2px solid #EB9CB4 !important;
        background-color: #c57a8e;
        transform: scale(0.98);
    }
</style>
""", unsafe_allow_html=True)

#Cabeçalho
col1, col2 = st.columns([5,8])
with col1:
    st.image("logo_total_semfundo.png", width=150)
with col2:
    st.title("IntegraCAR - Dashboard")

# Filtros
col1, col2, col3, col4 = st.columns(4)

with col1:
    campus_options = ["Todos"] + sorted(dados["Campus de Atuação"].unique().tolist())
    campi = st.selectbox("Campus", campus_options, key='campus_select')

with col2:
    municipio_options = ["Todos"] + sorted(dados["3) Município onde reside:"].unique().tolist())
    municipios = st.selectbox("Município", municipio_options, key='municipio_select')

with col3:
    bolsista_options = ["Todos"] + sorted(dados["6) Função exercida no Projeto IntegraCAR:"].unique().tolist())
    bolsistas = st.selectbox("Função", bolsista_options, key='funcao_select')

with col4:
    st.write("")
    st.write("")
    if st.button("Limpar filtros"):
        if 'campus_select' in st.session_state:
            del st.session_state['campus_select']
        if 'municipio_select' in st.session_state:
            del st.session_state['municipio_select']
        if 'funcao_select' in st.session_state:
            del st.session_state['funcao_select']
        st.rerun()


#Aplicar filtros
dados_filtrados = dados.copy()

if campi != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Campus de Atuação"] == campi]
    
if municipios != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["3) Município onde reside:"] == municipios]

if bolsistas != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["6) Função exercida no Projeto IntegraCAR:"] == bolsistas]


# Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("TOTAL DE REGISTROS", len(dados_filtrados))

with col2:
    st.metric("CAMPI", dados_filtrados["Campus de Atuação"].nunique())

with col3:
    st.metric("MUNICÍPIOS", dados_filtrados["3) Município onde reside:"].nunique())

with col4:
    bolsistas_count = len(dados[dados["6) Função exercida no Projeto IntegraCAR:"].str.contains("Orientador", case=False, na=False)])
    st.metric("BOLSISTAS CAR", bolsistas_count)

st.divider()


# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Registros por Campus")
    registros_campus = dados_filtrados["Campus de Atuação"].value_counts().reset_index()
    registros_campus.columns = ["Campus", "Quantidade"]
    registros_campus = registros_campus.sort_values("Quantidade", ascending=False)

    fig_campus = px.bar(
        registros_campus,
        x="Campus",
        y="Quantidade",
        color_discrete_sequence=["#2373B7"]
    )

    fig_campus.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=400,
        xaxis={'tickangle': -45}
    )

    st.plotly_chart(fig_campus, use_container_width=True)

with col2:
    st.subheader("Registros por Município")
    registros_municipio = dados_filtrados["3) Município onde reside:"].value_counts().head(10).reset_index()
    registros_municipio.columns = ["Município", "Quantidade"]
    registros_municipio = registros_municipio.sort_values("Quantidade", ascending=False)

    fig_municipio = px.bar(
        registros_municipio,
        x="Município",
        y="Quantidade",
        color_discrete_sequence=["#8BB7C5"]
    )

    fig_municipio.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=400,
        xaxis={'tickangle': -45}
    )

    st.plotly_chart(fig_municipio, use_container_width=True)

st.divider()

st.subheader("Distribuição por Função")
registros_funcao = dados_filtrados["6) Função exercida no Projeto IntegraCAR:"].value_counts().reset_index()
registros_funcao.columns = ["Função", "Quantidade"]

fig_funcao = px.pie(
    registros_funcao,
    values="Quantidade",
    names="Função",
    color_discrete_sequence=["#2373B7", "#8BB7C5", "#EB9CB4", "#E8CBD4", "#A8D5E2"],
    hole=0.4
)

fig_funcao.update_traces(
    textposition='inside',
    textinfo='percent+label',
    textfont_size=12
)

fig_funcao.update_layout(
    height=500,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig_funcao, use_container_width=True)

st.divider()

# Tabela de dados
st.subheader("Base Completa")

col1, col2 = st.columns([4, 1])
with col2:
    csv = dados_filtrados.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="Exportar CSV",
        data=csv,
        file_name=f"integracar_dados.csv",
        mime="text/csv",
        use_container_width=True
    )

st.dataframe(
    dados_filtrados,
    use_container_width=True,
    hide_index=True,
    height=400
)

st.caption(f"Exibindo {len(dados_filtrados)} registros de {len(dados)} totais")