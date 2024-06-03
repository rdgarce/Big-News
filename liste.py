
entity_list="""
• Persona: Nome di individuo rilevante nel contesto dell’articolo. Es. poli-
tici, leader economici, amministratori delegati, analisti economici, ecc. Es.
”Joe Biden”, ”Angela Merkel”, ”Elon Musk”.
• Organizzazione: Nome di ente, azienda, istituzione, ONG, partito poli-
tico, e organismo internazionale. Es. ”Nazioni Unite”, ”Banca Mondiale”,
”Google”, ”Partito Democratico”.
• Località: Nome di luogo geografico, come paese, citt`a, regione, e conti-
nente. Es. ”Italia”, ”New York”, ”Asia”, ”Europa”.
• Data o Periodo Temporale: Riferimento a data specifica, anno, mese,
giorno della settimana, o periodo di tempo. Es. ”12 marzo 2024”, ”nel
2023”, ”secondo trimestre”, ”decennio del 1990”.
• Misura o Quantità: Misura o quantit`a numerica che si riferisce a misure
specifiche, come l’inflazione, il PIL, e altre metriche economiche. Es. ”100
milioni di dollari”, ”50.000 euro”, ”3 milioni di barili”, ”200 miliardi di
metri cubi”, ”5%”, ”2,5%”.
• Prodotto o Servizo: Nome di bene o servizo, spesso associato a specifici
settori economici. Es. ”iPhone”, ”energia solare”, ”servizi bancari”.
• Evento: Nome di evento significativo che ha impatto economico o geopo-
litico. Es. ”Brexit”, ”G20”, ”Forum Economico Mondiale”.
• Legge, Regolamento o Programma Politico: Nome di legge, regola-
mento, trattato o accordo internazionale. Es. ”Accordo di Parigi”, ”Re-
golamento GDPR”, ”Trattato di Maastricht”, ”politica monetaria espansi-
va”, ”riforma fiscale”, ”politica di austerit`a”, ”Belt and Road Initiative”,
”Piano Marshall”, ”Progetto Manhattan”.
• Settore Economico: Riferimento a specifico settore dell’economia. Es.
”settore tecnologico”, ”industria manifatturiera”, ”settore dei servizi”.
• Risorsa Naturale: Nome di risorsa naturale che ha rilevanza economica
e geopolitica. Es. ”petrolio”, ”gas naturale”, ”minerali rari”.
• Entità Governativa: Nome di dipartimento, ministero o altra entit`a go-
vernativa. Es. ”Ministero delle Finanze”, ”Dipartimento di Stato”, ”Banca
Centrale Europea”.
• Infrastruttura: Nome di infrastruttura strategica che pu`o influire su geo-
politica ed economia. Es. ”Canale di Suez”, ”Pipeline Nord Stream”,
”Autostrada del Sole”.
• Tecnologia: Nome di tecnologia emergente o consolidata che influenza
l’economia e la geopolitica. Es. ”intelligenza artificiale”, ”blockchain”,
”5G”.
• Incidente o Crisi: Riferimento a incidente significativo o crisi economica o
politica. Es. ”crisi del debito sovrano”, ”attacco informatico SolarWinds”,
”pandemia COVID-19”.

"""
valid_categories = [
    "Persona","Città","Località","Data o Periodo Temporale","Misura o Quantità","Prodotto o Servizio",
    "Evento","Legge, Regolamento o Programma Politico","Settore Economico","Risorsa Naturale","Entità Governativa",
    "Infrastruttura","Tecnologia","Incidente o Crisi"
]


