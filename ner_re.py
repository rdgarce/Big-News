import torch
import gc
import transformers
import re
import os
from article import ATCqueue
from redis import Redis
from tabulate import tabulate
from tqdm import tqdm
from liste import *
from gcontrol import *
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# Classe istanza della tripla
class Instance:
    def __init__(self, entity1, category1, relation,sentiment, entity2, category2, data, link):
        self.entity1 = entity1.strip()
        self.category1 = category1.strip()
        self.relation = relation.strip()
        self.entity2 = entity2.strip()
        self.category2 = category2.strip()
        self.data = data
        self.link = link
        self.sentiment=sentiment

# Funzione per filtrare le triple raw
def filtra_righe(string):
    lines = string.splitlines()
    filtered_lines = [line for line in lines if line.strip().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
                      and line.strip().endswith(')') and line.count(',') == 2]
    return '\n'.join(filtered_lines)


# Funzione per filtrare le triple categorizzate
def filtra_righe_categorie(string):
    lines = string.splitlines()
    filtered_lines = [line for line in lines if line.strip().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
                      and line.strip().endswith(')')
                      and line.count(',') == 2
                      and line.count('[') == 2
                      and line.count(']') == 2]
    return '\n'.join(filtered_lines)

# Funzione per sostituire la parola con la coppia e restituire il valore
def sostituisci_coppia_sentimento(parola):
    if parola in dizionario:
        return dizionario[parola]
    else:
        return [parola, 0]

# Crea una pipeline per la generazione del testo utilizzando il modello LLM
pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    # The quantization line
    model_kwargs={"torch_dtype": torch.bfloat16, "load_in_4bit": True}
)

# Token di terminazione utilizzati per la generazione del testo
terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]


# Funzione per la generazione del testo 
def generate_text(messages,temp=0.6):
    prompt = pipeline.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Applica la pipeline al prompt
    outputs = pipeline(
        prompt,
        max_new_tokens=350,   
        eos_token_id=terminators,
        do_sample=True,
        temperature=temp,
        top_p=0.9,
    )

    # Restituisce il testo generato, escludendo il prompt
    generated_text = outputs[0]["generated_text"][len(prompt):]
    return generated_text.strip()  # Rimuove eventuali spazi bianchi in eccesso

# Funzione di generazione della tripla dato il testo e l'elenco di relazioni consentite
def genera_tripla(stringa):
    messages = [
    {"role": "system", "content": "Answer questions"},
    {"role": "user", "content": f"""Estrapola da questo testo delle triple numerate composte da : (entità1,verbo all'infinito,entità2) .
    Il primo elemento di ciascuna tripla non può rigorosamente essere un verbo o un avverbio e non può contenere virgole.
    Il secondo elemento di ciascuna tripla può essere esclusivamente un concetto contenuto nel seguente elenco:
    {relations_list}
    Il terzo elemento di ciascuna tripla non può rigorosamente essere un verbo o un avverbio e non può contenere virgole.
    Le triple estratte devono riguardare concetti rilevanti, le entità non devono essere troppo generiche.
     Esempio dell'output che mi dovrai rigorosamente fornire considerando anche le parentesi , non mostrarmi risultati senza questa struttura:
     1 (Marco,essere,artista)
     2 (Luca,mangia,mela)
     3 (Tedeschi, votano, elezioni)
     4 (Maria, dipinge, quadri)

     Di seguito il testo da cui devi estrapolare le triple:
      {stringa} ?"""},
    ]
    generated_response = generate_text(messages,0.4)
    return generated_response

