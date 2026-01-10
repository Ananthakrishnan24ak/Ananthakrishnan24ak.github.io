"""Color matching utilities.

This module provides a richer set of color combinations (hand-curated) used
by the outfit generator. It normalizes color names and treats "any" as a
wildcard. Matching is symmetric where appropriate.
"""

from typing import List


# Hand-curated color pairing suggestions. Keys are normalized color names.
# Values are lists of colors that generally look good when paired with the key.
COLOR_MATCHES = {
    "black": ["white", "grey", "beige", "blue", "red", "olive"],
    "white": ["black", "blue", "navy", "beige", "olive", "denim"],
    "grey": ["white", "black", "pink", "navy", "denim"],
    "blue": ["white", "black", "beige", "grey", "denim", "khaki"],
    "navy": ["white", "beige", "brown", "grey", "denim"],
    "denim": ["white", "black", "grey", "beige", "navy"],
    "beige": ["navy", "white", "brown", "olive", "denim"],
    "brown": ["beige", "navy", "olive", "white"],
    "olive": ["white", "beige", "brown", "navy"],
    "khaki": ["white", "navy", "brown", "denim"],
    "green": ["white", "navy", "beige", "brown"],
    "red": ["black", "white", "denim", "beige"],
    "pink": ["grey", "white", "navy"],
    "purple": ["black", "white", "grey"],
    "mustard": ["navy", "denim", "brown", "beige"],
    "yellow": ["navy", "denim", "white"],
    "orange": ["denim", "white", "navy"],
    "any": ["any"]
}


SYNONYMS = {
    "denim": ["jeans", "blue denim"],
    "navy": ["navy blue"],
    "khaki": ["tan"],
    "beige": ["tan", "camel"],
    "grey": ["gray"],
    "mustard": ["golden"],
}


def normalize(color: str) -> str:
    if not color:
        return ""
    c = color.strip().lower()
    # remove common punctuation
    for ch in ["#", " "]:
        c = c.replace(ch, " ")
    c = c.replace("  ", " ").strip()

    # map synonyms
    for key, syns in SYNONYMS.items():
        if c == key:
            return key
        for s in syns:
            if c == s:
                return key

    # if the color string contains a known word, map it
    for key, syns in SYNONYMS.items():
        for s in syns:
            if s in c:
                return key

    # fallback: if the word matches a key or value directly
    c_word = c.split()[0]
    if c_word in COLOR_MATCHES:
        return c_word

    return c


def get_color_matches(color: str) -> List[str]:
    """Return a list of colors that pair well with `color`.

    The returned list is normalized (lowercase) and always includes 'any'
    as a fallback option.
    """
    c = normalize(color)
    if not c:
        return list(COLOR_MATCHES.keys())
    # direct mapping
    if c in COLOR_MATCHES:
        return COLOR_MATCHES[c]

    # try reverse lookup: colors that list c as a match
    matches = [k for k, vals in COLOR_MATCHES.items() if c in vals]
    if matches:
        return matches

    # fallback to very permissive set
    return ["any"]


def is_color_match(color1: str, color2: str) -> bool:
    """Return True if color1 pairs well with color2 based on rules.

    Treats 'any' as wildcard. Normalizes inputs and checks both directions
    so mapping doesn't need to be exhaustive.
    """
    c1 = normalize(color1)
    c2 = normalize(color2)
    if not c1 or not c2:
        return False
    if c1 == "any" or c2 == "any":
        return True
    if c1 == c2:
        return True

    # check direct mapping
    if c2 in COLOR_MATCHES.get(c1, []):
        return True

    # check reverse mapping
    if c1 in COLOR_MATCHES.get(c2, []):
        return True

    # check synonym-based suggestions
    return c2 in get_color_matches(c1)

