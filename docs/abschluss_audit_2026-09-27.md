# Product Data Copilot – Abschlussprüfung vom 27.09.2026

> **Historischer Befund zum Ausgangscommit.** Die folgenden Reproduktionen und Prioritäten beschreiben den Zustand *vor* der anschließenden Korrektur. Sie sind keine aktuelle Liste offener Codefehler. Die aktuelle Anforderung/Abnahme steht in [requirements_traceability.md](requirements_traceability.md).

## Nachbearbeitung am 27.09.2026

- Die P1-Punkte 1–8 wurden gezielt umgesetzt: datensatzgebundener Review-Zustand, neue Freigabe bei jeder KI-Generierung, validierte Textimporte, eindeutige SKUs, sichere CSV/XLSX-Zellen, Abgleich von V2-Vorschlägen mit dem Quellprodukt, Entfernung des Demo-Laders aus der App und konsistente Readiness-Grenzen.
- P2-Punkt 9: Regressionstests für Import, Zustand, AI-Quellen, Streamlit-Abläufe und Export ergänzt. Letzter lokaler Stand: 186 bestandene Tests.
- P2-Punkte 10–13: README, Case Study, aktueller Kontext und Status auf das tatsächliche Produkt ausgerichtet. Der GitHub-Zugriff ohne Anmeldung, externe Veröffentlichungen, Live-AI-Qualität und eine visuelle Excel-Abnahme bleiben offene externe/manuelle Prüfungen.
- Nach dem Push wurde die Repository-Seite in einem nicht angemeldeten Browser geöffnet: GitHub zeigte 404. Der Link ist für Bewerbungsprüfer ohne zusätzliche Zugriffsregel aktuell nicht verwendbar.
- Der Eigentümer entschied anschließend, das Repository privat zu lassen und nur namentlich bekannten GitHub-Nutzern Zugriff zu geben. Bis solche Prüfer bekannt sind, ist „Quellcode auf Anfrage“ die korrekte öffentliche Formulierung.
- Später am selben Tag änderte der Eigentümer das Ziel auf einen öffentlichen GitHub-Link für Bewerbungen. Die Sichtbarkeit ist noch nicht umgestellt; bis zur Prüfung ohne Anmeldung ist der Link weiterhin nicht öffentlich verwendbar.
- Alle unten genannten Zeilennummern beziehen sich auf den geprüften Ausgangscommit und können nach den Korrekturen abweichen.

Geprüfter Stand: `6ef265cca65e7f3810140f4d6dac82bb9f5d14fd` (`main`). Zieltermin: 28.09.2026.

## Ergebnis

Der normale Beispieldaten-Ablauf funktioniert, und alle 122 vorhandenen Tests bestehen. Für einen belastbaren Abschluss als lokales Portfolio-MVP sind trotzdem gezielte Korrekturen erforderlich. Die wichtigsten Probleme betreffen Datenzuordnung, wiederverwendete Freigaben, Dateiimporte und Excel-Exporte. Mehr Funktionen oder ein großer Umbau sind für diesen Abschluss nicht nötig.

Diese Prüfung hat keine Produktfunktionen verändert. Die beschriebenen Fehler sind noch offen. Geändert wurden nur dieser Bericht und der Projektlog.

## Prüfungsumfang und Grenzen

