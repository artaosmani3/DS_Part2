"""Laden, Prüfen und reproduzierbares Aufbereiten der Inside-Airbnb-Daten für Paris.

Grundsätze (siehe docs/projektvorschlag.md, Abschnitt 5):
- Die Rohdatei wird nie verändert. Alle abgeleiteten Grössen landen in neuen Spalten.
- Jeder Filter erscheint mit Begründung und Zeilenzahl in der Bereinigungstabelle.
- Auffällige Werte werden nicht gelöscht, sondern über Flags gekennzeichnet.
  Sie werden nur in Sensitivitätsvarianten ausgeschlossen.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import trim_mean

# ---------------------------------------------------------------------------
# Pfade und Snapshot
# ---------------------------------------------------------------------------
PROJEKT = Path(__file__).resolve().parents[1]
SNAPSHOT = "2026-09-16"
ROH_ORDNER = PROJEKT / "data" / "raw" / f"paris_{SNAPSHOT}"
ROH_DATEI = ROH_ORDNER / "listings.csv.gz"
DOWNLOAD_URL = (
    "https://data.insideairbnb.com/france/ile-de-france/paris/"
    f"{SNAPSHOT}/data/listings.csv.gz"
)
# Prüfsumme der am 10.11.2026 heruntergeladenen Datei. Sie stellt sicher, dass alle mit
# genau demselben Snapshot rechnen (Inside Airbnb ersetzt ältere Dateien ohne Ankündigung).
ROH_SHA256 = "3285e5096c1869a684d5e65eb38526f07aa16bdc41cd76686feba8a2b78bd019"

TABELLEN = PROJEKT / "outputs" / "tables"
GRAFIKEN = PROJEKT / "outputs" / "figures"
VERARBEITET = PROJEKT / "data" / "processed"

SEED = 42

# Inhaltlich begründete Grenzen, vor der Gruppenauswertung festgelegt (Projektvorschlag 5.2/5.3)
GRENZE_MONATSABFRAGE = 28          # Nächte: ab hier liefert Airbnb einen rabattierten Monatspreis
GRENZE_PREIS_EXTREM = 10_000       # EUR pro Nacht
GRENZE_PREIS_PRO_PERSON = 1_000    # EUR pro Person und Nacht

ZIMMERART_REIHENFOLGE = ["Entire home/apt", "Private room", "Hotel room", "Shared room"]
ZIMMERART_DEUTSCH = {
    "Entire home/apt": "Ganze Unterkunft",
    "Private room": "Privatzimmer",
    "Hotel room": "Hotelzimmer",
    "Shared room": "Geteiltes Zimmer",
}


# ---------------------------------------------------------------------------
# Rohdaten
# ---------------------------------------------------------------------------
def sha256(pfad: Path) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def stelle_rohdatei_bereit(herunterladen: bool = True) -> Path:
    """Lädt die Rohdatei herunter, falls sie fehlt, und prüft ihre Prüfsumme."""
    if not ROH_DATEI.exists():
        if not herunterladen:
            raise FileNotFoundError(ROH_DATEI)
        ROH_ORDNER.mkdir(parents=True, exist_ok=True)
        anfrage = urllib.request.Request(DOWNLOAD_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(anfrage) as antwort, open(ROH_DATEI, "wb") as ziel:
            ziel.write(antwort.read())
    pruefsumme = sha256(ROH_DATEI)
    if pruefsumme != ROH_SHA256:
        raise ValueError(
            f"Prüfsumme weicht ab ({pruefsumme}). Die Datei ist nicht der dokumentierte "
            f"Snapshot {SNAPSHOT}; Ergebnisse wären nicht vergleichbar."
        )
    return ROH_DATEI


def lade_rohdaten() -> pd.DataFrame:
    """Rohdaten genau so, wie Inside Airbnb sie liefert (keine Typumwandlung ausser durch read_csv)."""
    return pd.read_csv(stelle_rohdatei_bereit(), low_memory=False)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_preis(spalte: pd.Series) -> pd.Series:
    """'$1,386.50' -> 1386.5. Das '$' ist laut Data Dictionary ein Exportartefakt; Währung siehe JSON."""
    return pd.to_numeric(spalte.str.replace(r"[$,]", "", regex=True), errors="coerce")


def parse_preisabfrage(roh_json: pd.Series) -> pd.DataFrame:
    """Extrahiert die für uns relevanten Felder aus dem (nicht dokumentierten) JSON price_quote_raw."""

    def felder(text):
        if not isinstance(text, str):
            return {}
        q = json.loads(text).get("quote") or {}
        return {
            "abfrage_waehrung": q.get("currency"),
            "abfrage_verfuegbar": q.get("is_available"),
            "abfrage_monatspreis": q.get("is_monthly_priced"),
            "abfrage_rabatt_eur": q.get("discount_amount"),
            "abfrage_steuern_eur": q.get("taxes"),
        }

    teile = pd.DataFrame([felder(t) for t in roh_json], index=roh_json.index)
    for c in ["abfrage_rabatt_eur", "abfrage_steuern_eur"]:
        teile[c] = pd.to_numeric(teile[c], errors="coerce")
    # Wahrheitswerte als nullable boolean: fehlend bleibt fehlend (<NA>) statt False
    for c in ["abfrage_verfuegbar", "abfrage_monatspreis"]:
        teile[c] = teile[c].astype("boolean")
    return teile


# ---------------------------------------------------------------------------
# Aufbereitung
# ---------------------------------------------------------------------------
def leite_spalten_ab(roh: pd.DataFrame) -> pd.DataFrame:
    """Fügt abgeleitete Spalten hinzu. Die Rohspalten bleiben unverändert erhalten."""
    df = roh.copy()
    df["preis_eur"] = parse_preis(df["price"])
    df = df.join(parse_preisabfrage(df["price_quote_raw"]))

    df["last_scraped"] = pd.to_datetime(df["last_scraped"])
    df["abfrage_checkin"] = pd.to_datetime(df["price_quote_checkin_date"])
    df["abfrage_checkout"] = pd.to_datetime(df["price_quote_checkout_date"])
    df["abfrage_naechte"] = (df["abfrage_checkout"] - df["abfrage_checkin"]).dt.days
    df["abfrage_vorlauf_tage"] = (df["abfrage_checkin"] - df["last_scraped"]).dt.days

    df["zimmerart"] = pd.Categorical(df["room_type"], categories=ZIMMERART_REIHENFOLGE, ordered=False)
    df["arrondissement"] = df["neighbourhood_cleansed"]
    df["preis_pro_person"] = df["preis_eur"] / df["accommodates"]
    df["inserate_des_hosts"] = df["calculated_host_listings_count"]

    # Flags: kennzeichnen, nicht löschen
    df["flag_extrem"] = (df["preis_eur"] >= GRENZE_PREIS_EXTREM) | (
        df["preis_pro_person"] > GRENZE_PREIS_PRO_PERSON
    )
    df["flag_abfrage_nicht_verfuegbar"] = df["abfrage_verfuegbar"].eq(False).fillna(False).astype(bool)
    return df


def bereite_auf(roh: pd.DataFrame | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Gibt (alle Zeilen mit abgeleiteten Spalten, Kern-Analysedatensatz, Bereinigungstabelle) zurück."""
    if roh is None:
        roh = lade_rohdaten()
    alle = leite_spalten_ab(roh)

    schritte = []

    def protokoll(name, regel, begruendung, vorher, nachher):
        schritte.append(
            {
                "Schritt": name,
                "Regel": regel,
                "Begründung": begruendung,
                "Zeilen vorher": len(vorher),
                "entfernt": len(vorher) - len(nachher),
                "Anteil entfernt (%)": round(100 * (len(vorher) - len(nachher)) / len(vorher), 1)
                if len(vorher)
                else 0.0,
                "Zeilen nachher": len(nachher),
            }
        )

    s0 = alle
    protokoll("0 Rohdaten", "keine", "vollständiger Snapshot, ein Inserat je Zeile", s0, s0)

    s1 = s0[s0["preis_eur"].notna()]
    protokoll(
        "1 Preis beobachtet",
        "preis_eur nicht fehlend",
        "Kein Angebotspreis = kein buchbares Angebot im Abfragezeitraum (NB01 Abschnitt 5); "
        "keine Imputation der Zielvariable",
        s0,
        s1,
    )

    s2 = s1[s1["preis_eur"] > 0]
    protokoll("2 Preis > 0", "preis_eur > 0", "Preis 0 oder negativ wäre ungültig", s1, s2)

    s3 = s2[s2["abfrage_naechte"] < GRENZE_MONATSABFRAGE]
    protokoll(
        "3 Kurzaufenthalt-Abfrage",
        f"abfrage_naechte < {GRENZE_MONATSABFRAGE}",
        "Ab 28 Nächten liefert Airbnb einen rabattierten Monatspreis; andere Messgrösse. "
        "Wird in der Sensitivität wieder aufgenommen",
        s2,
        s3,
    )

    kern = s3.copy()
    tabelle = pd.DataFrame(schritte)
    return alle, kern, tabelle


