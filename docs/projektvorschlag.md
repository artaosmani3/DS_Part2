# Projektvorschlag: Angebotene Übernachtungspreise von Airbnb-Inseraten in Paris

*Statistik für Data Science (Kurs 3,906, HS2026). Stand: 10.11.2026. Status: **Frage A freigegeben am 17.11.2026**, umgesetzt in `notebooks/01–04`. Abweichungen vom Vorschlag stehen in `docs/entscheidungslog.md` (E12: eigene P90-Grenze im Lagesegment).*

> Alle Zahlen in diesem Dokument stammen aus einer ersten Sichtung des Rohdatensatzes. Es handelt sich um Zählungen zur Datenqualität, nicht um Analyseergebnisse. Sie werden in Notebook 01 reproduzierbar nachgerechnet. Gruppenvergleiche der Preise wurden bewusst noch nicht ausgewertet, damit Filter- und Methodenentscheidungen nicht vom Ergebnis abhängen.

---

## 0. Sichtung: Quellen, Projektstand, fehlende Vorgaben

### 0.1 Was im Repository liegt

| Material | Inhalt | Verwendung |
|---|---|---|
| VL01–VL05 (PDF) | Daten und Bias, deskriptive Statistik, robuste Diagnostik, Korrelation, Wahrscheinlichkeit | Kern des Projekts |
| VL06 (PDF, zwei identische Dateien `(1)` und `(2)`) | Normalverteilung, Schätzer, Bootstrap, Konfidenzintervalle | optionale Erweiterung (Abschnitt 8) |
| VL07 (PDF) | Hypothesentests | nicht im Auftrag; wird nicht eingebaut (Begründung in Abschnitt 8) |
| NB01–NB04 sowie NB03_Ausreisserregeln | TA-Notebooks im Schema «Problem → Theorie → Code → Bedeutung → Euer Datensatz» | methodische und didaktische Vorlage |
| `Sample-Präsentation.pdf` | Beispielpräsentation einer anderen Gruppe (7 Folien, Kreditkartendaten) | nur Orientierung für Umfang und Format, keine inhaltliche Vorlage |
| `README.md` | nur die Überschrift `# DS_Part2` | – |

**Bestehende Analysen:** Im Repository gibt es keine eigenen Notebooks, Daten oder Ergebnisse. Es existiert nur ein Initial-Commit. Ich überschreibe daher nichts und übernehme keine Zahlen.

**Foliennummern:** In allen Foliensätzen stimmt die Foliennummer in der Fusszeile mit der PDF-Seite überein. Die Angabe «S. 18» bezeichnet daher beides. Stichprobenartig geprüft: VL01 S. 42, VL03 S. 18 und VL04 S. 39.

### 0.2 Tatsächlich vorhandene Vorgaben zum Projekt

- **VL01, S. 5:** Das «eigene Statistikprojekt» ist Teil der dezentralen Portfolioarbeit (65 %, zusammen mit Übungsblättern und Notebooks).
- **VL01, S. 4 / VL02, S. 2:** Projektanalyse in den Wochen 10–11, Projektabgabe in Woche 12.
- **VL05, S. 45 und VL06, S. 43:** «Am Dienstag, 10.11., Gruppenvorträge in der Übung.» **Das ist laut Systemdatum heute** (siehe Rückfragen am Ende).
- **NB01, Zelle 2:** «Der Syllabus verlangt, dass Notebooks Umgebung, Pakete und Seeds dokumentieren.»
- **NB01 §5, NB03 §4, NB04 §6:** Die Notebooks verlangen ein **Entscheidungs-Log** mit Berichtssätzen nach festem Muster, zum Beispiel «Zwischen x und y: r = …, ρ = …, n = …, Form …; innerhalb der Gruppen von z …». NB03_Ausreisserregeln §3 verlangt zusätzlich **Fallnotizen** für auffällige Einzelwerte.

### 0.3 Fehlende Vorgaben

Diese Vorgaben fehlen. Ich erfinde sie nicht.

1. Es gibt kein Bewertungsraster für Projekt oder Vortrag.
2. Vortragsdauer, Folienzahl und Gruppengrösse sind nicht festgelegt. Die Beispielpräsentation hat 6 Folien plus eine Bonusfolie, aber das ist keine Vorgabe.
3. Es gibt keine Folienvorlage und kein Corporate Design.
4. Abgabeform (Repository, ZIP, PDF) und Abgabetermin der Notebooks sind unklar. Bekannt ist nur «Woche 12».
5. Der Syllabus selbst liegt nicht vor. Bekannt ist nur das Zitat in NB01.

**Vorläufige Annahmen für diesen Vorschlag:** etwa 10 Minuten Vortrag mit 8 bis 10 Kernfolien plus Anhang. Abgabe als Repository mit ausgeführten Notebooks und PPTX. Kein Pflichttemplate, also eine schlichte und konsistente eigene Gestaltung.

### 0.4 Datenquelle und Snapshot