- Bestandsaufnahme der 77 versionierten Dateien, des App-Codes, der 17 Python-Dateien unter `src`, der 10 Testdateien, der Beispieldaten und der 40 bisherigen Dokumentationsdateien.
- Prüfung des erreichbaren Git-Verlaufs mit 80 Commits und Mustersuche in 405 unterschiedlichen Text-Dateiversionen; zusätzlich Kontrolle der früheren Demo-XLSX-Dateien und Commit-Metadaten.
- Remote-Abfrage bestätigt: GitHub-Branch `main` und lokaler HEAD stehen auf demselben Commit. Der Remote meldet einen Branch und keine Tags.
- Alle 122 vorhandenen Tests, Syntaxprüfung und Diff-Prüfung erfolgreich.
- Zusätzliche Laufzeitprüfungen mit Streamlits `AppTest`: Beispielstart, Demo laden, Freigabe, Dateiwechsel, problematische Uploads und erneute KI-Generierung mit kontrollierter Testantwort.
- Tatsächliche Excel-Bytes erzeugt und wieder eingelesen; Tabellen, Produktzuordnung und Zelltypen untersucht.
- Keine echten KI-Aufrufe, keine Übertragung von Produktdaten an einen KI-Dienst und keine Prüfung der Qualität einer aktuellen Live-Modellantwort.
- Keine vollständige visuelle Browserabnahme oder manuelle Prüfung in Microsoft Excel durchgeführt. Automatisierte Streamlit-Prüfungen ersetzen diese abschließende Sichtprüfung nicht.
- Der GitHub-Connector und ein anonymer HTTP-Zugriff auf die konfigurierte Repository-URL liefern 404. Der Git-Remote ist dagegen erreichbar. Ob das Repository aktuell privat, umbenannt oder durch Berechtigungen eingeschränkt ist, wurde nicht abschließend geklärt. Öffentliche Sichtbarkeit, Issues, PR-Diskussionen und GitHub-Releases konnten deshalb nicht vollständig geprüft werden.
- Weitere Veröffentlichungen wurden vom Nutzer angekündigt; ihre Links lagen bei Erstellung dieses Berichts noch nicht vor. Portfolio, LinkedIn, Lebenslauf und andere externe Texte sind daher noch nicht geprüft.

## Prioritäten

- **P1:** Vor dem Abschluss beheben, weil Ergebnisse falsch zugeordnet, Freigaben ungewollt übernommen oder Dateien fehlerhaft verarbeitet werden können.
- **P2:** Vor dem Teilen mindestens klarstellen oder mit einem kleinen Abschlussblock erledigen.
- **Später:** Kein notwendiger Bestandteil des Abschlusses morgen.

## P1 – notwendige Codekorrekturen

### 1. Review- und KI-Zustand an den geladenen Datensatz binden

**Beobachtung:** Manuelle Review-Entscheidungen werden nur anhand der SKU gespeichert. Beim Upload einer anderen Datei werden diese Entscheidungen und V1-KI-Texte nicht zurückgesetzt. Der Management-Export übernimmt gespeicherte V1-Vorschläge ohne Prüfung, ob sie zum aktuellen Datensatz gehören.

**Reproduziert:** Produkt `ONE` auf `Ready for Export` gesetzt; anschließend eine neue Datei mit gleicher SKU, anderem Produktnamen und fehlender EAN geladen. Das neue Produkt bleibt `Ready for Export`, und der alte KI-Titel wird weiter angezeigt.

**Fundstellen:** [app.py](../app.py), Zeilen 704–716, 1032–1038, 1131–1146 und 1633–1640.

**Minimaler Abschluss:** Datensatz eindeutig identifizieren; bei einem tatsächlichen Datenwechsel alle dazugehörigen Review-Entscheidungen, KI-Antworten und abhängigen Auswahlen löschen oder getrennt speichern. Exporte dürfen nur Zustand des aktuellen Datensatzes verwenden.

**Abnahme:** Datei A → Datei B mit gleicher SKU sowie Upload → Beispieldaten übertragen weder Freigaben noch KI-Texte.

### 2. Neue KI-Generierung darf keine alte Freigabe erben

**Beobachtung:** Der Freigabeschlüssel enthält nur SKU, Zielfeld, bisherigen Wert und Vorschlag. Quelle, Begründung, Risiko und Generierung sind nicht enthalten. Bei einer neuen Live-Generierung wird die Entscheidungsliste nicht geleert.

