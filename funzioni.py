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
    # Copia la riga con TIME = 2003 e assegna il valore TIME = 2004
    df_2003 = df[df["TIME"] == 2003].copy()
    df_2003["TIME"] = 2004
    df = pd.concat([df, df_2003], ignore_index=True)
    # # pivottiamo la tabella sugli anni
    # df = df.pivot_table(index=["TIME"],
    #                     columns=["Tipo dato", "Sesso", "Classe di età"], values="Value")
    # # Combina i livelli dell'header in un'unica riga
    # df.columns = ['_'.join(col).strip() for col in df.columns.values]
    # print(df)
    # Gestisce i valori non numerici o NaN nella colonna "Value"
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0).astype(int)
    # Sostituisce gli spazi nei nomi delle colonne con "_"
    # Converte la colonna TIME in formato data (yyyy)
    df["TIME"] = pd.to_datetime(df["TIME"], format="%Y").dt.year
    
    df.columns = df.columns.str.replace(" ", "_")
    df.to_csv(output_path, index=False, header=True)
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
    # Copia la riga con TIME = 2003 e assegna il valore TIME = 2004
    df_2003 = df[df["TIME"] == 2003].copy()
    df_2003["TIME"] = 2004
    df = pd.concat([df, df_2003], ignore_index=True)
    # Gestisce i valori non numerici o NaN nella colonna "Value"
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0).astype(int)
    # Converte la colonna TIME in formato data (yyyy)
    df["TIME"] = pd.to_datetime(df["TIME"], format="%Y").dt.year
    
    # Sostituisce gli spazi nei nomi delle colonne con "_"
    df.columns = df.columns.str.replace(" ", "_")
    df.to_csv(output_path, index=False, header=True)
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
    # Copia la riga con TIME = 2003 e assegna il valore TIME = 2004
    df_2003 = df[df["TIME"] == 2003].copy()
    df_2003["TIME"] = 2004
    df = pd.concat([df, df_2003], ignore_index=True)
    # # pivottiamo la tabella sugli anni
    # df = df.pivot_table(index=["TIME"],
    #                     columns=["Tipo dato", "Territorio"], values="Value")
    # # Combina i livelli dell'header in un'unica riga
    # df.columns = ['_'.join(col).strip() for col in df.columns.values]
    # print(df)
    # Gestisce i valori non numerici o NaN nella colonna "Value"
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0).astype(int)
    # Sostituisce gli spazi nei nomi delle colonne con "_"
    # Converte la colonna TIME in formato data (yyyy)
    df["TIME"] = pd.to_datetime(df["TIME"], format="%Y").dt.year
    df.columns = df.columns.str.replace(" ", "_")
    # Sostituisce il simbolo "%" nei nomi delle colonne con "percentuale"
    df.columns = df.columns.str.replace("%", "percentuale")
    df.to_csv(output_path, index=False, header=True)
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

    df_2003 = df[df["TIME"] == 2003].copy()
    df_2003["TIME"] = 2004
    df = pd.concat([df, df_2003], ignore_index=True)
    # # pivottiamo la tabella sugli anni
    # df = df.pivot_table(index=["TIME"],
    #                     columns=["Tipo dato", "Sesso", "Classe di età", "Titolo di studio"], values="Value")
    # Combina i livelli dell'header in un'unica riga
    # df.columns = ['_'.join(col).strip() for col in df.columns.values]
    # print(df)
    # Gestisce i valori non numerici o NaN nella colonna "Value"
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0).astype(int)
    # Converte la colonna TIME in formato data (yyyy)
    df["TIME"] = pd.to_datetime(df["TIME"], format="%Y").dt.year
    # Sostituisce gli spazi nei nomi delle colonne con "_"
    df.columns = df.columns.str.replace(" ", "_")
    df.to_csv(output_path, index=False, header=True)
    print(f"Tabella elaborata e salvata in: {output_path}")


