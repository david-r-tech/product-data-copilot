# Product Data Copilot — Product-Owner-Artefakte

**Stand: 28. September 2026.** Dieses Dokument beschreibt die Produktentscheidungen des eigenständig entwickelten lokalen Prototyps. Die Stakeholder-Rollen sind angenommene Zielgruppen für die Anforderungsarbeit, keine dokumentierten Interviews. Das Messkonzept ist definiert, aber es liegen noch keine belastbaren Vorher-nachher-Messwerte vor.

## Vision und Product Goal

**Vision:** E-Commerce-Teams sollen unvollständige Produktlisten aus dem Einkauf zügig in nachvollziehbare Korrekturarbeit und fachlich prüfbare Produkttexte überführen können, ohne KI-Entwürfe mit gesicherten Produktfakten zu verwechseln.

**Product Goal für den lokalen MVP:** Eine Person kann eine CSV-/Excel-Tabelle laden, konkrete Datenprobleme pro SKU erkennen, deutsche HTML-Produkttexte mit Bullet Points und Übersetzungen erzeugen, die Ergebnisse anhand der Quelldaten je Artikel prüfen und nur ausdrücklich freigegebene Texte als Excel-Datei exportieren. Die Quelldatei bleibt unverändert.

**Bewusste Grenze:** Die regelbasierte Datenprüfung erkennt Pflichtfeld-, Format- und einzelne explizite Merkmalsabweichungen. Sie bestätigt weder vollständige inhaltliche Konsistenz noch Marktplatz- oder Rechtskonformität. Die KI kann trotz Prompt-Regeln unbelegte Aussagen erzeugen.

## Stakeholder-Map

| Rolle | Interesse / Entscheidung | Bedarf im Produkt |
| --- | --- | --- |
| Einkauf / Lieferantendaten | Liefert teils unvollständige Merkmale | Verständliche Hinweise auf fehlende oder abweichende Angaben |
| Produktdatenpflege | Korrigiert den Quellbestand | Korrekturliste mit SKU, Problem und nächstem Schritt |
| Content-Review | Prüft Texte und Übersetzungen fachlich | Sichtbare Quelle, Entwurf und eindeutige Freigabe je Artikel |
| E-Commerce-Verantwortliche | Entscheidet über Weiterverwendung | Nur freigegebene Texte im Text-Export, Überblick über offene Arbeit |
| IT / Datenschutz | Bewertet Datenfluss und Betrieb | Lokale Anwendung, bewusster API-Aufruf, keine Schlüssel im Repository |

Diese Rollen sind eine Arbeitsannahme. Interviews oder eine Freigabe durch ein reales Unternehmen werden nicht behauptet.

## Roadmap und MoSCoW-Backlog

| Priorität | Produktinkrement | Stand / Begründung |
| --- | --- | --- |
| Must | CSV/XLSX sicher laden und SKU eindeutig zuordnen | Umgesetzt; Voraussetzung für jede nachvollziehbare Prüfung |
| Must | Fehlende/ungültige Angaben und explizite Merkmalsabweichungen als Korrekturaufgaben zeigen | Umgesetzt; macht Datenprobleme handlungsfähig |
| Must | DE-Produkttext und Bullet Points erzeugen; Text und Bullets in EN/FR/ES übersetzen | Umgesetzt; Kernnutzen für Content-Teams |
| Must | Pro Artikel menschlich prüfen und nur Freigegebenes als Text-Excel exportieren | Umgesetzt; reduziert Risiko unbelegter KI-Aussagen im Übergabeergebnis |
| Should | Verständliche Prüfstatus-Übersicht und getrennten Qualitätsbericht bieten | Umgesetzt; unterstützt Priorisierung und Übergabe |
| Could | Weitere Spaltenzuordnung und vertiefte semantische Widerspruchsprüfung | Offen; Bedarf und Fehlalarmquote erst mit realistischen Tabellen validieren |
| Won't for MVP | Automatische Publikation, Shop-Integrationen, Benutzerkonten, Datenbank, Rechtsfreigabe | Bewusst ausgeschlossen; für den lokalen MVP nicht erforderlich |

