# Folienplan

*Abgeleitet aus den ausgeführten Notebooks (Snapshot 2026-09-16). Dieselben Texte stehen als Sprechernotizen in `docs/praesentation.pptx`. Rund 12 Kernfolien für etwa 15 Minuten, danach ein Anhang.*

**Roter Faden:** Problem und Frage → Datenbasis und Grenzen → Methodenentscheidungen → zentrale Ergebnisse → Robustheit und alternative Erklärungen → Antwort und Einschränkungen.

## 1. Was kostet eine Nacht in Paris?

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Titel und Frage
- **Grafik/Tabelle:** –
- **Herkunft der Zahlen:** –
- **Sprechtext:** Wir haben untersucht, wie sich die auf Airbnb angebotenen Übernachtungspreise in Paris nach Unterkunftsart, Grösse und Lage unterscheiden – und wie sehr man diesen Unterschieden trauen kann. Grundlage ist der Inside-Airbnb-Snapshot vom September 2026.
- **Übergang:** Wir beginnen mit der Antwort und zeigen danach, wie wir zu ihr gekommen sind.

## 2. Frage und Antwort vorweg

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Lage und Grösse prägen den angebotenen Preis stärker als die Unterkunftsart allein
- **Grafik/Tabelle:** drei Kennzahl-Karten (keine Grafik)
- **Herkunft der Zahlen:** NB04 §6; Werte aus NB03 §3–5
- **Sprechtext:** Unsere Hauptfrage: Wie unterscheiden sich die angebotenen Preise pro Nacht nach Unterkunftsart, Kapazität und Arrondissement – und wie robust ist das? Drei Antworten. Erstens Lage: Bei gleicher Unterkunft für zwei Gäste liegt zwischen dem günstigsten und dem teuersten Arrondissement ein Faktor zwei. Zweitens Kapazität: Der Preis steigt monoton mit der Gästezahl, Spearman rho 0.60. Drittens Zimmerart: Der rohe Unterschied von Faktor 1.57 schrumpft bei gleicher Gästezahl auf etwa 1.14. Die Richtung all dieser Aussagen ist robust – das absolute Preisniveau dagegen nicht.
- **Übergang:** Damit diese Zahlen etwas bedeuten, müssen wir zuerst klären, was der Preis im Datensatz überhaupt misst.

## 3. Der «Preis» ist ein Abfragepreis, kein bezahlter Preis

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Jeder Preis gilt für einen konkreten Termin und eine konkrete Aufenthaltsdauer
- **Grafik/Tabelle:** outputs/figures/01_abfragebedingungen.png
- **Herkunft der Zahlen:** NB01 §3; Data Dictionary v4.3 (Inside Airbnb)
- **Sprechtext:** Das Data Dictionary nennt price einen 'daily price'. Im aktuellen Snapshot gibt es aber undokumentierte Abfragefelder. Wir haben geprüft: price ist in 100 Prozent der Fälle identisch mit dem Preis pro Nacht einer Testabfrage – Gesamtpreis geteilt durch Nächte, Währung Euro. Links sieht man die Abfragedauer: meist ein bis sechs Nächte. Ab 28 Nächten liefert Airbnb fast immer einen rabattierten Monatspreis – das ist eine andere Messgrösse, deshalb haben wir diese 5'953 Inserate aus der Hauptanalyse genommen. Rechts: Die Termine liegen grösstenteils im September und Oktober 2026. Wichtig: Das ist kein bezahlter Preis, kein Umsatz und kein Mass für Nachfrage.
- **Übergang:** Für fast die Hälfte der Inserate gibt es aber gar keinen Preis – das ist die nächste Frage.

