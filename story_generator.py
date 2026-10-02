import json

from ai_client import client


def generate_story(age, topic, outcomes):

    outcomes_text = "\n".join(
        f"- {outcome}" for outcome in outcomes
    )

    prompt = f"""

Topic: {topic}
Age Group: {age}

Learning Outcomes:
{outcomes_text}

The story will eventually be turned into an animated educational video
for young children and should be suitable for an international audience.

STORY LENGTH AND COMPLEXITY:
- Keep the story short and age-appropriate.
- For 3 year olds: use about 100-140 words total. Include AT MOST 2 speaking characters in the entire story. Each scene should have at most 1 short line of dialogue per character (3-6 words where possible). Repeat key words often.
- For 4 year olds: use about 120-160 words total. Include AT MOST 3 speaking characters in the entire story. Keep dialogue to 1-2 short lines per character per scene.
- For 5-6 year olds: use about 160-220 words total. Up to 4 speaking characters is acceptable, with slightly richer dialogue, but keep exchanges clear and easy to follow.
- Use simple sentences and familiar vocabulary appropriate to the age.
- Focus on one clear storyline connected to the learning outcomes.
- Avoid unnecessary descriptions, long conversations and extra events.
- The story should be easy to turn into a short animated video.

The story should reflect the location and cultural setting described
by the topic or context. If no location is specified, use a neutral,
globally welcoming setting.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "",
    "characters": [],
    "character_descriptions": {{
        "Character Name": ""
    }},
    "scenes": [
        {{
            "scene_number": 1,
            "characters_present": [],
            "visual": "",
            "narration": "",
            "dialogue": ""
        }}
    ],
    "ending": ""
}}

Rules:

STORY:
- Make the story suitable for children aged {age}.
- Keep the language simple, warm and engaging.
- Make it educational and connected to the topic.
- Create exactly 4 short scenes.
- Each scene should clearly describe what the child would see.
- Keep each scene's narration to 25–40 words.
- Keep dialogue very short and natural.
- Keep the complete story within the recommended word count for the child's age.
- Include simple dialogue where appropriate.
- Avoid scary, violent or inappropriate content.
- Make the story fun, memorable and easy for young children to follow.
- The story must reinforce the learning outcomes listed above.
- Include situations where children can practice or recognize the
  skills in the learning outcomes.
- Return ONLY valid JSON.

CHARACTERS:
- Create a small cast of memorable characters.
- Characters may include children, teachers, parents, community members
  or animals depending on the story.
- Give every important human character a clearly defined appearance.
- Keep the same character's appearance consistent throughout the story.
- Characters should look like believable people rather than generic
  cartoon characters.
- Characters should have distinct personalities and visual identities.
- Avoid making all characters look alike.

GLOBAL CHARACTER DIVERSITY:
- The application is intended for children internationally.
- Create natural visual diversity among characters when appropriate.
- Characters may have a wide range of skin tones including very light,
  light, tan, medium brown, dark brown and deep brown.
- Characters may represent different ethnic, cultural and geographic
  backgrounds.
- Do not automatically make every character white.
- Do not automatically make every character Black or African.
- Do not automatically make every character Kenyan.
- Do not associate skin tone with a particular personality,
  hairstyle, intelligence or behavior.
- Diversity should feel natural rather than forced.
- Avoid stereotypes and exaggerated cultural features.
- When several characters appear together, they may have different
  backgrounds and appearances.
- A story can have characters from the same cultural background when
  that makes sense for the setting.

CHARACTER DESCRIPTIONS:
For every character in the "characters" list, provide a description in
"character_descriptions".

For human characters, include:
- approximate age
- skin tone
- gender where relevant
- hair texture
- hairstyle
- hair length
- eye color
- clothing
- one or two distinctive visual features

HAIR AND HAIRSTYLE DIVERSITY:
- Hair must reflect realistic diversity across all characters.
- Do not associate long hair only with white or light-skinned characters.
- Do not associate short hair only with Black or African characters.
- Include different hair textures, lengths and hairstyles.
- Hair may be straight, wavy, curly, coily or tightly coiled.
- Include short, medium and long hairstyles where appropriate.
- Black and African characters may have natural curls, coils, afros,
  short natural hair, fades, tapered cuts, braids, cornrows, twists,
  locs, puffs, ponytails, buns or other appropriate hairstyles.
- Black and African characters may also have medium or longer natural
  hairstyles.
- Characters from other backgrounds should also have varied hair
  lengths, textures and hairstyles.
- Girls do not all need to have long hair.
- Boys do not all need to have very short hair.
- Do not give every character the same hairstyle.
- Hairstyles should be appropriate for the character's age, setting
  and activity.
- When the story takes place in a school, hairstyles should be
  age-appropriate and practical for that school environment.
- Do not use stereotypes where skin tone automatically determines
  hairstyle or hair length.

FACIAL FEATURES:
- Use natural human facial proportions.
- Eyes should be natural-sized and proportional to the face.
- Do NOT create extremely large cartoon eyes.
- Do NOT create oversized heads.
- Do NOT create tiny bodies.
- Facial expressions should be warm and expressive but not exaggerated.
- Characters should look friendly and approachable.
- Give characters distinct facial features so they can be recognized
  throughout the story.

CLOTHING:
- Clothing should match the character's age, setting and activity.
- Clothing should reflect the story location when appropriate.
- If the story takes place at a school, use realistic school clothing
  or uniforms appropriate to that setting.
- Do not automatically use Western school uniforms.
- Do not automatically use Kenyan school uniforms.
- Adapt clothing naturally to the country or community represented.
- Avoid exaggerated cultural costumes unless they are specifically
  relevant to the story.

CHARACTER CONSISTENCY:
- Once a character has been described, their appearance must remain
  consistent throughout the entire story.
- Do not randomly change a character's hairstyle, hair length, skin tone,
  eye color, age or facial features between scenes.
- Keep clothing consistent unless the story specifically requires a
  clothing change.
- If clothing changes, clearly explain why in the visual description.
- Use the exact character name whenever referring to that character.
- Every scene must include a "characters_present" list.
- Only include characters in "characters_present" who actually appear
  in that scene.
- Do not introduce a new important character halfway through the story
  without adding that character to the "characters" list and providing
  a character description.

VISUAL SCENES:
- Visual descriptions must be detailed enough for an image generator
  to create the scene accurately.
- Describe the characters' actions.
- Describe the environment.
- Describe important objects.
- Describe the location.
- Mention the appropriate time of day when relevant.
- Make the setting believable and visually interesting.
- Use clear visual storytelling that young children can understand.
- Keep the environment appropriate to the story.

LIGHTING:
- Lighting must match the actual scene, time of day, location and mood.
- Do not use one fixed lighting style for every scene.
- Do not make daytime scenes look like nighttime.
- Do not make classroom scenes unnecessarily dark.
- Do not make every scene extremely bright.
- Daytime scenes should use believable natural daylight.
- Morning scenes may use soft warm morning light.
- Afternoon scenes may use natural daylight and appropriate shadows.
- Sunset scenes may use warm golden light.
- Evening scenes should use softer natural or practical lighting.
- Night scenes should use believable moonlight or appropriate
  artificial lighting.
- Indoor lighting should make sense for the environment.
- Lighting should support the mood of the story without overpowering
  the characters or environment.

SETTING AND CULTURAL CONTEXT:
- Adapt the setting naturally to the location of the story.
- If the story is set in Kenya, include appropriate Kenyan environmental,
  school or community details when relevant.
- If the story is set in another country, adapt the environment and
  cultural details naturally to that location.
- If no country is specified, use a neutral and globally welcoming
  environment.
- Do not automatically make every story Kenyan.
- Do not automatically make every story Western.
- Do not insert cultural details that are unrelated to the story.
- Avoid stereotypes.
- Cultural details should feel natural and respectful.

CHILD-FRIENDLY VISUAL STORYTELLING:
- Make scenes visually attractive to young children.
- Use clear actions and recognizable objects.
- Characters should be friendly and approachable.
- Use colorful but balanced environments.
- Avoid excessive visual clutter.
- Avoid frightening or disturbing imagery.
- Make important educational concepts visually obvious.
- The story should feel like a polished children's animated program.

ANIMATION STYLE DIRECTION:
- The eventual images should be suitable for a smooth, polished 2D
  animated children's story.
- Characters should have natural proportions rather than exaggerated
  cartoon proportions.
- Avoid extremely large eyes, oversized heads or exaggerated faces.
- Keep characters visually appealing without making them look like
  simple preschool clip-art.
- Maintain a consistent visual identity for each character.

Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert Early Childhood Education "
                    "storyteller and children's animation story designer. "
                    "Create educational stories that are culturally "
                    "respectful, globally inclusive and visually "
                    "consistent."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    story_text = response.choices[0].message.content

    story = json.loads(story_text)

    return story