import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN


st.set_page_config(page_title="Regressão", page_icon="🏥", layout="wide")

st.title('_Regressão Linear Simples - OLS_ :hospital:')
st.markdown("---")


@st.cache_data
def gerar_df():
    df = pd.read_excel('./data/variaveis_uf_ano.xlsx',
                       engine='openpyxl',
                       usecols='A:F',
                       nrows=244)
    return df


variaveis_uf_ano = gerar_df()


# gráficos de outliers

# fig1_out
cluster_df = variaveis_uf_ano[['gastos', 'valor_emendas']].copy()
dbscan = DBSCAN(eps=0.1, min_samples=5)
cluster_df['cluster'] = dbscan.fit_predict(
    cluster_df[['valor_emendas', 'gastos']])

# fig2_out
clusterpc_df = variaveis_uf_ano[['gastos_percapita', 'valor_emendas']].copy()
dbscan = DBSCAN(eps=0.1, min_samples=5)
clusterpc_df['cluster'] = dbscan.fit_predict(
    clusterpc_df[['gastos_percapita', 'valor_emendas']])


col1, col2 = st.columns(2)

with col1:
    fig1_out = px.scatter(cluster_df, x='valor_emendas', y='gastos', color='cluster', template='plotly_dark',
                          labels={'valor_emendas': 'Emendas Parlamentares',
                                  'gastos': 'Gastos Hospitalares'},
                          hover_data=['valor_emendas', 'gastos']).update_layout(
        title=dict(
            text='Verificando Existência de Outliers', font=dict(size=24)),
        title_x=0.5).update_traces(marker=dict(size=5)).update_layout(
            legend_title='Legend', showlegend=True).update_layout(
                legend=dict(title=dict(text='Cluster'))).update_layout(
                    legend_traceorder='reversed').update_xaxes(
                        showgrid=False).update_yaxes(showticklabels=False,
                                                     showgrid=False)
    st.plotly_chart(fig1_out, theme=None, use_container_width=True)


with col2:
    fig2_out = px.scatter(clusterpc_df, x='valor_emendas', y='gastos_percapita', color='cluster', template='plotly_dark',
                          labels={'valor_emendas': 'Emendas Parlamentares',
                                  'gastos_percapita': 'Gastos Hospitalares per capita'},
                          hover_data=['valor_emendas', 'gastos_percapita']).update_layout(
        title=dict(text='Verificando Existência de Outliers',
                   font=dict(size=24)), title_x=0.5).update_traces(
        marker=dict(size=5)).update_layout(
        legend_title='Legend', showlegend=True).update_layout(
        legend=dict(title=dict(text='Cluster'))).update_layout(
        legend_traceorder='reversed').update_xaxes(
        showgrid=False).update_yaxes(
        showticklabels=False, showgrid=False)
    st.plotly_chart(fig2_out, theme=None, use_container_width=True)


# regressão 1 gastos x emendas
X = variaveis_uf_ano['valor_emendas']
X = sm.add_constant(X)
y = variaveis_uf_ano['gastos']
model_gasto = sm.OLS(y, X).fit()
r2_g = model_gasto.rsquared

# regressão 2 gastos_percapita x emendas
X = variaveis_uf_ano['valor_emendas']
X = sm.add_constant(X)
y = variaveis_uf_ano['gastos_percapita']
model_gastopc = sm.OLS(y, X).fit()
r2_gpc = model_gastopc.rsquared


col3, col4 = st.columns(2)

with col3:
    fig_reg1 = px.scatter(variaveis_uf_ano, x='valor_emendas', y='gastos', trendline="ols", template='plotly_dark',
                          labels={'valor_emendas': 'Emendas Parlamentares',
                                  'gastos': 'Gastos Hospitalares'},
                          hover_data=['valor_emendas', 'gastos']).update_layout(
        title=dict(text='Regressão Linear Simples - OLS', font=dict(size=24)),
        title_x=0.5).update_xaxes(showgrid=False).update_yaxes(
        showticklabels=False, showgrid=False).add_annotation(x=0.1, y=0.9, text=f"R² = {r2_g:.2f}", showarrow=False,
                                                             xref="paper", yref="paper")
    st.plotly_chart(fig_reg1, theme=None, use_container_width=True)


with col4:
    fig_reg2 = px.scatter(variaveis_uf_ano, x='valor_emendas', y='gastos_percapita', trendline="ols", template='plotly_dark',
                          labels={'valor_emendas': 'Emendas Parlamentares',
                                  'gastos_percapita': 'Gastos Hospitalares per capita'},
                          hover_data=['valor_emendas', 'gastos_percapita']).update_layout(
        title=dict(text='Regressão Linear Simples - OLS', font=dict(size=24)),
        title_x=0.5).update_xaxes(showgrid=False).update_yaxes(
        showticklabels=False, showgrid=False).add_annotation(
        x=0.1, y=0.9, text=f"R² = {r2_gpc:.2f}", showarrow=False,
        xref="paper", yref="paper")
    st.plotly_chart(fig_reg2, theme=None, use_container_width=True)