## 4. Wer keinen Preis hat, ist meist gar nicht buchbar

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Wir imputieren den Preis nicht, sondern beschreiben bewusst nur buchbar angebotene Inserate
- **Grafik/Tabelle:** outputs/figures/01_fehlrate_preis.png + Bereinigungsschritte aus outputs/tables/01_bereinigungstabelle.csv
- **Herkunft der Zahlen:** NB01 §4–7; outputs/tables/01_bereinigungstabelle.csv, 01_fehlrate_preis_nach_gruppen.csv
- **Sprechtext:** Bei 43.6 Prozent der Inserate fehlt der Preis. Die Grafik zeigt die Fehlrate je beobachteter Gruppe: Inserate ohne einen einzigen verfügbaren Tag im nächsten Jahr haben zu 98 Prozent keinen Preis, verfügbare nur zu 16 Prozent. Das ist sicher nicht völlig zufällig. Ob MAR oder MNAR vorliegt, können wir aus den Daten nicht entscheiden. Unsere Annahme: Für nicht buchbare Inserate existiert gar kein Angebotspreis. Eine Imputation würde Angebote erfinden. Deshalb definieren wir die Zielpopulation als buchbar angebotene Inserate. Unten die Bereinigung: von 77'149 auf 37'584 Inserate. Diese sind etwas grösser und gehören häufiger Mehrfach-Hosts – das nehmen wir in die Robustheitsprüfung mit.
- **Übergang:** Mit diesen 37'584 Preisen schauen wir uns zuerst die Form der Verteilung an.

## 5. Stark rechtsschief: Wir berichten Median und Quartile

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Der Mittelwert beschreibt kein typisches Inserat – erst die Form, dann die Kennzahl
- **Grafik/Tabelle:** outputs/figures/02_histogramm_linear_log.png
- **Herkunft der Zahlen:** NB02 §1–4; outputs/tables/02_kennzahlen_kern.csv
- **Sprechtext:** Links die lineare Achse, schon bei P99 abgeschnitten – trotzdem drängt sich alles links zusammen. Rechts dieselben Werte auf einer logarithmischen Achse; wichtig: Das ist nur eine andere Achse, die Werte bleiben Euro. Die Verteilung ist eingipflig und stark rechtsschief mit einer Flanke bis 100'000 Euro. Der Mittelwert von 367 Euro liegt deutlich über dem Median von 240; 73 Prozent der Inserate kosten weniger als der Mittelwert. Die Standardabweichung ist sogar grösser als der Mittelwert. Wir berichten deshalb Median und Quartile: Die mittlere Hälfte kostet zwischen 162 und 386 Euro. Auch der Logarithmus ist laut QQ-Plot an den Rändern nicht normal – wir behaupten also keine Verteilungsfamilie.
- **Übergang:** Was machen wir mit den extremen Preisen ganz rechts?

## 6. Extremwerte: behalten, kennzeichnen, robust berichten

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Die Wahl der Kennzahl wiegt schwerer als die Frage, ob man Extremwerte löscht
- **Grafik/Tabelle:** outputs/figures/02_sensitivitaet_kennzahlen.png
- **Herkunft der Zahlen:** NB02 §5–7; outputs/tables/02_sensitivitaet_extremwerte.csv, 02_fallnotizen_top12.csv
- **Sprechtext:** Tukey-Zäune würden allein bei den ganzen Unterkünften 2'525 Preise markieren – das ist die legitime rechte Flanke, kein Fehler. Wir haben stattdessen vorab eine inhaltliche Regel festgelegt: ab 10'000 Euro oder über 1'000 Euro pro Person und Nacht. Das betrifft 117 Inserate, 0.3 Prozent. Ein Beispiel: ein Studio für zwei Personen zu 34'537 Euro, Name 'indisponible' – vermutlich ein Sperrpreis. Belegen können wir das nicht, deshalb löschen wir nichts. Die Grafik zeigt warum das kaum zählt: Ohne diese Fälle ändern sich Median, IQR und P90 um höchstens 1.3 Prozent, der Mittelwert um 8 und die Standardabweichung um 61 Prozent.
- **Übergang:** Mit robusten Kennzahlen können wir jetzt Gruppen vergleichen – zuerst die Zimmerart.