| Merkmal | Wert |
|---|---|
| Quelle | Inside Airbnb, <https://insideairbnb.com/get-the-data/> (Abschnitt Paris, Île-de-France) |
| Snapshot | **2026-09-16** (`scrape_id` 20260916052215). Das ist der einzige aktuell verlinkte Paris-Snapshot. |
| Tatsächliches Abrufdatum der Seiten | `last_scraped` liegt zwischen dem 17.09. und dem 24.09.2026 |
| Heruntergeladen am | 10.11.2026 |
| Dateien (unverändert unter `data/raw/paris_2026-09-16/`) | `listings.csv.gz` (detailliert, SHA-256 `3285e509…d019`), `neighbourhoods.csv`, `neighbourhoods.geojson`, `data_dictionary_listings_v4.3.csv` |
| Nicht heruntergeladen | `calendar.csv.gz` (68 MB) und `reviews.csv.gz`. Für die Kernfrage werden sie nicht gebraucht (siehe optionale Erweiterungen). |
| Dokumentation | Data Dictionary «listings.csv detailed file», **Version 4.3 (August 2022)**, Google Sheet, verlinkt auf der Download-Seite |
| Beobachtungseinheit | **ein Inserat** (`id`) zum Zeitpunkt des Scrapes. Das ist weder eine Buchung noch ein Gast noch eine Wohnung im physischen Sinn. |
| Umfang | 77 149 Zeilen × 90 Spalten, `id` eindeutig, keine doppelten Zeilen |

### 0.5 Kritischer Befund zur Preisvariable

Laut Data Dictionary ist `price` der «daily price in local currency», und das `$` ist «a technical artifact of the export». Im Snapshot von 2026 enthält der Datensatz jedoch **Spalten, die im Data Dictionary v4.3 nicht dokumentiert sind**: `price_quote_checkin_date`, `price_quote_checkout_date`, `price_quote_total_price`, `price_quote_price_per_night`, `price_quote_raw` (JSON), `estimated_occupancy_l365d`, `estimated_revenue_l365d`, `availability_eoy`, `number_of_reviews_ly` und `hosts_time_as_*`.

Die Sichtung zeigt:

- `price` stimmt in allen 43 006 Fällen, in denen beide Werte vorliegen, exakt mit `price_quote_price_per_night` überein. Dieser Wert ist bei 98.8 % der Inserate `total_price / Nächte`.
- Der Preis ist also **ein Preis pro Nacht aus einer Preisabfrage für einen konkreten Aufenthalt**, nämlich ein bestimmtes Check-in-Datum und eine bestimmte Anzahl Nächte. Die Dauer entspricht in 86 % der Fälle `minimum_nights`.
- Im JSON steht als Währung **EUR**. Die Gebühren (`cleaning_fee`, `service_fee`) sind fast immer leer, Steuern erscheinen nur in etwa 10 % der Abfragen.
- Bei Abfragen über **28 oder mehr Nächte** ist das Inserat praktisch immer «monthly priced», also ein Monatspreis mit Langzeitrabatt (5 950 von 5 953 bepreisten Fällen). Damit wird **eine andere Grösse** gemessen als bei Kurzaufenthalten.
- Die Check-in-Daten der Abfragen reichen von September 2026 bis September 2027. Der Median liegt etwa 15 Tage nach dem Scrape. Der Zeitpunkt ist eine mögliche Störgrösse (Saison).

**Folge:** Gemessen wird ein **angebotener Abfragepreis pro Nacht in EUR**. Das ist weder der bezahlte Preis noch der Umsatz noch die Nachfrage. Die nicht dokumentierten Spalten `estimated_occupancy_l365d` und `estimated_revenue_l365d` sind Modellschätzungen von Inside Airbnb mit unbekannter Methode. Sie werden **nicht** als Fakten zu Auslastung oder Umsatz verwendet.

---

## 1. Motivation und Forschungsfragen

### 1.1 Motivation

Wer in Paris eine Unterkunft sucht oder die Kurzzeitvermietung politisch beurteilt, fragt zuerst: «Was kostet eine Nacht, und wovon hängt das ab?» Ein einzelner Durchschnittspreis beantwortet das schlecht. Preise sind rechtsschief, Unterkunftsart und Grösse vermischen sich, und einzelne Extremwerte können Kennzahlen verschieben. Das Projekt soll zeigen, welche Aussagen der Datensatz trägt und wie stark sie von Datenentscheidungen abhängen.

### 1.2 Drei Kandidaten