**Reproduziert:** Einen Vorschlag freigegeben; neue Testantwort mit gleichem Text, aber anderer Begründung, nicht existierender Quelle und Risiko `high` erzeugt. Die neue Zeile wird sofort wieder als `approved` angezeigt.

**Fundstellen:** [app.py](../app.py), Zeilen 945–959 und 1750–1774. Der Demo-Lader setzt Entscheidungen bereits zurück, der Live-Pfad nicht.

**Minimaler Abschluss:** Jede neue Antwort beginnt mit `pending`; Freigaben an eine konkrete Antwortversion und deren Prüfinformationen binden.

**Abnahme:** Eine erneut erzeugte Antwort benötigt eine neue Entscheidung, auch wenn ihr vorgeschlagener Text unverändert ist.

### 3. Dateiimporte robust machen und Kennungen als Text erhalten

**Beobachtung:** CSV/XLSX werden ohne gezielte Datentypen, Prüfung des Dateiinhalts oder kontrollierte Fehlerbehandlung eingelesen.

**Reproduziert:**

| Eingabe | Aktuelles Ergebnis |
| --- | --- |
| SKU `000123`, EAN `0123456789012` in CSV | Werden zu `123` und `123456789012`; führende Nullen gehen verloren. |
| CSV nur mit Spaltenüberschriften | Abbruch mit `KeyError: overall_readiness_score`. |
| Leere CSV-Datei | Abbruch mit `No columns to parse from file`. |
| Beschädigte XLSX-Datei | Unbehandelter Fehler beim Einlesen. |
| Gültige Excel-Datei mit Endung `.XLSX` | Wird als CSV gelesen und verursacht einen Dekodierungsfehler. |
| CSV mit Semikolon | Wird als eine unbekannte Spalte akzeptiert; anschließend werden irreführende Fehlstellen berechnet. |

**Fundstellen:** [app.py](../app.py), Zeilen 1131–1146 sowie die anschließende Score-Auswertung.

**Minimaler Abschluss:** Kennungen unverändert als Text einlesen; leere Daten und ungeeignete Spaltenstruktur vor der Auswertung abweisen; Dateiendungen unabhängig von Großschreibung behandeln; Einlesefehler verständlich anzeigen. CSV-Trennzeichen entweder unterstützen oder das unterstützte Format ausdrücklich nennen und abweichende Dateien erkennbar ablehnen. Fehlende optionale Produktfelder dürfen weiterhin als Datenqualitätsprobleme behandelt werden.

**Abnahme:** Die obigen Fälle verlieren keine Kennungen und erzeugen keine unbehandelten App-Fehler. Der exportierte Snapshot erhält die eingelesenen Textkennungen.

### 4. Fehlende und doppelte SKUs korrekt behandeln

**Beobachtung:** SKU wird als Produktschlüssel verwendet, ohne ihre Eindeutigkeit zu prüfen. Fehlende SKUs bekommen zwar eine Anzeige wie `Row 1`, aber keinen eigenen Issue. Bei doppelten SKUs werden Issues vermischt; Review-Aufgaben verwenden den ersten gefundenen Produktnamen.

**Reproduziert:** Zwei verschiedene Produkte mit SKU `ONE`; nur das zweite hat eine fehlende EAN. Beide bekommen `Missing Data`, und die Aufgabe zur fehlenden EAN wird dem Namen des ersten Produkts zugeordnet. Ein ansonsten vollständiges Produkt ohne SKU erreicht 95 Punkte, `Ready` und `Ready for Export`, ohne Issue.

**Fundstellen:** [app.py](../app.py), Zeilen 537–548, 664–676 und 723–731.

**Minimaler Abschluss:** Fehlende und doppelte SKUs sichtbar beanstanden. Für morgen ist es ausreichend, mehrdeutige Datensätze kontrolliert zu sperren; alternativ stabile interne Zeilenkennungen konsequent für Zuordnung und Freigaben verwenden.

