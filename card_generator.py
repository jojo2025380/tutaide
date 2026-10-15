import base64
import io

from PIL import Image, ImageChops, ImageDraw, ImageFont

from ai_client import client



def _process_card_sheet(image_b64, labels):

    import io

    from PIL import Image, ImageChops

    image_bytes = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    width, height = image.size
    half_width = width // 2
    half_height = height // 2

    boxes = [
        (0, 0, half_width, half_height),
        (half_width, 0, width, half_height),
        (0, half_height, half_width, height),
        (half_width, half_height, width, height),
    ]

    cards = []
    target_scale = 0.78

    for box in boxes:
        cropped = image.crop(box)
        card_width, card_height = cropped.size

        gray = cropped.convert("L")
        threshold = gray.point(lambda p: 255 if p > 235 else 0)
        background = Image.new("L", threshold.size, 255)
        diff = ImageChops.difference(threshold, background)
        content_bbox = diff.getbbox()

        content = cropped.crop(content_bbox) if content_bbox else cropped
        content_width, content_height = content.size

        max_width = int(card_width * target_scale)
        max_height = int(card_height * target_scale)

        resize_ratio = min(
            max_width / content_width,
            max_height / content_height
        )

        new_width = max(1, int(content_width * resize_ratio))
        new_height = max(1, int(content_height * resize_ratio))

        resized = content.resize(
            (new_width, new_height),
            Image.LANCZOS
        )

        canvas = Image.new("RGB", (card_width, card_height), "white")

        paste_x = (card_width - new_width) // 2
        paste_y = (card_height - new_height) // 2

        canvas.paste(resized, (paste_x, paste_y))
        cards.append(canvas)

    sheet = Image.new(
        "RGB",
        (half_width * 2, half_height * 2),
        "white"
    )

    positions = [
        (0, 0),
        (half_width, 0),
        (0, half_height),
        (half_width, half_height),
    ]

    for card_img, pos in zip(cards, positions):
        sheet.paste(card_img, pos)

    buffer = io.BytesIO()
    sheet.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")




def generate_number_cards(style="colour"):
    """Create four number cards with exactly matching quantities of objects."""

    import io
    import base64
    from PIL import Image, ImageDraw, ImageFont

    card_size = 512
    sheet = Image.new("RGB", (card_size * 2, card_size * 2), "white")
    draw = ImageDraw.Draw(sheet)

    try:
        number_font = ImageFont.truetype("arial.ttf", 110)
    except OSError:
        number_font = ImageFont.load_default()

    positions = [
        (0, 0),
        (card_size, 0),
        (0, card_size),
        (card_size, card_size),
    ]

    colours = ["red", "blue", "gold", "green"]
    is_colour = style == "colour"

    for number, (left, top) in enumerate(positions, start=1):
        right = left + card_size
        bottom = top + card_size

        draw.rectangle(
            (left + 8, top + 8, right - 8, bottom - 8),
            outline="black",
            width=3,
        )

        number_text = str(number)
        bbox = draw.textbbox((0, 0), number_text, font=number_font)
        number_width = bbox[2] - bbox[0]

        draw.text(
            (left + (card_size - number_width) // 2, top + 35),
            number_text,
            fill="black",
            font=number_font,
        )

        for index in range(number):
            col = index % 2
            row = index // 2

            x = left + 170 + col * 170
            y = top + 275 + row * 95
            radius = 28

            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                outline="black",
                fill=colours[number - 1] if is_colour else "white",
                width=4,
            )

    buffer = io.BytesIO()
    sheet.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")



def generate_picture_cards(topic, card_items, outcomes):
    
    if "number" in topic.lower():
        return generate_number_cards(style="black_and_white")

    cards_text = "\n".join(
        f"- {item}"
        for item in card_items
    )

    prompt = f"""
Create one printable educational picture-card sheet for young children.

TOPIC:
{topic}

LEARNING OUTCOMES:
{chr(10).join(f"- {outcome}" for outcome in outcomes)}

CARDS TO INCLUDE:
{cards_text}

STRICT CONTENT REQUIREMENT:

- Create exactly 4 cards, one for each item listed in CARDS TO INCLUDE, in order.
- Each card MUST show the exact requested item as its main subject.
- Never replace a requested item with a person, child, face, animal or unrelated object unless the item itself is a person.
- For plant-part cards, show the requested plant part clearly and separately.
- If the requested item is "root", show visible roots underground attached to the plant.
- If the requested item is "stem", show a clear upright plant stem or stalk as the main subject, visibly connecting the roots to the leaves. The stem must be a distinct elongated structure, not a leaf.
- If the requested item is "leaf", show a recognisable leaf with a clear leaf shape and visible leaf veins. Do not use a stem as the main subject.
- If the requested item is "flower", show a recognisable flower as the main subject.
- The requested object must be large, clear and immediately recognisable.
- One main concept per card.
- Do not add extra cards, watermarks, logos or speech bubbles.

TEXT:
Do NOT generate ANY words, labels, captions or letters inside the image. The image must contain illustrations only, no text of any kind.

STYLE:
The final result must be a printable black-and-white colouring-page resource
for young children aged 3-6.

It should be:
- black and white only, clean line drawings, simple bold outlines
- clear shapes that are easy for young children to colour
- large open areas for colouring
- simple and uncluttered, educational, child-friendly

LAYOUT:
- Arrange the 4 cards in a clean 2 x 2 grid.
- Each card's illustration must fit entirely inside its own quadrant, with generous empty margin on every side.
- When a card shows a person, the ENTIRE head, face and at least the shoulders must be fully visible — never touching or crossing the quadrant boundary.
- Zoom illustrations out if needed so nothing is close to any edge.
- Keep all four cards clearly separated by empty white space.

Do NOT use color, shading, gradients, realistic textures, photorealism, or any text.

The artwork must be original.

Return only the image.
"""

    result = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        quality="medium"
    )

    raw_b64 = result.data[0].b64_json

    return _process_card_sheet(raw_b64, card_items)