## 7. Ganze Unterkünfte sind teurer, die Gruppen überlappen

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Ein Lageunterschied der Mediane ist nicht dasselbe wie eine Trennung der Gruppen
- **Grafik/Tabelle:** outputs/figures/03_zimmerart_box_ecdf.png
- **Herkunft der Zahlen:** NB03 §1; outputs/tables/03_kennzahlen_zimmerart.csv, 03_ueberlappung_zimmerart.csv
- **Sprechtext:** Links der Boxplot je Zimmerart auf log-Achse, mit n. Ganze Unterkünfte kosten im Median 252 Euro, Privatzimmer 160 – Faktor 1.57. Rechts die ECDF: Eine Kurve weiter rechts heisst teurer. Die Kurve der ganzen Unterkünfte liegt fast überall rechts; erst im obersten Prozent kreuzen sich die Kurven, und diese Kreuzung verschwindet, wenn man die gekennzeichneten Extremwerte weglässt. Gleichzeitig überlappen die Verteilungen stark: 27 Prozent der Privatzimmer sind teurer als die typische ganze Unterkunft. Hotel- und geteilte Zimmer sind klein und beschreiben wir nur.
- **Übergang:** Ist das wirklich ein Effekt der Zimmerart – oder sind ganze Unterkünfte einfach grösser?

## 8. Gleiche Gästezahl: Der Zimmerart-Unterschied schrumpft

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Kapazität ist eine Drittvariable: Sie erklärt einen grossen Teil des Rohunterschieds
- **Grafik/Tabelle:** outputs/figures/03_zimmerart_gleiche_kapazitaet.png
- **Herkunft der Zahlen:** NB03 §3–4; outputs/tables/03_zimmerart_bei_gleicher_kapazitaet.csv, 03_korrelation_kapazitaet.csv
- **Sprechtext:** Ganze Unterkünfte nehmen im Median vier Gäste auf, Privatzimmer zwei. Vergleicht man bei gleicher Gästezahl, liegen die Linien nahe beieinander: Das Verhältnis der Mediane fällt von 1.57 auf 1.10 bis 1.27. Die gepunkteten Linien sind die Gesamtmediane – ihr Abstand ist vor allem ein Grössenunterschied. Zum Zusammenhang Kapazität–Preis: Spearman rho 0.60 bei ganzen Unterkünften, 0.43 bei Privatzimmern, also innerhalb jeder Art positiv, kein Simpson-Effekt. Pearson r läge nur bei 0.22, weil wenige Extremwerte es drücken – deshalb das Rangmass. Kausal ist das nicht: Kapazität steht auch für Fläche und Ausstattung.
- **Übergang:** Dasselbe Prinzip – Drittvariablen festhalten – wenden wir auf die Lage an.

## 9. Lage: Faktor 2 zwischen den Arrondissements

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Ganze Unterkunft für 2 Gäste: von 133 € (Ménilmontant) bis 271 € (Louvre)
- **Grafik/Tabelle:** outputs/figures/03_lage_segment.png
- **Herkunft der Zahlen:** NB03 §5; outputs/tables/03_lage_segment_2_gaeste.csv, 03_bedingte_anteile_lage.csv
- **Sprechtext:** Um Lage nicht mit Grösse und Zimmerart zu vermischen, vergleichen wir nur ganze Unterkünfte für zwei Gäste – 12'145 Inserate, mindestens 302 je Arrondissement. Punkt ist der Median, der Balken die mittlere Hälfte. Von Ménilmontant mit 133 Euro bis Louvre mit 271 Euro: Faktor zwei. Die Extreme überlappen kaum, nur 7 Prozent in Ménilmontant sind teurer als der Louvre-Median; in der Mitte überlappen die Bänder dagegen stark. Bedingte Anteile: Im Luxembourg liegen 27 Prozent im oberen Dezil des Segments, in Vaugirard 10 Prozent – obwohl Vaugirard 8 Prozent aller teuren Inserate stellt. Das liegt nur an seiner Grösse: P von teuer gegeben Arrondissement ist nicht P von Arrondissement gegeben teuer.
- **Übergang:** Halten diese drei Befunde, wenn wir die Daten anders behandeln?