# Funzione che categorizza le entità delle triple raw
def uniforma_enitity(stringa):
    messages = [
    {"role": "system", "content": "Answer questions"},
    {"role": "user", "content": f"""Per ogni tripla numerata [ 1. (entity1,relation,enitity2)] categorizza ogni entità aggiungendo la categoria tra parentesi quadre accanto al nome( sia per la prima che per la seconda entità)rispetto ad una singola tra le categorie
    proposte di seguito (ogni entità deve essere necessariamente associata ad una di queste, se non è possibile ignora la tripla) :
    {entity_list}

Esempio dell'output che mi dovrai rigorosamente fornire considerando anche le parentesi:
    1.(entity1[categoria_x],relazione,entity2[categoria_y])
    2.(entity1[categoria_z],relazione,entity2[categoria_x])
    3.(entity1[categoria_j],relazione,entity2[categoria_k])
    4.(entity2[categoria_z],relazione,entity5[categoria_x])


Non fornire più dettagli di quelli che ti ho richiesto
Queste sono le righe che devi adattare:
    {stringa}"""},
]
    generated_response = generate_text(messages,0.3)
    return generated_response

# Funzione che converte le relazioni presenti nelle relazioni consentite semanticamente più simili
def uniforma_relazioni(stringa):
    messages = [
    {"role": "system", "content": "Answer questions"},
    {"role": "user", "content": f"""Per ogni riga sostituisci SOLAMENTE i verbi presenti con verbi presi da questo elenco in base alla loro similarità semantica , i verbi già adatti non modificarli.
    Questa è la lista di verbi consentiti:
    {relations_list}


     Esempio di come dovrà essere l'output:
    1.(entity1[categoria_x],relazione,entity2[categoria_y])
    2.(entity1[categoria_z],relazione,entity2[categoria_x])
    3.(entity1[categoria_j],relazione,entity2[categoria_k])
    4.(entity2[categoria_z],relazione,entity5[categoria_x])

    Queste sono le righe che devi adattare:
    {stringa}"""},
]
    generated_response = generate_text(messages,0.01)
    return generated_response

# Funzione che converte la stringa restituita dal modello in un'istanza di tripla 
def string_to_vector(string,data,link):
    # Pattern per estrarre i dati
    pattern = r'\((.*?)\[(.*?)\],\s*(.*?),\s*(.*?)\[(.*?)\]\)'
    # Match nella stringa restituita dal llm
    matches = re.findall(pattern, string)

    # Vettore di tuple con gli attributi richiesti
    vector = []
    for match in matches:
        entity1, category1, relation, entity2, category2 = match
        sentiment=0
        # Filtra in base alle relazioni e categorie valide
        if relation.strip():
          relazione = ((relation.strip()).lower()).replace(" ", "")
        if category1.strip() in valid_categories and category2.strip() in valid_categories and relazione in valid_relations:
          coppia_sentimento=sostituisci_coppia_sentimento(relazione)
          if coppia_sentimento[1] != 0:
            relazione=coppia_sentimento[0]
            sentiment=coppia_sentimento[1]
          instance = Instance(entity1.strip(), category1.strip().replace(" ", "_"),relazione.replace("/", "_"),sentiment, entity2.strip(), category2.strip().replace(" ", "_"), data, link)
          vector.append(instance)

    return vector

# Funzione per la divisione degli articoli in chunk  
def chunk_article(article,max_chunk_size=500):
    title = article["title"]
    link = article["link"]
    date = article["date"]
    text = article["text"]

    # Lista per memorizzare i chunk
    chunks = []

    # Inizializza il primo chunk con il titolo dell'articolo
    current_chunk_text = title + ". "
    current_chunk_size = len(current_chunk_text)
    remaining_text = text

    while remaining_text:
        next_period_index = remaining_text.find('.')
        if next_period_index == -1 or (current_chunk_size + next_period_index + 1) > max_chunk_size:
            # Aggiungi il chunk corrente ai chunks e inizia un nuovo chunk
            chunks.append({
                "text": current_chunk_text.strip(),
                "link": link,
                "date": date
            })
            current_chunk_text = ''
            current_chunk_size = 0
        else:
            # Aggiungi la porzione al chunk corrente
            current_chunk_text += remaining_text[:next_period_index + 1]
            current_chunk_size += next_period_index + 1
            remaining_text = remaining_text[next_period_index + 1:].strip()

    if current_chunk_text:
        chunks.append({
            "text": current_chunk_text.strip(),
            "link": link,
            "date": date
        })

    return chunks

