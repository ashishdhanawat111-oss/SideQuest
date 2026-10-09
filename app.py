
import streamlit as st
from ollama import chat
from database import init_db, load_progress, save_completed_quest


st.set_page_config(
    page_title="SideQuest | Real-World Adventures",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

init_db()

st.markdown("""
<style>

.quest-card {
    background: linear-gradient(135deg, #1b4332, #2d6a4f);
    border: 1px solid #74c69d;
    border-radius: 20px;
    padding: 28px;
    margin: 20px 0;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.quest-label {
    color: #b7e4c7;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 14px;
}

.quest-title {
    color: #ffffff;
    font-size: 23px;
    font-weight: 700;
    line-height: 1.4;
    margin-bottom: 18px;
}

.quest-reward {
    display: inline-block;
    background: #081c15;
    color: #ffd166;
    padding: 8px 14px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 700;
}

/* Main app background */
.stApp {
    background: linear-gradient(160deg, #081c15, #163b2c);
    color: #f1f7ef;
}

/* Main content spacing */
.block-container {
    max-width: 780px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #d8f3dc !important;
}

/* Quest cards and notification boxes */
div[data-testid="stAlert"] {
    background: #204b38;
    border: 1px solid #52b788;
    border-radius: 16px;
    color: #ffffff;
}

/* Buttons */
.stButton > button {
    background: #2d6a4f;
    color: white;
    border: 1px solid #74c69d;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #40916c;
    color: white;
    border-color: #b7e4c7;
}

/* Upload area */
div[data-testid="stFileUploader"] {
    background: #143427;
    border: 1px solid #40916c;
    border-radius: 16px;
    padding: 12px;
}

/* XP metrics */
div[data-testid="stMetric"] {
    background: #143427;
    padding: 18px;
    border: 1px solid #40916c;
    border-radius: 16px;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div {
    background-color: #74c69d;
}

/* Captions */
.stCaption {
    color: #b7e4c7;
}
</style>
""", unsafe_allow_html=True)


st.title("🌿 SideQuest")
st.write("The real world is your playground. AI is your judge!")

quests = [
    "Find something man-made that nature is slowly reclaiming.",
    "Find something in nature that looks like a face.",
    "Find an object that creates an interesting shadow.",
    "Find something that looks older than its surroundings.",
    "Find two completely different things growing together."
]

def get_next_quest_index():
    current = st.session_state.quest_index

    for step in range(1, len(quests) + 1):
        index = (current + step) % len(quests)

        if quests[index] not in st.session_state.completed_quests:
            return index

    return (current + 1) % len(quests)

if "quest_index" not in st.session_state:
    st.session_state.quest_index = 0

quest = quests[st.session_state.quest_index]

if "last_verdict" not in st.session_state:
    st.session_state.last_verdict = None

if "quest_completed" not in st.session_state:
    st.session_state.quest_completed = False

if "xp" not in st.session_state or "completed_quests" not in st.session_state:
    saved_xp, saved_quests = load_progress()
    st.session_state.xp = saved_xp
    st.session_state.completed_quests = saved_quests

xp = st.session_state.xp

if xp < 300:
    level = "🌱 Explorer"
    progress = xp / 300
    next_level = "🌲 Adventurer"
    xp_remaining = 300 - xp

elif xp < 700:
    level = "🌲 Adventurer"
    progress = (xp - 300) / 400
    next_level = "🏆 Legend"
    xp_remaining = 700 - xp

else:
    level = "🏆 Legend"
    progress = 1.0
    next_level = None
    xp_remaining = 0

st.metric("⭐ Total XP", xp)
st.subheader(f"🎮 Level: {level}")
st.progress(progress)

if next_level:
    st.caption(f"{xp_remaining} XP until {next_level}")
else:
    st.success("🏆 Maximum level reached!")


st.write(
    f"🏆 Completed Quests: {len(st.session_state.completed_quests)}"
)


st.markdown(
    f"""
    <div class="quest-card">
        <div class="quest-label">🎯 ACTIVE SIDE QUEST</div>
        <div class="quest-title">{quest}</div>
        <div class="quest-reward">⭐ REWARD: 100 XP</div>
    </div>
    """,
    unsafe_allow_html=True
)



if st.button("🔄 Skip Quest"):
    st.session_state.quest_index = get_next_quest_index()

    st.session_state.quest_completed = False
    st.session_state.last_verdict = None

    st.rerun()


uploaded_file = st.file_uploader(
    "📸 Upload your discovery",
    type=["jpg", "jpeg", "png", "webp"]
)

if st.button("🤖 Judge My Photo"):
    if uploaded_file is None:
        st.warning("Please upload a photo first!")
    else:
        with st.spinner("AI is examining your discovery..."):
            try:
                response = chat(
                    model="gemma3:4b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
                            You are the judge of a real-world
                            outdoor scavenger hunt.

                            QUEST: {quest}

                            Examine the attached photo carefully.

                            If it clearly satisfies the quest,
                            start your answer with PASS.
                            Otherwise, start with FAIL.

                            Explain your decision briefly.
                            End with one funny sentence.
                            Do not invent objects.
                            """,
                            "images": [uploaded_file.getvalue()]
                        }
                    ]
                )

                st.session_state.last_verdict = response.message.content

                st.subheader("⚖️ AI Verdict")
                st.write(response.message.content)

                verdict = response.message.content.strip()

                if verdict.upper().startswith("PASS"):
                    st.session_state.quest_completed = True
                    if quest not in st.session_state.completed_quests:
                        save_completed_quest(quest)

                        saved_xp, saved_quests = load_progress()
                        st.session_state.xp = saved_xp
                        st.session_state.completed_quests = saved_quests

                        st.success("🎉 Quest completed! +100 XP")
                        st.rerun()
                    else:
                        st.info("🏅 You've already completed this quest!")

                elif verdict.upper().startswith("FAIL"):
                    st.warning("❌ Quest failed! Try another photo or skip.")

                else:
                    st.warning("⚠️ AI gave an unclear verdict. Please try again.")


                

            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.last_verdict:
    st.divider()
    st.subheader("📜 Last AI Verdict")
    st.write(st.session_state.last_verdict)


if st.session_state.quest_completed:
    if st.button("➡️ Next Quest", type="primary"):
        st.session_state.quest_index = get_next_quest_index()

        st.session_state.quest_completed = False
        st.session_state.last_verdict = None

        st.rerun()