**Abnahme:** Kein Issue, Review-Status oder KI-Vorschlag landet beim falschen Produkt. Fehlende Identität wird nicht stillschweigend als exportbereit eingestuft.

### 5. Excel- und CSV-Exporte gegen Formelauswertung absichern

**Beobachtung:** Eingabetexte werden unverändert über `to_excel` bzw. `to_csv` ausgegeben. Excel interpretiert bestimmte Inhalte als Formeln. Nicht unterstützte Steuerzeichen können die Workbook-Erstellung abbrechen lassen; diese wird bereits während des normalen App-Durchlaufs ausgeführt.

**Reproduziert:** Die Produktbeschreibung `=1+1` wird im Management-Workbook in `Source Products!D2` als Formel gespeichert (`data_type = f`). Eine Beschreibung mit dem Steuerzeichen U+000B führt im App-Lauf zu `cannot be used in worksheets`.

**Fundstellen:** [app.py](../app.py), Zeilen 1069–1076 und 1089–1091; CSV-Downloads ab Zeile 1266.

**Minimaler Abschluss:** Eingabe- und KI-Texte in XLSX ausdrücklich als Text schreiben; CSV für die Nutzung in Tabellenprogrammen absichern. Unzulässige Steuerzeichen kontrolliert behandeln oder den Export mit verständlicher Meldung ablehnen. Die Behandlung dokumentieren, ohne das Original-DataFrame zu verändern.

**Abnahme:** Ein harmloser Testwert wie `=1+1` bleibt Text, und problematische Zeichen bringen die App nicht zum Absturz. Beides in beiden Excel-Exporten prüfen. Eine tatsächlich ausgeführte schädliche Formel wurde nicht getestet oder nachgewiesen.

### 6. KI-Vorschläge mit dem tatsächlichen Produkt abgleichen

**Beobachtung:** Der Parser prüft die Struktur, aber nicht, ob die SKU zum ausgewählten Produkt gehört, das Zielfeld zulässig ist, der bisherige Wert stimmt oder genannte Quellen tatsächlich existieren. Auch ein leerer Vorschlagswert kann freigegeben werden.

**Reproduziert:** Antworten mit SKU `WRONG`, Quelle `nonexistent`, Zielfeld `nonsense_field` oder leerem `proposed_value` bleiben `review_required` und damit über die UI grundsätzlich freigebbar. Das ist kein Beleg für echte Halluzinationen des verwendeten Modells; es ist eine nachgewiesene Lücke in der lokalen Validierung.

**Zusätzlicher Befund:** `get_ai_product_context` entfernt vorhandene Felder wie `translation_de`, `translation_en`, `warning_notes`, `ean`, `price` und `image_url`. Der V2-Adapter könnte sie verarbeiten, erhält sie im App-Pfad aber nicht. Damit fehlen bei Übersetzungs- und Sicherheitsprüfungen wichtige Originalinformationen. Fehlwerte wie `NaN` werden in den Prompt-Helfern zudem nicht durchgängig als leer behandelt.

**Fundstellen:** [suggestion_schema.py](../src/product_data_copilot/ai/suggestion_schema.py), Zeilen 184–200; [suggestion_parser.py](../src/product_data_copilot/ai/suggestion_parser.py), Zeilen 84–99; [app.py](../app.py), Zeilen 798–810 und 1696–1700.

**Minimaler Abschluss:** Nach dem Parsen gegen den aktuellen Produktdatensatz prüfen: richtige SKU, erlaubtes Zielfeld, nachvollziehbare vorhandene Quellen und tatsächlicher bisheriger Wert. Leere Vorschläge als Arbeitsauftrag darstellen, nicht als freigebbare Feldverbesserung. Den benötigten Produktkontext vollständig und fehlwertbereinigt an den Prompt übergeben.

