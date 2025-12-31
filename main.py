import streamlit as st
import pandas as pd

def calc_general_stats(df):
    #agrupando por data e somando os valores
    df_data = df.groupby(by="Data")[["Valor"]].sum()

    #jogando a coluna de valor uma linha para baixo
    df_data["lag_1"] = df_data["Valor"].shift(1)

    #diferenca mensal
    df_data["Diferença Mensal"] = df_data["Valor"]-df_data["lag_1"]

    #media de 6 meses
    df_data["Média 6M Diferença Mensal"] = df_data["Diferença Mensal"].rolling(6).mean()

    #media de 12 meses
    df_data["Média 12M Diferença Mensal"] = df_data["Diferença Mensal"].rolling(12).mean()

    #media de 24 meses
    df_data["Média 6M Diferença Mensal"] = df_data["Diferença Mensal"].rolling(24).mean()

    df_data["Diferença mensal %"] =df_data["Valor"] / df_data["lag_1"] - 1

    df_data = df_data.drop("lag_1", axis=1)

    return df_data

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

    df_stats = calc_general_stats(df)

    columns_config = {
        "Diferença Mensal": st.column_config.NumberColumn("Diferença Mensal", format="R$ %.2f"),
        "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        "Média 6M Diferença Mensal": st.column_config.NumberColumn( "Média 6M Diferença Mensal", format="R$ %.2f"),
        "Média 12M Diferença Mensal": st.column_config.NumberColumn("Média 12M Diferença Mensal", format="R$ %.2f"),
        "Média 6M Diferença Mensal": st.column_config.NumberColumn( "Média 6M Diferença Mensal", format="R$ %.2f"),
        "Diferença mensal %": st.column_config.NumberColumn( "Diferença mensal %", format="percent")
    }
    
    st.dataframe(df_stats,column_config=columns_config)