def generate_picture_cards_colour(topic, card_items, outcomes):
    
    if "number" in topic.lower():
        return generate_number_cards(style="colour")

    cards_text = "\n".join(
        f"- {item}"
        for item in card_items
    )

    prompt = f"""
Create one printable educational picture-card sheet for young children.

TOPIC:
{topic}

LEARNING OUTCOMES:
{chr(10).join(f"- {outcome}" for outcome in outcomes)}

CARDS TO INCLUDE:
{cards_text}

STRICT CONTENT REQUIREMENT:
- Create exactly 4 cards, one for each item listed in CARDS TO INCLUDE, in order.
- Each card MUST show the exact requested item as its main subject.
- Never replace a requested item with a person, child, face, animal or unrelated object unless the item itself is a person.
- The requested object must be large, clear and immediately recognisable.
- One main concept per card.
- Do not add extra cards, watermarks, logos or speech bubbles.

TEXT:
Do NOT generate ANY words, labels, captions or letters inside the image. The image must contain illustrations only, no text of any kind.

STYLE:
The final result must be a full-colour, polished educational illustration
for young children aged 3-6, suitable for a teacher to print and use directly.

It should be:
- fully coloured, clean, smooth, polished 2D illustration
- natural balanced colors
- varied backgrounds per card (not the same background repeated)
- friendly and clear, professionally designed for printing

LAYOUT:
- Arrange the 4 cards in a clean 2 x 2 grid.
- Each card's illustration must fit entirely inside its own quadrant, with generous empty margin on every side.
- When a card shows a person, the ENTIRE head, face and at least the shoulders must be fully visible — never touching or crossing the quadrant boundary.
- Zoom illustrations out if needed so nothing is close to any edge.
- Keep all four cards clearly separated by empty space.

Do NOT use black-and-white-only outlines or any text.

The artwork must be original.

Return only the image.
"""

    result = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        quality="medium"
    )

    raw_b64 = result.data[0].b64_json

    return _process_card_sheet(raw_b64, card_items)


def get_picture_card_items(topic):

    topic_lower = topic.lower()

    card_sets = {

        "animals": [
            "dog",
            "cat",
            "cow",
            "bird"
        ],

        "weather": [
            "sunny weather",
            "rainy weather",
            "cloudy weather",
            "windy weather"
        ],

        "family": [
            "mother",
            "father",
            "sister",
            "brother"
        ],

        "shapes": [
            "circle",
            "square",
            "triangle",
            "star"
        ],

        "colours": [
            "red",
            "blue",
            "yellow",
            "green"
        ],

        "transport": [
            "car",
            "bus",
            "train",
            "airplane"
        ],

        "plants": [
            "root",
            "stem",
            "leaf",
            "flower"
        ],

                "food": [
            "apple",
            "banana",
            "bread",
            "carrot"
        ],

        "numbers": [
            "number 1",
            "number 2",
            "number 3",
            "number 4"
        ],

        "alphabet": [
            "letter A",
            "letter B",
            "letter C",
            "letter D"
        ],

        "body parts": [
            "eyes",
            "nose",
            "hands",
            "feet"
        ],

        "my home": [
            "bed",
            "door",
            "window",
            "table"
        ],

        "clothing": [
            "shirt",
            "trousers",
            "shoes",
            "hat"
        ],

        "community helpers": [
            "doctor",
            "teacher",
            "police officer",
            "firefighter"
        ],

        "health and hygiene": [
            "toothbrush",
            "soap",
            "towel",
            "comb"
        ],

        "my school": [
            "classroom",
            "desk",
            "book",
            "school bag"
        ],

        "water": [
            "rain",
            "tap",
            "cup",
            "river"
        ],

        "insects": [
            "butterfly",
            "bee",
            "ant",
            "ladybird"
        ],

        "feelings and emotions": [
            "happy face",
            "sad face",
            "angry face",
            "surprised face"
        ],

        "five senses": [
            "eye",
            "ear",
            "nose",
            "hand"
        ],

        "space and sky": [
            "sun",
            "moon",
            "star",
            "rocket"
        ],

        "art supplies": [
            "paintbrush",
            "crayon",
            "scissors",
            "glue stick"
        ],

        "musical instruments": [
            "drum",
            "guitar",
            "tambourine",
            "piano"
        ],

        "safety": [
            "traffic light",
            "stop sign",
            "zebra crossing",
            "fire extinguisher"
        ],

        "earth care": [
            "recycling bin",
            "tree",
            "water drop",
            "trash bin"
        ]

    }

    for key, cards in card_sets.items():

        if key in topic_lower:
            return cards

    return [
        topic,
        "one example",
        "another example",
        "a related object"
    ]