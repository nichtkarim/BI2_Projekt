import pandas as pd
from tkinter import Tk, filedialog

# Dialog zum Öffnen der Eingabedatei
root = Tk()
root.withdraw()
input_path = filedialog.askopenfilename(title="Wähle die CSV-Datei aus", filetypes=[("CSV-Dateien", "*.csv")])
if not input_path:
    print("Keine Datei ausgewählt.")
    exit()

# CSV-Datei einlesen
df = pd.read_csv(input_path, encoding="latin1")

# Stornobelege entfernen (InvoiceNo beginnt mit "C")
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[~df['InvoiceNo'].astype(str).str.startswith('A')]

# Datensätze mit Quantity ≤ 0 entfernen
df = df[df['Quantity'] > 0]

# Fehlende Kundennummern auf "Unknown" setzen
df['CustomerID'] = df['CustomerID'].fillna('Unknown')

# InvoiceDate ins Datumsformat umwandeln
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# Berechnete Spalte TotalPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['TotalPrice'] = df['TotalPrice'].round(2)

# Dialog zum Speichern der Ausgabedatei
output_path = filedialog.asksaveasfilename(
    title="Speicherort auswählen",
    defaultextension=".csv",
    filetypes=[("CSV-Dateien", "*.csv")]
)
if not output_path:
    print("Kein Speicherort ausgewählt.")
    exit()

df.to_csv(output_path, index=False)
print(f"Datei wurde gespeichert unter: {output_path}")