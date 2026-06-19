"""Small, pure validation helpers for product data checks."""

GENERIC_PRODUCT_NAMES = {
    "bt",
    "headphones",
    "cable",
    "shirt",
    "product",
    "item",
    "unknown",
}

ATTRIBUTE_PLACEHOLDERS = {"none", "n/a", "unknown", "-"}

SAFETY_RELEVANT_CATEGORY_TERMS = {
    "electronics",
    "kitchen",
    "appliance",
    "baby",
    "sports",
    "fitness",
    "toy",
    "beauty",
}


def is_blank(value):
    """Return True when a value is missing or empty after trimming."""
    if value is None:
        return True

    try:
        if value != value:
            return True
    except TypeError:
        pass

    return str(value).strip() == ""


def normalize_text(value):
    """Return stripped text or an empty string for blank values."""
    if is_blank(value):
        return ""
    return str(value).strip()


def has_min_length(value, min_length):
    """Return True when a non-blank value has at least min_length characters."""
    return len(normalize_text(value)) >= min_length


def is_valid_ean(value):
    """Return True for 8, 12, 13, or 14 digit EAN/GTIN-like values."""
    if is_blank(value):
        return False

    if isinstance(value, float) and value.is_integer():
        value = int(value)

    ean = str(value).strip()
    return ean.isdigit() and len(ean) in [8, 12, 13, 14]


def is_valid_price(value):
    """Return True when value can be parsed as a number greater than 0."""
    if is_blank(value):
        return False

    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def is_suspicious_image_url(value):
    """Return True for non-blank image URLs that look incomplete or non-public."""
    if is_blank(value):
        return False

    image_url = str(value).strip().lower()
    return not image_url.startswith(("http://", "https://")) or "example.com" in image_url


def is_generic_product_name(value):
    """Return True when a product name is too short or overly generic."""
    if is_blank(value):
        return False

    product_name = str(value).strip()

    if len(product_name) < 10:
        return True

    return product_name.lower() in GENERIC_PRODUCT_NAMES


def has_useful_attributes(value):
    """Return True when attributes are not blank or placeholder text."""
    if is_blank(value):
        return False

    attributes = str(value).strip().lower()
    return attributes not in ATTRIBUTE_PLACEHOLDERS


def is_safety_relevant_category(category):
    """Return True for categories that should have warning notes reviewed."""
    if is_blank(category):
        return False

    category_text = str(category).lower()
    return any(term in category_text for term in SAFETY_RELEVANT_CATEGORY_TERMS)

