import streamlit as st
from streamlit.components.v1 import html
from datetime import datetime, date
from gquery import *
from graph_builder import *
from credentials import *
from pyvis.network import Network
import pandas as pd
import time

def get_record_data(record):
    source = record['s']['nome'] if 'nome' in record['s'] else str(record['s']['id'])
    target = record['t']['nome'] if 'nome' in record['t'] else str(record['t']['id'])
    relationship = record['r'][1]
    attributi_relazione = record['attributi_relazione']
    label_e1 = record['label_e1'][0] if 'label_e1' in record else None
    label_e2 = record['label_e2'][0] if 'label_e2' in record else None

    if attributi_relazione["sentiment"] == 0:
        risultato = "Sentimento Neutro"
    elif attributi_relazione["sentiment"] == 1:
        risultato = "Sentimento Positivo"
    elif attributi_relazione["sentiment"] == -1:
        risultato = "Sentimento Negativo"

    return {
        'Source': source,
        'Target': target,
        'Relationship': relationship,
        'Link': attributi_relazione["link"],
        'Date': attributi_relazione["data"],
        'Sentiment': risultato,
    }

def main():
    

    html_file_path = "filtered_graph.html"
    st.header('Graph Explorer :ringed_planet:', divider='blue')
    st.markdown("""Questa pagina consente di costruire dinamicamente un grafo selezionando un nodo radice, un intervallo temporale di pubblicazione delle notizie e un insieme di categorie di entità con cui si vogliono cercare le relazioni.
I nodi del grafo sono interattivi e sulle relazioni è possibile visualizzare la data e il link dell'articolo originale da cui proviene l'informazione. Viene inoltre fornita una visualizzazione alternativa tabellare delle informazioni rappresentate nel grafo costruito.
""")
    
    available_labels = list(colori_labels.keys())
    # Lettura del contenuto del file HTML
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
    with open(html_file_path, "r") as f:
        html_content = f.read()

    # Definire il range di date per il double ended slider
    start_date = date(2022, 9, 3)
    end_date = date.today()

    #entity_name = st.text_input("Inserisci il nome dell'entità:")
    col1,col2=st.columns([3,5])
    with col1:
        avlbl_entity = get_all_entities_name(driver)
        entity_name = st.selectbox(
        "Seleziona l'entità che desideri analizzare",
        avlbl_entity)
    with col2:
        selected_date_range = st.slider("Seleziona intervallo di date di pubblicazione degli articoli", start_date, end_date, (start_date, end_date))


    container_graph = st.container(border=False)


    col1,col2=st.columns([3,1])
    with col1:
        selected_labels = st.multiselect("Seleziona le categorie (etichette) con cui vuoi vedere i collegamenti", available_labels)

    with col2:
        layout_method = st.radio("Layout del grafo:", ("forceatlas_2based", "hrepulsion"))

    

    
    # Convertire le date selezionate in formato stringa
    start_date_str = selected_date_range[0].strftime("%Y-%m-%d")
    end_date_str = selected_date_range[1].strftime("%Y-%m-%d")
    # Conversione delle labels in stringhe
    selected_labels_str = ', '.join([f"'{label}'" for label in selected_labels])


    net,data=build_graph(driver,entity_name, start_date_str, end_date_str, selected_labels_str,layout_method)
    net.show(html_file_path)
    # Visualizzazione dell'HTML
    with container_graph:
        with open(html_file_path, "r") as f:
            html_content = f.read()
        st.components.v1.html(html_content,height=390)
    if data:
        data2 = [get_record_data(record) for record in data]
        df = pd.DataFrame(data2)

        # Mostra la tabella in Streamlit
        st.subheader("Triple(Entità1, Relazione, Entità2) estratte", divider='blue')
        st.dataframe(df)


if __name__ == "__main__":
    main()