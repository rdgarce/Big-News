import streamlit as st
from streamlit.components.v1 import html
from datetime import date, date
import time
from gquery import *
from graph_builder import *
from credentials import *
import pandas as pd
import plotly.express as px

import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
available_labels = list(colori_labels.keys())

# Configura la connessione al database Neo4j
spec= [0.7, 0.3]
st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 3])




def get_statistiche(driver):
    results = get_graph_statistics(driver)

    total_nodes = None
    total_relationships = None
    node_categories = {}
    relationship_types = {}

    for record in results:
        tipo = record["tipo"]
        conteggio = record["conteggio"]
        if tipo == "Numero totale di nodi":
            total_nodes = conteggio
        elif tipo == "Numero totale di relazioni":
            total_relationships = conteggio
        elif isinstance(tipo, list):  # Etichette dei nodi
            category_key = ', '.join(tipo)
            node_categories[category_key] = conteggio
        else:  # Tipi di relazioni
            relationship_types[tipo] = conteggio
    
    return total_nodes,total_relationships,node_categories,relationship_types



def main():
    st.title("Benvenuto")
    col1,col2=st.columns([0.28,0.72])
    with col1:
        st.image('logo.png')
    with col2:
        st.write("""
            Questa Dashboard consente di esplorare dinamiche di geopolitica internazionale, fornendo strumenti per l'analisi e la visualizzazione delle informazioni contenute in un Knowledge Graph costruito attraverso l'estrazione di Entità e Relazioni da testi di articoli di news in lingua italiana.
            
            La HomePage offre:
            - Statistiche sommarie sullo stato attuale del Grafo di conoscenza.
            - Rappresentazione parziale dello stato attuale del grafo.
            - Strumento per visualizzare le Entità più citate al variare dei mesi.
        """)

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))

    st.header('Statistiche generali', divider='blue')
    color_sequence = px.colors.qualitative.Pastel

    html_file_path = "full_graph.html"
    total_nodes,total_relationships,node_categories,relationship_types=get_statistiche(driver)

    col1,col2,col3=st.columns([0.3,0.3,0.3])
    with col1:
        st.subheader(f'''Numero totale di Istanze: :green[{total_nodes+total_relationships}]''')
    with col2:
        st.subheader(f'''Numero totale di Entità: :blue[{total_nodes}]''')
    with col3:
        st.subheader(f'''Numero totale di Relazioni: :red[{total_relationships}]''')
    

    col1,col2=st.columns([0.5,0.5])
    with col1:
        if node_categories:
            categories = list(node_categories.keys())
            counts = list(node_categories.values())
            fig = px.pie(values=counts, names=categories, title='Distribuzione delle Categorie delle Entità', 
                        color_discrete_sequence=color_sequence)
            st.plotly_chart(fig)

    with col2:
        if relationship_types:
            # Raggruppa le categorie minoritarie sotto "Altro"
            sorted_rel_types = sorted(relationship_types.items(), key=lambda item: item[1], reverse=True)
            main_rel_types = {k: v for k, v in sorted_rel_types if v >= 5}  # Adjust the threshold as needed
            other_count = sum(v for k, v in sorted_rel_types if v < 5)
            if other_count > 0:
                main_rel_types["Altro"] = other_count

            rel_types = list(main_rel_types.keys())
            counts = list(main_rel_types.values())
            fig = px.bar(x=rel_types, y=counts, title='Distribuzione delle Relazioni',
                        labels={'x': 'Tipo di Relazione', 'y': 'Occorrenze'},
                        color_discrete_sequence=color_sequence)
            st.plotly_chart(fig)

    with open(html_file_path, "r") as f:
        html_content = f.read()

    st.header('Preview del Grafo', divider='blue')
    col1,col2=st.columns([0.8,0.2])
    with col1:
        container_graph = st.container(border=False)
    with col2:
        layout_method = st.radio("Layout del grafo:", ("forceatlas_2based", "hrepulsion"))
        st.write("La Preview di questa pagina mostra solamente 120 nodi del grafo")
    net=build_full_graph(neo4j_uri,neo4j_user,neo4j_pass,layout_method)
    net.show(html_file_path)

    st.header('Top 10 Entità più citate per mese', divider='blue')

    start_date = date(2022, 9, 1)
    end_date = date.today()

    # Slider per selezionare la data
    selected_date = st.slider('Seleziona mese e anno', min_value=start_date, max_value=end_date, value=date(2023, 9, 1), format="MMM YYYY")

    # Estrai anno e mese dalla data selezionata
    selected_year = selected_date.year
    selected_month = selected_date.month



    with driver.session() as session:
        nodi_connessi = get_nodi_connessi_mese_anno(driver, selected_year, selected_month)
    #driver.close()

    
    df = pd.DataFrame(nodi_connessi, columns=['Nome Nodo', 'Connessioni', 'Categoria'])
    df = df.sort_values(by='Connessioni', ascending=False)
    # Visualizza il grafico a barre orizzontali
    st.bar_chart(df.set_index('Nome Nodo')['Connessioni'], use_container_width=True, color="#95e6be")
    
        
    # Visualizzazione dell'HTML
    with container_graph:
        with open(html_file_path, "r") as f:
            html_content = f.read()
        with st.spinner('Caricamento del grafo...'):
            time.sleep(1)
        st.components.v1.html(html_content,height=390)
if __name__ == "__main__":
    main()
