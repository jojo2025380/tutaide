import json
from ai_client import client


def generate_lesson(age, topic, duration, outcomes_text=""):

    outcomes_section = ""

    if outcomes_text.strip():

        outcomes_section = f"""
Curriculum Learning Outcomes (provided by the teacher):
{outcomes_text}

Use these EXACT outcomes as the "outcomes" list in your JSON response (one per line/item, do not reword them).
Build the materials, warmup, steps, assessment, and home activity so that EACH outcome is explicitly addressed somewhere in the lesson.
"""

    else:

        outcomes_section = """
No curriculum outcomes were provided. Generate appropriate learning outcomes yourself, based on the topic and age group.
"""

    prompt = f"""
You are an expert Early Childhood Education lesson planner.
Generate ONE complete lesson plan.
Topic: {topic}
Age Group: {age}
Duration: {duration}
{outcomes_section}
Return ONLY valid JSON.
Use exactly this structure:
{{
  "title":"",
  "age":"",
  "duration":"",
  "outcomes":[],
  "materials":[],
  "warmup":"",
  "steps":[],
  "assessment":"",
  "home":"",
  "tune":"",
  "song":"",
  "story":"",
  "game":""
}}
Rules:
- Make the lesson suitable for the selected age.
- Use engaging classroom activities.
- Keep the language simple.
- Return ONLY JSON.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert Early Childhood Education teacher."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    lesson_text = response.choices[0].message.content
    lesson = json.loads(lesson_text)
    return lesson