import streamlit as st
from streamlit.components.v1 import html
import datetime
from gquery import *
from graph_builder import *
from credentials import *
from pyvis.network import Network
import time


def main():
    html_file_path = "filtered_graph.html"
    st.header('Graph Builder', divider='blue')
    available_labels = list(colori_labels.keys())
    # Lettura del contenuto del file HTML
    with open(html_file_path, "r") as f:
        html_content = f.read()

    # Definire il range di date per il double ended slider
    start_date = datetime.date(2022, 9, 3)
    end_date = datetime.date.today()

    #entity_name = st.text_input("Inserisci il nome dell'entità:")
    col1,col2=st.columns([3,5])
    with col1:
        entity_name = st.text_input("Inserisci il nome dell'entità che vuoi cercare:")
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


    net=build_graph(neo4j_uri,neo4j_user,neo4j_pass,entity_name, start_date_str, end_date_str, selected_labels_str,layout_method)
    net.show(html_file_path)
    # Visualizzazione dell'HTML
    with container_graph:
        with open(html_file_path, "r") as f:
            html_content = f.read()
        st.components.v1.html(html_content,height=390)

if __name__ == "__main__":
    main()