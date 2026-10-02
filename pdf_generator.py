from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------------- PDF GENERATOR ----------------
def generate_pdf(lesson, filename="lesson.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    print("OUTCOMES:", lesson["outcomes"])
    print("MATERIALS:", lesson["materials"])
    print("WARMUP:", lesson["warmup"])
    print("STEPS:", lesson["steps"])

# ---------------- PDF HEADER ----------------

    content.append(
    Paragraph(
        "ECE AI ASSISTANT<br/>Early Childhood Lesson Plan",
        styles["Title"]
    )
)

    content.append(Spacer(1, 15))

    content.append(
    Paragraph(
        f"<b>Topic:</b> {lesson['title'].replace('Introduction to ', '')}",
        styles["Normal"]
    )
)

    content.append(
    Paragraph(
        f"<b>Age Group:</b> {lesson['age']}",
        styles["Normal"]
    )
)

    content.append(
    Paragraph(
        f"<b>Duration:</b> {lesson['duration']}",
        styles["Normal"]
    )
)

    content.append(Spacer(1, 20))

    # Learning Outcomes
   
    content.append(
    Paragraph(
        "<b>LEARNING OUTCOMES</b>",
        styles["Heading2"]
    )
)

    for item in lesson["outcomes"]:
     content.append(
        Paragraph(f"• {item}", styles["Normal"])
    )

    content.append(Spacer(1, 12))
    

    # Materials

    content.append(
    Paragraph(
        "<b>MATERIALS NEEDED</b>",
        styles["Heading2"]
    )
)

    for item in lesson["materials"]:
     content.append(
        Paragraph(f"• {item}", styles["Normal"])
    )

    content.append(Spacer(1, 12))
    
    # Warm-up
    content.append(
    Paragraph(
        "<b>WARM-UP ACTIVITY</b>",
        styles["Heading2"]
    )
)
    content.append(Paragraph(lesson["warmup"], styles["Normal"]))
    content.append(Spacer(1, 12))
    
    # Teaching Steps
    content.append(
    Paragraph(
        "<b>TEACHING STEPS</b>",
        styles["Heading2"]
    )
)
    
    for i, step in enumerate(lesson["steps"], 1):
        content.append(Paragraph(f"{i}. {step}", styles["Normal"]))
    content.append(Spacer(1, 12))

    # Song
    content.append(
    Paragraph(
        "<b>SONG</b>",
        styles["Heading2"]
    )
)
    content.append(Paragraph(f"<b>Tune:</b> {lesson['tune']}", styles["Normal"]))
    content.append(Paragraph(lesson["song"].replace("\n", "<br/>"), styles["Normal"]))
    content.append(Spacer(1, 12))

    # Story
    content.append(
    Paragraph(
        "<b>STORY</b>",
        styles["Heading2"]
    )
)
    content.append(Paragraph(lesson["story"].replace("\n", "<br/>"), styles["Normal"]))
    content.append(Spacer(1, 12))

    # Game
    content.append(
    Paragraph(
        "<b>GAME</b>",
        styles["Heading2"]
    )
)
    content.append(Paragraph(lesson["game"], styles["Normal"]))
    content.append(Spacer(1, 12))

    # Assessment
    content.append(
    Paragraph(
        "<b>ASSESSMENT</b>",
        styles["Heading2"]
    )
)
    content.append(Paragraph(lesson["assessment"], styles["Normal"]))
    content.append(Spacer(1, 12))

    # Home Activity
    content.append(
    Paragraph(
        "<b>HOME ACTIVITY</b>",
        styles["Heading2"]
    )
)
    content.append(Paragraph(lesson["home"], styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Spacer(1, 25))

    content.append(
    Paragraph(
        "Generated with ECE AI Assistant",
        styles["Italic"]
    )
)

    doc.build(content)

    return filename
