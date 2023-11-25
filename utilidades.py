import streamlit as st
import pandas as pd

def leitura_de_dados():
    if not 'dados' in st.session_state:
        df_lojas = pd.read_csv(r"C:\Users\Aluno\Documents\suporte\projetos\Base _de_dados\Lojas.csv",
                       sep=";",encoding="latin1", index_col="ID Loja", parse_dates=True)
        df_vendas = pd.read_excel(r"C:\Users\Aluno\Documents\suporte\projetos\Base _de_dados\Vendas.xlsx")
        dados = {'df_vendas' : df_vendas,
                 'df_lojas' : df_lojas}
        st.session_state['dados'] = dados