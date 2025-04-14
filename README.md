

# 🥗 Trend2Table  
## Analisi della Mutazione dei Consumi Alimentari in Italia
### *Un insight data-driven sull’influenza del contesto nelle scelte alimentari*


## Indice
- [Descrizione del Progetto](#descrizione-del-progetto)
- [Obiettivi dell'Analisi](#obiettivi-dellanalisi)
- [Fasi Progetto](#fasi-progetto)
- [Base Dati](#base-dati)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Conclusioni](#conclusioni)
- [Sviluppi](#Prossimi-Sviluppi)
- [Aggiornamenti e versioni](#Update)

## Descrizione del Progetto
Questo progetto prevede la creazione di una **dashboard interattiva in Power BI** con l'obiettivo di analizzare la mutazione dei consumi alimentari in Italia negli ultimi 30 anni. Attraverso questa analisi, vogliamo comprendere come sono cambiate le abitudini alimentari degli italiani nel tempo e quali fattori hanno influenzato tali cambiamenti.

## Obiettivi dell'Analisi
1. **Evoluzione delle Abitudini Alimentari**
   - Analizzare come sono cambiati i consumi alimentari regione per regione ed anno per anno.
   - Evidenziare variazioni nei pasti principali (colazione, pranzo, cena) e nei consumi di specifici gruppi alimentari.


2. **Fattori di Influenza**
   - Esaminare il ruolo di fattori socio-economici come:
     - **Lavoro**: impatto delle ore lavorative e del tipo di impiego sulle abitudini alimentari.
     - **Titolo di studio**: correlazione tra livello di istruzione e scelte alimentari.
     - **Età**: differenze generazionali nelle preferenze alimentari.

3. **Nuove Tendenze e Scelte Alimentari**
   - Identificare l'impatto di nuove opportunità per il consumatore, come:
     
     - **Diete Vegane/Vegetariane** e aumento dell'attenzione alla sostenibilità.
     - **Stili di vita sedentari** e il loro effetto sulle abitudini alimentari.

4. **Salute e Qualità della Dieta**
   - Utilizzare i dati per comprendere se i consumatori si stanno orientando verso una **dieta più sana** o se preferiscono una **dieta veloce e poco equilibrata**.

## Fasi Progetto
Il progetto mira a utilizzare i report ufficiali provenienti da più [fonti](#base-dati),

   - Raccolta e pulizia dei dati:
      1. Download dei dataset Istat, questi dati possono essere organizzati direttamente dal portale istat pertanto non richiedono un lavoro preliminare di pulizia e organizzazione. Il grosso del lavoro è stato reperire i dati dai report che di loro natura sono "discorsivi". Con l'utilizzo di strumenti AI ho acccelerato il processo di estrazione dei dati sotto forma di tabelle ricavando cosi il file "extra.doc"
      2. Ho convertito il file in .docx per poter estrarre con python le tabelle presenti nel file.
      3. Per poter utilizzare python ho creato un ambiente virtuale col comando `python -m venv venv`, per riproporlo sulla propria macchina seguire le istruzioni di seguito solo se disponete di un sistema operativo windows, su un sistema linux i comandi SONO DIVERSI.
      Lanciare in ordine i comandi da terminale:
      `python -m venv venv` che crea l'ambiente virtuale
      `venv\Scripts\activate` che attiva l'ambiente virtuale sulla macchina
      `pip install -r requirements.txt` che installerà tutte le librerie necessarie per l'esecuzione degli algoritmi
      4. Ai fini del progetto ho diviso l'elaborazione python in due file uno che contiene la logica generale "main.py" che ho utilizzato per pulire i dati ed individuare le correlazioni ed uno in cui sarà possibile vedere cosa ogni singola funzione richiamata nel file main faccia esattamente "funzioni.py"
      5. Ora disponiamo di 3 tabelle extra, verificate iniziamo la nostra indagine con python
      6. Con python è stata creata una funzione che permette di farsi un idea generale dei dati che abbiamo inserito nella cartella dati.
      i file csv infatti vengono associati al rispettivo df.
      Vengono salvati tutti in un dizionario che a sua volta viene passato ad una funzione apposita per darci un idea generale di cosa contengano i file:
      Prime righe del DataFrame, Nomi delle colonne, Informazioni sul DataFrame e Statistiche riassuntive per le colonne numeriche.
      7. Con python sono stati popolate le tabelle "scarne" in modo da poter utilizzare i dati in nostro possesso per avere una panoramica generale dell'andamento delle diete Veg.
      8. COn Python è stato riempito il gap del 2004 anno in cui non sono state raccolte info dall'Istat.
      9. Con python sono stati puliti i dati estratti dai report, le tabelle risultanti sono state modificate affinche si potessero creare delle relazioni tra tabelle su PowerBI
    
   - Creazione delle prime visualizzazioni:
      Utilizzeremo PowerBI per poter rendere autoesplicativi e più tangibili questi dati.
   - Validazione dei modelli di analisi.
   - Refinamento della dashboard per una maggiore usabilità.

## Base Dati
- **Fonti Dati**:
IN ORDINE DI AUTOREVOLEZZA
   - Dataset provenienti da [ISTAT](#https://www.istat.it/). L'Istituto nazionale di statistica (conosciuto anche come Istat) è un ente pubblico di ricerca italiano che si occupa dei censimenti generali della popolazione, dei servizi e dell'industria, dell'agricoltura, di indagini campionarie sulle famiglie e di indagini economiche generali a livello nazionale. L'operato dell'istituto è supervisionato dalla Commissione per la garanzia dell'informazione statistica della Presidenza del Consiglio dei ministri, che ha il compito di garantire l'imparzialità e la completezza dei dati raccolti e pubblicati. I contenuti pubblicati dall'Istat sono disponibili con licenza Creative Commons Attribuzione 3.0. L'Istat è un membro del Sistema statistico europeo.
   - Rapporti [EURISPES](#https://eurispes.eu/). L'Eurispes (dal 1982 al 1993 chiamato Ispes) è un ente privato italiano che si occupa di studi politici, economici e sociali, ed operante nel campo della ricerca politica, economica, sociale e della formazione.- Rapporto FIPE 2023. 
   - Rapporto 2024 [FIPE](#https://www.fipe.it/wp-content/uploads/2024/04/Rapporto-Ristorazione-2024.pdf?utm_source=chatgpt.com). La Fipe, Federazione Italiana Pubblici Esercizi, è l'associazione leader nel settore della ristorazione, dell'intrattenimento e del turismo.
   - Dati provenienti da [STATISTA](#https://www.statista.com/). Statista è un sito web tedesco per la statistica, che rende disponibili dati raccolti da istituzioni che si occupano di ricerca, di mercato e di opinioni, così come statistiche riguardanti l'ambito economico e statale. L'azienda afferma che sulla sua piattaforma sono presenti statistiche riguardanti più di 80.000 temi e provenienti da più di 22.500 fonti.
   
- **Struttura dei Dati**: informazioni suddivise per regione, età, occupazione e altri parametri rilevanti. La dove questa analisi non può essere condotta con questi parametri abbiamo utilizzato i dati Istat per dare un significato ai dati dei report indicati nelle fonti dati.
Per i dati relativi a fastfood e diete vegane vegetariane 
- **Periodo di Analisi**: ultimi 30 anni per individuare trend significativi. Per quanto riguarda le nuove "mode" non abbiamo una base dati importante e ben strutturata e dobbiamo affidarci ai rapporti annuali che possono essere ritenuti rilevanti ai fini delle analisi solo dagli ultimi 5 anni.

## Tecnologie Utilizzate
- **Power BI** per la creazione della dashboard interattiva.
- **Python** per la manipolazione e la preparazione dei dati ed individuare tendenze e correlazioni.


## Conclusioni
L'obiettivo finale di questa analisi è quello di comprendere meglio l'evoluzione delle abitudini alimentari italiane e i principali fattori che le hanno influenzate. I risultati di questa ricerca potranno essere utili per nutrizionisti, policy maker e aziende del settore alimentare, offrendo una visione chiara su come il comportamento dei consumatori sia cambiato nel tempo e quali possano essere le prospettive future.
Questo progetto mira a fornire un quadro chiaro e interattivo dei cambiamenti nelle abitudini alimentari italiane, offrendo insight utili per ricercatori, nutrizionisti e policy maker.

## Prossimi Sviluppi
- Analizzare le **Diete FAST** (consumo rapido e cibi preconfezionati) e la loro influenza.

## Update
- 04/04/2025 versione iniziale del progetto.
- 09/04/2025 sviluppo sfondi dashboard.
- 10/04/2025 sviluppo grafici con seaborn per diete veg
- 12/04/2025 utilizzo fonti sui fastfood del 2024
