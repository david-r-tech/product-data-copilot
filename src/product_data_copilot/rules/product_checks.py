"""Pure orchestration for deterministic product-data checks."""

import pandas as pd

from product_data_copilot.data.product_input import validate_product_identity
from product_data_copilot.rules.attribute_consistency import explicit_attribute_conflicts
from product_data_copilot.rules.validators import (
    has_useful_attributes,
    is_blank,
    is_generic_product_name,
    is_safety_relevant_category,
    is_suspicious_image_url,
    is_valid_ean,
    is_valid_price,
)


def _get_value(row, field_name):
    if field_name in row.index:
        return row[field_name]
    return ""


def add_issue(issues, sku, issue_type, field_name, severity, message, recommended_action):
    issues.append(
        {
            "sku": sku,
            "issue_type": issue_type,
            "field_name": field_name,
            "severity": severity,
            "message": message,
            "recommended_action": recommended_action,
        }
    )


def add_core_data_checks(issues, row, sku):
    product_name = _get_value(row, "product_name")
    description = _get_value(row, "description")
    brand = _get_value(row, "brand")
    ean = _get_value(row, "ean")
    category = _get_value(row, "category")
    manufacturer = _get_value(row, "manufacturer")

    if is_blank(product_name):
        add_issue(
            issues,
            sku,
            "Missing product_name",
            "product_name",
            "Critical",
            "Produktname fehlt.",
            "Eine eindeutige Produktbezeichnung ergänzen.",
        )
    elif len(str(product_name).strip()) < 10:
        add_issue(
            issues,
            sku,
            "Short product_name",
            "product_name",
            "Warning",
            "Der Produktname hat weniger als 10 Zeichen.",
            "Den Produktnamen aussagekräftiger formulieren.",
        )
    elif is_generic_product_name(product_name):
        add_issue(
            issues,
            sku,
            "Generic product_name",
            "product_name",
            "Warning",
            "Der Produktname ist für Marktplätze zu allgemein.",
            "Produkttyp, Marke oder ein wichtiges Merkmal im Titel ergänzen.",
        )

    if is_blank(description):
        add_issue(
            issues,
            sku,
            "Missing description",
            "description",
            "Critical",
            "Produktbeschreibung fehlt.",
            "Eine aussagekräftige Produktbeschreibung ergänzen.",
        )
    elif len(str(description).strip()) < 30:
        add_issue(
            issues,
            sku,
            "Short description",
            "description",
            "Warning",
            "Die Produktbeschreibung hat weniger als 30 Zeichen.",
            "Weitere relevante Produktdetails ergänzen.",
        )

    if is_blank(brand):
        add_issue(
            issues,
            sku,
            "Missing brand",
            "brand",
            "Warning",
            "Marke fehlt.",
            "Die Produktmarke ergänzen.",
        )

    if is_blank(ean):
        add_issue(
            issues,
            sku,
            "Missing ean",
            "ean",
            "Critical",
            "EAN fehlt.",
            "Eine gültige Produkt-EAN ergänzen.",
        )
    elif not is_valid_ean(ean):
        add_issue(
            issues,
            sku,
            "Invalid ean",
            "ean",
            "Critical",
            "Das EAN-Format ist ungültig.",
            "Eine gültige 8-, 12-, 13- oder 14-stellige EAN/GTIN ergänzen.",
        )

    if is_blank(category):
        add_issue(
            issues,
            sku,
            "Missing category",
            "category",
            "Critical",
            "Produktkategorie fehlt.",
            "Eine eindeutige Produktkategorie ergänzen.",
        )

    if is_blank(manufacturer):
        add_issue(
            issues,
            sku,
            "Missing manufacturer",
            "manufacturer",
            "Warning",
            "Hersteller fehlt.",
            "Den Hersteller ergänzen, sofern bekannt.",
        )


def add_marketplace_checks(issues, row, sku):
    price = _get_value(row, "price")
    attributes = _get_value(row, "attributes")

    if is_blank(price):
        add_issue(
            issues,
            sku,
            "Missing price",
            "price",
            "Warning",
            "Produktpreis fehlt.",
            "Vor der Marktplatzprüfung einen Produktpreis ergänzen.",
        )
    elif not is_valid_price(price):
        add_issue(
            issues,
            sku,
            "Invalid price",
            "price",
            "Warning",
            "Der Produktpreis muss größer als 0 sein.",
            "Den Produktpreis prüfen und korrigieren.",
        )

    if not has_useful_attributes(attributes):
        add_issue(
            issues,
            sku,
            "Missing attributes",
            "attributes",
            "Warning",
            "Produktmerkmale fehlen.",
            "Wichtige Merkmale wie Farbe, Größe, Material, Kapazität oder Maße ergänzen.",
        )


