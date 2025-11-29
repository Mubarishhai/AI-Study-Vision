
#    author  :  Shaikh Mubarish Maheboob

import streamlit as st

st.set_page_config(page_title="AI StudyVision", layout="wide")

st.title("📘 AI StudyVision")
st.write("Upload an image or enter text to generate explanations, notes, and MCQs.")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "OCR", "Explanation", "MCQs", "Notes", "Dashboard"])



# ---------------------- HOME PAGE ----------------------
if page == "Home":
    st.header("Welcome to AI StudyVision")
    st.write("This AI tool helps you learn faster using OCR + AI + MCQs.")


# ---------------------- OCR PAGE ----------------------
elif page == "OCR":
    st.header("📷 OCR - Image to Text")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        import ocr_engine.ocr as ocr

        if st.button("Extract Text"):
            with st.spinner("Extracting text..."):
                text = ocr.extract_text_from_image(uploaded_image)

            st.subheader("📝 Extracted Text")
            st.write(text)


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

# ---------------------- MCQ PAGE ----------------------
elif page == "MCQs":
    st.header("❓ MCQ Generator")

    if "mcqs" not in st.session_state:
        st.session_state["mcqs"] = []

    mcq_text = st.text_area("Enter topic or extracted text for MCQ generation:")

    if st.button("Generate MCQs"):
        if mcq_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("AI generating MCQs..."):
                from ai_engine.llm_engine import generate_mcqs
                mcqs_output = generate_mcqs(mcq_text)

            st.subheader("Generated MCQs")
            st.write(mcqs_output)

            st.session_state["mcqs"].append(
                {"text": mcq_text, "mcqs": mcqs_output}
            )




# ---------------------- DASHBOARD PAGE ----------------------
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






elif page == "Dashboard":
    st.header("📊 Progress Dashboard")

    explanations = st.session_state.get("explanations", [])
    mcqs_history = st.session_state.get("mcqs", [])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Total Explanations")
        st.metric("Count", len(explanations))

    with col2:
        st.subheader("❓ MCQ Sessions")
        st.metric("Count", len(mcqs_history))

    st.markdown("---")

    st.subheader("Recent Explanations")
    if explanations:
        for item in explanations[-3:][::-1]:
            st.markdown(f"**Q:** {item['text']}")
            st.markdown(f"**Ans (short):** {item['answer'][:200]}...")
            st.markdown("---")
    else:
        st.write("No explanations generated yet.")

    st.subheader("Recent MCQ Generations")
    if mcqs_history:
        for item in mcqs_history[-3:][::-1]:
            st.markdown(f"**Topic:** {item['text']}")
            st.markdown(f"**Preview:** {item['mcqs'][:200]}...")
            st.markdown("---")
    else:
        st.write("No MCQs generated yet.")



