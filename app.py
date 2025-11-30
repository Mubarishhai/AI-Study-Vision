#    author  :  Shaikh Mubarish Maheboob

import streamlit as st
from PIL import Image

# DB functions
from db.db_helper import (
    init_db,
    save_explanation,
    save_quiz_result,
    get_stats,
    get_recent_explanations,
    get_recent_quizzes,
)

# init database tables
init_db()

st.set_page_config(page_title="AI StudyVision", layout="wide")

# ---------------- GLOBAL UI STYLING ----------------
st.markdown("""
    <style>
        .main { background-color: #111827; color: white; }
        [data-testid="stSidebar"] { background-color: #0f172a; }
        [data-testid="stSidebar"] * { color: white !important; }
        .stButton>button {
            background-color: #2563eb; color: white;
            border-radius: 8px; padding: 8px 16px;
        }
        .stTextArea>div>textarea, .stTextInput>div>div>input {
            background-color: #1f2937; color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER + LOGO ----------------
logo = Image.open("assets/logo.png.png")   # same naam use kar raha jo tere project me hai
st.image(logo, width=120)

st.markdown("""
<h1 style='color:white;'>AI StudyVision</h1>
<p style='color:#cbd5e1;'>Your Personal AI Study Assistant</p>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(90deg, #2563eb, #1e40af);
padding: 20px; border-radius: 12px; margin-bottom: 20px;">
<h2 style="color:white;">🚀 AI StudyVision – Your Personal Study Assistant</h2>
<p style="color:white;">OCR • Explanation • Notes • MCQs • Chat • Voice • PPT • Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("assets/logo.png.png", width=80)
    st.markdown("### AI StudyVision")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "OCR",
        "Explanation",
        "MCQs",
        "Notes",
        "Chat",
        "Auto Study Mode",
        "Mind Map",
        "PPT Generator",
        "Doubt Scanner",
        "PDF Highlighter",
        "Dashboard",
    ]
)

# =================== PAGES START ===================

# ---------------- HOME ----------------
if page == "Home":
    st.header("Welcome to AI StudyVision")
    st.write("This AI tool helps you learn faster using OCR + AI + Notes + MCQs + Voice + Dashboard.")


# ---------------- OCR ----------------
elif page == "OCR":
    st.header("📷 OCR - Image / PDF to Text")

    # IMAGE OCR
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, use_container_width=True)

        import ocr_engine.ocr as ocr

        if st.button("Extract Text from Image"):
            with st.spinner("Extracting text from image..."):
                text = ocr.extract_text_from_image(uploaded_image)

            st.subheader("📝 Extracted Image Text")
            st.write(text)
            st.session_state["ocr_text"] = text

    st.markdown("---")

    # PDF OCR
    st.subheader("📄 PDF Upload")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        import pdfplumber
        with st.spinner("Extracting text from PDF..."):
            pdf_text = ""
            with pdfplumber.open(uploaded_pdf) as pdf:
                for p in pdf.pages:
                    t = p.extract_text()
                    if t:
                        pdf_text += t + "\n"

        st.subheader("📝 Extracted PDF Text")
        st.write(pdf_text)
        st.session_state["pdf_text"] = pdf_text


# ---------------- EXPLANATION ----------------
elif page == "Explanation":
    st.header("🧠 AI Explanation")

    if "explanations" not in st.session_state:
        st.session_state["explanations"] = []

    input_text = st.text_area("Enter text or question:")

    if st.button("Generate Explanation"):
        if not input_text.strip():
            st.warning("Please enter some text first.")
        else:
            from ai_engine.llm_engine import ask_ai

            with st.spinner("AI generating explanation..."):
                answer = ask_ai(
                    f"Explain this in very simple language, with small examples:\n\n{input_text}"
                )

            st.subheader("📘 Explanation")
            st.write(answer)

            st.session_state["explanations"].append(
                {"text": input_text, "answer": answer}
            )
            save_explanation(input_text, answer)