**Abnahme:** Falsche Identität, erfundene Quellen, unerlaubte Felder und leere Verbesserungen bleiben nicht freigebbar. Strukturprüfung darf weiterhin keine Garantie für faktische Richtigkeit vortäuschen.

### 7. Demo-Vorschläge und echtes Exportmaterial sauber zuordnen

**Beobachtung:** Der Demo-Lader verbindet eine feste Testantwort mit dem aktuell ausgewählten Produkt. Die enthaltene SKU lautet immer `DEMO-SKU-001`, unabhängig von den geladenen Produkten. Der Hinweis auf die Demo-Herkunft ist in der UI vorhanden, wird aber nicht als entsprechender Herkunftshinweis in das Workbook übernommen.

**Reproduziert:** Standardauswahl `GEN-023`; Demo laden und einen Vorschlag freigeben. `Approved Improvements` enthält `DEMO-SKU-001`, während diese SKU im mitgelieferten Original-Snapshot nicht existiert. Ein ausdrücklicher Demo-Herkunftsmarker fehlt im Workbook.

**Fundstellen:** [app.py](../app.py), Zeilen 1705–1734; [Demo-Testantwort](../tests/fixtures/smart_suggestions_v2_demo_response.json); [export_helpers.py](../src/product_data_copilot/export/export_helpers.py), Exportzusammenstellung.

**Minimaler Abschluss:** Die Demo mit einem passenden, getrennten Demo-Quelldatensatz betreiben und den Export ausdrücklich als Demo kennzeichnen; alternativ Demo-Exporte von normalen Produkt-Exporten trennen. Die SKU einfach auf ein fremdes Produkt umzuschreiben würde die unbelegten Inhalte nicht korrekt machen.

**Abnahme:** Exportierte Verbesserungen gehören zum enthaltenen Quelldatensatz; Testdaten sind auch außerhalb der App eindeutig als Testdaten erkennbar.

### 8. Bereitschaftsstatus darf kritische Fehler nicht verdecken

**Beobachtung:** `readiness_status` wird ausschließlich aus dem gewichteten Durchschnitt gebildet. Kritische Issues können von guten Teilwerten überdeckt werden; der davon getrennte Review-Status widerspricht anschließend der Anzeige `Ready`.

**Reproduziert:** Ein ansonsten vollständiges Produkt mit fehlender EAN erhält 92 Punkte und `Ready`, gleichzeitig `Missing Data`. Eine Ein-Zeichen-Beschreibung erreicht 98 Punkte und `Ready for Export`, obwohl ein Beschreibungs-Issue vorhanden ist.

**Fundstellen:** [app.py](../app.py), Zeilen 572–649 und 661–676; [review_helpers.py](../src/product_data_copilot/review/review_helpers.py), Funktion `derive_review_status`.

**Minimaler Abschluss:** Kritische Issues und fehlende Produktidentität müssen den Gesamtstatus begrenzen. Klar erklären, was Score, technischer Prüfstatus und manuelle Geschäftsentscheidung jeweils bedeuten. Warnungen müssen nicht zwingend denselben Sperreffekt haben; diese Regel sollte ausdrücklich festgelegt sein.

**Abnahme:** Kein Produkt mit kritischen Datenlücken erscheint automatisch als bereit. Score und Status bleiben nachvollziehbar.

## P2 – Codequalität und nachprüfbarer Abschluss

### 9. Gezielt die bisher ungetesteten Abläufe absichern

Die 122 Tests sind eine hilfreiche Basis, decken aber überwiegend Hilfsfunktionen ab. Es gibt bisher keine `AppTest`-Tests und keine automatisierte Abdeckung der oben geprüften vollständigen App-Abläufe; Exporttests prüfen überwiegend DataFrames und Blattzuordnungen statt der tatsächlich geschriebenen Excel-Zelltypen.

