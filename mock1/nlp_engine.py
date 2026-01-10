def parse_prompt(text):
    """
    Analyzes natural language text to extract fashion context.
    Returns a dictionary with 'occasion' and/or 'temperature' if found.
    """
    if not text:
        return {}
    
    text = text.lower()
    result = {}

    # Occasion Keywords
    occasions = {
        "Formal": ["interview", "meeting", "office", "work", "business", "presentation"],
        "Party": ["party", "club", "date", "dinner", "night", "dance", "birthday"],
        "Casual": ["park", "walk", "friends", "chill", "home", "movie", "coffee", "shop"],
        "Office": ["office", "corporate"]
    }

    for occasion, keywords in occasions.items():
        if any(word in text for word in keywords):
            result["occasion"] = occasion
            break
            
    # Temperature/Weather Keywords
    # Mapping to approximate temperatures for the engine
    weather_keywords = {
        "10°C": ["cold", "chilly", "winter", "snow", "freezing", "coat", "jacket", "ice"],
        "30°C": ["hot", "sunny", "summer", "beach", "warm", "heat", "shorts"],
        "20°C": ["cool", "breeze", "spring", "autumn", "fall", "mild"]
    }

    for temp, keywords in weather_keywords.items():
        if any(word in text for word in keywords):
            result["temperature"] = temp
            break
            
    return result
