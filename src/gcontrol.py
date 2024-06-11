from neo4j import GraphDatabase

    #Inserisce la tripla nel Database creando i relativi nodi o archi se non esistono
def push_triplet(conn, triplet):
    query = (
        f"MERGE (a:{triplet.category1} {{nome: $entita1}}) "
        f"MERGE (b:{triplet.category2} {{nome: $entita2}}) "
        f"MERGE (a)-[r:{triplet.relation} {{data: $data, link: $link, sentiment: $sentimento}}]->(b) "
        "ON CREATE SET r.data = $data, r.link = $link, r.sentiment = $sentimento "
        "RETURN r"
    )

    with conn.session() as session:
        result = session.run(query,
                             entita1=triplet.entity1,
                             entita2=triplet.entity2,
                             data=triplet.data,
                             link=triplet.link,
                             sentimento=triplet.sentiment)
    return result