| | Forschungsfrage | Machbarkeit mit diesen Daten | Bewertung |
|---|---|---|---|
| **A** | Wie unterscheiden sich die angebotenen Preise pro Nacht nach **Unterkunftsart, Kapazität und Lage**, und wie robust sind diese Unterschiede gegenüber extremen Preisen und den Abfragebedingungen? | Alle Variablen sind vorhanden. Gut abgedeckt: VL01 bis VL04, gezielt VL05. | **empfohlen** |
| B | Unterscheiden sich Inserate mit **Mittelfrist-Mindestaufenthalt (≥ 28 Nächte)** von Kurzzeitinseraten in Preis, Lage und Host-Struktur? | Machbar und regulatorisch interessant. Der Preis ist dann aber ein rabattierter Monatspreis, und eine Begründung verlangt Domänenwissen zu den Pariser Regeln, das wir nicht belegen können. | als Robustheitsaspekt in A enthalten |
| C | Hängen **Bewertungen** (`review_scores_*`) oder die **Bewertungszahl** mit dem Preis zusammen? | Bewertungen sind keine Nachfrage. Bei 17 % der bepreisten Inserate fehlen sie strukturell, weil es keine Reviews gibt. Die Scores sind stark gestaucht (Deckeneffekt). Eine «Nachfrage»-Deutung wäre nicht haltbar. | nicht empfohlen |

### 1.3 Empfehlung: Frage A

Frage A passt am besten zum Auftrag. Sie verlangt genau das Datenverständnis, das hier heikel ist: Was ist der Preis, wer hat keinen Preis, was ist ein Extremwert? Ausserdem trägt sie sinnvolle Gruppenvergleiche und Zusammenhänge mit Drittvariablen, und jede Methode hat dabei eine klare Funktion. Die vorgeschlagene Richtung aus dem Auftrag ist **bearbeitbar**, braucht aber zwei Präzisierungen:

1. Unter «Preis» ist ein **angebotener Abfragepreis** zu verstehen, kein bezahlter Preis.
2. Zur Robustheit gehören neben Extremwerten auch die **Abfragebedingungen** (Dauer, Zeitpunkt) und die **Host-Abhängigkeit**.

**Hauptfrage:**
> Wie unterscheiden sich die auf Airbnb angebotenen Preise pro Nacht für Inserate in Paris (Snapshot September 2026) nach Unterkunftsart, Kapazität und Arrondissement, und wie robust sind diese Unterschiede gegenüber extremen Preisen, den Bedingungen der Preisabfrage und Mehrfachinseraten derselben Hosts?

**Teilfragen (bauen aufeinander auf):**

- **TF1 – Datenbasis:** Was misst die Preisvariable, für welche Inserate liegt ein Preis vor, und wie unterscheiden sich Inserate mit Preis von solchen ohne Preis?
- **TF2 – Verteilung und Robustheit:** Wie ist der Preis pro Nacht verteilt, welche Lage- und Streuungsmasse beschreiben ihn angemessen, und wie stark verändern plausible Extremwerte diese Kennzahlen?
- **TF3 – Gruppen und Zusammenhänge:** Wie unterscheiden sich die Preisverteilungen nach Unterkunftsart, Kapazität und Arrondissement? Bleibt der Zusammenhang mit der Kapazität innerhalb der Unterkunftsarten bestehen, und wie stark überlappen die Gruppen?

---

## 2. Zielpopulation, Datenbasis und Aussagegrenzen

| Ebene | Definition |
|---|---|
| **Inhaltliche Zielpopulation** | Airbnb-Inserate in der Stadt Paris (20 Arrondissements), die im September 2026 **buchbar angeboten** wurden |
| **Beobachtete Datenbasis** | Inserate, die Inside Airbnb beim Scrape gefunden hat (über die Quartiersuche oder als «previous scrape» der letzten 65 Tage) und für die eine Preisabfrage einen Preis lieferte |
| **Analysedatensatz (Kern)** | Inserate mit Preis **und** Abfrage über weniger als 28 Nächte: 37 584 Inserate von 25 382 Hosts (vorläufig) |

**Was die Aussagen bedeuten:** Es sind Beschreibungen der **Angebotsseite** zu einem Zeitpunkt. Sie gelten für Inserate, nicht für Gäste, Buchungen oder Wohnungen.

**Was sie nicht bedeuten:**

- **Bezahlter Preis:** Rabatte, Verhandlungen, Gebühren und Steuern sind nur teilweise enthalten.
- **Typischer Preis einer Nacht im Jahr:** Jedes Inserat hat einen anderen Abfragetermin.
- **Nachfrage oder Auslastung:** Laut Data Dictionary kann ein Kalendertag nicht verfügbar sein, weil er gebucht **oder** vom Host blockiert wurde.
- **Ursache:** «Die Lage verursacht den Preis» lässt sich nicht zeigen, weil Lage, Grösse und Unterkunftsart gemeinsam variieren.

**Bekannte Auswahlprozesse (VL01, S. 20–21, 25):**

