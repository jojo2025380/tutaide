import streamlit as st

from config import (
    AGE_GROUPS,
    LESSON_DURATIONS,
)


def show_lesson_form():

    st.subheader("📚 Create a Lesson")

    with st.form("lesson_form"):

        left, right = st.columns([2, 1])

        with left:

            topic = st.text_input(
                "📖 Lesson Topic",
                placeholder="e.g. Plants, Family, Weather..."
            )

        with right:

            age = st.selectbox(
                "👶 Age Group",
                AGE_GROUPS
            )

            duration = st.selectbox(
                "⏱️ Lesson Duration",
                LESSON_DURATIONS
            )

        st.divider()

        outcomes_text = st.text_area(
            "🎯 Curriculum Learning Outcomes",
            placeholder=(
                "Enter each learning outcome on a new line.\n\n"
                "Example:\n"
                "By the end of the lesson, the learner should be able to tell their name for identity.\n"
                "Classify pictures of boys and girls for self-identity.\n"
                "Appreciate oneself for self-esteem."
            ),
            height=150
        )

        submitted = st.form_submit_button("Generate Lesson Plan")

    return topic, age, duration, outcomes_text, submitted