Vor Abschluss müssen Regressionstests mindestens Dateiwechsel, erneute KI-Freigabe, Kennungserhalt, leere/fehlerhafte Uploads, SKU-Zuordnung, kritische Bereitschaftsstatus und tatsächliche Workbook-Ausgabe absichern. Die in diesem Audit ausgeführten Zusatzprüfungen wurden bewusst nicht als Produktänderung in die Testsuite geschrieben.

Danach einen dokumentierten Durchlauf im Browser und mit beiden geöffneten Excel-Dateien durchführen. Der aktuelle Teststand allein ist kein Nachweis, dass die gefundenen Fehler behoben sind.

### 10. Installation und Grenzen reproduzierbar beschreiben

In [requirements.txt](../requirements.txt) sind alle sechs Pakete ohne Versionsangaben aufgeführt. Die README nennt keine getestete Python-Version und beschreibt das erwartete Uploadschema nur indirekt über die Beispieldaten.

Für den Abschluss: getestete Python- und Paketversionen festhalten, eine isolierte Installation nach der Anleitung prüfen und ein kleines Uploadbeispiel bzw. die erforderlichen Spalten und das CSV-Format nennen. Vorhandene Projektabhängigkeiten gezielt festlegen; kein großer Verpackungsumbau nötig.

Die Audit-Prüfungen liefen mit Python 3.14.4, Streamlit 1.58.0, pandas 3.0.3, openpyxl 3.1.5, openai 2.38.0 und pytest 9.1.1. Das ist ein getesteter Umgebungsstand, keine behauptete Unterstützung aller Python-Versionen. Eine saubere Neuinstallation wurde in diesem Audit nicht durchgeführt.

Zusätzlich bei den Prüfregeln ehrlich bleiben: `is_valid_ean` prüft derzeit nur Zeichen und Länge, keine Prüfziffer; `is_valid_price('inf')` ist wahr; `9,99` wird nicht als positiver Preis erkannt. Prüfziffernprüfung und endliche Preise sind sinnvolle kleine Nachbesserungen. Andernfalls müssen Formate und Prüfgrenzen klar benannt werden. Bild-URLs und Compliance werden nur heuristisch geprüft.

## Bereits gepushte Inhalte und öffentliche Darstellung

### 11. Git-Hygiene, Kontaktdaten und Erreichbarkeit klären

**Vor weiterem Teilen nötig:**

- Die Commit-Metadaten enthalten den ausgeschriebenen Namen und eine vollständige geschäftliche Gmail-Adresse. Das ist kein gefundenes Passwort, sollte aber eine bewusste Veröffentlichung sein. Falls unerwünscht: künftige Commits mit passender nicht öffentlicher Commit-Adresse erstellen und die bereits geteilte Historie gesondert bewerten. Ein normaler neuer Commit entfernt alte Metadaten nicht. Kein pauschales Umschreiben der Historie nur aus kosmetischen Gründen.
- `.gitignore` schützt den alten Management-Export, aber **nicht** `product_data_copilot_improved_export.xlsx`. Das wurde mit `git check-ignore` geprüft. Diese Lücke schließen, damit ein später im Projektordner gespeicherter Export mit Echtdaten nicht versehentlich eingecheckt wird. Die Anforderung NFR-005 ist im Dokument bereits als umgesetzt markiert, obwohl diese Lücke besteht.
- Den für Bewerbungen/Portfolio verwendeten GitHub-Link ohne Anmeldung prüfen. Aktuell war die konfigurierte URL anonym nicht erreichbar. Sichtbarkeit bzw. Zugriffsfreigabe bewusst entscheiden; ein Repository-Rename ist dafür nicht grundsätzlich erforderlich.
- Lizenzabsicht klären und README-Wortlaut daran ausrichten. Es gibt keine `LICENSE`-Datei; daraus folgt keine Aussage über die tatsächliche GitHub-Sichtbarkeit. Es muss nicht zwingend für morgen eine bestimmte Open-Source-Lizenz gewählt werden.