- **Sampling durch den Scraper:** Inside Airbnb sieht nur, was die Suche liefert. Was die Suche ausschliesst, fehlt, und das ist nicht quantifizierbar.
- **Selektion durch fehlende Preise (survivorship-ähnlich):** Bei 43.6 % der Inserate fehlt der Preis. Diese Inserate sind fast alle nicht verfügbar (siehe Abschnitt 5).
- **Measurement:** Der Preis hängt von der abgefragten Dauer und vom Termin ab, ist also ein Messinstrument mit Bedingungen.
- **Abhängigkeit:** 45.9 % der bepreisten Inserate gehören Hosts mit mindestens zwei Inseraten, 22 % Hosts mit mindestens zehn. Ein einzelner Host hat 234 bepreiste Inserate. Die Beobachtungen sind daher nicht unabhängig.

---

## 3. Relevante Variablen

| Variable | Bedeutung (laut Data Dictionary bzw. Sichtung) | Speichertyp → Messniveau | Rolle | Datenlage (alle 77 149) |
|---|---|---|---|---|
| `price` | Preis pro Nacht der Abfrage, EUR, als Text mit `$` | str → **ratio** (metrisch, Null wäre «gratis») | Zielvariable | 33 612 fehlend (43.6 %), keine Werte ≤ 0, Min 10.38, Max 100 666 |
| `price_quote_checkin_date`, `…_checkout_date` | Termin der Abfrage (nicht dokumentiert) | str → Datum (**intervall**), daraus `naechte_abfrage` (**ratio**, diskret) | Abfragebedingung, Kontrollgrösse | fehlt bei 29 078 |
| `price_quote_raw` | JSON mit Währung, Rabatten, `is_monthly_priced` und `is_available` (nicht dokumentiert) | str → mehrere nominale Felder | Validierung von Währung und Definition | fehlt bei 29 078 |
| `room_type` | Entire home/apt, Private room, Hotel room, Shared room | str → **nominal** | Gruppierung (TF3), Drittvariable | vollständig. Hotel (386) und Shared (150) sind klein. |
| `accommodates` | maximale Gästezahl | int → **ratio**, aber diskret mit vielen Ties (1–16) | Kapazität (TF3) | vollständig, keine Nullen |
| `bedrooms` | Anzahl Schlafzimmer | float → **ratio**, diskret | zweites Kapazitätsmass (Gegenprobe) | 4 754 bepreiste Inserate mit **0** sind meist «Entire rental unit», plausibel Studios. Das ist eine **echte Null, kein Fehlwert**. |
| `neighbourhood_cleansed` | Arrondissement (20 Namen), per Geokoordinate zugeordnet | str → **nominal** | Lage (TF3) | vollständig, je Arrondissement mindestens 1 902 Inserate |
| `latitude`, `longitude` | WGS84 | float → intervall | nur zur Kontrolle oder Karte (optional) | vollständig |
| `host_id`, `calculated_host_listings_count` | Host und Anzahl seiner Inserate im Scrape | int → nominal bzw. ratio | Abhängigkeit, Sensitivität | vollständig |
| `minimum_nights` | Mindestaufenthalt | float → ratio | Erklärung der Abfragedauer | 116 fehlend (bepreist) |
| `availability_30/365`, `has_availability` | verfügbare Kalendertage | int → ratio | **nur** zur Erklärung der fehlenden Preise, nicht als Auslastung | – |
| `source` | «neighbourhood search» oder «previous scrape» (Dictionary) | str → nominal | Erklärung der fehlenden Preise | 44 105 leer. Laut Dictionary sollte es zwei Werte geben, im Snapshot ist der erste aber leer. Das wird geprüft und dokumentiert. |
| `number_of_reviews_ltm` | Reviews der letzten 12 Monate | int → ratio (Zählung) | Aktivitätsindikator für den Vergleich mit und ohne Preis | – |
| `property_type` | frei gewählter Typ | str → nominal | Fallprüfung bei Extremwerten | – |

Nicht verwendet: `bathrooms` (zu 100 % leer; `bathrooms_text` wäre der Ersatz, wird aber nicht benötigt), `estimated_*` (undokumentierte Modellwerte), Textfelder (nur bei Fallnotizen) und `review_scores_*` (siehe Kandidat C).

---

## 4. Analyseschritte in fester Reihenfolge

