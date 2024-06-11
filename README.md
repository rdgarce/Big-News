# Big News

Sistema Pipelined di big data per l'analisi di articoli di geopolitica in lingua italiana.

## Struttura delle cartelle

- src: contiene i sorgenti di tutto il progetto
- deploy: contiene dei notebook python per lanciare facilmente in cloud i componenti NER/RE e NER/RE Backup

## Come avviare il sistema

Tutti i componenti del sistema assumono la presenza di variabili d'ambiente contenenti gli accessi ai provider Redis e Neo4j. Per avviare correttamente i componenti del sistema:

- Collector node: per avviare un collector node, eseguire `./src/collector.sh`.
- Streamlit server: per avviare il server di presentazione, eseguire `./streamlit/start_server.sh`.
- NER/RE Engine (Backup): per avviare questi componenti si consiglia l'utilizzo dei notebook presenti nella cartella deploy