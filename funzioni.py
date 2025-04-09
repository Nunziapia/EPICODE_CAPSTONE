from docx import Document
import pandas as pd
import matplotlib.pyplot as plt # Per la visualizzazione dei grafici
import os  # Per la gestione dei file e delle cartelle
import re  # Per la pulizia dei nomi dei file


def pulisci_nome_file(nome):
    """
    Pulisce il nome del file rimuovendo caratteri non validi.
    """
    # Sostituisce caratteri non validi con "_"
    return re.sub(r'[<>:"/\\|?*]', '_', nome)



def estrai_tabelle_docx(doc_path, output_dir):
    """
    Estrae le tabelle da un file .docx e le salva in file CSV separati.
    Ogni tabella viene salvata in un file CSV con il nome "tabella_X.csv" 
    all'interno della cartella specificata da output_dir.
    """   
    # Carica il documento
    doc = Document(doc_path)

    # Estrazione delle tabelle e salvataggio in file CSV
    for idx, table in enumerate(doc.tables):
        data = []
        for row in table.rows:
            # Estrae e pulisce il testo di ogni cella
            data.append([cell.text.strip() for cell in row.cells])

        # Crea un DataFrame pandas
        df = pd.DataFrame(data)

        # Determina il nome del file in base alle colonne
        if not df.empty and len(df.columns) > 0:
            # Usa i nomi delle colonne (prima riga) per creare un nome significativo
            column_names = "_".join(df.iloc[0].dropna().astype(str).str.replace(" ", "_"))
            column_names = pulisci_nome_file(column_names)  # Pulisce il nome
            file_name = f"tb_{column_names}.csv"
        else:
            # Nome predefinito se non ci sono colonne
            file_name = f"tb_{idx+1}.csv"

        # Salva in CSV
        csv_path = os.path.join(output_dir, file_name)
        df.to_csv(csv_path, index=False, header=False)
        print(f"Tabella {idx+1} salvata in: {csv_path}")


def analizza_dataframe(dataframes):
    """
    Per ogni DataFrame in un dizionario, stampa:
    - Le prime righe del DataFrame
    - I nomi delle colonne
    - Informazioni sul DataFrame
    - Statistiche riassuntive per le colonne numeriche

    Args:
        dataframes (dict): Dizionario con i nomi dei file come chiavi e i DataFrame come valori.
    """
    for file_name, df in dataframes.items():
        print(f"Analisi del file: {file_name}")
        print("\nPrime righe del DataFrame:")
        print(df.head())
        print("\nNomi delle colonne:")
        print(df.columns)
        print("\nInformazioni sul DataFrame:")
        print(df.info())
        print("\nStatistiche riassuntive per le colonne numeriche:")
        print(df.describe())
        print("\n" + "="*50 + "\n")


def leggi_csv_da_cartella(folder):
    """
    data la cartella la funzione legge le tabelle e le salva in un dizionario
    con il nome del file come chiave e il DataFrame come valore.
    """
    # Dizionario per salvare i DataFrame
    dataframes = {}

    # Legge tutti i file CSV nella cartella
    for file_name in os.listdir(folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder, file_name)
            try:
                # Legge il file CSV in un DataFrame
                df = pd.read_csv(file_path, header=None)
                dataframes[file_name] = df
                print(f"File {file_name} letto correttamente.")
            except Exception as e:
                print(f"Errore durante la lettura del file {file_name}: {e}")

    return dataframes    


def lista_file_csv(cartella):
    """
    Restituisce una lista con i nomi di tutti i file CSV 
    presenti in una cartella.
    """
    # Controlla se la cartella esiste
    if not os.path.exists(cartella):
        print(f"La cartella {cartella} non esiste.")
        return []

    # Filtra i file con estensione .csv
    file_csv = [file for file in os.listdir(cartella) if file.endswith(".csv")]
    return file_csv