# ---------------- MCQs ----------------
elif page == "MCQs":
    st.header("❓ MCQ Quiz Mode")

    mcq_text = st.text_area("Enter text/topic for MCQs:")

    if st.button("Generate MCQs"):
        if not mcq_text.strip():
            st.warning("Please enter some text first.")
        else:
            from ai_engine.llm_engine import generate_mcqs

            with st.spinner("AI generating MCQs..."):
                mcqs = generate_mcqs(mcq_text)

            st.session_state["mcqs_saved"] = mcqs
            st.success("MCQs generated!")

    mcqs = st.session_state.get("mcqs_saved", [])

    if mcqs:
        st.markdown("### 📝 Quiz")

        for i, q in enumerate(mcqs):
            st.write(f"**Q{i+1}. {q['question']}**")
            st.radio(
                f"Select Option for Q{i+1}:",
                q["options"],
                key=f"mcq_{i}"
            )
            st.write("---")

        if st.button("Check Score"):
            score = 0
            for i, q in enumerate(mcqs):
                selected = st.session_state.get(f"mcq_{i}")
                if selected == q["options"][q["correct_index"]]:
                    score += 1

            st.success(f"Your Score: {score}/{len(mcqs)}")
            save_quiz_result(mcq_text, score, len(mcqs))


# ---------------- NOTES ----------------
elif page == "Notes":
    st.header("📝 Notes Generator")

    text = st.text_area("Enter text or topic for notes:")

    if st.button("Generate Notes"):
        if not text.strip():
            st.warning("Please enter some text first.")
        else:
            from ai_engine.llm_engine import generate_notes

            with st.spinner("AI generating notes..."):
                notes = generate_notes(text)

            st.subheader("📒 Notes")
            st.write(notes)


# ---------------- CHAT (VOICE) ----------------
elif page == "Chat":
    st.header("💬 AI Chat (with Voice Reply)")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "last_ai_audio" not in st.session_state:
        st.session_state["last_ai_audio"] = None

    for msg in st.session_state["chat_history"]:
        role = "You" if msg["role"] == "user" else "AI"
        st.markdown(f"**{role}:** {msg['content']}")
        st.markdown("---")

    user_input = st.text_input("Type your message:")

    col1, col2 = st.columns(2)

    if col1.button("Send"):
        if user_input.strip():
            st.session_state["chat_history"].append(
                {"role": "user", "content": user_input}
            )

            from ai_engine.llm_engine import ask_ai
            from voice.voice_engine import text_to_speech_bytes

            with st.spinner("AI thinking..."):
                context = ""
                for msg in st.session_state["chat_history"][-6:]:
                    prefix = "User" if msg["role"] == "user" else "AI"
                    context += f"{prefix}: {msg['content']}\n"

                prompt = "You are a helpful study assistant.\n" + context + "\nAI:"
                reply = ask_ai(prompt)

                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": reply}
                )

                st.session_state["last_ai_audio"] = text_to_speech_bytes(reply)

        st.rerun()

    if col2.button("Clear Chat"):
        st.session_state["chat_history"] = []
        st.session_state["last_ai_audio"] = None
        st.rerun()

    if st.session_state["last_ai_audio"]:
        st.subheader("🔊 Listen to AI Reply")
        st.audio(st.session_state["last_ai_audio"], format="audio/mp3")


# ---------------- AUTO STUDY MODE ----------------
elif page == "Auto Study Mode":
    st.header("⚡ One-Click Auto Study Mode")

    pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf:
        import pdfplumber

        with st.spinner("Extracting text from PDF..."):
            text = ""
            with pdfplumber.open(pdf) as p:
                for pg in p.pages:
                    t = pg.extract_text()
                    if t:
                        text += t + "\n"

        st.success("PDF Extracted!")

        if st.button("✨ Generate Explanation + Notes + MCQs"):
            from ai_engine.llm_engine import ask_ai

            with st.spinner("AI generating everything..."):
                explanation = ask_ai("Explain this in simple language:\n" + text)
                notes = ask_ai("Make short bullet notes:\n" + text)
                mcqs = ask_ai("Generate 5 MCQs with answers:\n" + text)

            st.subheader("📘 Explanation")
            st.write(explanation)

            st.subheader("📒 Notes")
            st.write(notes)

            st.subheader("❓ MCQs")
            st.write(mcqs)


# ---------------- MIND MAP ----------------
elif page == "Mind Map":
    st.header("🌳 AI Mind Map Generator")

    txt = st.text_area("Enter content for mind map:")

    if st.button("Generate Mind Map"):
        if not txt.strip():
            st.warning("Please enter some text first.")
        else:
            from ai_engine.llm_engine import ask_ai

            with st.spinner("Creating mind map..."):
                prompt = f"""
Convert the following text into a hierarchical mind map using tree structure:

Main Topic
 ├─ Subtopic 1
 │    ├─ Point A
 │    └─ Point B
 └─ Subtopic 2
      ├─ Point C
      └─ Point D

Text:
{txt}
"""
                mindmap = ask_ai(prompt)

            st.subheader("📌 Mind Map")
            st.text(mindmap)


