import streamlit as st
import json
from datetime import datetime, timedelta

from auth import (
    create_user,
    login_user
)


from config import (
    APP_TITLE,
    APP_DESCRIPTION,
    AGE_GROUPS,
    LESSON_DURATIONS,
    PLANS,
)


from lesson_generator import generate_lesson
from topic_validation import validate_topic
from story_generator import generate_story
from card_generator import (
    generate_picture_cards,
    generate_picture_cards_colour,
    get_picture_card_items
)

from image_generator import (
    generate_scene_image,
    generate_story_scene_sheet,
    split_story_scene_sheet
)

from components.dashboard import show_dashboard
from components.lesson_library import show_lesson_library
from components.lesson_form import show_lesson_form
from components.lesson_editor import show_lesson_editor


from mpesa import (
    initiate_stk_push,
    query_stk_push_status
)

from database import (
    create_database,
    save_lesson,
    get_usage,
    get_all_lessons,
    get_lesson,
    delete_lesson,
    count_user_lessons,
    can_generate_image,
    get_remaining_images,
    get_plan_limits,
    can_generate_story,
    get_remaining_stories,
    can_generate_picture_cards,
    get_remaining_picture_cards,
    increment_usage,
    add_extension_credits,
    get_extension_credits,
    use_extension_credit,
    save_picture_cards,
    save_picture_cards_colour,
    save_animated_story,
    set_subscription,
    save_payment,
    update_payment_status
)


# ---------------- DATABASE ----------------
create_database()


# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="ECE AI Assistant",
    page_icon="📚",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "lesson_history" not in st.session_state:
    st.session_state.lesson_history = []

if "lessons" not in st.session_state:
    st.session_state.lessons = []

if "story" not in st.session_state:
    st.session_state.story = None
    
if "selected_lesson" not in st.session_state:
    st.session_state.selected_lesson = None

if "edit_lesson" not in st.session_state:
    st.session_state.edit_lesson = None

if "user" not in st.session_state:
    st.session_state.user = None

if "story_topic" not in st.session_state:
    st.session_state.story_topic = None

if "picture_cards" not in st.session_state:
    st.session_state.picture_cards = None

if "card_items" not in st.session_state:
    st.session_state.card_items = []


# ---------------- LOGIN ----------------

if st.session_state.user is None:

    st.divider()

    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Create Account"])

    # ---------------- LOGIN ----------------

    with tab1:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            user = login_user(email, password)

            if user:

                st.session_state.user = user
                st.success(f"Welcome {user['name']}!")
                st.rerun()

            else:

                st.error("Invalid email or password.")

    # ---------------- CREATE ACCOUNT ----------------

    with tab2:

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button("Create Account"):

            success = create_user(
                name,
                email,
                password
            )

            if success:

                st.success("Account created successfully!")

            else:

                st.error("Email already exists.")

    st.stop()

st.divider()

lesson_count = count_user_lessons(st.session_state.user["id"])

show_dashboard(
    st.session_state.user,
    lesson_count
)


# ---------------- SIDEBAR ----------------
st.sidebar.title("📚 ECE AI Assistant")

st.sidebar.subheader("👤 Account")

st.sidebar.success(
    f"Logged in as\n\n**{st.session_state.user['name']}**"
)

if st.sidebar.button("🚪 Logout", use_container_width=True):

    st.session_state.user = None
    st.session_state.selected_lesson = None
    st.session_state.lessons = []
    st.rerun()

st.sidebar.divider()

# ---------------- PLAN & USAGE ----------------

plan_limits = get_plan_limits(
    st.session_state.user["id"]
)

lesson_count = count_user_lessons(
    st.session_state.user["id"]
)

remaining_stories = get_remaining_stories(
    st.session_state.user["id"],
    plan_limits["story_limit"]
)

remaining_images = get_remaining_images(
    st.session_state.user["id"],
    plan_limits["image_limit"]
)

st.sidebar.subheader("💳 Your Plan")

