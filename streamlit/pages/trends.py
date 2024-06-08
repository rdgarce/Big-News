import streamlit as st
from datetime import datetime
from neo4j import GraphDatabase
from gquery import get_all_entities_name, get_monthly_count_by_name
from credentials import *
import pandas as pd

def main():
    st.header('Trend view :chart_with_upwards_trend:', divider='blue')
    st.markdown(""" Questa pagina consente di selezionare un'entità presente nel database e visualizzare l'andamento temporale delle citazioni negli articoli riferite ad essa.""")
    conn = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
    avlbl_entity = get_all_entities_name(conn)
    slctd_entity = st.selectbox(
    "Seleziona l'entità che desideri analizzare",
    avlbl_entity)

    start_date = datetime(2022, 9, 1)
    end_date = datetime.today()

    data = get_monthly_count_by_name(conn, slctd_entity, start_date, end_date)
    # Convert data to DataFrame
    if data:
        df = pd.DataFrame(data)
        # Convert 'month' to datetime and set as index
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)
        st.bar_chart(df)


if __name__ == "__main__":
    main()