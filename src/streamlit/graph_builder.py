import datetime
from pyvis.network import Network
from gquery import *

colori_labels = {
    'Persona': '#7fa7c9',  
    'Città': '#ff8a66',  
    'Località': '#99ffab',  
    'Data_o_Periodo_Temporale': '#99abff',  
    'Misura_o_Quantità': '#ff99ff',  
    'Prodotto_o_Servizio': '#99ffeb',  
    'Evento': '#ffc266',  
    'Legge,_Regolamento_o_Programma_Politico': '#99e6ff',  
    'Settore_Economico': '#ffe699',  
    'Risorsa_Naturale': '#99ccff',  
    'Entità_Governativa': '#ff6680',  
    'Infrastruttura': '#99ffcc',  
    'Tecnologia': '#ffa366',  
    'Incidente_o_Crisi': '#99ff80'
}

def build_graph(driver,entity_name, start_date_str, end_date_str, selected_labels_str,layout_method):
    
    data = get_graph(driver, entity_name, start_date_str, end_date_str, selected_labels_str)
    net = Network(notebook=True,height='380px', width='100%')

    for record in data:
        source = record['s']['nome'] if 'nome' in record['s'] else str(record['s'].id)
        target = record['t']['nome'] if 'nome' in record['t'] else str(record['t'].id)
        relationship = record['r'][1]
        attributi_relazione = record['attributi_relazione']
        label_e1 = record['label_e1'][0] if 'label_e1' in record else None
        label_e2 = record['label_e2'][0] if 'label_e2' in record else None
    
        # Usa il colore corrispondente all'etichetta del nodo
        colore_source = colori_labels.get(label_e1, 'gray')  # Se l'etichetta non è presente, usa un colore predefinito
        colore_target = colori_labels.get(label_e2, 'gray')
        #st.write(attributi_relazione)
        if attributi_relazione["sentiment"] == 0:
            risultato = "Sentimento Neutro"
        elif attributi_relazione["sentiment"] == 1:
            risultato = "Sentimento Positivo"
        elif attributi_relazione["sentiment"] == -1:
            risultato = "Sentimento Negativo"
        preview=attributi_relazione["link"]+"\n"+attributi_relazione["data"]+"\n"+risultato
    
        net.add_node(source, label=source, color=colore_source,title=str(label_e1),borderWidth=0)
        net.add_node(target, label=target, color=colore_target,title=str(label_e2),borderWidth=0)
        net.add_edge(source, target, label=relationship, title=preview)

    #Layout di visualizzazione del Grafo
    if layout_method == "force_atlas_2based":
        net.force_atlas_2based(gravity=-50,node_distance=150, central_gravity=0.00009, spring_length=200, spring_strength=0.08, damping=0.4, overlap=0)
    elif layout_method == "hrepulsion":
        net.hrepulsion(node_distance=120, central_gravity=0.0, spring_length=100, spring_strength=0.01, damping=0.09)
    
    return net,data


def build_full_graph(neo4j_uri,neo4j_user,neo4j_pass,layout_method):
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        data = get_full_graph(driver)
    driver.close()
    net = Network(notebook=True,height='380px', width='100%')

    for record in data:
        source = record['s']['nome'] if 'nome' in record['s'] else str(record['s'].id)
        target = record['t']['nome'] if 'nome' in record['t'] else str(record['t'].id)
        relationship = record['r'][1]
        attributi_relazione = record['attributi_relazione']
        label_e1 = record['label_e1'][0] if 'label_e1' in record else None
        label_e2 = record['label_e2'][0] if 'label_e2' in record else None
    
        # Usa il colore corrispondente all'etichetta del nodo
        colore_source = colori_labels.get(label_e1, 'gray')  # Se l'etichetta non è presente, usa un colore predefinito
        colore_target = colori_labels.get(label_e2, 'gray')
        #st.write(attributi_relazione)
        if attributi_relazione["sentiment"] == 0:
            risultato = "Sentimento Neutro"
        elif attributi_relazione["sentiment"] == 1:
            risultato = "Sentimento Positivo"
        elif attributi_relazione["sentiment"] == -1:
            risultato = "Sentimento Negativo"
        preview=attributi_relazione["link"]+"\n"+attributi_relazione["data"]+"\n"+risultato
    
        net.add_node(source, label=source, color=colore_source,title=str(label_e1),borderWidth=0)
        net.add_node(target, label=target, color=colore_target,title=str(label_e2),borderWidth=0)
        net.add_edge(source, target, label=relationship, title=preview)

    #Layout di visualizzazione del Grafo
    if layout_method == "force_atlas_2based":
        net.force_atlas_2based(gravity=-50,node_distance=120, central_gravity=0.09, spring_length=100, spring_strength=0.08, damping=0.4, overlap=0)
    elif layout_method == "hrepulsion":
        net.hrepulsion(node_distance=120, central_gravity=0.0, spring_length=100, spring_strength=0.01, damping=0.09)
    
    return net