st.sidebar.info(
    f"**{plan_limits['name']}**\n\n"
    f"💰 KSh {plan_limits['price']:,}"
)

st.sidebar.markdown(
    f"📚 **Lessons:** "
    f"{lesson_count}/{plan_limits['lesson_limit']}"
)

st.sidebar.markdown(
    f"🎬 **Stories:** "
    f"{plan_limits['story_limit'] - remaining_stories}"
    f"/{plan_limits['story_limit']}"
)

st.sidebar.markdown(
    f"🖼️ **Images:** "
    f"{plan_limits['image_limit'] - remaining_images}"
    f"/{plan_limits['image_limit']}"
)

st.sidebar.divider()

# ---------------- PLANS & UPGRADE ----------------

st.sidebar.subheader("💳 Plans & Upgrade")

for plan_key, plan in PLANS.items():

    st.sidebar.markdown(
        f"**{plan['name']} — KSh {plan['price']:,}**"
    )

    st.sidebar.caption(
        f"📚 {plan['lesson_limit']} lessons  •  "
        f"🎬 {plan['story_limit']} stories  •  "
        f"🖼️ {plan['image_limit']} images"
    )

    if plan_key == plan_limits["key"]:

        st.sidebar.success(
            "✓ Current Plan"
        )

    else:

        if st.sidebar.button(
            f"Upgrade to {plan['name']}",
            key=f"upgrade_{plan_key}",
            use_container_width=True
        ):

            st.session_state[f"show_payment_{plan_key}"] = True
            st.rerun()

        if st.session_state.get(f"show_payment_{plan_key}"):

            phone_number = st.sidebar.text_input(
                "M-Pesa phone number (2547XXXXXXXX)",
                key=f"phone_{plan_key}"
            )

            if st.sidebar.button(
                "Pay Now",
                key=f"pay_now_{plan_key}",
                use_container_width=True
            ):

                if not phone_number.strip():

                    st.sidebar.error(
                        "Please enter your M-Pesa phone number."
                    )

                else:

                    try:

                        stk_response = initiate_stk_push(
                            phone_number.strip(),
                            plan["price"],
                            f"TutorAide-{plan_key}",
                            f"TutorAide {plan['name']} Plan"
                        )

                        checkout_id = stk_response.get(
                            "CheckoutRequestID"
                        )

                        save_payment(
                            st.session_state.user["id"],
                            plan["price"],
                            checkout_id,
                            "pending"
                        )

                        with st.spinner(
                            "Waiting for M-Pesa confirmation... "
                            "please enter your PIN on your phone."
                        ):

                            import time

                            payment_result = "pending"

                            for _ in range(10):

                                time.sleep(3)

                                payment_result = query_stk_push_status(
                                    checkout_id
                                )

                                if payment_result != "pending":
                                    break

                        if payment_result == "success":

                            update_payment_status(
                                checkout_id,
                                "success"
                            )

                            today = datetime.now().strftime("%Y-%m-%d")

                            next_month = (
                                datetime.now() + timedelta(days=30)
                            ).strftime("%Y-%m-%d")

                            set_subscription(
                                st.session_state.user["id"],
                                plan_key,
                                "active",
                                today,
                                next_month
                            )

                            st.session_state[
                                f"show_payment_{plan_key}"
                            ] = False

                            st.sidebar.success(
                                f"🎉 Payment successful! "
                                f"You're now on the {plan['name']} plan."
                            )

                            st.rerun()

                        elif payment_result == "failed":

                            update_payment_status(
                                checkout_id,
                                "failed"
                            )

                            st.sidebar.error(
                                "Payment failed or was cancelled. "
                                "Please try again."
                            )

                        else:

                            st.sidebar.warning(
                                "We couldn't confirm your payment yet. "
                                "If money left your account, contact "
                                "support with your phone number."
                            )

                    except Exception as e:

                        st.sidebar.error(
                            f"Payment error: {e}"
                        )

    st.sidebar.divider()

    st.sidebar.divider()

# ---------------- EXTENSION PACK ----------------