**Entlastende Befunde:** Keine `.env` in der erreichbaren Git-Historie, keine Treffer der verwendeten Muster für echte Provider-Tokens/private Schlüssel und keine entsprechenden Treffer in Commit-Nachrichten. In den untersuchten Text-Dateiversionen keine ausgeschriebenen privaten Benutzerverzeichnisse oder E-Mail-Adressen; die Adresse steht in den Commit-Metadaten. Das ist eine begrenzte Musterprüfung, kein lückenloses Geheimnis-Audit.

Die entfernte deutsche Möbel-Demo bleibt in früheren Commits abrufbar. Die beiden gefundenen XLSX-Versionen enthalten jeweils zehn Demo-Produkte und `openpyxl` als Ersteller. Es ergab sich daraus kein konkreter Befund, der eine sofortige Löschung der Historie rechtfertigt.

### 12. README und Case Study fachlich präzisieren

Die Positionierung als lokales MVP und die Grenzen zu SaaS, Integrationen und rechtlichen Garantien sind bereits vernünftig beschrieben. Korrigiert bzw. ergänzt werden sollten:

- **Freigabe:** V2 hat einen technischen Freigabeschritt; V1 zeigt Entwürfe und erlaubt deren Export ohne entsprechenden Freigabestatus. Die allgemeine Formulierung „User approval is required“ darf nicht den Eindruck einer überall technisch erzwungenen Sperre erzeugen. Zusätzlich erst nach Behebung von Punkt 2 behaupten, dass neue Vorschläge immer neu geprüft werden müssen.
- **KI-Sicherheit:** Quellenangaben und strukturierte Ausgabe bedeuten derzeit keinen Abgleich mit dem Original. Nach Punkt 6 präzise angeben, was validiert wird und was menschliche Prüfung bleibt.
- **Lokal:** Die App läuft lokal; beim bewussten Start einer KI-Generierung werden ausgewählter Produktkontext und Prüfkontext an OpenAI gesendet. Dies vor der Aktion und in der README klar nennen. Ohne KI-Aufruf erfolgen die Datenprüfung und lokale Exporterstellung ohne diesen Provider-Aufruf.
- **Originaldaten:** Die ursprüngliche Datei wird nicht überschrieben. Der exportierte „Original Source Snapshot“ ist jedoch eine Kopie der eingelesenen Tabelle, keine unveränderte Kopie der Originaldatei inklusive Formaten, Formeln und aller Arbeitsblätter. Den Kennungsverlust aus Punkt 3 beheben.
- **Validierung:** Keine umfassende EAN-, URL-, Marketplace- oder Compliance-Validierung behaupten, wenn tatsächlich nur einfache Regeln angewendet werden.

Fundstellen: [README](../README.md), besonders AI Safety / Human Review und Export Safety; [Portfolio Case Study](portfolio_case_study.md), Abschnitte 5, 7 und 8.

### 13. Sichtbaren Abschluss liefern statt weiterer Planungsdokumente

- README enthält nur einen Screenshot-Platzhalter; die Case Study hat zehn Screenshot-TODOs. Nach den Korrekturen vier bis sechs aussagekräftige Screenshots einfügen: Übersicht, Issues/Review, KI-Freigabe und korrekter Export reichen für einen schlüssigen Anfang.
- `current_context.md` und `project_status.md` nennen alte historische Baselines statt einer klaren aktuellen Abschlussreferenz. Den tatsächlichen Abschlussstand, Testdatum und verbleibende Grenzen eintragen; „Language Switch Planning“ für diesen Termin aus dem unmittelbaren nächsten Schritt nehmen.
- `testing_strategy.md` beschreibt noch den früheren Zustand, in dem der Import von `app.py` die komplette UI ausführen würde. Inzwischen gibt es den `run_app`-Einstieg. Historische Pläne erkennbar als historisch kennzeichnen und auf die aktuelle Teststrategie verweisen.
- Demo-Anleitung und einige aktuelle Anforderungs-/Testdokumente tragen weiterhin den alten Produktnamen. Die aktuelle Außenpräsentation angleichen; alte Changelog-Einträge nicht rückwirkend umschreiben.
- Die finalen Checklisten mit tatsächlichem Datum, Ergebnis und bekannten Restpunkten abschließen. Vorhandene „Done“-Einträge für das Erstellen einer QA-Checkliste sind nicht automatisch eine Abnahme aller darin beschriebenen Abläufe.
- Ein finaler Versionsstand bzw. Tag ist sinnvoll; aktuell werden keine Remote-Tags gemeldet. Commit, Push oder Release erst im dafür beauftragten Abschlussblock ausführen.

