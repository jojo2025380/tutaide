
import streamlit as st

from database import get_plan_limits


def show_dashboard(user, lesson_count):

    st.title("📚 TutAide")

    st.subheader(
        f"Welcome back, {user['name']} 👋"
    )

    st.caption(
        "Your AI-powered lesson planner for early childhood educators."
    )

    st.divider()

    st.subheader("📊 Dashboard")

    plan_limits = get_plan_limits(
        user["id"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Lessons Created",
            lesson_count
        )

    with col2:
        st.metric(
            "📖 Saved Lessons",
            lesson_count
        )

    
    with col3:
        st.metric(
            "💎 Account",
            plan_limits["name"]
        )

        st.caption(
            f"📚 {plan_limits['lesson_limit']} lessons\n\n"
            f"🎬 {plan_limits['story_limit']} stories\n\n"
            f"🖼️ {plan_limits['image_limit']} images\n\n"
            f"🃏 {plan_limits['picture_card_limit']} picture cards"
        )