**Reihenfolge:** Datenbasis und Prüfbarkeit → Textgenerierung/Übersetzung → menschliche Freigabe → nutzbarer Export → Validierung an realistischen Testtabellen. Der heutige Stand deckt die ersten vier Schritte ab; die letzte Stufe ist Teil der Endabnahme.

## Beispiel-User-Story mit Akzeptanzkriterien

**Als Content-Prüferin** möchte ich nach der Generierung einer ganzen Produktliste jeden Artikel mit seinen Quelldaten vergleichen und einzeln freigeben oder ablehnen, **damit** nur geprüfte Inhalte an die nächste Stelle übergeben werden.

- **Gegeben** mehrere erzeugte Entwürfe, **wenn** ich noch keinen Artikel freigegeben habe, **dann** ist kein Text-Excel-Download verfügbar.
- **Gegeben** ein freigegebener und ein abgelehnter Artikel, **wenn** ich das Text-Excel herunterlade, **dann** stehen nur Text und passende Quelldaten des freigegebenen Artikels in den zwei Blättern.
- **Gegeben** ein neuer Datei- oder Sprachkontext, **wenn** ich ihn auswähle, **dann** gilt die frühere Freigabe nicht für dessen Texte.
- **Gegeben** ein erzeugter Entwurf, **wenn** er eine unbelegte Produkteigenschaft enthält, **dann** kann ich ihn ablehnen; die App erklärt, dass die fachliche Prüfung beim Menschen liegt.

Die technische Zuordnung und Tests stehen in der [Anforderungsnachverfolgung](requirements_traceability.md).

## Definition of Done für ein MVP-Inkrement

Ein Inkrement ist für diesen Prototyp fertig, wenn sein Nutzerablauf verständlich beschrieben ist, die relevanten Akzeptanzkriterien automatisiert oder manuell geprüft wurden, ein Fehlerfall verständlich behandelt wird, Quell- und Exportdaten unverändert beziehungsweise sicher bleiben, README und Anforderungsnachweise den tatsächlichen Stand beschreiben und keine Zugangsdaten eingecheckt wurden. Für die Veröffentlichung kommen ein visueller Excel-Check, die Bestätigung des privaten Status vor der Freigabe und anschließend die Prüfung des GitHub-Links ohne Anmeldung hinzu.

## Messkonzept — noch keine Wirkungsbehauptung

| Kennzahl | Definition | Erhebung für einen späteren Vergleich |
| --- | --- | --- |
| Durchlaufzeit | Minuten vom bereitgestellten Lieferanten-Excel bis zum exportierten, geprüften Textsatz | Gleiche Testliste einmal manuell und einmal mit Tool bearbeiten; Start/Ende protokollieren |
| Nacharbeit | Anzahl fachlicher Korrekturen an KI-Entwürfen vor Freigabe | Pro SKU Korrekturen und Grund erfassen, z. B. unbelegtes Merkmal oder unpräzise Übersetzung |
| Freigabequote | Freigegebene Artikel / erzeugte prüfbare Artikel | Für einen definierten Durchlauf zählen; getrennt von technischen Fehlern ausweisen |
| Technische Fehlerquote | Fehlgeschlagene Generierungen / angestoßene Artikel | Statusliste und API-Fehler je Durchlauf erfassen |

Erst mit wiederholten, vergleichbaren Durchläufen und fachlich geprüften Ergebnissen lassen sich Aussagen über Zeitersparnis oder Qualitätsgewinn treffen.

## Dokumentierte Produktentscheidung aus einem KI-Test

Ein Test mit fiktiven Produkten zeigte einen sprachlich plausiblen, aber nicht belegten Produktnutzen und eine ungenaue Produktart-Übersetzung. Daraus folgten strengere Prompt-Regeln gegen erfundene Fakten und ein separater, ausdrücklicher Human-Review-Schritt vor dem Text-Export. Die Prompt-Regel senkt das Risiko, ersetzt aber keine fachliche Prüfung; auch ein freigegebener Text ist keine automatische Markt- oder Rechtsfreigabe.
