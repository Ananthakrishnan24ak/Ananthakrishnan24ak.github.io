from color_rules import is_color_match


def generate_outfits(wardrobe, occasion, temperature):
    """Generate outfit combinations (top + bottom + shoe) from wardrobe.

    Simple rule-based scoring:
    - top/bottom color match: +50
    - shoe matches bottom or top color: +30
    - exact formality match for all pieces: +20
    - "All" formality counts as acceptable but gives less score (+5)

    Returns a list of outfits sorted by score (desc).
    """
    outfits = []

    tops = [w for w in wardrobe if w.get("category") == "Top"]
    bottoms = [w for w in wardrobe if w.get("category") == "Bottom"]
    shoes = [w for w in wardrobe if w.get("category") in ("Shoe", "Shoes")]

    for top in tops:
        for bottom in bottoms:
            for shoe in (shoes or [None]):
                # formality checks
                def formality_score(item):
                    if not item:
                        return 0
                    if item.get("formality") == occasion:
                        return 20
                    if item.get("formality") == "All":
                        return 5
                    return 0

                score = 0
                # color matches
                if is_color_match(top.get("color"), bottom.get("color")):
                    score += 50

                shoe_score = 0
                if shoe:
                    if is_color_match(shoe.get("color"), bottom.get("color")):
                        shoe_score += 30
                    elif is_color_match(shoe.get("color"), top.get("color")):
                        shoe_score += 15
                score += shoe_score

                # formality scoring
                score += formality_score(top)
                score += formality_score(bottom)
                if shoe:
                    score += formality_score(shoe)

                # small heuristic: prefer matching season with temperature
                # assume temperature like '20°C' -> numeric
                try:
                    temp_val = int(str(temperature).replace('°C', '').strip())
                except Exception:
                    temp_val = None

                season_bonus = 0
                if temp_val is not None:
                    # winter < 15, summer > 25
                    if temp_val < 15 and (top.get('season') == 'Winter' or bottom.get('season') == 'Winter'):
                        season_bonus = 5
                    if temp_val > 25 and (top.get('season') == 'Summer' or bottom.get('season') == 'Summer'):
                        season_bonus = 5
                score += season_bonus

                # only include sensible combinations (require at least one color match)
                if score > 0:
                    outfits.append({
                        "top": top,
                        "bottom": bottom,
                        "shoe": shoe,
                        "score": score
                    })

    # sort by score desc and return top results
    outfits.sort(key=lambda o: o['score'], reverse=True)
    return outfits
