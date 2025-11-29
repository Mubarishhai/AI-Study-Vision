
#    author  :  Shaikh Mubarish Maheboob


import streamlit as st
from db.db_helper import init_db, save_explanation, save_quiz_result
init_db()


st.set_page_config(page_title="AI StudyVision", layout="wide")
st.markdown("""
    <style>
        .main {
            background-color: #111827;
            color: white;
        }
        .css-1d391kg {
            background-color: #111827 !important;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
        }
        .stTextInput>div>div>input {
            background-color: #1f2937;
            color: white;
            border-radius: 6px;
        }
        .stTextArea>div>textarea {
            background-color: #1f2937;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


from PIL import Image

logo = Image.open("assets/logo.png")
st.image(logo, width=120)

st.markdown("""
<h1 style='color:white;'>AI StudyVision</h1>
<p style='color:#cbd5e1;'>Your Personal AI Study Assistant</p>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: linear-gradient(90deg, #2563eb, #1e40af);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;">
    <h2 style="color:white;">🚀 AI StudyVision – Your Personal Study Assistant</h2>
    <p style="color:white; font-size:16px;">OCR • Explanation • Notes • MCQs • Chat • Dashboard</p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0f172a;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.write("Upload an image or enter text to generate explanations, notes, and MCQs.")

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", width=80)
    st.markdown("### **AI StudyVision**")

page = st.sidebar.radio(
    "Go to",
    ["Home", "OCR", "Explanation", "MCQs", "Notes", "Chat", "Dashboard"]
)




# ---------------------- HOME PAGE ----------------------
if page == "Home":
    st.header("Welcome to AI StudyVision")
    st.write("This AI tool helps you learn faster using OCR + AI + MCQs.")


# ---------------------- OCR PAGE ----------------------
elif page == "OCR":
    st.header("📷 OCR - Image to Text")

    # ---------------- IMAGE UPLOAD ----------------
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        import ocr_engine.ocr as ocr

        if st.button("Extract Text from Image"):
            with st.spinner("Extracting text..."):
                text = ocr.extract_text_from_image(uploaded_image)

            st.subheader("📝 Extracted Image Text")
            st.write(text)

            st.session_state["ocr_text"] = text

    st.markdown("---")

    # ---------------- PDF UPLOAD ----------------
    st.subheader("📄 PDF Upload")

    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_pdf is not None:
        import pdfplumber

        with st.spinner("Extracting text from PDF..."):
            pdf_text = ""

            with pdfplumber.open(uploaded_pdf) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += page_text + "\n"

        st.subheader("📝 Extracted PDF Text")
        st.write(pdf_text)

        st.session_state["pdf_text"] = pdf_text

# ---------------------- EXPLANATION PAGE ----------------------
elif page == "Explanation":

    st.header("🧠 AI Explanation")

    # session_state me history list bana lo
    if "explanations" not in st.session_state:
        st.session_state["explanations"] = []

    input_text = st.text_area("Enter the extracted text or your question:")

    if st.button("Generate Explanation"):
        if input_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("AI generating explanation..."):
                from ai_engine.llm_engine import ask_ai
                answer = ask_ai(
                    f"Explain this in simple words with an example:\n\n{input_text}"
                )

            st.subheader("📘 Explanation")
            st.write(answer)

            # dashboard ke liye history save
            st.session_state["explanations"].append(
                {"text": input_text, "answer": answer}
            )
            save_explanation(input_text, answer)


# ---------------------- MCQ PAGE ----------------------
elif page == "MCQs":
    st.header("❓ MCQ Quiz Mode")

    mcq_text = st.text_area("Enter topic or text for MCQ quiz:")

    if st.button("Generate MCQs"):
        if mcq_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("AI generating MCQs..."):
                from ai_engine.llm_engine import generate_mcqs

                mcqs_list = generate_mcqs(mcq_text)

            if not mcqs_list:
                st.error("Error: Could not generate MCQs.")
            else:
                st.success("MCQs generated!")

                st.session_state["mcqs_saved"] = mcqs_list

    # QUIZ section
    mcqs_list = st.session_state.get("mcqs_saved", [])

    if mcqs_list:
        st.markdown("### 📝 Quiz")

        for i, q in enumerate(mcqs_list):
            st.write(f"**Q{i + 1}. {q['question']}**")
            st.radio(
                f"Select Option for Q{i + 1}:",
                q["options"],
                key=f"mcq_{i}"
            )
            st.write("---")

        if st.button("Check Score"):
            score = 0
            total = len(mcqs_list)

            for i, q in enumerate(mcqs_list):
                correct = q["options"][q["correct_index"]]
                selected = st.session_state.get(f"mcq_{i}", "")

                if selected == correct:
                    score += 1

            st.success(f"Your Score: {score}/{total}")
            save_quiz_result(mcq_text, score, total)



# ---------------------- DASHBOARD PAGE ----------------------
elif page == "Chat":
    st.header("💬 AI Chat Mode")

    # Chat history ko session_state me store kare
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Pura chat history show karo
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")
        st.markdown("---")

    # Input box
    user_input = st.text_input("Type your question or message:")

    col1, col2 = st.columns([1, 1])
    with col1:
        send = st.button("Send")
    with col2:
        clear = st.button("Clear Chat")

    if clear:
        st.session_state["chat_history"] = []
        st.rerun()

    if send and user_input.strip() != "":
        # Pehle user ka message history me daal
        st.session_state["chat_history"].append(
            {"role": "user", "content": user_input}
        )

        with st.spinner("AI is thinking..."):
            from ai_engine.llm_engine import ask_ai
            # Chat-style prompt (optional: last few messages bhej de)
            context = ""
            for msg in st.session_state["chat_history"][-6:]:
                prefix = "User" if msg["role"] == "user" else "AI"
                context += f"{prefix}: {msg['content']}\n"

            prompt = (
                "You are a helpful study assistant. Answer clearly and briefly.\n\n"
                + context
                + "\nAI:"
            )
            ai_reply = ask_ai(prompt)

        # AI reply history me add
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": ai_reply}
        )

        st.rerun()

    #dash









elif page == "Notes":
    st.header("📝 Notes Generator")

    input_text = st.text_area("Enter text or topic for notes:")

    if st.button("Generate Notes"):
        if input_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("AI generating notes..."):
                from ai_engine.llm_engine import generate_notes
                notes = generate_notes(input_text)

            st.subheader("📒 Notes")
            st.write(notes)



#ddddddddd

elif page == "Dashboard":
    st.header("📊 Progress Dashboard")

    from db.db_helper import get_stats, get_recent_explanations, get_recent_quizzes

    explanations_count, quiz_count, avg_accuracy = get_stats()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🧠 Total Explanations")
        st.metric("Count", explanations_count)

    with col2:
        st.subheader("❓ Quiz Sessions")
        st.metric("Count", quiz_count)

    with col3:
        st.subheader("🏆 Average Accuracy")
        st.metric("Accuracy", f"{avg_accuracy * 100:.1f}%")

    st.markdown("---")

    st.subheader("📝 Recent Explanations")
    recent_expl = get_recent_explanations()
    if recent_expl:
        for q, ans, created in recent_expl:
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {ans[:200]}...")
            st.caption(f"📅 {created}")
            st.markdown("---")
    else:
        st.write("No explanations yet.")

    st.subheader("🎯 Recent Quiz Results")
    recent_quiz = get_recent_quizzes()
    if recent_quiz:
        for topic, score, total, created in recent_quiz:
            st.markdown(f"**Topic:** {topic}")
            st.markdown(f"**Score:** {score}/{total}")
            st.caption(f"📅 {created}")
            st.markdown("---")
    else:
        st.write("No quiz results saved yet.")