1. **Rohdaten laden und prüfen (NB01):** IDs, Duplikate, Datentypen, Parsing von `price` (Text mit `$` und Tausender-Komma), Abgleich mit `price_quote_price_per_night` und `total_price / Nächte`, Währung aus dem JSON, Datumsfelder.
2. **Messniveaus festlegen** (Hand-Mapping wie in NB01 §1), getrennt vom dtype.
3. **Fehlende Werte dokumentieren:** insgesamt sowie Fehlrate des Preises nach `room_type`, Arrondissement, `availability_365 = 0`, `source` und Reviews in den letzten 12 Monaten. Danach die Inserate **mit und ohne Preis** in Unterkunftsart, Kapazität und Lage vergleichen (Selektionsfolgen).
4. **Bereinigungstabelle** mit Schritt, Regel, Begründung, entfernten Zeilen, Anteil und verbleibenden Zeilen. Erst danach werden Preise angesehen.
5. **Verteilungsdiagnostik des Preises (NB02):** Kennzahlen (Mittelwert, Median, getrimmtes Mittel, SD, IQR, MAD), ECDF, Histogramm mit KDE (lineare und Log-Achse), QQ-Plot gegen die Normalverteilung für den Preis und für log(Preis).
6. **Extremwerte:** Tukey-Zäune und modifizierter z-Score **je Unterkunftsart**, Fallnotizen für die obersten Fälle und vorab definierte Sensitivitätsvarianten (Abschnitt 5.3).
7. **Gruppen (NB03):** Unterkunftsart, dann Kapazität innerhalb der Unterkunftsart, dann Arrondissement innerhalb eines vergleichbaren Segments. Berichtet werden Lage, Streuung, Gruppengrösse und **Überlappung**.
8. **Zusammenhang Kapazität–Preis:** Darstellung je Stufe, Spearman ρ (mit Kendall τ als Gegenprobe), gesamt und **innerhalb** der Unterkunftsarten (Simpson-Prüfung).
9. **Bedingte Anteile (VL05):** Anteil der Inserate oberhalb einer vorab festgelegten Preisgrenze je Gruppe, mit absoluten Häufigkeiten und Bezugsgruppe.
10. **Robustheit (NB04):** Die zentralen Kennzahlen aus 7–9 unter den Varianten «alle Preise», «Extremwerte gekennzeichnet ausgeschlossen», «ein Inserat pro Host», «inklusive ≥ 28 Nächte» und «Check-in innerhalb von 30 Tagen». Danach die Synthese mit einer Antwort auf die Hauptfrage.

---

## 5. Entscheidungen zu fehlenden, ungültigen und extremen Werten

### 5.1 Fehlende Preise

- **Befund (Sichtung):** Von den Inseraten mit `availability_365 = 0` haben 97.6 % keinen Preis. Bei `source = previous scrape` sind es 91 %. Bei Inseraten ohne Review in den letzten 12 Monaten fehlt der Preis zu 65 %, mit Review zu 24 %. Bei 29 078 Inseraten fehlt auch jede Preisabfrage, bei 4 534 lieferte die Abfrage keinen Preis.
- **Konsequenz:** MCAR ist unplausibel, weil die Fehlrate von beobachteten Merkmalen abhängt (NB01 §3.2). Ob MAR oder MNAR vorliegt, lässt sich aus den Daten **nicht** entscheiden (NB01 §3.4). Wir vermuten als **Annahme**, dass vor allem nicht aktiv angebotene oder blockierte Inserate keinen Preis haben. Für diese Inserate existiert dann gar kein «angebotener Preis».
- **Entscheidung:** **Keine Imputation des Preises.** Eine Imputation (zum Beispiel mit dem Gruppenmedian) würde einen Angebotspreis für Inserate erfinden, die gar nicht angeboten werden. Bei MNAR wäre sie zudem verzerrt (VL01, S. 36). Wir definieren die Zielpopulation stattdessen ausdrücklich als «buchbar angebotene Inserate». Anschliessend zeigen wir, wie sich diese Basis in Unterkunftsart, Kapazität und Lage von allen Inseraten unterscheidet.

### 5.2 Ungültige und unplausible Werte

| Prüfung | Vorläufiger Stand | Vorgehen |
|---|---|---|
| Preis ≤ 0 | keine | trotzdem als Regel festhalten |
| Parsing (`$`, Komma) | alle 43 537 parsebar | Rohspalte bleibt erhalten, neue Spalte `preis_eur` |
| Währung | im JSON überall EUR, wo angegeben | Inserate ohne Währungsangabe werden gezählt und dokumentiert |
| `is_available = False` trotz Preis | 531 | behalten und kennzeichnen, Sensitivität mit Ausschluss |
| `bedrooms = 0` | 4 754, meist Studios | echte Null, kein Fehler |
| `accommodates` | 1–16, keine Nullen | – |
| Abfragen ≥ 28 Nächte | 5 953 bepreist, fast alle «monthly priced» | **im Kern ausgeschlossen**, weil eine andere Messgrösse vorliegt (rabattierter Monatspreis pro Nacht). Begründet wird das mit der Definition, nicht mit dem Ergebnis. Als Sensitivität wieder aufgenommen. |

### 5.3 Extremwerte

- **Befund:** 29 Kerninserate kosten ≥ 10 000 € pro Nacht, einzelne Zwei-Personen-Wohnungen liegen über 40 000 €.
- **Grundsatz** (NB03_Ausreisserregeln §3, «im Zweifel behalten, robust berichten, dokumentieren»): Kein Wert wird gelöscht, nur weil er hoch ist. Drei Fälle werden getrennt:
  1. **Belegter Erfassungsfehler:** Im Datensatz nicht belegbar, weil keine externe Quelle verfügbar ist. Deshalb wird **kein** Wert als Fehler korrigiert.
  2. **Plausible besondere Angebote,** etwa grosse Wohnungen und Villen für 10 bis 16 Personen: behalten.
  3. **Statistisch auffällig und inhaltlich zweifelhaft:** Kennzeichnung nach einer **vorab** festgelegten Regel. Vorschlag: Preis pro Person und Nacht über 1 000 € **oder** Preis ≥ 10 000 €. Dazu Fallnotizen für die obersten etwa 10 Fälle (Typ, Kapazität, Reviews, Verfügbarkeit, Abfragedauer, Host-Inserate).
