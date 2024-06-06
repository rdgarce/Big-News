import streamlit as st
from streamlit.components.v1 import html
import datetime
from gquery import *
from graph_builder import *
from credentials import *

import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
available_labels = list(colori_labels.keys())

# Configura la connessione al database Neo4j
spec= [0.7, 0.3]
st.columns(spec)
col1, col2 = st.columns([1, 3])
st.title("ciao")













def main():
    st.title("Benvenuti")
    html_file_path = "full_graph.html"
    st.header('Grafo Completo', divider='blue')


    with open(html_file_path, "r") as f:
        html_content = f.read()

    container_graph = st.container(border=False)
    layout_method = st.radio("Layout del grafo:", ("forceatlas_2based", "hrepulsion"))
    net=build_full_graph(neo4j_uri,neo4j_user,neo4j_pass,layout_method)
    net.show(html_file_path)
    # Visualizzazione dell'HTML
    with container_graph:
        with open(html_file_path, "r") as f:
            html_content = f.read()
        st.components.v1.html(html_content,height=390)
if __name__ == "__main__":
    main()