def flag_tabelle(kern: pd.DataFrame) -> pd.DataFrame:
    """Kennzeichnungen im Kern-Datensatz: Diese Zeilen bleiben im Kern und werden nur in der Sensitivität ausgeschlossen."""
    zeilen = [
        (
            "flag_extrem",
            f"preis_eur ≥ {GRENZE_PREIS_EXTREM:,} oder Preis pro Person > {GRENZE_PREIS_PRO_PERSON:,}".replace(",", "'"),
            "inhaltlich zweifelhaft hoch; nicht als Fehler belegbar",
        ),
        (
            "flag_abfrage_nicht_verfuegbar",
            "abfrage_verfuegbar == False",
            "Abfrage meldet 'nicht verfügbar', liefert aber einen Preis",
        ),
    ]
    return pd.DataFrame(
        [
            {
                "Kennzeichnung": name,
                "Regel": regel,
                "Bedeutung": bedeutung,
                "betroffen": int(kern[name].sum()),
                "Anteil am Kern (%)": round(100 * kern[name].mean(), 2),
            }
            for name, regel, bedeutung in zeilen
        ]
    )


# ---------------------------------------------------------------------------
# Kennzahlen
# ---------------------------------------------------------------------------
def kennzahlen(werte: pd.Series) -> pd.Series:
    """Lage, Streuung und Rand einer metrischen Variable (VL02). SD mit ddof=1, MAD unskaliert und skaliert."""
    s = pd.Series(werte).dropna()
    q1, med, q3, p90 = s.quantile([0.25, 0.5, 0.75, 0.9])
    mad = (s - med).abs().median()
    return pd.Series(
        {
            "n": len(s),
            "Mittelwert": s.mean(),
            "Median": med,
            "getrimmtes Mittel 10%": trim_mean(s, 0.1) if len(s) else np.nan,
            "SD (ddof=1)": s.std(ddof=1),
            "Q1": q1,
            "Q3": q3,
            "IQR": q3 - q1,
            "MAD": mad,
            "MAD skaliert (1.4826)": 1.4826 * mad,
            "P90": p90,
            "Maximum": s.max(),
        }
    )