- **Hauptanalyse:** alle Kernpreise, mit robusten Kennzahlen (Median, IQR, Quantile).
- **Sensitivität:** (a) gekennzeichnete Fälle ausgeschlossen, (b) Winsorisierung am 99.5-%-Quantil je Unterkunftsart als neue Spalte. Berichtet wird, ob sich Mediane, Rangfolgen, ρ und bedingte Anteile ändern. Die Regeln stehen vor der Gruppenauswertung fest und werden nachträglich nicht angepasst.
- **Statistische Markierungsregeln** (Tukey, modifizierter z-Score) dienen nur zur **Beschreibung** des rechten Rands je Unterkunftsart. Sie sind kein Löschkriterium, da sie bei rechtsschiefen Verteilungen grosse Teile der legitimen rechten Flanke markieren (NB03_Ausreisserregeln §2 zeigt das an den Titanic-Preisen). Für die Pariser Preise wird die Zahl der Markierungen in NB02 berechnet.

### 5.4 Host-Abhängigkeit

Mehrere Inserate desselben Hosts sind keine unabhängigen Beobachtungen und können eine Gruppe dominieren. Die Prüfung umfasst drei Schritte:

1. Anteil der Inserate von Hosts mit ≥ 2 und ≥ 10 Inseraten je Gruppe.
2. Sensitivität «ein Inserat pro Host», zufällig gezogen mit festem Seed.
3. Optional ein Cluster-Bootstrap über `host_id` (Abschnitt 8).

---

## 6. Zuordnung: Teilfrage → Variablen → Methode → Grafik → mögliche Aussage → Einschränkung