# FUNZIONI PER LEGGERE E MODIFICARE I CSV PER UNA LETTURA SU LOOKER
def csv_pasti_eta(csv_path, output_path):
    """
    Funzione per elaborare i dati dei pasti in base all'età.
    """
    # Legge il CSV
    print(f'tabella {csv_path}')
    df = pd.read_csv(csv_path, header=0)
    # eliminiamo i valori che non sono in migliaglia
    df = df[df["Misura"] == "valori in migliaia"]
    # Filtra le righe dove "Sesso" non è "Totale"
    df = df[df["Sesso"] != "totale"]
    # prendiamo in considerazione solo le colonne che ci interessano
    df = df[["Tipo dato", "Sesso", "Classe di età", "TIME", "Value"]]
    # pivottiamo la tabella sugli anni
    df = df.pivot_table(index=["TIME"],
                        columns=["Tipo dato", "Sesso", "Classe di età"], values="Value")
    # Combina i livelli dell'header in un'unica riga
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    print(df)
    df.to_csv(output_path, index=True, index_label='Anno', header=True)
    print(f"Tabella elaborata e salvata in: {output_path}")

def csv_pasti_lavoro(csv_path, output_path):
    """
    Funzione per elaborare i dati dei pasti in base alla professione.
    """
    # Legge il CSV
    print(f'tabella {csv_path}')
    df = pd.read_csv(csv_path, header=0)
    # eliminiamo i valori che non sono in migliaglia
    df = df[df["Misura"] == "valori in migliaia"]
    # Filtra le righe dove "Sesso" non è "Totale"
    df = df[df["Sesso"] != "totale"]
    # prendiamo in considerazione solo le colonne che ci interessano
    df = df[["Tipo dato", "Sesso", "Condizione e posizione nella professione", "TIME", "Value"]]
    # pivottiamo la tabella sugli anni
    df = df.pivot_table(index=["TIME"],
                        columns=["Tipo dato", "Sesso", "Condizione e posizione nella professione"], values="Value")
    # Combina i livelli dell'header in un'unica riga
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    print(df)
    df.to_csv(output_path, index=True, index_label='Anno', header=True)
    print(f"Tabella elaborata e salvata in: {output_path}")


def csv_pasti_regione(csv_path, output_path):
    """
    Funzione per elaborare i dati dei pasti in base alla regione.
    """
    # Legge il CSV
    print(f'tabella {csv_path}')
    df = pd.read_csv(csv_path, header=0)    
    # eliminiamo i valori che non sono in migliaglia
    df = df[df["Misura"] == "valori in migliaia"]
    
    # Filtra righe dove territorio non è "Italia"
    df = df[df["Territorio"] != "Italia"]    
    # prendiamo in considerazione solo le colonne che ci interessano
    df = df[["Tipo dato", "Territorio", "TIME", "Value"]]
    # pivottiamo la tabella sugli anni
    df = df.pivot_table(index=["TIME"],
                        columns=["Tipo dato", "Territorio"], values="Value")
    # Combina i livelli dell'header in un'unica riga
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    print(df)
    df.to_csv(output_path, index=True, index_label='Anno', header=True)
    print(f"Tabella elaborata e salvata in: {output_path}")


def csv_pasti_istruzione(csv_path, output_path):
    """
    Funzione per elaborare i dati dei pasti in base ai titoli di studio.
    """
    # Legge il CSV
    print(f'tabella {csv_path}')
    df = pd.read_csv(csv_path, header=0)    
    # eliminiamo i valori che non sono in migliaglia
    df = df[df["Misura"] == "valori in migliaia"]
    
    # Filtra righe dove sesso non è "totale"
    df = df[df["Sesso"] != "totale"]    
    # prendiamo in considerazione solo le colonne che ci interessano
    df = df[["Tipo dato", "Sesso", "TIME", "Classe di età", "Titolo di studio", "Value"]]
    # pivottiamo la tabella sugli anni
    df = df.pivot_table(index=["TIME"],
                        columns=["Tipo dato", "Sesso", "Classe di età", "Titolo di studio"], values="Value")
    # Combina i livelli dell'header in un'unica riga
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    print(df)
    df.to_csv(output_path, index=True, index_label='Anno', header=True)
    print(f"Tabella elaborata e salvata in: {output_path}")