st.sidebar.subheader("🎁 Extension Pack")

st.sidebar.caption(
    "Need more generations? "
    "Get extra resources without changing your plan."
)

extension_resource = st.sidebar.selectbox(
    "Choose what you need:",
    [
        "🎬 Extra Stories",
        "🖼️ Extra Images",
        "🃏 Extra Picture Cards"
    ],
    key="extension_resource"
)

if st.sidebar.button(
    "🎁 Get Extension Pack — KSh 150",
    use_container_width=True
):

    st.session_state["show_extension_payment"] = True
    st.rerun()

if st.session_state.get("show_extension_payment"):

    ext_phone_number = st.sidebar.text_input(
        "M-Pesa phone number (2547XXXXXXXX)",
        key="phone_extension"
    )

    if st.sidebar.button(
        "Pay Now",
        key="pay_now_extension",
        use_container_width=True
    ):

        if not ext_phone_number.strip():

            st.sidebar.error(
                "Please enter your M-Pesa phone number."
            )

        else:

            try:

                resource_map = {
                    "🎬 Extra Stories": "stories",
                    "🖼️ Extra Images": "images",
                    "🃏 Extra Picture Cards": "picture_cards"
                }

                selected_resource = resource_map[extension_resource]

                stk_response = initiate_stk_push(
                    ext_phone_number.strip(),
                    150,
                    "TutorAide-Extension",
                    "TutorAide Extension Pack"
                )

                checkout_id = stk_response.get(
                    "CheckoutRequestID"
                )

                save_payment(
                    st.session_state.user["id"],
                    150,
                    checkout_id,
                    "pending"
                )

                with st.spinner(
                    "Waiting for M-Pesa confirmation... "
                    "please enter your PIN on your phone."
                ):

                    import time

                    payment_result = "pending"

                    for _ in range(10):

                        time.sleep(3)

                        payment_result = query_stk_push_status(
                            checkout_id
                        )

                        if payment_result != "pending":
                            break

                if payment_result == "success":

                    update_payment_status(
                        checkout_id,
                        "success"
                    )

                    add_extension_credits(
                        st.session_state.user["id"],
                        selected_resource,
                        3
                    )

                    st.session_state["show_extension_payment"] = False

                    st.sidebar.success(
                        f"🎁 3 extra "
                        f"{extension_resource.replace('🎬 Extra ', '').replace('🖼️ Extra ', '').replace('🃏 Extra ', '').lower()} "
                        f"added!"
                    )

                    st.rerun()

                elif payment_result == "failed":

                    update_payment_status(
                        checkout_id,
                        "failed"
                    )

                    st.sidebar.error(
                        "Payment failed or was cancelled. "
                        "Please try again."
                    )

                else:

                    st.sidebar.warning(
                        "We couldn't confirm your payment yet. "
                        "If money left your account, contact "
                        "support with your phone number."
                    )

            except Exception as e:

                st.sidebar.error(
                    f"Payment error: {e}"
                )

# ---------------- LESSON LIBRARY ----------------

st.sidebar.subheader("📚 Lesson Library")

show_lesson_library(
    st.session_state.user
)



# ---------------- LESSON FORM ----------------

topic, age, duration, outcomes_text, submitted = show_lesson_form()


# ---------------- GENERATE BUTTON ----------------

