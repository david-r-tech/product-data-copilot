"""Conservative checks for conflicting explicitly named product attributes."""

import re

from product_data_copilot.rules.validators import normalize_text


ATTRIBUTE_NAMES = {
    "material": {"material", "materials", "materialien", "stoff"},
    "color": {"color", "colour", "farbe"},
    "surface": {"surface", "finish", "oberflaeche", "oberfläche"},
}
EMPTY_VALUES = {"none", "n/a", "na", "unknown", "unbekannt", "-"}


def _normalized(value):
    return " ".join(normalize_text(value).casefold().split())


def _name_key(value):
    return _normalized(value).replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")


def _same_value(left, right):
    left, right = _normalized(left), _normalized(right)
    return left == right or bool(
        re.search(r"(?<!\w)" + re.escape(left) + r"(?!\w)", right)
        or re.search(r"(?<!\w)" + re.escape(right) + r"(?!\w)", left)
    )


def explicit_attribute_conflicts(row):
    """Find different explicit values, not inferred contradictions in prose."""
    values = {kind: [] for kind in ATTRIBUTE_NAMES}
    aliases = {
        _name_key(alias): kind
        for kind, names in ATTRIBUTE_NAMES.items()
        for alias in names
    }
    for column in row.index:
        kind = aliases.get(_name_key(column))
        value = normalize_text(row.get(column))
        if kind and value and _normalized(value) not in EMPTY_VALUES:
            values[kind].append((str(column), value))

    for item in re.split(r"[;\n|]", normalize_text(row.get("attributes", ""))):
        if ":" not in item:
            continue
        name, value = item.split(":", 1)
        kind = aliases.get(_name_key(name))
        value = value.strip()
        if kind and value and _normalized(value) not in EMPTY_VALUES:
            values[kind].append(("attributes", value))

    conflicts = []
    for kind, entries in values.items():
        for index, first in enumerate(entries):
            second = next((other for other in entries[index + 1:] if not _same_value(first[1], other[1])), None)
            if second:
                conflicts.append((kind, first, second))
                break
    return conflicts
