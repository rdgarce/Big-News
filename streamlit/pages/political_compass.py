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
        avlbl_entities = get_all_entities_name(conn)
        slctd_entity = st.selectbox(
        "Seleziona l'entità che desideri analizzare",
        avlbl_entities)

    with col2:
        avlbl_rels = get_all_sentimental_rels(conn)
        slctd_rel = st.selectbox(
        "Seleziona l'entità che desideri analizzare",
        avlbl_rels)

    data = get_sentimental_entities(conn, slctd_entity, slctd_rel)
    print(data)
    sentiments = [x['sentiment'] for x in data]
    names = [x['nome'] for x in data]
    print(sentiments)
    print(names)
    d = list(zip(names, sentiments))
    print(d)
    chart_data = pd.DataFrame(d)
    st.scatter_chart(data=([1,2,3,4],[1,2,3,4]),)

if __name__ == "__main__":
    main()