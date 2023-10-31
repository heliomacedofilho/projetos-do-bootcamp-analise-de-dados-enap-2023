import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Regressão", page_icon="🏥", layout="wide")
st.title('_Regressão Linear_ :hospital:')
st.markdown("---")

st.write("## mostrar os resultados da regressão")


# Layout Bootstrap
st.markdown("""
<div class="container text-center">
  <div class="row">
    """)

# Função para renderizar gráficos Plotly em colunas Bootstrap
def render_plotly_chart(chart, chart_title, chart_width=400, chart_height=400):
    st.markdown('<div class="col">', unsafe_allow_html=True)
    st.markdown(f'<h3>{chart_title}</h3>', unsafe_allow_html=True)
    st.plotly_chart(chart, use_container_width=True, width=chart_width, height=chart_height)
    st.markdown('</div>', unsafe_allow_html=True)

# Renderiza os gráficos Plotly nas colunas
scatter_chart = px.scatter(x=[1, 2, 3], y=[4, 3, 7])
bar_chart = px.bar(x=[1, 2, 3], y=[4, 3, 7])
pie_chart = px.pie(values=[5, 3, 2], names=['A', 'B', 'C'])

render_plotly_chart(scatter_chart, "Gráfico de Dispersão")
render_plotly_chart(bar_chart, "Gráfico de Barras")
render_plotly_chart(pie_chart, "Gráfico de Pizza")

# Fecha o layout Bootstrap
st.markdown("""
  </div>
</div>
""")