# ---------------- PPT GENERATOR ----------------
elif page == "PPT Generator":
    st.header("📊 PPT Auto Generator")

    text = st.text_area("Paste your topic / text / notes:")

    if st.button("Generate PPT"):
        if not text.strip():
            st.warning("Please enter some text first.")
        else:
            from ai_engine.llm_engine import ask_ai
            from ppt_engine.ppt_maker import create_ppt

            with st.spinner("AI preparing PPT content..."):
                explanation = ask_ai("Explain shortly:\n" + text)
                notes = ask_ai("Make bullet notes:\n" + text)
                mcqs = ask_ai("Generate 5 MCQs:\n" + text)

            ppt_file = create_ppt(
                title="AI StudyVision – PPT",
                explanation=explanation,
                notes=notes,
                mcqs=mcqs,
            )

            st.success("PPT Created Successfully!")
            with open(ppt_file, "rb") as f:
                st.download_button(
                    "📥 Download PPT",
                    data=f,
                    file_name=ppt_file,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )


# ---------------- DOUBT SCANNER ----------------
elif page == "Doubt Scanner":
    st.header("📸 Smart Doubt Scanner (AI Solver)")

    doubt_img = st.file_uploader(
        "Upload your doubt image", type=["jpg", "jpeg", "png"]
    )

    if doubt_img:
        st.image(doubt_img, use_container_width=True)

        if st.button("🔍 Scan & Solve"):
            from doubt_scanner.scanner import scan_doubt
            from ai_engine.llm_engine import ask_ai

            with st.spinner("Reading your doubt..."):
                text = scan_doubt(doubt_img)

            st.subheader("📜 Extracted Doubt")
            st.write(text)

            with st.spinner("AI solving your doubt..."):
                solution = ask_ai(
                    f"Solve this doubt step-by-step in simple language:\n\n{text}"
                )

            st.subheader("🧠 AI Solution")
            st.write(solution)


# ---------------- PDF HIGHLIGHTER ----------------
elif page == "PDF Highlighter":
    st.header("🔦 AI PDF Highlighter")

    pdf_file = st.file_uploader("Upload PDF to highlight important lines", type=["pdf"])

    if pdf_file:
        import pdfplumber

        with st.spinner("Reading PDF..."):
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for p in pdf.pages:
                    t = p.extract_text()
                    if t:
                        text += t + "\n"

        st.subheader("📄 Extracted PDF Text")
        st.write(text)

        if st.button("✨ Highlight Important Points"):
            from ai_engine.llm_engine import ask_ai

            with st.spinner("AI analyzing importance..."):
                prompt = f"""
Highlight MOST important lines from this content.

Return output like:

🔵 Important:
- line 1
- line 2

🟡 Medium:
- line 3

🔴 Critical Definitions:
- line 4

Text:
{text}
"""
                highlighted = ask_ai(prompt)

            st.subheader("📌 Highlighted Content")
            st.markdown(highlighted)


# ---------------- DASHBOARD ----------------
elif page == "Dashboard":
    st.header("📊 Progress Dashboard")

    e_count, q_count, avg = get_stats()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Explanations", e_count)
    c2.metric("Quiz Sessions", q_count)
    c3.metric("Avg Accuracy", f"{avg * 100:.1f}%")

    st.markdown("---")

    st.subheader("📝 Recent Explanations")
    recent_expl = get_recent_explanations()
    if recent_expl:
        for q, ans, dt in recent_expl:
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A (preview):** {ans[:200]}...")
            st.caption(f"📅 {dt}")
            st.markdown("---")
    else:
        st.write("No explanations yet.")

    st.subheader("🎯 Recent Quizzes")
    recent_quiz = get_recent_quizzes()
    if recent_quiz:
        for topic, score, total, dt in recent_quiz:
            st.markdown(f"**Topic:** {topic}")
            st.markdown(f"**Score:** {score}/{total}")
            st.caption(f"📅 {dt}")
            st.markdown("---")
    else:
        st.write("No quiz results yet.")