def grafico_vegetariani_vegani(csv_path, output_path, new_df):
    """
    Legge il file CSV e genera due grafici:
    1. Percentuale di italiani vegetariani e vegani per anno.
    2. Tasso di crescita annuale di vegetariani e vegani.
    Entrambi i grafici vengono salvati come immagini.

    Args:
        csv_path (str): Percorso del file CSV.
        output_path (str): Cartella in cui salvare i grafici.
    """
    # Legge il CSV e sostituisce "Non disponibile" con NaN
    print(f"Leggendo il file: {csv_path}")
    df = pd.read_csv(csv_path, na_values=["Non disponibile"])

    # Controlla che le colonne necessarie siano presenti
    colonne_necessarie = ["Anno", "Vegetariani", "Vegani"]
    for colonna in colonne_necessarie:
        if colonna not in df.columns:
            raise ValueError(f"La colonna '{colonna}' non è presente nel file CSV.")

    # Converte la colonna "Anno" in formato numerico (se non lo è già)
    df["Anno"] = pd.to_numeric(df["Anno"], errors="coerce")
    # Ordina i dati per anno
    df = df.sort_values(by="Anno")
    # Aggiunge gli anni mancanti tra il 2014 e il 2024
    anni_completi = pd.DataFrame({"Anno": range(2014, 2025)})
    df = pd.merge(anni_completi, df, on="Anno", how="left")

    # Riempie i valori mancanti copiando i valori dell'anno precedente
    df["Vegetariani"] = df["Vegetariani"].fillna(method="ffill").fillna(0)
    df["Vegani"] = df["Vegani"].fillna(method="ffill").fillna(0)

    # Rimuove il simbolo "%" dalle colonne e converte in valori numerici
    for colonna in ["Vegetariani", "Vegani", "Totale Veg"]:
        if colonna in df.columns:
            df[colonna] = df[colonna].str.replace("%", "", regex=False).str.replace(",", ".", regex=False).astype(float)

    # Calcolo della colonna "Totale Veg" come somma di "Vegetariani" e "Vegani"
    df["Totale Veg"] = df["Vegetariani"] + df["Vegani"]
    
    # Calcolo Crescita Annuale    
    df["Crescita_Vegetariani"] = df["Vegetariani"].pct_change() * 100
    df["Crescita_Vegani"] = df["Vegani"].pct_change() * 100
    # Arrotonda tutti i valori numerici a 2 cifre decimali
    df = df.round(2)
    # Salva il DataFrame aggiornato nel percorso specificato
    df.to_csv(new_df, index=False, header=True)
    print(f"DataFrame aggiornato salvato in: {new_df}")
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Grafico 1: Percentuale di vegetariani e vegani per anno
    plt.figure(figsize=(10, 6))
    plt.plot(df["Anno"], df["Vegetariani"], label="Vegetariani", marker="o", color="green")
    plt.plot(df["Anno"], df["Vegani"], label="Vegani", marker="o", color="orange")
    plt.title("Percentuale di Italiani Vegetariani e Vegani per Anno", fontsize=16)
    plt.xlabel("Anno", fontsize=14)
    plt.ylabel("Percentuale (%)", fontsize=14)
    plt.legend(title="Gruppo", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    grafico_percentuale_path = os.path.join(output_path, "veg_percentuale.png")
    plt.savefig(grafico_percentuale_path)
    print(f"Grafico percentuale salvato in: {grafico_percentuale_path}")
    plt.close()

    # Grafico 2: Tasso di crescita annuale di vegetariani e vegani
    plt.figure(figsize=(10, 6))
    plt.plot(df["Anno"], df["Crescita_Vegetariani"], label="Crescita Vegetariani", marker="o", color="blue")
    plt.plot(df["Anno"], df["Crescita_Vegani"], label="Crescita Vegani", marker="o", color="red")
    plt.axhline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)  # Linea di riferimento per crescita 0%
    plt.title("Tasso di Crescita Annuale di Vegetariani e Vegani", fontsize=16)
    plt.xlabel("Anno", fontsize=14)
    plt.ylabel("Tasso di Crescita (%)", fontsize=14)
    plt.legend(title="Gruppo", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    grafico_crescita_path = os.path.join(output_path, "veg_crescita.png")
    plt.savefig(grafico_crescita_path)
    print(f"Grafico tasso di crescita salvato in: {grafico_crescita_path}")
    plt.close()


def confronto_ristoranti_fastfood(csv_path_fast_food, csv_path_ristoranti, output_path, new_df):
    """
    Funzione per confrontare i ristoranti e i fast food.
    """
    # Legge il CSV e lo associa a un DataFrame
    df_fast_food = pd.read_csv(csv_path_fast_food)
    df_ristoranti = pd.read_csv(csv_path_ristoranti)
    # Prendiamo in considerazione solo le colonne "Regione" e "Valore"
    df_fast_food = df_fast_food[["Regione", "Valore"]]
    # Cambiamo il nome della colonna "Valore" in "NrFastFood"
    df_fast_food = df_fast_food.rename(columns={"Valore": "NrFastFood"})
    # Eliminiamo la riga dove "Regione" è "Altre regioni"
    df_fast_food = df_fast_food[df_fast_food["Regione"] != "Altre regioni"]
    # Prendiamo solo le colonne "Regione" e "Valori assoluti" del DataFrame ristoranti
    df_ristoranti = df_ristoranti[["Regione", "Valori assoluti"]]
    # Cambiamo il nome della colonna "Valori assoluti" in "Numeri servizi di ristorazione"
    df_ristoranti = df_ristoranti.rename(columns={"Valori assoluti": "Numeri servizi di ristorazione"})
    # Cambiamo il valore "Emilia Romagna" in "Emilia-Romagna"
    df_ristoranti["Regione"] = df_ristoranti["Regione"].replace("Emilia Romagna", "Emilia-Romagna")
    # Uniamo i due DataFrame sulla colonna "Regione"
    total_df = pd.merge(df_fast_food, df_ristoranti, on="Regione", how="outer")
    # print(total_df)
    # Salviamo il Dataframe in un file CSV
    total_df.to_csv(new_df, index=False, header=True)