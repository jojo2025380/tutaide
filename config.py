# ---------------- APPLICATION SETTINGS ----------------

APP_TITLE = "📚 ECE AI Assistant"

APP_DESCRIPTION = (
    "Generate structured early childhood lesson plans instantly."
)


# ---------------- AGE GROUPS ----------------

AGE_GROUPS = [
    "3 Years",
    "4 Years",
    "5 Years",
    "6 Years"
]


# ---------------- LESSON DURATIONS ----------------

LESSON_DURATIONS = [
    "15 Minutes",
    "30 Minutes",
    "45 Minutes"
]

# ---------------- SUBSCRIPTION PLANS ----------------

PLANS = {

    "basic": {
        "name": "Basic",
        "price": 599,
        "lesson_limit": 5,
        "story_limit": 2,
        "image_limit": 2,
        "picture_card_limit": 2,
    },

    "creative": {
        "name": "Creative",
        "price": 899,
        "lesson_limit": 30,
        "story_limit": 10,
        "image_limit": 20,
        "picture_card_limit": 6,
    },

    "pro": {
        "name": "Pro",
        "price": 4999,
        "lesson_limit": 200,
        "story_limit": 60,
        "image_limit": 150,
        "picture_card_limit": 50,
    }

}
