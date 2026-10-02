import streamlit as st

from database import update_lesson


def _text_to_list(text):
    """
    Convert each non-empty line into a list item.
    """
    return [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]


def _list_to_text(items):
    """
    Convert a list into one item per line.
    """
    return "\n".join(items)


def _save_edit(user_id, lesson_id, prefix):

    lesson = {
        "title": st.session_state[f"{prefix}_title"],
        "age": st.session_state[f"{prefix}_age"],
        "duration": st.session_state[f"{prefix}_duration"],

        "outcomes": _text_to_list(
            st.session_state[f"{prefix}_outcomes"]
        ),

        "materials": _text_to_list(
            st.session_state[f"{prefix}_materials"]
        ),

        "warmup": st.session_state[f"{prefix}_warmup"],

        "steps": _text_to_list(
            st.session_state[f"{prefix}_steps"]
        ),

        "tune": st.session_state[f"{prefix}_tune"],
        "song": st.session_state[f"{prefix}_song"],
        "story": st.session_state[f"{prefix}_story"],
        "game": st.session_state[f"{prefix}_game"],

        "assessment": st.session_state[f"{prefix}_assessment"],
        "home": st.session_state[f"{prefix}_home"],
    }

    update_lesson(
        user_id,
        lesson_id,
        lesson
    )

    # Keep session state updated too
    st.session_state.edit_lesson.update(lesson)
    st.session_state.selected_lesson = st.session_state.edit_lesson


def show_lesson_editor(user):

    lesson = st.session_state.get("edit_lesson")

    if not lesson:
        return

    lesson_id = lesson["id"]

    prefix = f"lesson_editor_{lesson_id}"

    # --------------------------------------------------
    # INITIALISE EDITOR VALUES
    # --------------------------------------------------

    defaults = {
        "title": lesson["title"],
        "age": lesson["age"],
        "duration": lesson["duration"],

        "outcomes": _list_to_text(
            lesson["outcomes"]
        ),

        "materials": _list_to_text(
            lesson["materials"]
        ),

        "warmup": lesson["warmup"],

        "steps": _list_to_text(
            lesson["steps"]
        ),

        "tune": lesson["tune"],
        "song": lesson["song"],
        "story": lesson["story"],
        "game": lesson["game"],

        "assessment": lesson["assessment"],
        "home": lesson["home"],
    }

    for field, value in defaults.items():

        key = f"{prefix}_{field}"

        if key not in st.session_state:
            st.session_state[key] = value

    # --------------------------------------------------
    # AUTO-SAVE CALLBACK
    # --------------------------------------------------

    def autosave():
        _save_edit(
            user["id"],
            lesson_id,
            prefix
        )

        st.session_state.editor_saved = True

    # --------------------------------------------------
    # EDITOR
    # --------------------------------------------------

    st.divider()

    st.header("✏️ Edit Lesson")

    st.caption(
        "Changes are automatically saved to your account."
    )

    st.text_input(
        "📖 Lesson Title",
        key=f"{prefix}_title",
        on_change=autosave
    )

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "👶 Age Group",
            key=f"{prefix}_age",
            on_change=autosave
        )

    with col2:

        st.text_input(
            "⏱ Duration",
            key=f"{prefix}_duration",
            on_change=autosave
        )

    st.divider()

    st.subheader("🎯 Learning Outcomes")

    st.text_area(
        "One outcome per line",
        key=f"{prefix}_outcomes",
        height=150,
        on_change=autosave
    )

    st.divider()

    st.subheader("🧰 Materials Needed")

    st.text_area(
        "One material per line",
        key=f"{prefix}_materials",
        height=150,
        on_change=autosave
    )

    st.divider()

    st.subheader("🔥 Warm-Up Activity")

    st.text_area(
        "Warm-up",
        key=f"{prefix}_warmup",
        height=150,
        on_change=autosave
    )

    st.divider()

    st.subheader("🧑‍🏫 Teaching Steps")

    st.text_area(
        "One step per line",
        key=f"{prefix}_steps",
        height=250,
        on_change=autosave
    )

    st.divider()

    st.subheader("🎵 Song")

    st.text_input(
        "Tune",
        key=f"{prefix}_tune",
        on_change=autosave
    )

    st.text_area(
        "Song",
        key=f"{prefix}_song",
        height=150,
        on_change=autosave
    )

    st.divider()

    st.subheader("📖 Story")

    st.text_area(
        "Story",
        key=f"{prefix}_story",
        height=250,
        on_change=autosave
    )

    st.divider()

    st.subheader("🎲 Classroom Game")

    st.text_area(
        "Game",
        key=f"{prefix}_game",
        height=150,
        on_change=autosave
    )

    st.divider()

    st.subheader("🧪 Assessment")

    st.text_area(
        "Assessment",
        key=f"{prefix}_assessment",
        height=150,
        on_change=autosave
    )

    st.divider()

    st.subheader("🏠 Home Activity")

    st.text_area(
        "Home activity",
        key=f"{prefix}_home",
        height=150,
        on_change=autosave
    )

    if st.session_state.get("editor_saved"):

        st.success("💾 Changes saved automatically.")
        
    if st.button(
        "✅ Done Editing",
        use_container_width=True
    ):

        st.session_state.edit_lesson = None
        st.session_state.editor_saved = False

        st.rerun()