Die geprüften relativen Markdown-Dateilinks in README und vorhandenen Dokumenten waren nicht gebrochen.

## Empfohlene Reihenfolge bis morgen

| Block | Inhalt | Richtwert für konzentrierte Arbeit |
| --- | --- | --- |
| A | Datensatzbindung, neue Freigaben, SKU-Zuordnung und Statusregeln – Punkte 1, 2, 4, 8 | 2–3 Stunden |
| B | Import mit Kennungserhalt und sichere Exportausgabe – Punkte 3, 5 | 2–3 Stunden |
| C | KI-Quellabgleich, vollständiger Kontext und passende Demo – Punkte 6, 7 | 2–3 Stunden |
| D | Regressionstests, dokumentierter Browser-/Excel-Durchlauf und Setup-Nachweis | 1,5–2,5 Stunden |
| E | Git-Hygiene, öffentliche Aussagen, Statusdokumente und Screenshots | 1–2 Stunden |

Das sind grobe Planungswerte, keine Lieferzusage; Fehlerbehebung und Nachprüfung können länger dauern. Insgesamt ist eher mit 9–14 konzentrierten Stunden als mit einem kurzen kosmetischen Abschluss zu rechnen. Tests sollten jeweils zusammen mit den Korrekturen entstehen. Der Stand sollte nur dann als abgeschlossen bezeichnet werden, wenn die Abnahmekriterien erfüllt sind; andernfalls einen klar begrenzten Release Candidate mit offenen Punkten benennen.

## Was für morgen warten kann

- Sprachumschaltung Deutsch/Englisch und umfassende Neugestaltung.
- Vollständige Zerlegung der 2.190 Zeilen von `app.py`.
- Datenbank, Benutzerkonten, Hosting, SaaS und externe Shop-Anbindungen.
- Massen-KI, automatisches Zurückschreiben und automatische Freigaben.
- Repository-Umbenennung aus reinen Branding-Gründen.
- Umfangreiche weitere Architektur- und Planungsdokumente.
- Zusätzliche Workbook-Gestaltung über Lesbarkeit und korrekte Ausgabe hinaus.

## Abschließende Abnahmeliste

- [ ] P1-Befunde 1–8 korrigiert und mit den beschriebenen Fällen geprüft.
- [ ] Bestehende und neue Regressionstests bestehen.
- [ ] Beide Excel-Ausgaben öffnen korrekt; Formelinhalte bleiben Text; Quellen und SKUs passen zusammen.
- [ ] Dateiwechsel und erneute KI-Generierung übertragen keine alten Freigaben.
- [ ] README beschreibt den realen Funktionsumfang, Datenfluss und die tatsächlichen Grenzen.
- [ ] Öffentlicher Projektlink bzw. beabsichtigter Empfängerzugriff funktioniert.
- [ ] Commit-Kontaktdaten und Lizenz-/Sichtbarkeitsabsicht sind bewusst entschieden.
- [ ] Screenshots und datierte QA-Ergebnisse sind vorhanden.
- [ ] Angekündigte weitere Veröffentlichungen nach Erhalt der Links geprüft.
- [ ] Finaler Stand geprüft, dann nur auf ausdrücklichen Auftrag committet/gepusht.