| TF | Variablen | Methode und Begründung | Grafik | Mögliche Aussageform (noch ohne Ergebnis) | Einschränkung | Vorlesung (Folie = PDF-Seite) | TA-Notebook |
|---|---|---|---|---|---|---|---|
| 1 | `price`, `room_type`, Arrondissement, `availability_365`, `source`, `number_of_reviews_ltm` | Fehlrate je Gruppe: Der **Mechanismus** ist wichtiger als die Anzahl. Mit- und ohne-Preis-Vergleich der Kategorien über Anteile, weil diese nominal sind. | Balken der Fehlrate je Gruppe; gestapelte Anteile mit und ohne Preis | «Ein Preis fehlt vor allem bei …; Inserate mit Preis sind häufiger/seltener …» | MAR/MNAR nicht beweisbar; Scraper-Selektion nicht quantifizierbar | VL01 S. 8–13 (Messniveaus), 20–21, 25 (Bias), 31–36 (MCAR/MAR/MNAR, Strategiematrix), 40–42 (EDA) | NB01 §1, §2, §3.1–3.4, §4.3 (stille Datenreduktion), §5 Checkliste |
| 1 | `price`, `price_quote_*` | Abgleich der Definitionen (Gleichheit, Quotient): Messung verstehen, bevor gerechnet wird | Tabelle; Histogramm der Abfragedauer | «`price` ist der Abfragepreis pro Nacht in EUR für einen Termin …» | Dictionary v4.3 dokumentiert die Abfrage nicht | VL01 S. 25 (Measurement Bias) | NB01 §2 (Measurement) |
| 2 | `preis_eur` | Mittelwert, Median, 10-%-getrimmtes Mittel; SD (`ddof=1`, nur ergänzend), IQR, MAD. Die Form entscheidet, welche Kennzahl trägt. | ECDF; Histogramm mit KDE (FD-Bins, `bw_adjust` 0.5/1/2) auf linearer **Achse** und log-**Achse** | «Typischer Preis (Median) …, mittlere 50 % zwischen …; der Mittelwert liegt … darüber» | Beschreibt nur die Kernbasis; abhängig vom Abfragetermin | VL02 S. 7, 11, 13–14, 18–21, 26, 31–35, 43, 47–50 | NB02 §1.1–1.4, §2.4–2.5, §3.1, §3.3 |
| 2 | `preis_eur`, log(`preis_eur`) | Normal-QQ-Plot, um Bogen oder S-Form zu erkennen. Die Log-**Transformation** ergibt eine neue Variable und ist kein Beweis für eine Log-Normalverteilung. | QQ-Plots nebeneinander | «Rechtsschief mit schwerem rechtem Tail; auch log(Preis) weicht an den Enden ab …» | Ein QQ-Plot beweist keine Verteilungsfamilie | VL03 S. 18, 29–34 | NB03 §2.3, §3.2–3.4 (Diagnose-Routine, Entscheidungssatz) |
| 2 | `preis_eur`, `room_type` | Tukey und modifizierter z-Score **je Gruppe** zur Beschreibung; Fallnotizen; Kennzahlen mit und ohne Eingriff | Tabelle der Sensitivität; Boxplot (log-Achse) mit markierten Fällen | «Median und IQR ändern sich um weniger als …; der Mittelwert um …» | Fehler nicht extern verifizierbar | VL02 S. 13–14, 32, 35; VL03 S. 15, 25–26 | NB03_Ausreisserregeln §1–3 |
| 3 | `preis_eur`, `room_type` | Gruppenkennzahlen mit **n**; Überlappung als Quantilvergleich (z. B. Anteil der Private Rooms über dem Median von Entire home/apt). Hotel und Shared werden wegen kleinem n und anderem Produkt nur beschrieben. | Boxplot mit Punkten bzw. Violine (`cut=0`, Quartile) auf log-Achse; **ECDF-Overlay** für die Überlappung | «Median A > Median B; dennoch liegen …% von B über dem Median von A» | Ohne Inferenz bleibt es Beschreibung; Notches sind kein Test | VL03 S. 15–17, 19–25, 31 | NB03 §1.1 (Counts vs. Dichte), §2.1–2.4, §3.1 |
| 3 | `accommodates` (und `bedrooms`), `preis_eur`, `room_type` | Streudiagramm ist bei 16 diskreten Stufen wenig sinnvoll, deshalb **Boxplot je Kapazitätsstufe**. **Spearman ρ** statt Pearson wegen Schiefe, Extremwerten und Monotonie statt Linearität; **Kendall τ** als Gegenprobe wegen vieler Ties. Gesamt **und** je Unterkunftsart (Drittvariable, Simpson). | Boxplots je Stufe (log-Achse), nach `room_type` gefacettet; Median-Linie je Stufe | «Gesamt ρ = …, innerhalb Entire home/apt ρ = …; die Richtung hält/kehrt …» | Korrelation ≠ Kausalität; Kapazität ist eine Angabe des Hosts | VL04 S. 8–10, 21–22, 26–30, 36, 39–41, 44 | NB04 §1.1, §3.1–3.3, §4.1, §4.3, §6 Transfer |
| 3 | Arrondissement, `preis_eur` (optional Preis pro Person) | Gruppenmediane und IQR nach Median sortiert, **innerhalb eines Vergleichssegments** (Entire home/apt, 2 Gäste), damit die Zusammensetzung (Grösse/Art) den Lagevergleich nicht treibt. Keine Korrelation, weil die Variable nominal ist. | Punkt-und-Intervall-Grafik (Median, Q1–Q3) je Arrondissement, mit n | «Im Segment liegt der Median zwischen … (günstigstes) und … (teuerstes); die IQR überlappen …» | Restliche Zusammensetzungsunterschiede (Ausstattung, Abfragetermin) bleiben | VL04 S. 36, 39–41 (Drittvariable); NB04 §6 Schritt 5 (nominal → Gruppenvergleich) | NB04 §4.3, §6 |
| 3 | `preis_eur`, `room_type`, Arrondissement | **Empirische bedingte Anteile** P(Preis > Grenze ∣ Gruppe) mit absoluten Häufigkeiten. Grenze vorab festgelegt: das 90-%-Quantil der gesamten Kernbasis («oberes Preisdezil»). Ergänzend die Umkehrung P(Gruppe ∣ oberes Dezil), um die Verwechslung der Bedingung zu zeigen. | Häufigkeitstabelle; Balken mit n | «Von n Private Rooms liegen k (…%) im oberen Dezil; von allen Inseraten im oberen Dezil sind …% Entire homes» | Beschreibende Anteile des Snapshots, kein Wahrscheinlichkeitsmodell | VL05 S. 16–18, 22 | (kein TA-Notebook zu VL05 im Repository) |
| alle | Varianten aus Abschnitt 5 | Sensitivitätstabelle: zentrale Kennzahlen je Variante | Tabelle oder «Forest»-artige Punktgrafik | «Die Rangfolge der Gruppen ist unter allen Varianten gleich/ändert sich bei …» | Varianten decken nicht alle Unsicherheiten ab | VL02 S. 35; VL06 S. 20 | NB03_Ausreisserregeln §3 (Sensitivität statt Löschen) |

**Bewusst nicht eingesetzte Vorlesungsinhalte:**

