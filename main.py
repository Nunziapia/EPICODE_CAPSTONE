# N.B. il file main.py è il file principale del progetto, che ha come scopo
# quello di mostrare la logica generale del progetto.
# per capire cosa sta accadendo è necessario visualizzare il file funzioni.py
# che contiene le funzioni create per elaborare i dati e generare i grafici.

from funzioni import * # per importare le funzioni create per elaborare i dati
import os # per navigare tra le cartelle e i file

# variabili principali
dir = "dati" # la cartella in cui salviamo tutte le tabelle
doc_path = os.path.join(dir, "extra.docx") # file docx da cui estraiamo le tabelle extra


def main():
    """
    Funzione principale del programma.
    """
    # estraiamo le tabelle dal file docx e le salviamo in file CSV
    estrai_tabelle_docx(doc_path, dir)
    # adesso disponiamo di 3 tabelle extra!
    #andiamo a salvare le tabelle in un dizionario che chiamaimo dati
    dati = leggi_csv_da_cartella(dir)
    # facciamoci un idea di cosa contengano questi df
    analizza_dataframe(dati)
    # iniziamo la lettura dei singoli file csv
    csv_pasti_eta(
                os.path.join(dir, 'ab_pasti_eta_dettaglio.csv'),
                os.path.join(dir, 'lk_pasti_eta.csv')
                 )
    csv_pasti_lavoro(        
                    os.path.join(dir, 'ab_pasti_lavoro_dettaglio.csv'),
                    os.path.join(dir, 'lk_pasti_lavoro.csv')
                )
    csv_pasti_regione(
                    os.path.join(dir, 'ab_pasti_regione_dettaglio.csv'),
                    os.path.join(dir, 'lk_pasti_regione.csv')
                )
    csv_pasti_istruzione(
                    os.path.join(dir, 'ab_pasti_titolostudio_dettaglio.csv'),
                    os.path.join(dir, 'lk_pasti_istruzione.csv')
                )
    print(
        """
        Tutte le tabelle sono state elaborate
        e salvate correttamente.
        """
        )

# l'indicazione successiva ci assicura che la funzione main() venga eseguita solo se il file viene eseguito direttamente
# e non se viene importato come modulo in un altro file
if __name__ == "__main__":
    main()