def add_content_quality_checks(issues, row, sku):
    product_name = _get_value(row, "product_name")

    if not is_blank(product_name) and is_generic_product_name(product_name):
        existing_name_issues = [
            issue
            for issue in issues
            if issue["sku"] == sku and issue["field_name"] == "product_name"
        ]

        if len(existing_name_issues) == 0:
            add_issue(
                issues,
                sku,
                "Generic product_name",
                "product_name",
                "Warning",
                "Der Produktname ist für Marktplätze zu allgemein.",
                "Produkttyp, Marke oder ein wichtiges Merkmal im Titel ergänzen.",
            )


def add_translation_checks(issues, row, sku):
    translation_de = _get_value(row, "translation_de")
    translation_en = _get_value(row, "translation_en")

    if is_blank(translation_de):
        add_issue(
            issues,
            sku,
            "Missing translation_de",
            "translation_de",
            "Warning",
            "Deutsche Übersetzung fehlt.",
            "Die deutsche Produktübersetzung ergänzen.",
        )

    if is_blank(translation_en):
        add_issue(
            issues,
            sku,
            "Missing translation_en",
            "translation_en",
            "Warning",
            "Englische Übersetzung fehlt.",
            "Die englische Produktübersetzung ergänzen.",
        )


def add_compliance_checks(issues, row, sku):
    category = _get_value(row, "category")
    warning_notes = _get_value(row, "warning_notes")

    if is_safety_relevant_category(category) and is_blank(warning_notes):
        add_issue(
            issues,
            sku,
            "Missing warning_notes",
            "warning_notes",
            "Warning",
            "Bei diesem sicherheitsrelevanten Produkt fehlen Warnhinweise.",
            "Sicherheits- oder Nutzungshinweise ergänzen und fachlich prüfen.",
        )


def add_media_checks(issues, row, sku):
    image_url = _get_value(row, "image_url")

    if is_blank(image_url):
        add_issue(
            issues,
            sku,
            "Missing image_url",
            "image_url",
            "Info",
            "Bild-URL fehlt.",
            "Eine Produktbild-URL ergänzen.",
        )
    elif is_suspicious_image_url(image_url):
        add_issue(
            issues,
            sku,
            "Image URL suspicious",
            "image_url",
            "Info",
            "Die Bild-URL wirkt unvollständig oder nicht öffentlich erreichbar.",
            "Eine vollständige, öffentlich erreichbare Bild-URL ergänzen.",
        )


def add_attribute_consistency_checks(issues, row, sku):
    labels = {"material": "Material", "color": "Farbe", "surface": "Oberfläche"}
    for kind, first, second in explicit_attribute_conflicts(row):
        label = labels[kind]
        add_issue(
            issues,
            sku,
            f"Different {kind} values",
            kind,
            "Warning",
            f"{label} unterschiedlich angegeben: {first[0]} = {first[1]}; {second[0]} = {second[1]}.",
            f"{label}-Angaben in den genannten Spalten mit der Produktquelle abgleichen.",
        )


def find_product_issues(products):
    validate_product_identity(products)
    issues = []

    for row_number, row in products.iterrows():
        sku = _get_value(row, "sku")

        if is_blank(sku):
            sku = f"Row {row_number + 1}"

        add_core_data_checks(issues, row, sku)
        add_marketplace_checks(issues, row, sku)
        add_content_quality_checks(issues, row, sku)
        add_translation_checks(issues, row, sku)
        add_compliance_checks(issues, row, sku)
        add_attribute_consistency_checks(issues, row, sku)
        add_media_checks(issues, row, sku)

    return pd.DataFrame(
        issues,
        columns=[
            "sku",
            "issue_type",
            "field_name",
            "severity",
            "message",
            "recommended_action",
        ],
    )


def prioritize_issues(issues):
    """Show critical work first while preserving order within each severity."""
    severity_order = {"Critical": 0, "Warning": 1, "Info": 2}
    return (
        issues.assign(_severity_order=issues["severity"].map(severity_order).fillna(3))
        .sort_values("_severity_order", kind="stable")
        .drop(columns="_severity_order")
        .reset_index(drop=True)
    )