relations_list="""
Essere(Es.):Giorgia Meloni è il presidente del consiglio
Avere(Es.):Marco ha fame
Incontrare (Es.): Joe Biden incontra Angela Merkel a Berlino.
Discutere (Es.): I leader mondiali discutono delle questioni climatiche al G20.
Apprezzare (Es.): Il pubblico apprezza i discorsi di Joe Biden.
Disprezzare (Es.):Il pubblico disprezza le politiche di austerità.
Supportare/Ostacolare (Es.): La Germania supporta le iniziative dell’Unione Europea
Ostacolare (Es.): La Germania ostacola le nuove regolamentazioni fiscali.
Promuovere (Es.): Google promuove l’adozione di tecnologie sostenibili.
Boicottare (Es.): Google boicotta le nuove leggi sulla privacy.
Investire(Es.): La Banca Mondiale investe nei progetti di sviluppo in Africa.
Tagliare (Es.):  La Banca Mondiale taglia i fondi per i progetti in Europa.
Celebrare(Es.): L’Italia celebra la Festa della Repubblica il 2 giugno.
Ignorare (Es.): L’Italia ignora le raccomandazioni dell’Unione Europea.
Commemorare(Es.): Le Nazioni Unite commemorano il Giorno della Terra.
Dimenticare (Es.): Le Nazioni Unite commemorano il Giorno della Terra.
Accogliere(Es.): L’Europa accoglie i rifugiati.
Respingere (Es.): L’Europa respinge le richieste di asilo.
Valorizzare (Es.): L’Egitto valorizza il Canale di Suez come infrastruttura chiave.
Trascurare (Es.): L’Egitto trascura la manutenzione delle strade locali.
Adottare(Es.): Le aziende adottano l’intelligenza artificiale.
Rifiutare (Es.): Le aziende rifiutano di implementare nuove tecnologie.
Incoraggiare (Es.): Il governo incoraggia l’innovazione tecnologica.
Dissuadere (Es.): Il governo dissuade gli investimenti esteri.
Esaltare(Es.): La stampa esalta le capacità diplomatiche di Angela Merkel.
Denigrare (Es.): La stampa denigra le scelte politiche di Boris Johnson.
Confliggere (Es.): I paesi collaborano per affrontare il cambiamento climatico.
Collaborare (Es.): I paesi confliggono per le risorse naturali.
Proteggere (Es.): La nuova legge protegge i diritti dei lavoratori.
Minacciare (Es.): La nuova politica minaccia la libertà di stampa.
Impedire (Es.): Le politiche favoriscono la crescita economica.
Favorire (Es.): Le regolamentazioni impediscono l’espansione del mercato.
Riconoscere (Es.): L’ONU riconosce l’indipendenza del nuovo stato.
Negare (Es.): L’ONU nega la legittimità delle elezioni.
Innovare(Es.): Apple innova con nuovi prodotti ogni anno.
Restare indietro (Es.):  Apple resta indietro rispetto alla concorrenza nel settore laptop.
Sostenere (Es.): Il governo sostiene le start-up tecnologiche.
Abbandonare (Es.): Il governo abbandona le innovazioni
Partecipare (Es.): Elon Musk partecipa a una conferenza sull’innovazione tecnologica.
Annunciare (Es.): La Banca Mondiale annuncia nuovi finanziamenti per l’Africa.
Riferire (Es.): Le Nazioni Unite riferiscono sulle condizioni umanitarie in Siria.
Prevedere (Es.): Gli economisti prevedono una crescita del PIL per il 2025.
Collaborare (Es.): Google e Microsoft collaborano su progetti di intelligenza artificiale.
Pubblicare (Es.): L’ONU pubblica un rapporto sul cambiamento climatico.
Registrare (Es.): L’Italia registra un aumento delle esportazioni nel primo trimestre.
Lanciare (Es.): Tesla lancia un nuovo modello di auto elettrica.
Monitorare (Es.): La BCE monitora l’inflazione nell’Eurozona.
Analizzare (Es.): Gli analisti economici analizzano le tendenze di mercato.
Accettare (Es.): La Grecia accetta gli aiuti finanziari internazionali.
Sviluppare (Es.): L’azienda sviluppa nuove tecnologie per l’energia solare.
Rivedere (Es.): Il governo rivede le normative sul lavoro.
Osservare (Es.): I media osservano le reazioni dei mercati finanziari.
Intervistare (Es.): I giornalisti intervistano il CEO di Tesla.
Firmare (Es.): I leader europei firmano un accordo commerciale.
Trasmettere (Es.): Le notizie trasmettono aggiornamenti sulla situazione economica.
Raccogliere (Es.): Gli esperti raccolgono dati sulle nuove tecnologie.
Valutare (Es.): Le agenzie di rating valutano il rischio di credito delle aziende.
Pianificare (Es.): Il governo pianifica nuove politiche fiscali.
Coordinare (Es.): Le organizzazioni internazionali coordinano gli aiuti umanitari.
Proporre (Es.): Il ministro delle Finanze propone una nuova riforma fiscale.
Progettare (Es.): La società progetta un nuovo impianto di produzione.
Consultare (Es.): Il governo consulta gli esperti prima di adottare nuove leggi.
Implementare (Es.): Le aziende implementano nuove strategie di marketing.
Condurre (Es.): I ricercatori conducono uno studio sulle energie rinnovabili.
Indagare (Es.): Il governo indaga sulle cause dell’inflazione.
Verificare (Es.): Gli ispettori verificano la conformità delle normative ambientali.
Esplorare (Es.): Gli scienziati esplorano nuove fonti di energia rinnovabile.
Confermare (Es.): Il ministro conferma la data delle elezioni.
Presentare (Es.): Il consiglio direttivo presenta il bilancio annuale.
Promuovere (Es.): L’organizzazione promuove l’educazione finanziaria.
Stabilire (Es.): Il trattato stabilisce nuove regole commerciali.
"""

