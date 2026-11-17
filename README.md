# Angebotene Übernachtungspreise von Airbnb-Inseraten in Paris

Projekt im Modul *Statistik für Data Science* (Kurs 3,906, HSG, HS2026).

**Hauptfrage.** Wie unterscheiden sich die auf Airbnb angebotenen Preise pro Nacht für Inserate in Paris nach Unterkunftsart, Kapazität und Arrondissement, und wie robust sind diese Unterschiede gegenüber extremen Preisen, den Bedingungen der Preisabfrage und Mehrfachinseraten derselben Hosts?

**Kurzantwort** (Details in `notebooks/04_synthese.ipynb`, Abschnitt 6):

- **Lage:** Bei gleicher Zimmerart und Kapazität unterscheiden sich die Arrondissement-Mediane etwa um den Faktor 2 (133 € bis 271 €).
- **Kapazität:** Der Preis steigt monoton, aber weniger als proportional mit der Gästezahl (ρ = 0.60 bei ganzen Unterkünften).
- **Zimmerart:** Der rohe Unterschied von Faktor 1.57 schrumpft bei gleicher Gästezahl auf 10–27 %.
- **Robustheit:** Die Richtung aller Aussagen hält jede Robustheitsvariante aus. Das absolute Preisniveau hängt dagegen stark vom Abfragetermin ab.

## Daten

| | |
|---|---|
| Quelle | Inside Airbnb, <https://insideairbnb.com/get-the-data/> (Paris, Île-de-France) |
| Snapshot | 2026-09-16 (`scrape_id` 20260916052215), heruntergeladen am 10.11.2026 |
| Datei | `data/raw/paris_2026-09-16/listings.csv.gz`, SHA-256 `3285e5096c1869a684d5e65eb38526f07aa16bdc41cd76686feba8a2b78bd019` |
| Dokumentation | `data/raw/paris_2026-09-16/data_dictionary_listings_v4.3.csv` (Inside Airbnb, Version 4.3) |
| Beobachtungseinheit | ein Inserat zum Zeitpunkt des Scrapes |

Die Rohdateien werden nie verändert. Fehlt `listings.csv.gz`, lädt `src/daten.py` die Datei herunter und prüft die Prüfsumme. Bei einer anderen Datei bricht die Analyse ab.

## Struktur

```
data/raw/paris_2026-09-16/   Rohdaten (unverändert) und Data Dictionary
data/processed/              von NB01 erzeugter Analysedatensatz (nicht versioniert)
src/daten.py                 Laden, Parsen, Bereinigungstabelle, Kennzeichnungen, Sensitivitätsvarianten
src/grafik.py                Farben, log-Preisachse, Speichern
notebooks/01_…  Teilfrage 1: Datenverständnis und Datenqualität
notebooks/02_…  Teilfrage 2: Preisverteilung und Robustheit gegenüber Extremwerten
notebooks/03_…  Teilfrage 3: Zimmerart, Kapazität, Lage
notebooks/04_…  Synthese: Sensitivität, alternative Erklärungen, Antwort
outputs/figures, outputs/tables   von den Notebooks erzeugt
docs/projektvorschlag.md   freigegebener Projektvorschlag
docs/entscheidungslog.md   alle Entscheidungen mit Begründung
docs/folienplan.md         Folienplan der Präsentation
docs/praesentation.pptx    Präsentation
```

## Reproduzieren

```bash
pip install -r requirements.txt
cd notebooks
for nb in 01_datenverstaendnis_und_qualitaet 02_preisverteilung_und_robustheit 03_gruppen_und_zusammenhaenge 04_synthese; do
  jupyter nbconvert --to notebook --execute --inplace "$nb.ipynb"
done
```

Jedes Notebook erzeugt seinen Analysedatensatz selbst aus der Rohdatei (`D.bereite_auf()`) und läuft unabhängig. Zufall kommt nur in der Ziehung «ein Inserat pro Host» und im Bootstrap vor, beide mit Seed 42. Zuletzt geprüft am 17.11.2026: Alle vier Notebooks liefen mit frischem Kernel fehlerfrei durch (je etwa 15 s).

Getestet mit Python 3.14.2, numpy 2.5.4, pandas 3.1.1, scipy 1.18.1, matplotlib 3.11.2, seaborn 0.13.2.
