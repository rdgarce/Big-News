from neo4j import GraphDatabase

class Neo4jConnector:
    #Inizializza il connettore Neo4j 
    #uri (str): URI del database Neo4j.
    #auth (tuple): Tuple che contiene le credenziali di autenticazione (username, password).
    def __init__(self, uri, auth):
        self._driver = GraphDatabase.driver(uri, auth=auth)

    #Chiude la connessione al DB
    def close(self):
        self._driver.close()


    #Inserisce la tripla nel Database creando i relativi nodi o archi se non esistono
    def push_triplet(self, triplet):
        query = (
            f"MERGE (a:{triplet.category1} {{nome: $entita1}}) "
            f"MERGE (b:{triplet.category2} {{nome: $entita2}}) "
            f"MERGE (a)-[r:{triplet.relation} {{data: $data, link: $link, sentiment: $sentimento}}]->(b) "
            "ON CREATE SET r.data = $data, r.link = $link, r.sentiment = $sentimento "
            "RETURN r"
        )

        with self._driver.session() as session:
            result = session.run(query,
                                 entita1=triplet.entity1,
                                 entita2=triplet.entity2,
                                 data=triplet.data,
                                 link=triplet.link,
                                 sentimento=triplet.sentiment,
                                 categoria1=triplet.category1,
                                 categoria2=triplet.category2,
                                 relazione=triplet.relation)
            return result