valid_relations = [
    "incontrare","discutere","partecipare","annunciare","riferire","prevedere","collaborare","pubblicare","registrare","lanciare","monitorare","analizzare","essere","avere","accettare","sviluppare","rivedere","osservare","intervistare","firmare","trasmettere","raccogliere","valutare","pianificare","coordinare","proporre","progettare","consultare","implementare","condurre","indagare","verificare","esplorare","confermare","presentare","promuovere","stabilire","apprezzare","disprezzare","supportare","ostacolare","promuovere","boicottare","investire","tagliare","celebrare","ignorare","commemorare","dimenticare","accogliere","rifiutare","valorizzare/trascurare","adottare/rifiutare","incoraggiare","dissuadere","esaltare","denigrare","collaborare","confliggere","proteggere","minacciare","favorire","impedire","riconoscere","negare","innovare","restare_indietro","sostenere","abbandonare"
]

dizionario = {
    "apprezzare": ["apprezzare/disprezzare", 1],
    "disprezzare": ["apprezzare/disprezzare", -1],
    "supportare": ["supportare/ostacolare", 1],
    "ostacolare": ["supportare/ostacolare", -1],
    "promuovere": ["promuovere/boicottare", 1],
    "boicottare": ["promuovere/boicottare", -1],
    "investire": ["investire/tagliare", 1],
    "tagliare": ["investire/tagliare", -1],
    "celebrare": ["celebrare/ignorare", 1],
    "ignorare": ["celebrare/ignorare", -1],
    "commemorare": ["commemorare/dimenticare", 1],
    "dimenticare": ["commemorare/dimenticare", -1],
    "accogliere": ["accogliere/rifiutare", 1],
    "rifiutare": ["accogliere/rifiutare", -1],
    "valorizzare": ["valorizzare/trascurare", 1],
    "trascurare": ["valorizzare/trascurare", -1],
    "adottare": ["adottare/rifiutare", 1],
    "dissuadere": ["incoraggiare/dissuadere", -1],
    "esaltare": ["esaltare/denigrare", 1],
    "denigrare": ["esaltare/denigrare", -1],
    "collaborare": ["collaborare/confliggere", 1],
    "confliggere": ["collaborare/confliggere", -1],
    "proteggere": ["proteggere/minacciare", 1],
    "minacciare": ["proteggere/minacciare", -1],
    "favorire": ["favorire/impedire", 1],
    "impedire": ["favorire/impedire", -1],
    "riconoscere": ["riconoscere/negare", 1],
    "negare": ["riconoscere/negare", -1],
    "innovare": ["innovare/restare_indietro", 1],
    "restare indietro": ["innovare/restare_indietro", -1],
    "sostenere": ["sostenere/abbandonare", 1],
    "abbandonare": ["sostenere/abbandonare", -1]
}
