"""Small Streamlit workspace for product copy and translation."""

import json

import pandas as pd

from product_data_copilot.ai.content_generation import (
    LANGUAGES, approved_content_export_frames, build_content_prompt, clean_text,
    normalize_content_response, parse_bullet_cell, product_facts, source_identifier,
)

MAX_REQUESTS_PER_CLICK = 100
LANGUAGE_LABELS = {"en": "Englisch", "fr": "Französisch", "es": "Spanisch"}


def _select_review_article(st, sku):
    st.session_state["content_preview_sku"] = sku


def render_content_workspace(st, products, provider, workbook_writer, has_key):
    st.subheader("Texte erstellen & übersetzen")
    st.caption("Aus deiner hochgeladenen Tabelle werden prüfbare Textentwürfe erstellt. Die Originaldatei bleibt unverändert.")
    st.info("KI-Entwurf → Quelldaten prüfen → Mensch gibt frei → nur Freigegebenes wird exportiert.")

    task_label = st.radio(
        "1. Was möchtest du tun?",
        ["Produkttexte erstellen", "Vorhandene Texte übersetzen"],
        horizontal=True,
        key="content_task",
    )
    mode = "create" if task_label == "Produkttexte erstellen" else "translate"
    if mode == "create":
        st.info(
            "So entsteht der Text: Die KI liest pro Artikel die ausgefüllten Angaben deiner Tabelle "
            "(z. B. Name, Beschreibung, Material, Farbe und weitere Merkmale). Daraus schreibt sie zuerst "
            "einen deutschen HTML-Text und bis zu fünf deutsche Bullet Points. Danach übersetzt sie "
            "den vollständigen Text und die Bullet Points in die gewählte Sprache."
        )
    else:
        st.info("Vorhandene Texte aus einer gewählten Spalte werden übersetzt. Es wird kein neuer deutscher Produkttext geschrieben.")
    scope = st.radio("2. Für welche Artikel?", ["Gesamte Liste", "Einzelner Artikel"],
                     horizontal=True, key="content_scope")
    selected_skus = [source_identifier(sku) for sku in products["sku"]]
    if scope == "Einzelner Artikel":
        labels = {
            f"{source_identifier(row.get('sku'))} · {clean_text(row.get('product_name'))}": source_identifier(row.get("sku"))
            for _, row in products.iterrows()
        }
        chosen = st.selectbox("Artikel auswählen", list(labels), key="content_product")
        selected_skus = [labels[chosen]]
    language = st.selectbox("3. Zielsprache", list(LANGUAGES), format_func=lambda code: LANGUAGE_LABELS[code],
                            key="content_language")

    source_column = "description"
    bullet_column = None
    if mode == "translate":
        text_columns = [column for column in products.columns if column not in {"sku", "ean", "price", "image_url"}]
        source_column = st.selectbox("Spalte mit deutschem Quelltext", text_columns,
                                     index=text_columns.index("description") if "description" in text_columns else 0,
                                     key="content_source_column")
        bullet_options = ["Keine Bullet-Points-Spalte"] + [col for col in text_columns if col != source_column]
        selected_bullet_column = st.selectbox("Bullet-Points-Spalte (optional)", bullet_options,
                                              key="content_bullet_column")
        bullet_column = None if selected_bullet_column == bullet_options[0] else selected_bullet_column
        st.caption("Vorhandener Text und vorhandene Bullet Points werden übersetzt. Fehlende Angaben werden nicht ergänzt.")

    st.markdown("#### Welche Daten werden an OpenAI gesendet?")
    by_sku = {source_identifier(row.get("sku")): row for _, row in products.iterrows()}
    if mode == "create":
        st.caption(
            "Pro Artikel werden die SKU zur Zuordnung und die ausgefüllten Produktfelder als Faktenquelle gesendet. "
            "EAN, Preis und Bild-URL sind ausgeschlossen; zusätzliche ausgefüllte Lieferantenspalten können enthalten sein. "
            "Die Übermittlung beginnt erst, wenn du den Erstellen-Button anklickst."
        )
        if scope == "Einzelner Artikel":
            selected_sku = selected_skus[0]
            sent_values = {"sku": selected_sku, **product_facts(by_sku[selected_sku])}
            st.dataframe(
                pd.DataFrame([{"Feld": name, "Gesendeter Wert": value} for name, value in sent_values.items()]),
                hide_index=True, width="stretch", height=220,
            )
        else:
            used_columns = sorted({
                name
                for sku in selected_skus
                for name in product_facts(by_sku[sku])
            })
            st.caption(
                "Die Auswahlregel wird für jeden Artikel einzeln angewendet. Potenziell verwendete ausgefüllte "
                f"Spalten in dieser Liste: {', '.join(used_columns) if used_columns else 'keine'}."
            )
    else:
        bullet_detail = (
            f" sowie der Inhalt der Bullet-Point-Spalte „{bullet_column}“"
            if bullet_column else ""
        )
        st.caption(
            f"Pro Artikel werden nur die SKU zur Zuordnung, der Inhalt der gewählten Textspalte "
            f"„{source_column}“{bullet_detail} gesendet. Die Übermittlung beginnt erst, wenn du den "
            "Übersetzen-Button anklickst."
        )

    job_key = json.dumps([mode, language, source_column if mode == "translate" else "",
                          bullet_column if mode == "translate" else ""], ensure_ascii=False)
    jobs = st.session_state.get("content_jobs", {})
    results = jobs.get(job_key, {})
    pending = [sku for sku in selected_skus if sku not in results or results[sku].get("status") == "Fehler"]
    st.markdown("#### 4. Starten")
    st.caption(f"{len(selected_skus)} Artikel gewählt · {len(selected_skus) - len(pending)} bereits verarbeitet · "
               f"{len(pending)} offen. Für jeden offenen Artikel fällt eine kostenpflichtige KI-Anfrage an.")
    if not has_key:
        st.info("Für die Texterstellung ist ein eigener OpenAI-API-Schlüssel in der lokalen .env-Datei nötig.")
    elif pending:
        request_count = min(len(pending), MAX_REQUESTS_PER_CLICK)
        label = (f"Jetzt Texte für {request_count} Artikel erstellen und übersetzen"
                 if mode == "create" else f"Jetzt {request_count} Artikel übersetzen")
        if st.button(label, type="primary", width="stretch", key="content_generate"):
            work = pending[:MAX_REQUESTS_PER_CLICK]
            bar = st.progress(0, text="Texte werden erstellt …")
            for index, sku in enumerate(work, start=1):
                product = by_sku[sku]
                if mode == "translate" and not clean_text(product.get(source_column)):
                    results[sku] = {"sku": sku, "status": "Quelltext fehlt", "review_note": "In der gewählten Spalte steht kein Text."}
                else:
                    try:
                        prompt = build_content_prompt(product, mode, language, source_column, bullet_column)
                        raw = provider(prompt)
                        bullet_count = len(parse_bullet_cell(product.get(bullet_column))) if bullet_column else 0
                        results[sku] = normalize_content_response(raw, sku, mode, bullet_count)
                    except Exception as error:
                        # Provider details can include private information; only the class is shown.
                        results[sku] = {"sku": sku, "status": "Fehler",
                                        "review_note": f"Erstellung fehlgeschlagen ({type(error).__name__}). Erneut versuchen."}
                jobs[job_key] = results
                st.session_state["content_jobs"] = jobs
                bar.progress(index / len(work), text=f"{index} von {len(work)} Artikeln verarbeitet")
            st.rerun()
    else:
        st.success("Alle gewählten Artikel sind verarbeitet. Die Entwürfe stehen unten zum Prüfen bereit.")

    if len(pending) > MAX_REQUESTS_PER_CLICK:
        st.caption("Bei großen Dateien verarbeitet ein Start bis zu 100 Artikel. Der nächste Klick setzt ohne erneute Anfragen für fertige Artikel fort.")

    if not results:
        st.info("Noch kein Ergebnis. Wähle Aufgabe, Artikel und Zielsprache und starte dann die Verarbeitung.")
        return

    st.markdown("#### 5. Artikel prüfen und freigeben")
    st.caption("Wähle einen erzeugten Artikel und vergleiche alle Aussagen mit den Quelldaten. Jede Freigabe gilt nur für diesen Text und diese Zielsprache in der aktuellen Sitzung.")
    status_rows = []
    for _, row in products.iterrows():
        sku = source_identifier(row.get("sku"))
        if sku not in selected_skus:
            continue
        result = results.get(sku, {})
        review_status = result.get("review_status")
        status = {"approved": "Freigegeben", "rejected": "Abgelehnt"}.get(review_status)
        if status is None:
            status = "Zur Prüfung" if result.get("translated_html") else result.get("status", "Noch nicht erstellt")
        status_rows.append({"SKU": sku, "Produkt": clean_text(row.get("product_name")),
                            "Status": status, "Prüfhinweis": result.get("review_note", "")})
    st.dataframe(pd.DataFrame(status_rows), hide_index=True, width="stretch",
                 height=min(320, 35 * (len(status_rows) + 1) + 3))

    ready_skus = [sku for sku in selected_skus if results.get(sku, {}).get("translated_html")]
    if ready_skus:
        product_by_sku = {source_identifier(row.get("sku")): row for _, row in products.iterrows()}
        if st.session_state.get("content_preview_sku") not in ready_skus:
            st.session_state["content_preview_sku"] = ready_skus[0]
        preview_sku = st.selectbox(
            "Artikel zur Prüfung auswählen", ready_skus,
            format_func=lambda sku: f"{sku} · {clean_text(product_by_sku[sku].get('product_name'))}",
            key="content_preview_sku",
        )
        draft = results[preview_sku]
        review_status = draft.get("review_status")
        if review_status == "approved":
            st.success("Dieser Text ist freigegeben und kann exportiert werden.")
        elif review_status == "rejected":
            st.warning("Dieser Text wurde abgelehnt und wird nicht exportiert.")
        else:
            st.info("Prüfung offen: Dieser Text wird noch nicht exportiert.")
        with st.expander("Quelldaten zum Abgleich", expanded=True):
            facts = product_facts(product_by_sku[preview_sku])
            st.dataframe(
                pd.DataFrame([{"Spalte": name, "Inhalt": value} for name, value in facts.items()]),
                hide_index=True, width="stretch", height=220,
            )
        st.markdown("**Textentwurf und Übersetzung**")
        if mode == "create":
            st.markdown("**Deutsch**")
            st.markdown(draft["de_html"], unsafe_allow_html=True)
            for bullet in draft["de_bullets"]:
                st.markdown(f"- {bullet}")
        st.markdown(f"**{LANGUAGE_LABELS[language]}**")
        st.markdown(draft["translated_html"], unsafe_allow_html=True)
        for bullet in draft["translated_bullets"]:
            st.markdown(f"- {bullet}")
        with st.expander("HTML-Code ansehen"):
            if mode == "create":
                st.code(draft["de_html"], language="html")
            st.code(draft["translated_html"], language="html")

        if draft.get("review_note"):
            st.warning(f"Prüfhinweis: {draft['review_note']}")
        st.caption("Prüfe besonders Material, Farbe, Maße, Produktart und werbliche Versprechen. Die KI kann glaubwürdig klingende, aber unbelegte Aussagen erzeugen.")
        approve, reject = st.columns(2)
        if approve.button("Freigeben", type="primary", width="stretch", key="content_approve",
                          disabled=review_status == "approved"):
            draft["review_status"] = "approved"
            st.session_state["content_jobs"] = jobs
            st.rerun()
        if reject.button("Ablehnen", width="stretch", key="content_reject",
                         disabled=review_status == "rejected"):
            draft["review_status"] = "rejected"
            st.session_state["content_jobs"] = jobs
            st.rerun()

        current_index = ready_skus.index(preview_sku)
        previous, position, following = st.columns([1, 1, 1])
        previous.button(
            "← Vorheriger Artikel", width="stretch", key="content_previous_article",
            disabled=current_index == 0, on_click=_select_review_article,
            args=(st, ready_skus[max(0, current_index - 1)]),
        )
        position.markdown(f"**Artikel {current_index + 1} von {len(ready_skus)}**")
        following.button(
            "Nächster Artikel →", width="stretch", key="content_next_article",
            disabled=current_index == len(ready_skus) - 1, on_click=_select_review_article,
            args=(st, ready_skus[min(len(ready_skus) - 1, current_index + 1)]),
        )

    approved_count = sum(result.get("review_status") == "approved" for result in results.values())
    st.markdown("#### 6. Freigegebene Texte exportieren")
    st.caption(f"{approved_count} freigegeben · Im Excel stehen nur freigegebene Texte und die zugehörigen Quelldaten. Offene und abgelehnte Entwürfe bleiben draußen.")
    if approved_count == 0:
        st.info("Gib mindestens einen Artikel nach der Prüfung frei, um den Excel-Download zu aktivieren.")
        return
    try:
        frames = approved_content_export_frames(products, results, mode, language, source_column, bullet_column)
        download = workbook_writer(frames)
    except ValueError as error:
        st.error(str(error))
    else:
        st.download_button(
            "Freigegebene Texte als Excel herunterladen", download,
            f"product_data_copilot_freigegeben_{language}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary", width="stretch",
        )
        st.caption("Freigaben gelten nur in dieser Sitzung. Die hochgeladene Datei wird nicht verändert.")
