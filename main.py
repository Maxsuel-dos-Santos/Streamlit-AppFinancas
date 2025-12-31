import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finanças",page_icon=":moneybag:")


st.markdown("""
# Boas vindas!
            
## Esse é um aplicativo financeiro para testes 


""")

#widget de upload de dados
file_upload = st.file_uploader(label="Faça o upload dos dados aqui", type=['csv'])

if file_upload:

    exp1 = st.expander("Dados Brutos")
    exp2 = st.expander("Instituições")

    tab_data, tab_history, tab_share = exp2.tabs(["Dados","Histórico","Distribuição"])

    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

    formato_colunas = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=formato_colunas)

    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")

    with tab_data:
        st.dataframe(df_instituicao)
    
    with tab_history:
        st.line_chart(df_instituicao)
    
    with tab_share:

        date = st.selectbox("Selecione a data que deseja filtrar", options=df_instituicao.index)
        st.bar_chart(df_instituicao.loc[date])