- **Pearson r** wird nur als Kontrast gezeigt, nicht als Hauptmass, weil der Preis stark schief ist und einzelne Punkte r kippen (VL04 S. 21–22).
- Eine **Korrelationsmatrix** oder einen **Pairplot** über viele Spalten verwenden wir nicht. Er erzeugt Zahlen ohne Bezug zur Frage.
- Für **Bayes** gibt es hier keine Prior-/Likelihood-Situation. Die Umkehrung bedingter Anteile reicht, um VL05 S. 18 sinnvoll anzuwenden.
- **Bernoulli/Binomial/Poisson** passen nicht. Der Preis ist keine Zählung. `number_of_reviews` ist zwar eine Zählung, aber die Expositionszeit ist unterschiedlich, die Inserate sind heterogen, und Überdispersion ist zu erwarten (VL05 S. 37, Glossar S. 56). Ein Poissonmodell wäre damit nicht durch den Entstehungsprozess gedeckt und beantwortet unsere Frage nicht.
- **Zeitreihen- und Trendkorrelation** (VL04 S. 38) ist nicht relevant, weil nur ein Snapshot vorliegt.

---

## 7. Notebook-Struktur und Präsentationsdramaturgie

### 7.1 Struktur (an die TA-Konventionen angelehnt: Seed, Paketversionen, «Problem → Code → Bedeutung»)

```
data/raw/paris_2026-09-16/      Rohdaten, unverändert, mit SHA-256 in der README
data/processed/                 reproduzierbar erzeugte Analysedatensätze (Parquet/CSV)
src/daten.py                    Laden, Parsen, Bereinigungsschritte, Bereinigungstabelle
src/grafik.py                   gemeinsame Farben und Plotfunktionen
notebooks/01_datenverstaendnis_und_qualitaet.ipynb   TF1
notebooks/02_preisverteilung_und_robustheit.ipynb    TF2
notebooks/03_gruppen_und_zusammenhaenge.ipynb        TF3
notebooks/04_synthese.ipynb                          Sensitivität, Antwort, Grenzen
outputs/figures/, outputs/tables/
docs/projektvorschlag.md, docs/entscheidungslog.md, docs/folienplan.md, docs/praesentation.pptx
README.md, requirements.txt
```

Jedes Notebook folgt den sieben geforderten Punkten. Die Entscheidungssätze sammeln wir zusätzlich in `docs/entscheidungslog.md`, wie es NB03/NB04 verlangen. `data/raw` sollte wegen der Grösse (40 MB) nicht ins Git, sondern per Download-Funktion mit Prüfsumme geholt werden.

### 7.2 Dramaturgie (etwa 9 Kernfolien)

1. **Frage:** Was kostet eine Nacht in Paris, und wovon hängt das ab?
2. **Was ist «der Preis»?** Ein Abfragepreis pro Nacht für einen Termin, nicht bezahlt, nicht Umsatz.
3. **Wer hat keinen Preis?** Selektion und Zielpopulation, Bereinigungstabelle.
4. **Form der Verteilung:** Warum Median und IQR, lineare gegen logarithmische Achse.
5. **Extremwerte:** Fallnotiz und Sensitivität («Was ändert sich, was nicht?»).
6. **Unterkunftsart:** Lageunterschied und Überlappung (ECDF).
7. **Kapazität innerhalb der Unterkunftsart:** ρ gesamt und je Gruppe.
8. **Lage im Vergleichssegment:** Arrondissements, bedingte Anteile im oberen Dezil.
9. **Robustheit und Antwort:** Sensitivitätstabelle, Antwort, Grenzen.

Anhang: Methodendetails, weitere Sensitivitäten, wahrscheinliche Dozentenfragen mit Antworten.

---

## 8. Kernumfang und optionale Erweiterungen

**Kern (verbindlich):** TF1–TF3 mit den Methoden aus Abschnitt 6, die Bereinigungstabelle, die Sensitivitätsvarianten aus Abschnitt 5 sowie Präsentation und Anhang.

**Optional (nur bei Zeit und nach Rücksprache):**

1. **VL06, Bootstrap mit Host-Clustern:** Ein Intervall für den Median je Unterkunftsart oder die Mediandifferenz, mit Resampling ganzer Hosts. Dabei sind drei Punkte zu beachten:
   - Der **Parameter** und die **Population** müssen benannt werden, etwa der Median eines gedachten Prozesses, der vergleichbare Angebote erzeugt.
   - Unser Snapshot ist fast eine **Vollerhebung** der gefundenen Inserate. Für die Beschreibung genau dieses Snapshots ist keine Inferenz nötig. Die Endlichkeitskorrektur aus VL06 S. 29 und 35 würde das Intervall bei n ≈ N gegen null schrumpfen lassen.
   - Ein Intervall behebt **keinen** Selection Bias (VL06 S. 20).

   **Empfehlung:** höchstens als «Stabilitätsmass» im Anhang.
2. **Karte** der Mediane je Arrondissement (`neighbourhoods.geojson`).
3. **Kalenderdaten** (`calendar.csv.gz`): Prüfen, ob dort Preise je Datum vorliegen, um Termin und Saison zu kontrollieren. In neueren Snapshots ist die Preisspalte dort möglicherweise leer, das wäre zuerst zu prüfen.
4. **Hypothesentests (VL07)** sind nicht beauftragt und werden ohne Zufallsstichprobe ohnehin nicht eingebaut.