if submitted:

    plan_limits = get_plan_limits(
        st.session_state.user["id"]
    )

    usage = get_usage(
        st.session_state.user["id"]
    )

    lesson_count = usage["lessons_used"]

    if lesson_count >= plan_limits["lesson_limit"]:

        st.warning(
            f"🔒 You have reached your "
            f"{plan_limits['name']} lesson limit "
            f"of {plan_limits['lesson_limit']} lessons "
            f"for this month."
        )

        st.stop()

    if not topic.strip():

        st.error(
            "Please enter a lesson topic."
        )

        st.stop()

    result, value = validate_topic(topic)

    if result is True:

        clean_topic = value

    elif result == "suggest":

        st.warning(
            f"⚠️ Did you mean: {value}?"
        )

        st.stop()

    else:

        st.error(
            "⚠️ Invalid topic. Use: Animals, Shapes, "
            "Colours, Transport, Plants, Food, Weather, "
            "Numbers, Alphabet, Family, Body Parts, "
            "My Home, Clothing, Community Helpers, "
            "Health and Hygiene, My School, Water, "
            "Insects, Feelings and Emotions, "
            "Five Senses, Space and Sky, Art Supplies, "
            "Musical Instruments, Safety, Earth Care."
        )

        st.stop()

    try:

        lesson = generate_lesson(
            age,
            clean_topic,
            duration,
            outcomes_text
        )

    except Exception as e:

        st.error(
            f"AI Error: {e}"
        )

        st.stop()

    # ---------------- STORE CLEAN TOPIC ----------------

    lesson["topic"] = clean_topic

    # ---------------- APPLY TEACHER OUTCOMES ----------------

    if outcomes_text.strip():

        teacher_outcomes = [
            line.strip()
            for line in outcomes_text.split("\n")
            if line.strip()
        ]

        lesson["outcomes"] = teacher_outcomes

    # ---------------- SAVE LESSON ----------------

    lesson_id = save_lesson(
        st.session_state.user["id"],
        lesson
    )

    lesson["id"] = lesson_id

    increment_usage(
        st.session_state.user["id"],
        "lessons_used"
    )

    # Initialise Picture Cards for this lesson
    lesson["picture_cards"] = None

    st.session_state.lesson_history.append(
        clean_topic
    )

    st.session_state.lessons.append(
        lesson
    )

    st.session_state.selected_lesson = None
    st.session_state.edit_lesson = None

    # Remember the cleaned topic for the animated story

    st.session_state.story_topic = clean_topic

    # Reset story and Picture Cards for the new lesson
    st.session_state.story = None
    st.session_state.picture_cards = None
    st.session_state.picture_cards_colour = None

    st.success(
    "Lesson generated successfully!"
    )


# ---------------- DISPLAY LESSON ----------------

if st.session_state.edit_lesson:

    lesson = st.session_state.edit_lesson

elif st.session_state.selected_lesson:

    lesson = st.session_state.selected_lesson

elif st.session_state.lessons:

    lesson = st.session_state.lessons[-1]

else:

    lesson = None


