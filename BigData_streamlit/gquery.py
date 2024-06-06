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
    


def get_nodi_connessi_mese_anno(conn, tipo_nodo, anno, mese):
    mese_str = f"{anno}-{mese:02}"  # Formatta il mese come "YYYY-MM"
    query = (
        f"""
        MATCH (s)-[r]-(t)
        WHERE ANY(label IN labels(t) WHERE label = '{tipo_nodo}')
        AND r.data STARTS WITH '{mese_str}'
        RETURN s.nome as nome_nodo, COUNT(r) as connessioni
        ORDER BY connessioni DESC
        LIMIT 5
        """
    )

    with conn.session() as session:
        result = session.run(query)
        return [record["nome_nodo"] for record in result]

