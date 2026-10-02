from ai_client import client


def generate_scene_image(
    visual_description,
    character_descriptions=None,
    characters_present=None
):

    character_descriptions = character_descriptions or {}
    characters_present = characters_present or []

    # Build character information only for characters appearing
    # in the current scene.
    character_details = []

    for character in characters_present:

        description = character_descriptions.get(
            character,
            "No detailed description available."
        )

        character_details.append(
            f"- {character}: {description}"
        )

    character_details_text = "\n".join(character_details)

    prompt = f"""
Create an original illustrated children's story scene.

SCENE DESCRIPTION:
{visual_description}

CHARACTERS PRESENT IN THIS SCENE:
{character_details_text}

IMPORTANT CHARACTER CONSISTENCY:
The character descriptions above are the established visual identities
for this story.

When a character appears in this scene:
- Follow their established appearance exactly.
- Keep their skin tone consistent.
- Keep their facial features consistent.
- Keep their age consistent.
- Keep their hair texture consistent.
- Keep their hairstyle and hair length consistent.
- Keep their general clothing consistent unless the scene description
  specifically requires a clothing change.
- Do not randomly redesign the characters.
- Do not change a character's ethnicity or appearance between scenes.
- Do not add unnecessary characters.
- Only show the characters listed as present in this scene.

VISUAL STYLE:

Create the image in a polished, high-quality 2D animated storybook
illustration style inspired by the smooth visual quality of
classic television animation.

The result should feel like a professionally produced children's
animated series rather than a generic AI cartoon.

The overall appearance should be:

- smooth and beautifully rendered
- polished traditional 2D animation aesthetic
- clean, refined character shapes
- natural human proportions
- natural-sized eyes proportional to the face
- realistic facial proportions while remaining friendly and expressive
- subtle, believable facial expressions
- smooth curved forms
- detailed characters with gentle dimensional shading
- soft highlights and realistic shadows
- rich, carefully painted backgrounds
- clear depth and perspective
- rich but naturally balanced colors
- moderate color saturation
- accurate and believable color relationships
- visually interesting environments
- warm and emotionally engaging when appropriate
- professional children's television animation quality

Do NOT make the image look like a generic preschool cartoon.

CHARACTERS:

- Children and adults should look like believable human characters,
  but illustrated rather than photorealistic.
- Use natural human body proportions.
- Do NOT give characters oversized heads.
- Do NOT give characters extremely large eyes.
- Eyes must remain natural-sized and proportional to the face.
- Facial features should be gentle, natural and believable.
- Characters should have distinctive facial features.
- Follow the established character descriptions exactly.
- Characters should look appealing without becoming exaggerated.

GLOBAL DIVERSITY:

- The application is designed for an international audience.
- Characters may represent different ethnic, cultural and geographic
  backgrounds.
- Include natural diversity in skin tones.
- Skin tones may range from very light to light, tan, medium brown,
  dark brown and deep brown.
- Do not automatically make all characters white.
- Do not automatically make all characters Black or African.
- Do not automatically make every story Kenyan.
- Diversity should feel natural rather than forced.
- Do not use stereotypes.
- Different characters should genuinely look like different people.

HAIR AND HAIRSTYLES:

Hair must reflect realistic diversity across ALL characters.

IMPORTANT:
Do NOT associate hair length, hair texture or hairstyle with
skin color or ethnicity.

- Do NOT associate long hair only with white or light-skinned characters.
- Do NOT associate short hair only with Black or African characters.
- Hair may be straight, wavy, curly, coily or tightly coiled.
- Include natural variation in hair length and hairstyles.

For Black and African characters, hairstyles may include:

- natural curls
- coils
- afros
- short natural hair
- fades
- tapered cuts
- braids
- cornrows
- twists
- locs
- puff hairstyles
- ponytails
- buns
- medium or longer natural hairstyles

Characters from other backgrounds should also have varied:

- hair textures
- hair lengths
- hairstyles

IMPORTANT:

- Girls do NOT all need long hair.
- Boys do NOT all need short hair.
- Do not give every character the same hairstyle.
- Do not use skin tone to determine hairstyle.
- Hair should be age-appropriate.
- School hairstyles should be practical and appropriate for the
  school environment.
- Give characters visibly different hairstyles so they feel
  like individual people.

CLOTHING:

- Clothing must match the character's age, setting and activity.
- Follow the established character description.
- If the scene takes place in a school, use clothing appropriate
  to that school's location and context.
- If the story is set in Kenya, Kenyan school clothing may be used
  when appropriate.
- If the story is set elsewhere, adapt clothing to that setting.
- Do not automatically use Kenyan uniforms in international stories.
- Do not automatically use Western uniforms.
- Avoid exaggerated cultural costumes unless specifically relevant.

FACIAL DESIGN:

- Natural human facial proportions.
- Natural-sized eyes.
- No oversized eyes.
- No oversized heads.
- No tiny bodies.
- No exaggerated cartoon facial features.
- Expressions should be subtle and believable.
- Characters should remain attractive and appealing to children
  without becoming overly cartoonish.

LIGHTING:

Lighting is determined ONLY by the scene description, the time of day,
the weather, the location and the mood.

DO NOT apply a default yellow, golden, warm or glowing lighting style.

IMPORTANT:

The image must NOT automatically have a yellow or orange color cast.

Lighting should look natural and believable for the exact scene.

Examples:

Bright daytime classroom:
- Use neutral natural daylight coming through windows.
- Whites should remain white.
- Avoid yellow or golden color casts.

Outdoor daytime:
- Use natural daylight appropriate to the weather.
- The sky, grass, buildings and clothing should retain natural colors.

Cloudy or overcast day:
- Use soft, diffused, neutral light with gentle shadows.

Morning:
- Use natural early daylight.
- A slightly warm tone is acceptable only if the scene specifically
  suggests early morning sunlight.

Afternoon:
- Use neutral natural daylight with realistic shadows.

Sunset:
- Use warm orange or golden light because the scene actually calls
  for sunset.

Evening:
- Use softer, lower natural light appropriate to the setting.

Night:
- Use believable moonlight or appropriate indoor artificial lighting.

LIGHTING CONSISTENCY:

Lighting should change naturally from scene to scene.

Do NOT make every scene:

- bright yellow
- golden
- orange
- glowing
- strongly warm
- heavily saturated

Do NOT use a permanent warm-yellow filter over the entire image.

Do NOT make children's illustrations look like they are illuminated
by studio lights.

Do NOT make every scene look sunny.

Do NOT brighten dark scenes artificially.

The final image should have:

- natural color balance
- believable light direction
- believable shadows
- appropriate contrast
- realistic relationships between light, shadow and color

The lighting must support the story rather than dominate the artwork.


OUTDOOR NATURE COLORS:

- When a scene takes place outdoors during the day, actively use a
  believable blue or light blue sky, green grass, and natural
  greenery where appropriate to the setting.
- Nature-based outdoor scenes should look like a natural, sunny or
  overcast day outside — not a warm interior glow.
- Vary the environment, setting and color palette from scene to
  scene rather than repeating the same background style throughout
  the story.
- Do not default to a warm indoor or golden-hour palette for
  outdoor daytime scenes unless the scene specifically describes
  sunset or golden hour.

ENVIRONMENT:

- Create a detailed and believable environment appropriate to
  the scene description.

ENVIRONMENT:

- Create a detailed and believable environment appropriate to
  the scene description.
- Include useful background details that help children understand
  where the story is happening.
- Keep environments colorful, clean and inviting.
- Use realistic perspective and depth.
- Make backgrounds visually rich rather than empty.
- Avoid simple clip-art backgrounds.
- Background colors should respond naturally to the lighting
  and time of day.
  
BACKGROUND CONTENT AND EDUCATIONAL MATERIALS:

- Only include background objects that are relevant to the scene.
- Do not randomly add educational posters, maps, charts, flags,
  diagrams or classroom decorations.
- Do not add maps of Africa or other geographical maps unless the
  story or lesson specifically involves geography.
- Do not add alphabet charts unless the scene specifically involves
  alphabet learning.
- Do not add number charts unless the scene specifically involves
  numbers or mathematics.
- Do not add random letters, words or numbers to walls, books,
  posters or classroom materials.
- Avoid unnecessary text anywhere in the background.

IMPORTANT:
If educational text is not specifically required by the scene,
use pictures, shapes, objects and visual materials instead of written
text.

If a classroom scene requires learning materials, make them simple,
age-appropriate and directly relevant to the lesson.

Do not add unrelated classroom decorations just to fill empty space.

TEXT:

- Do not generate readable text unless it is explicitly required
  by the scene.
- Do not generate random letters or words.
- Do not generate incorrect alphabet sequences.
- Do not generate random numbers.
- Do not generate fake signs or labels.
- Avoid text-heavy posters and charts.
- When written educational content is not essential, represent the
  concept visually instead.
- Never add an alphabet chart unless alphabet learning is part of
  the actual scene.
- Never add a map unless geography or a location lesson is part of
  the actual scene.

If text is explicitly required, keep it minimal and simple.

CHILD-FRIENDLY DESIGN:

The image should attract children aged 3–6 through:

- interesting characters
- expressive but natural actions
- beautiful environments
- clear visual storytelling
- engaging but naturally balanced colors
- recognizable objects
- appropriate facial expressions

Do NOT rely on excessive brightness, oversized eyes or exaggerated
cartoon features to make the image attractive to children.

Characters should be friendly and approachable.

Actions should be easy for children to understand.

Make important educational concepts visually understandable.

Avoid frightening, disturbing or overly dramatic imagery.

IMPORTANT STYLE BALANCE:

The result should sit between realistic illustration and cartoon.

It should NOT look like:

- a photograph
- photorealistic CGI
- 3D CGI
- 3D Pixar-style animation
- flat vector graphics
- clip-art
- watercolor
- rough sketches
- anime
- manga
- exaggerated caricature
- baby-style cartoon characters
- oversized heads
- huge eyes
- tiny bodies
- extremely exaggerated facial expressions
- overly bright artificial colors
- heavy yellow color grading
- heavy orange color grading
- glowing fantasy lighting

Aim for a smooth, polished, dimensional 2D animated illustration
with natural-looking characters and beautifully detailed environments.

The artwork should feel like a frame from a high-quality children's
animated television program.

The artwork must be completely original.

Do not copy existing cartoon characters or copyrighted artwork.

Do not include:

- unnecessary text
- captions
- logos
- watermarks
- speech bubbles
"""

    result = client.images.generate(
    model="gpt-image-1-mini",
    prompt=prompt,
    size="1024x1024",
    quality="medium"
)

    return result.data[0].b64_json