if lesson:

    # ---------------- EDIT LESSON ----------------

    if st.session_state.edit_lesson:

        show_lesson_editor(
            st.session_state.user
        )

    # ---------------- DISPLAY LESSON ----------------

    else:

        st.header("📚 Lesson Plan")
        st.subheader(lesson["title"])

                # ---------------- Lesson Summary ----------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "👶 Age Group",
                lesson["age"]
            )

        with col2:

            st.metric(
                "⏱ Duration",
                lesson["duration"]
            )

        st.divider()


               # ---------------- Tabs ----------------

        lesson_tab, activities_tab, assessment_tab = st.tabs(
            ["📖 Lesson", "🎵 Activities", "🧪 Assessment"]
        )


        # ==================================================
        # LESSON TAB
        # ==================================================

        with lesson_tab:

            st.subheader("🎯 Learning Outcomes")

            for outcome in lesson["outcomes"]:

                st.markdown(
                    f"✅ **{outcome}**"
                )

            st.divider()

            st.subheader("🧰 Materials Needed")

            for material in lesson["materials"]:

                st.markdown(
                    f"📌 {material}"
                )

            st.divider()

            st.subheader("🔥 Warm-Up Activity")

            st.info(
                lesson["warmup"]
            )

            st.divider()

            st.subheader("🧑‍🏫 Teaching Steps")

            for i, step in enumerate(
                lesson["steps"],
                start=1
            ):

                st.markdown(
                    f"**Step {i}:** {step}"
                )


        # ==================================================
        # ACTIVITIES TAB
        # ==================================================

        with activities_tab:

            st.subheader("🎵 Song")

            st.write(
                f"**Tune:** {lesson['tune']}"
            )

            st.text(
                lesson["song"]
            )

            st.divider()

            st.subheader("📖 Story")

            st.info(
                lesson["story"]
            )

            st.divider()

            st.subheader("🎲 Classroom Game")

            st.success(
                lesson["game"]
            )


            # ==================================================
            # ANIMATED STORY
            # ==================================================

            st.divider()

            st.subheader("🎬 Animated Story")

            if st.button(
                "🎬 Generate Animated Story",
                use_container_width=True
            ):

                plan_limits = get_plan_limits(
                    st.session_state.user["id"]
                )

                remaining_stories = get_remaining_stories(
                    st.session_state.user["id"],
                    plan_limits["story_limit"]
                )

                if remaining_stories > 0:

                    try:

                        with st.spinner(
                            "Creating your story..."
                        ):

                            story = generate_story(
                                lesson["age"],
                                st.session_state.story_topic,
                                lesson["outcomes"]
                            )

                    except Exception:

                        st.error(
                            "⚠️ We couldn't generate the story right now. "
                            "Please try again later."
                        )

                        st.stop()

                    st.session_state.story = story

                    increment_usage(
                        st.session_state.user["id"],
                        "stories_used"
                    )

                    st.success(
                     "🎬 Story generated successfully!"
                    )

                else:

                    extension_stories = get_extension_credits(
                        st.session_state.user["id"],
                        "stories"
                    )

                    if extension_stories > 0:

                        st.info(
                            f"🎁 Your monthly story allowance is finished. "
                            f"You have {extension_stories} Extension Pack "
                            f"story credit(s) available."
                        )

                        if st.button(
                            "🎬 Use Extension Pack Credit",
                            use_container_width=True,
                            key="use_story_extension"
                        ):

                            try:

                                with st.spinner(
                                    "Creating your story..."
                                ):

                                    story = generate_story(
                                        lesson["age"],
                                        st.session_state.story_topic,
                                        lesson["outcomes"]
                                    )

                            except Exception:

                                st.error(
                                    "⚠️ We couldn't generate the story right now. "
                                    "Please try again later."
                                )

                                st.stop()

                            use_extension_credit(
                                st.session_state.user["id"],
                                "stories"
                            )

                            st.session_state.story = story

                            st.success(
                                "🎬 Story generated using "
                                "1 Extension Pack credit!"
                            )

                            st.rerun()

                        else:

                            st.warning(
                            f"🔒 You have used all your "
                            f"{plan_limits['name']} story generations "
                            f"and have no Extension Pack story credits."
                        )


            # ==================================================
            # STORY DISPLAY
            # ==================================================

            if st.session_state.story:

                story = st.session_state.story

                st.markdown(
                    f"## {story['title']}"
                )

                st.subheader("👥 Characters")

                for character in story["characters"]:

                    st.markdown(
                        f"🐾 {character}"
                    )

                st.subheader("🎞️ Story Scenes")

                plan_limits = get_plan_limits(
                    st.session_state.user["id"]
                )

                remaining_images = get_remaining_images(
                    st.session_state.user["id"],
                    plan_limits["image_limit"]
                )

                extension_images = get_extension_credits(
                    st.session_state.user["id"],
                    "images"
                )

                missing_images = any(
                    not scene.get("image_data")
                    for scene in story["scenes"]
                )

                if missing_images:

                    if len(story["scenes"]) != 4:

                        st.error(
                            "⚠️ This story does not contain exactly 4 scenes. "
                            "Please generate the story again."
                        )

                    elif remaining_images > 0:

                        if st.button(
                            "🖼️ Generate Story Images",
                            key="generate_story_images",
                            use_container_width=True
                        ):

                            try:

                                with st.spinner(
                                    "Creating all 4 story scenes..."
                                ):

                                    sheet_data = generate_story_scene_sheet(
                                        story["scenes"],
                                        story.get(
                                            "character_descriptions",
                                            {}
                                        )
                                    )

                                    scene_images = split_story_scene_sheet(
                                        sheet_dataT
                                    )

                            except Exception:

                                st.error(
                                    "⚠️ We couldn't generate the story images "
                                    "right now. Please try again later."
                                )

                                st.stop()

                            for index, scene in enumerate(
                                story["scenes"]
                            ):

                                scene["image_data"] = scene_images[index]

                            increment_usage(
                                st.session_state.user["id"],
                                "images_used"
                            )

                            st.session_state.story = story

                            import json as _json

                            save_animated_story(
                                st.session_state.user["id"],
                                lesson["id"],
                                _json.dumps(story)
                            )

                            st.success(
                                "🖼️ All 4 story images generated successfully!"
                            )

                            st.rerun()

                    elif extension_images > 0:

                        st.info(
                            f"🎁 Your monthly image allowance is finished. "
                            f"You have {extension_images} Extension Pack "
                            f"image credit(s) available."
                        )

                        if st.button(
                            "🖼️ Use Extension Pack Credit",
                            use_container_width=True
                        ):

                            try:

                                with st.spinner(
                                    "Creating all 4 story scenes..."
                                ):

                                    sheet_data = generate_story_scene_sheet(
                                        story["scenes"],
                                        story.get(
                                            "character_descriptions",
                                            {}
                                        )
                                    )

                                    scene_images = split_story_scene_sheet(
                                        sheet_data
                                    )

                            except Exception:

                                st.error(
                                    "⚠️ We couldn't generate the story images "
                                    "right now. Please try again later."
                                )

                                st.stop()

                            use_extension_credit(
                                st.session_state.user["id"],
                                "images"
                            )

                            for index, scene in enumerate(
                                story["scenes"]
                            ):

                                scene["image_data"] = scene_images[index]

                            st.session_state.story = story

                            import json as _json

                            save_animated_story(
                                st.session_state.user["id"],
                                lesson["id"],
                                _json.dumps(story)
                            )

                            st.success(
                                "🖼️ All 4 story images generated using "
                                "1 Extension Pack credit!"
                            )

                            st.rerun()

                    else:

                        st.warning(
                            f"🔒 You have used all your "
                            f"{plan_limits['name']} image generations "
                            f"and have no Extension Pack image credits."
                        )

                image_cols = st.columns(4)

                for i, scene in enumerate(story["scenes"]):

                    if scene.get("image_data"):

                        import base64

                        image_bytes = base64.b64decode(
                            scene["image_data"]
                        )

                        with image_cols[i]:

                            st.image(
                                image_bytes,
                                use_container_width=True
                            )

                for scene in story["scenes"]:

                    st.markdown(
                        f"### Scene {scene['scene_number']}"
                    )

                    st.write(
                        scene.get("narration", "")
                    )

                    if scene.get("dialogue"):

                        st.markdown(
                            f"*{scene['dialogue']}*"
                        )


                # ==================================================
                # PICTURE CARDS
                # ==================================================

                st.divider()

                st.subheader("🃏 Picture Cards")

                plan_limits = get_plan_limits(
                    st.session_state.user["id"]
                )

                remaining_picture_cards = get_remaining_picture_cards(
                    st.session_state.user["id"],
                    plan_limits["picture_card_limit"]
                )

                if remaining_picture_cards > 0:

                    if st.button(
                        f"🃏 Generate Picture Cards "
                        f"({remaining_picture_cards} remaining)",
                        key="generate_picture_cards",
                        use_container_width=True
                    ):

                        try:

                            card_items = get_picture_card_items(
                                lesson.get("topic") or lesson["title"]
                            )

                            with st.spinner(
                                "Creating picture cards..."
                            ):

                                picture_cards = generate_picture_cards(
                                    lesson["title"],
                                    card_items,
                                    lesson["outcomes"]
                                )

                                picture_cards_colour = generate_picture_cards_colour(
                                    lesson["title"],
                                    card_items,
                                    lesson["outcomes"]
                                )

                        except Exception:

                            st.error(
                                "⚠️ We couldn't generate the picture cards "
                                "right now. Please try again later."
                            )

                            st.stop()

                        st.session_state.picture_cards = picture_cards
                        st.session_state.picture_cards_colour = picture_cards_colour

                        save_picture_cards(
                            st.session_state.user["id"],
                            lesson["id"],
                            picture_cards
                        )

                        save_picture_cards_colour(
                            st.session_state.user["id"],
                            lesson["id"],
                            picture_cards_colour
                        )


                        increment_usage(
                            st.session_state.user["id"],
                            "picture_cards_used"
                        )

                        st.success(
                            f"🃏 Picture Cards generated successfully! "
                            f"{remaining_picture_cards - 1} "
                            f"picture card generation(s) remaining."
                        )

                        st.rerun()

                else:

                    extension_picture_cards = get_extension_credits(
                        st.session_state.user["id"],
                        "picture_cards"
                    )

                    if extension_picture_cards > 0:

                        st.info(
                            f"🎁 Your monthly picture card allowance is finished. "
                            f"You have {extension_picture_cards} Extension Pack "
                            f"picture card credit(s) available."
                        )

                        if st.button(
                            "🃏 Use Extension Pack Credit",
                            use_container_width=True,
                            key="use_picture_card_extension"
                        ):

                            try:

                                card_items = get_picture_card_items(
                                    lesson.get("topic") or lesson["title"]
                                )

                                with st.spinner(
                                    "Creating picture cards..."
                                ):

                                    picture_cards = generate_picture_cards(
                                        lesson["title"],
                                        card_items,
                                        lesson["outcomes"]
                                    )

                            except Exception:

                                st.error(
                                    "⚠️ We couldn't generate the picture cards "
                                    "right now. Please try again later."
                                )

                                st.stop()

                            use_extension_credit(
                                st.session_state.user["id"],
                                "picture_cards"
                            )

                            st.session_state.picture_cards = picture_cards

                            save_picture_cards(
                                st.session_state.user["id"],
                                lesson["id"],
                                picture_cards
                            )

                            st.success(
                                "🃏 Picture Cards generated using "
                                "1 Extension Pack credit!"
                            )

                            st.rerun()

                    else:

                        st.warning(
                            f"🔒 You have used all your "
                            f"{plan_limits['name']} picture card generations "
                            f"and have no Extension Pack picture card credits."
                        )

                    # ---------------- DISPLAY PICTURE CARDS ----------------

                picture_cards_to_display = st.session_state.picture_cards

                if (
                    not picture_cards_to_display
                    and lesson
                    and lesson.get("picture_cards")
                ):

                    picture_cards_to_display = lesson.get(
                       "picture_cards"
                    )

                if picture_cards_to_display:

                    import base64

                    st.markdown("**🖍️ For children to colour**")

                    card_bytes = base64.b64decode(
                        picture_cards_to_display
                    )

                    st.image(
                        card_bytes,
                        use_container_width=True
                    )

                    st.download_button(
                        "⬇️ Download colouring version",
                        data=card_bytes,
                        file_name="picture_cards_colouring.png",
                        mime="image/png"
                    )

                picture_cards_colour_to_display = st.session_state.get(
                    "picture_cards_colour"
                )

                if picture_cards_colour_to_display:

                    import base64

                    st.markdown("**🎨 Full-colour version (for you)**")

                    colour_bytes = base64.b64decode(
                        picture_cards_colour_to_display
                    )

                    st.image(
                        colour_bytes,
                        use_container_width=True
                    )

                    st.download_button(
                        "⬇️ Download colour version",
                        data=colour_bytes,
                        file_name="picture_cards_colour.png",
                        mime="image/png"
                    )

        # ==================================================
        # ASSESSMENT TAB
        # ==================================================

        with assessment_tab:

            st.subheader("🧪 Assessment")

            st.warning(
                lesson["assessment"]
            )

            st.divider()

            st.subheader("🏠 Home Activity")

            st.success(
                lesson["home"]
            )
            
            
                 