## 10. Was hätte uns widerlegen können?

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** Keine vorab festgelegte Variante kippt eine der drei Aussagen
- **Grafik/Tabelle:** outputs/figures/04_sensitivitaet_pruefkennzahlen.png
- **Herkunft der Zahlen:** NB04 §1–2; outputs/tables/04_sensitivitaet_alle_varianten.csv
- **Sprechtext:** Wir haben vorab festgelegt, was jede Aussage widerlegen würde – die grauen Linien – und alle Kennzahlen unter sieben Varianten neu gerechnet: ohne Extremwerte, winsorisiert, ohne fragwürdige Abfragen, ein Inserat pro Host, nach Abfragetermin getrennt und mit den Monatsabfragen. Kein Punkt erreicht eine graue Linie. Kapazität und Lage sind auch in ihrer Grösse stabil: rho zwischen 0.56 und 0.60, Lagefaktor zwischen 1.84 und 2.04, die Rangfolge der Arrondissements korreliert immer mit mindestens 0.97. Beim Zimmerart-Aufpreis bei gleicher Gästezahl ist nur die Richtung stabil – er liegt je nach Variante zwischen 3 und 30 Prozent.
- **Übergang:** Robust sind also die Unterschiede. Was dagegen nicht robust ist, zeigt die nächste Folie.

## 11. Nicht robust: das Preisniveau hängt am Abfragetermin

- **Abschnitt:** Vortrag
- **Zentrale Botschaft:** «Eine Nacht kostet 240 €» gilt nur für die abgefragten Termine – überwiegend September/Oktober 2026
- **Grafik/Tabelle:** outputs/figures/04_abfragetermin.png
- **Herkunft der Zahlen:** NB04 §3–5; outputs/tables/04_sensitivitaet_alle_varianten.csv, 04_cluster_bootstrap.csv
- **Sprechtext:** Jedes Inserat wurde für einen anderen Termin abgefragt. Bei höchstens sieben Tagen Vorlauf liegt der Median bei 299 Euro, bei 31 bis 60 Tagen bei 191. Ob das Saison, kurzfristige Preissetzung oder Auswahl ist, können wir nicht trennen. Die Gruppenunterschiede bleiben aber innerhalb früher und später Termine bestehen. Auch Mehrfach-Hosts heben das Niveau: Mit nur einem Inserat pro Host sinkt der Median von 240 auf 218 Euro. Zum Vergleich ein Bootstrap über Hosts: Das Verhältnis 1.57 schwankt nur zwischen 1.50 und 1.65. Die zufällige Unsicherheit ist also viel kleiner als die systematischen Einflüsse – und gegen die hilft kein Intervall.
- **Übergang:** Damit können wir die Frage beantworten – und sagen, wo die Antwort endet.

## 12. Antwort und Grenzen

- **Abschnitt:** Vortrag
- **Grafik/Tabelle:** Zwei Spalten (Antwort / Grenzen), keine Grafik
- **Herkunft der Zahlen:** NB04 §6–7
- **Sprechtext:** Unsere Antwort: Die angebotenen Preise unterscheiden sich vor allem nach Lage und Grösse – Faktor zwei zwischen den Arrondissements, ein monotoner Anstieg mit der Gästezahl. Die Zimmerart selbst macht bei gleicher Grösse nur einen kleinen Unterschied. Diese Unterschiede sind robust; das absolute Preisniveau nicht. Grenzen: Wir beschreiben nur buchbare Inserate, fast die Hälfte hat keinen Preis. Wir messen Abfragepreise, keine bezahlten Preise. Wir halten jeweils nur eine Drittvariable fest und machen keine kausalen Aussagen. Und es ist ein einziger Snapshot.
- **Übergang:** Danke – wir freuen uns auf Fragen. Im Anhang liegen Details und Antworten auf erwartbare Fragen.

## 13. Anhang