def kennzahlen_je_gruppe(df: pd.DataFrame, gruppe: str, wert: str = "preis_eur") -> pd.DataFrame:
    return df.groupby(gruppe, observed=True)[wert].apply(kennzahlen).unstack()


# ---------------------------------------------------------------------------
# Sensitivitätsvarianten (vor der Auswertung festgelegt, Projektvorschlag Abschnitt 4 Schritt 10)
# ---------------------------------------------------------------------------
def winsorisiere_je_gruppe(df: pd.DataFrame, gruppe: str = "zimmerart", q: float = 0.995) -> pd.Series:
    obergrenze = df.groupby(gruppe, observed=True)["preis_eur"].transform(lambda s: s.quantile(q))
    return df["preis_eur"].clip(upper=obergrenze)


def ein_inserat_pro_host(df: pd.DataFrame, seed: int = SEED) -> pd.DataFrame:
    """Zieht pro Host zufällig ein Inserat (fester Seed), um die Host-Abhängigkeit zu prüfen."""
    gemischt = df.sample(frac=1.0, random_state=seed)
    return gemischt.drop_duplicates("host_id").sort_index()


def sensitivitaets_varianten(alle: pd.DataFrame, kern: pd.DataFrame) -> dict[str, pd.DataFrame]:
    mit_preis = alle[alle["preis_eur"].notna() & (alle["preis_eur"] > 0)]
    winsor = kern.copy()
    winsor["preis_eur"] = winsorisiere_je_gruppe(kern)
    return {
        "Kern (Hauptanalyse)": kern,
        "ohne Extrem-Kennzeichnung": kern[~kern["flag_extrem"]],
        "winsorisiert 99.5% je Zimmerart": winsor,
        "ohne 'nicht verfügbar'-Abfragen": kern[~kern["flag_abfrage_nicht_verfuegbar"]],
        "ein Inserat pro Host": ein_inserat_pro_host(kern),
        "Check-in ≤ 30 Tage nach Scrape": kern[kern["abfrage_vorlauf_tage"] <= 30],
        "inkl. Abfragen ≥ 28 Nächte": mit_preis,
    }


def speichere_tabelle(tabelle: pd.DataFrame, name: str, index: bool = True) -> Path:
    TABELLEN.mkdir(parents=True, exist_ok=True)
    pfad = TABELLEN / f"{name}.csv"
    tabelle.to_csv(pfad, index=index)
    return pfad
