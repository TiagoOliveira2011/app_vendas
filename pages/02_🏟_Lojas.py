import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Lojas", page_icon="🏟", layout="wide")

# Leitura de dados de utilidades
leitura_de_dados()

# Carregar DataFrames da sessão
df_vendas = st.session_state['dados']['df_vendas']
df_lojas = st.session_state['dados']['df_lojas']

df_data = pd.merge(df_vendas, df_lojas, on= "ID Loja", how= "left")
df_data = df_data.reset_index()

df_data = df_data.drop(['Código Venda', 'ID Loja'], axis=1)

lojas = df_lojas['Loja'].unique()
loja = st.sidebar.selectbox("loja",lojas)

st.markdown(f"# {loja}")
st.divider()

# Linha de código para filtro
df_data_filtered = df_data[df_data["Loja"] == loja]

#cálculo de faturamento total e médio para todos od dados e a loja selecionada
faturamento_total = df_data['Valor Final'].sum()
quantidade_total = df_data['Quantidade'].sum()
tkt_medio_total = faturamento_total / quantidade_total

faturamento_loja = df_data_filtered['Valor Final'].sum()
quantidade_loja = df_data_filtered['Quantidade'].sum()
tkt_medio_loja = faturamento_loja / quantidade_loja

col1, col2 = st.columns(2)
col1.markdown(f"##### Faturamento Grupo R$: {faturamento_total/1000:.2f} milhões")
col2.markdown(f"##### Ticket Médio R$: {tkt_medio_total:.2f}") 

col3, col4 = st.columns(2)
col3.markdown(f"##### Faturamento Loja R$: {faturamento_loja/1000:.2f} milhões")
col4.markdown(f"##### Ticket Médio R$: {tkt_medio_loja:.2f}")

st.divider()   

# Converte  e formata dados temporais 
df_data_filtered['Data'] = pd.to_datetime(df_data_filtered['Data'], format='%d%m%Y')
df_data_filtered['Mês/Ano'] = df_data_filtered['Data'].dt.to_period('M')
df_data_filtered['Mês/Ano'] = df_data_filtered['Mês/Ano'].dt.strftime("%Y-%m") 

# Agrupo dados po mês/ano e calcula faturamento mensal
df_faturamento_mensal = df_data_filtered.groupby('Mês/Ano')['Valor Final'].sum().reset_index()

# Criar gráfico de limha utilizando plotly express
fig = px.line(df_faturamento_mensal, x='Mês/Ano', y='Valor Final', title=f'Faturamento Mensalda Loja {loja}') 
fig.update_xaxes(title_text='Mês/Ano')   
fig.update_yaxes(title_text='Faturamento')  

#Exibe o gráfico no aplicativo
st.plotly_chart(fig)

st.divider()

st.dataframe(df_data)

