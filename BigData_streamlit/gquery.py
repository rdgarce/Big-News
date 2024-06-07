from neo4j import GraphDatabase

def get_graph(conn, entity_name, start_date_str, end_date_str, selected_labels_str):
    query = (
        f"""
        MATCH (s)-[r]-(t)
        WHERE (s.nome CONTAINS '{entity_name}')
        AND r.data >= '{start_date_str}' AND r.data <= '{end_date_str}'
        AND (ANY(label IN labels(t) WHERE label IN [{selected_labels_str}]))
        RETURN s, r, t, properties(r) as attributi_relazione,
        labels(s) as label_e1, labels(t) as label_e2
        LIMIT 100
        """
    )

    with conn.session() as session:
        result = session.run(query)
        return result.data()
    
def get_full_graph(conn):
    query = (
        """
        MATCH (s)-[r]-(t)
        RETURN s, r, t, properties(r) as attributi_relazione,
        labels(s) as label_e1, labels(t) as label_e2
        LIMIT 120
        """
    )

    with conn.session() as session:
        result = session.run(query)
        return result.data()
    


def get_nodi_connessi_mese_anno(conn, anno, mese):
    mese_str = f"{anno}-{mese:02}"  # Formatta il mese come "YYYY-MM"
    query = (
        f"""
        MATCH (s)-[r]-(t)
        WHERE r.data STARTS WITH '{mese_str}'
        AND s.nome =~ '^[A-Z].*'  // Assicura che il nome del nodo inizi con una lettera maiuscola
        RETURN s.nome as nome_nodo, COUNT(r) as connessioni , labels(s) as categoria
        ORDER BY connessioni DESC
        LIMIT 10
        """
    )

    with conn.session() as session:
        result = session.run(query)
        return [(record["nome_nodo"], record["connessioni"],record["categoria"]) for record in result]

def get_graph_statistics(driver):
    # La query Cypher
    query = """
    // Numero totale di nodi
    MATCH (n)
    RETURN 'Numero totale di nodi' AS tipo, count(n) AS conteggio
    UNION

    // Numero totale di relazioni
    MATCH ()-[r]->()
    RETURN 'Numero totale di relazioni' AS tipo, count(r) AS conteggio
    UNION

    // Numero di occorrenze per ciascuna categoria di nodo
    MATCH (n)
    RETURN labels(n) AS tipo, count(n) AS conteggio
    UNION

    // Numero di occorrenze per ciascun tipo di relazione
    MATCH ()-[r]->()
    RETURN type(r) AS tipo, count(r) AS conteggio
    """

    # Funzione per eseguire la query
    def execute_query(tx):
        return list(tx.run(query))

    # Connettersi al database e eseguire la query
    with driver.session() as session:
        results = session.read_transaction(execute_query)
        return results

