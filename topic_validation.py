from difflib import get_close_matches

# ---------------- CLEANING ----------------
def normalize_topic(topic):

    if topic is None:
        return ""

    topic = topic.strip()

    topic = " ".join(topic.split())

    return topic.lower()


# ---------------- TOPIC MAP ----------------
TOPIC_MAP = {
    "animals": "Animals",
    "shapes": "Shapes",
    "shape": "Shapes",
    "colours": "Colours",
    "colors": "Colours",
    "transport": "Transport",
    "transprt": "Transport",
    "plants": "Plants",
    "food": "Food",
    "weather": "Weather",
    "numbers": "Numbers",
    "counting": "Numbers",
    "count": "Numbers",
    "alphabet": "Alphabet",
    "letters": "Alphabet",
    "family": "Family",
    "people": "Family",
    "body parts": "Body Parts",
    "body": "Body Parts",
    "my home": "My Home",
    "home": "My Home",
    "clothing": "Clothing",
    "clothes": "Clothing",
    "community helpers": "Community Helpers",
    "helpers": "Community Helpers",
    "health": "Health and Hygiene",
    "hygiene": "Health and Hygiene",
    "health and hygiene": "Health and Hygiene",
    "my school": "My School",
    "school": "My School",
    "water": "Water",
    "insects": "Insects",
    "minibeasts": "Insects",
    "bugs": "Insects",
    "feelings": "Feelings and Emotions",
    "emotions": "Feelings and Emotions",
    "feelings and emotions": "Feelings and Emotions",
    "five senses": "Five Senses",
    "senses": "Five Senses",
    "space": "Space and Sky",
    "sky": "Space and Sky",
    "space and sky": "Space and Sky",
    "art supplies": "Art Supplies",
    "art": "Art Supplies",
    "musical instruments": "Musical Instruments",
    "instruments": "Musical Instruments",
    "music": "Musical Instruments",
    "safety": "Safety",
    "road safety": "Safety",
    "earth care": "Earth Care",
    "environment": "Earth Care",
    "recycling": "Earth Care"
}


# ---------------- SMART SUGGESTION ----------------
def suggest_topic(topic):
    t = normalize_topic(topic)
    keys = list(TOPIC_MAP.keys())

    match = get_close_matches(t, keys, n=1, cutoff=0.6)

    if match:
        return TOPIC_MAP[match[0]]

    return None


# ---------------- VALIDATION ----------------
def validate_topic(topic):

    t = normalize_topic(topic)

    if t == "":
        return False, None

    if len(t) > 50:
        return False, None

    if t in TOPIC_MAP:
        return True, TOPIC_MAP[t]

    suggestion = suggest_topic(t)

    if suggestion:
        return "suggest", suggestion

    return False, None