- **Abschnitt:** Anhang
- **Grafik/Tabelle:** –
- **Herkunft der Zahlen:** –
- **Sprechtext:** Methodische Details, weitere Sensitivitäten und Antworten auf erwartbare Fragen.

## 14. A1 · Bereinigungstabelle und Kennzeichnungen

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** Zwei Filter, zwei Kennzeichnungen – jede Zeile mit Regel, Begründung und Anzahl
- **Grafik/Tabelle:** Tabellen outputs/tables/01_bereinigungstabelle.csv, 01_kennzeichnungen_kern.csv
- **Herkunft der Zahlen:** NB01 §7; outputs/tables/01_bereinigungstabelle.csv, 01_kennzeichnungen_kern.csv
- **Sprechtext:** Gefiltert wird nur zweimal: fehlender Preis und Monatsabfragen. Kennzeichnungen entfernen nichts; sie werden nur in der Sensitivität ausgeschlossen.

## 15. A2 · Kapazität im Detail

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** Monotoner Anstieg in jeder Zimmerart; Rangmasse stabil, Pearson extremwertgetrieben
- **Grafik/Tabelle:** outputs/figures/03_kapazitaet_box.png + Tabelle 03_korrelation_kapazitaet.csv
- **Herkunft der Zahlen:** NB03 §3; outputs/tables/03_korrelation_kapazitaet.csv, 03_median_je_kapazitaet.csv
- **Sprechtext:** Boxplots je Kapazitätsstufe, getrennt nach Zimmerart. Stufen ab 9 Gästen nur in der Grafik zusammengefasst. Kendall tau ist wegen der vielen Ties kleiner als rho, aber in derselben Reihenfolge.

## 16. A3 · Verteilungsdiagnostik: QQ-Plots und KDE

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** Auch log10(Preis) ist nur in der Mitte normalnah – keine Verteilungsfamilie behauptet
- **Grafik/Tabelle:** outputs/figures/02_qq_roh_log.png, 02_kde_log_bandbreiten.png
- **Herkunft der Zahlen:** NB02 §3–4
- **Sprechtext:** Rohpreis: extremer Bogen. log10(Preis): in der Mitte auf der Geraden, an beiden Rändern abweichend, rechts stärker. KDE mit bw_adjust 0.5, 1, 2: der eine Gipfel bleibt stabil, die Zacken bei 0.5 sind Rauschen bzw. runde Preise.

## 17. A4 · Bedingte Anteile: oberes Preisdezil

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** P(teuer | Zimmerart) und P(Zimmerart | teuer) beantworten verschiedene Fragen
- **Grafik/Tabelle:** Tabelle outputs/tables/03_bedingte_anteile_zimmerart.csv
- **Herkunft der Zahlen:** NB03 §2; Grenze = P90 des Kerns = 643 €
- **Sprechtext:** Von 32'292 ganzen Unterkünften liegen 3'454 im oberen Dezil, 10.7 Prozent; von 4'908 Privatzimmern 265, 5.4 Prozent. Umgekehrt sind 91.9 Prozent der teuren Inserate ganze Unterkünfte – aber die machen schon 85.9 Prozent aus. Empirische Anteile, kein Binomialmodell: Inserate sind wegen Host-Clustern keine unabhängigen Versuche.

## 18. A5 · Bootstrap über Hosts (VL06, optional)

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** Ein Stabilitätsmass – kein Schutz gegen Selection Bias
- **Grafik/Tabelle:** outputs/figures/04_cluster_bootstrap.png + Tabelle 04_cluster_bootstrap.csv
- **Herkunft der Zahlen:** NB04 §5; 1000 Wiederholungen, Seed 42
- **Sprechtext:** Parameter: Median je Zimmerart in einem gedachten Prozess, der vergleichbare Angebote erzeugt. Zufallsannahme: Hosts unabhängig, deshalb ziehen wir ganze Hosts mit Zurücklegen. Für den Snapshot selbst wäre ein Intervall unnötig – fast Vollerhebung, Endlichkeitskorrektur gegen null.