def generate_story_scene_sheet(
    scenes,
    character_descriptions=None
):

    character_descriptions = character_descriptions or {}

    scene_details = []

    for scene in scenes:

        characters_present = scene.get(
            "characters_present",
            []
        )

        character_details = []

        for character in characters_present:

            description = character_descriptions.get(
                character,
                "No detailed description available."
            )

            character_details.append(
                f"- {character}: {description}"
            )

        characters_text = "\n".join(
            character_details
        )

        scene_details.append(
            f"""
SCENE {scene['scene_number']}

VISUAL:
{scene.get('visual', '')}

CHARACTERS:
{characters_text}
"""
        )

    scenes_text = "\n".join(scene_details)

    prompt = f"""
Create one educational story illustration sheet containing
exactly 4 separate scene panels.

The sheet will be used to illustrate a short children's
animated story.

STORY SCENES:
{scenes_text}

CHARACTER CONSISTENCY:
Keep the same characters visually consistent across all panels.
Use the character descriptions provided for each scene.

LAYOUT:
- Create exactly 4 scene panels.
- Arrange them in a clean 2 × 2 grid.
- Each panel must have equal space.
- Leave a clear margin between all panels.
- Keep every panel completely inside the image.
- Do not crop any panel.
- Do not allow characters or important objects to cross into another panel.
- Each panel must clearly represent only its assigned scene.

SCENE ACCURACY:
- Scene 1 must show the visual description for Scene 1.
- Scene 2 must show the visual description for Scene 2.
- Scene 3 must show the visual description for Scene 3.
- Scene 4 must show the visual description for Scene 4.
- Do not combine scenes.
- Do not invent additional scenes.
- Do not replace important story objects with unrelated objects.

STYLE:
Create polished, child-friendly 2D animated educational
illustrations suitable for children aged 3–6.

Use:
- natural-looking characters
- natural proportions
- clear facial expressions
- colourful but balanced colours
- simple readable environments
- consistent character appearance
- clear visual storytelling

Do NOT use:
- photorealism
- 3D CGI
- anime
- manga
- exaggerated caricatures
- oversized heads
- huge eyes
- unnecessary text
- captions
- logos
- watermarks
- speech bubbles

The artwork must be completely original.

Return only the image.
"""

    result = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        quality="medium"
    )

    return result.data[0].b64_json
   
def split_story_scene_sheet(image_b64):

    import base64
    import io

    from PIL import Image

    image_bytes = base64.b64decode(
        image_b64
    )

    image = Image.open(
        io.BytesIO(image_bytes)
    )

    image = image.convert("RGB")

    width, height = image.size

    half_width = width // 2
    half_height = height // 2

    boxes = [
        (0, 0, half_width, half_height),
        (half_width, 0, width, half_height),
        (0, half_height, half_width, height),
        (half_width, half_height, width, height),
    ]

    scene_images = []

    for box in boxes:

        cropped = image.crop(box)

        buffer = io.BytesIO()

        cropped.save(
            buffer,
            format="PNG"
        )

        scene_images.append(
            base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")
        )

    return scene_images