# Funzione che estrae le triple dal testo del chunk
def estrai_triple(raw_text_chunk,data,link,last_check):
    triple_raw=genera_tripla(raw_text_chunk)
    triple_raw_formattate=filtra_righe(triple_raw)
    #print(triple_raw_formattate)
    if not triple_raw_formattate:
      return []
    triple_uniformate=uniforma_enitity(triple_raw_formattate)
    #print(triple_uniformate)
    triple_final=filtra_righe_categorie(triple_uniformate)
    if not triple_final:
      return []
    #print(triple_final)
    if last_check:
        triple_final=uniforma_relazioni(triple_final)
        triple_final=filtra_righe_categorie(triple_final)
    #print(triple_final)
    return string_to_vector(triple_final,data,link)

#Funzione che processa il singolo Articolo
def process_articles(articles,max_attempts=2,chunk_size=1200,last_check=True):
    table_data = [["Entity 1", "Category 1", "Relation", "Sentiment", "Entity 2", "Category 2", "Date", "Link"]]
    triple_totali = []

    # Utilizzo di tqdm per la barra di caricamento degli articoli
    for j, article in enumerate(tqdm(articles, desc="Processing Articles")):
        lunghezza_text = len(article["text"])
        print("La lunghezza dell'articolo", j+1, "è:", lunghezza_text)
        torch.cuda.empty_cache()
        gc.collect()
        max_attempts = 2
        attempts = 0
        chunks = chunk_article(article, chunk_size)

        # Utilizzo di tqdm per la barra di caricamento dei chunk
        for i, chunk in enumerate(tqdm(chunks, desc=f"Processing Chunks for Article {j+1}", leave=False)):
            triple_chunk = []
            attempts = 0
            while attempts < max_attempts and not triple_chunk:
                triple_chunk = estrai_triple(chunk['text'], chunk['date'], chunk['link'],last_check)
                attempts += 1
            if triple_chunk:
                print(f"Triple estratte dal Chunk {i+1} dell'articolo {j+1}")
            for istance in triple_chunk:
                table_data.append([istance.entity1, istance.category1, istance.relation, istance.sentiment, istance.entity2, istance.category2, istance.data, istance.link])

            print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
            triple_totali += triple_chunk
            torch.cuda.empty_cache()

    return triple_totali



if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Usage: script.py <chunk_size> <max_attempts> <last_check>")
        exit(-1)

    #variabili di ingresso
    chunk_size = int(sys.argv[1])
    max_attempts = int(sys.argv[2])
    last_check = sys.argv[3] == "True"
    print("Last check settato su :",last_check)
    #credenziali dalle variabili d'ambiente
    redis_host = os.getenv("RESID_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_psw = os.getenv("REDIS_PASSWORD")
    neo4j_uri=os.getenv("NEO4J_URI")
    neo4j_auth=os.getenv("NEO4J_AUTH")

    if not redis_host or not redis_port or not redis_psw:
        exit(-1)
    redis_port = int(redis_port)

    queue = ATCqueue(
        Redis(host=redis_host, port=redis_port, password=redis_psw)
    )

    # Pop del Batch di articoli
    reference, articles = queue.pop_batch()
    if not articles:
        print('Nessun Articolo da processare nella Coda')
        exit(0)

    triple_articolo = process_articles(articles, max_attempts, chunk_size, last_check)
    
    #Backup
    #reference, articles = queue.peek_batch_from_BU()
    # Analizzi e pushi le triplette, poi cancelli

    connector = Neo4jConnector(neo4j_uri, neo4j_auth)
    for tripla in triple_articolo:
        result=connector.push_triplet(tripla)
    print(result)

    connector.close()
    queue.del_batch_from_BU(reference)
   
    print(articles)
