import streamlit as st

from database import (
    get_all_lessons,
    get_lesson,
    delete_lesson,
    search_lessons,
)


def show_lesson_library(user):

    st.sidebar.title("📚 Lesson Library")
    st.sidebar.divider()

    search = st.sidebar.text_input(
        "🔍 Search Lessons",
        placeholder="Search by topic..."
    )

    if search:

        saved_lessons = search_lessons(
            user["id"],
            search
        )

    else:

        saved_lessons = get_all_lessons(
            user["id"]
        )

    if saved_lessons:

        for lesson in saved_lessons:

            lesson_id = lesson["id"]
            title = lesson["title"]
            age = lesson["age"]
            duration = lesson["duration"]

            st.sidebar.markdown(
                f"**{title}**"
            )

            st.sidebar.caption(
                f"{age} • {duration}"
            )

            col1, col2, col3 = st.sidebar.columns(3)

            # ---------------- OPEN ----------------

            with col1:

                if st.button(
                    "📖",
                    key=f"open_{lesson_id}",
                    help="Open"
                ):

                    selected_lesson = get_lesson(
                        user["id"],
                        lesson_id
                    )

                    if selected_lesson:

                        st.session_state.selected_lesson = selected_lesson

                                                # Load this lesson's saved Picture Cards
                        st.session_state.picture_cards = (
                            selected_lesson.get("picture_cards")
                        )

                        st.session_state.picture_cards_colour = (
                            selected_lesson.get("picture_cards_colour")
                        )

                        # Load this lesson's saved Animated Story, if any
                        saved_story = selected_lesson.get("animated_story")

                        if saved_story:

                            import json

                            st.session_state.story = json.loads(saved_story)

                        else:

                            st.session_state.story = None

                        # Set the topic for this lesson
                        st.session_state.story_topic = (
                            selected_lesson["title"]
                        )

            # ---------------- DELETE ----------------

            with col2:

                if st.button(
                    "🗑",
                    key=f"delete_{lesson_id}",
                    help="Delete"
                ):

                    delete_lesson(
                        user["id"],
                        lesson_id
                    )

                    if (
                        st.session_state.selected_lesson
                        and st.session_state.selected_lesson["id"]
                        == lesson_id
                    ):

                        st.session_state.selected_lesson = None

                    st.rerun()

            # ---------------- EDIT ----------------

            with col3:

                if st.button(
                    "✏️",
                    key=f"edit_{lesson_id}",
                    help="Edit"
                ):

                    st.session_state.edit_lesson = get_lesson(
                        user["id"],
                        lesson_id
                    )

                    st.rerun()

            st.sidebar.divider()

    else:

        if search:

            st.sidebar.info(
                "🔍 No lessons matched your search."
            )

        else:

            st.sidebar.info(
                "No saved lessons yet."
            )
