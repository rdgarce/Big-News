import streamlit as st
from neo4j import GraphDatabase
from credentials import *
from gquery import get_all_entities_name, get_all_sentimental_rels, get_sentimental_entities
import pandas as pd

def main():
    st.header('Political Compass :compass:', divider='blue')
    st.markdown("""Il Political Compass consente di visualizzare il sentimento provato dalle entità per ad un'entità target rispetto ad una specifica relazione.
                Attraverso la selezione di una coppia relazione ed entità target, viene visualizzato un grafico che quantifica, per ogni entità collegata a quella target, il sentimento calcolato in base al numero di volta che la relazione è stata identificata in senso positivo o negativo.
                Qualora vengano visualizzare delle entità con dei sentimenti sarà possibile visionare una tabella che riporta i link agli articoli dove sono state individuate tali relazioni.
                """)
    
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
        "Seleziona l'entità target che desideri analizzare",
        avlbl_entities)

    names, sentiments, links = get_sentimental_entities(conn, slctd_entity, slctd_rel)

    df = pd.DataFrame(list(zip(names, sentiments)), columns=['Nome', 'Sentiment'])
    st.scatter_chart(df, x='Nome', y='Sentiment')

    table_data = list(zip(names, links))
    if table_data:
        data_frame = pd.DataFrame(table_data, columns=["Nome", "Link"]).explode("Link")
        st.dataframe(data_frame)

if __name__ == "__main__":
    main()