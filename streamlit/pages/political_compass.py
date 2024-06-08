import streamlit as st
from neo4j import GraphDatabase
from credentials import *
from gquery import get_all_entities_name, get_all_sentimental_rels, get_sentimental_entities
import pandas as pd

def main():
    st.header('Political compass', divider='blue')
    conn = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
    
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        avlbl_rels = get_all_sentimental_rels(conn)
        slctd_rel = st.selectbox(
        "Seleziona la relazione che desideri analizzare",
        avlbl_rels)

    with col2:
        avlbl_entities = get_all_entities_name(conn)
        slctd_entity = st.selectbox(
        "Seleziona l'entità che desideri analizzare",
        avlbl_entities)

    data = get_sentimental_entities(conn, slctd_entity, slctd_rel)
    names = [item['nome'] for item in data]
    sentiments = [item['sentiment'] for item in data]

    df = pd.DataFrame(list(zip(names, sentiments)), columns=['Nome', 'Sentiment'])

    st.scatter_chart(df, x='Nome', y='Sentiment')

if __name__ == "__main__":
    main()