## 19. A6 · Selektion: Inserate mit und ohne Preis

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** Inserate mit Preis sind aktiver, grösser und häufiger von Mehrfach-Hosts
- **Grafik/Tabelle:** Tabelle outputs/tables/01_vergleich_mit_ohne_preis.csv + outputs/figures/01_selektion_lage.png
- **Herkunft der Zahlen:** NB01 §5
- **Sprechtext:** Bei Zimmerart und Lage ist die Auswahl fast neutral – höchstens 3.4 Prozentpunkte Verschiebung je Arrondissement. Bei Host-Typ, Aktivität und Grösse nicht. Deshalb berichten wir Kennzahlen je Gruppe statt eines 'Paris-Gesamtpreises'.

## 20. A7 · Mögliche Fragen (1/2)

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** Kurze, sachlich gestützte Antworten
- **Grafik/Tabelle:** Frage-Antwort-Karten
- **Herkunft der Zahlen:** NB01–NB04; docs/entscheidungslog.md
- **Sprechtext:** Warum imputiert ihr die fehlenden Preise nicht? – Sie fehlen fast nur bei nicht buchbaren Inseraten (97.6 % bei 0 verfügbaren Tagen). Ein imputierter Preis wäre ein erfundenes Angebot; bei MNAR zudem verzerrt. Warum löscht ihr Ausreisser nicht nach Tukey? – Tukey markiert 2'525 ganze Unterkünfte – die legitime Flanke. Markiert heisst nicht falsch; Fehler sind nicht belegbar. Robuste Kennzahlen ändern sich ohne die 117 Fälle um ≤ 1.3 %. Ist der Preis nicht einfach log-normalverteilt? – Log10 ist symmetrischer, aber der QQ-Plot weicht an beiden Rändern ab. Wir brauchen keine Familie: Mediane, Quantile und Ränge kommen ohne aus. Warum Spearman statt Pearson? – Kapazität ist diskret mit vielen Ties, die Form monoton, nicht linear, und Extremwerte drücken r auf 0.22 (ohne sie 0.50). ρ bleibt 0.60. Ist die Grenze von 28 Nächten nicht ergebnisgetrieben? – Nein: Ab 28 Nächten kennzeichnet Airbnb fast jede Abfrage als Monatspreis (5'950 von 5'953). Mit diesen Fällen bleiben alle Aussagen in ihrer Richtung bestehen (NB04).

## 21. A8 · Mögliche Fragen (2/2)

- **Abschnitt:** Anhang
- **Zentrale Botschaft:** Kurze, sachlich gestützte Antworten
- **Grafik/Tabelle:** Frage-Antwort-Karten
- **Herkunft der Zahlen:** NB01–NB04; docs/entscheidungslog.md
- **Sprechtext:** Ist der Lageeffekt kausal? – Nein. Lage bündelt Nachfrage, Wohnungsqualität und Regulierung. Wir halten nur Zimmerart und Kapazität fest; Ausstattung und Host-Typ nicht. Warum keine Tests oder Konfidenzintervalle? – Keine Zufallsstichprobe, sondern fast eine Vollerhebung. Ein Intervall behebt keinen Selection Bias. Der Host-Bootstrap im Anhang zeigt nur die Stabilität. Verfälscht der Abfragetermin die Gruppenvergleiche? – Er verschiebt das Niveau stark (299 € vs. 191 €). Innerhalb früher und später Termine bleiben die Gruppenunterschiede aber bestehen. Wie sicher ist eure Deutung der undokumentierten Felder? – price = Abfragepreis pro Nacht in 100 % der Fälle, EUR laut JSON. Die Deutung «Monatspreis» stützt sich auf das Feld is_monthly_priced und die Rabattposten. Warum zählt ihr Inserate und nicht Hosts? – Die Frage gilt dem Angebot. Mit einem Inserat pro Host sinkt der Median auf 218 €; die Gruppenunterschiede bleiben bestehen.

