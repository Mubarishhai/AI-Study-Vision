import streamlit as st

st.set_page_config(page_title="AI StudyVision", layout="wide")

st.title("📘 AI StudyVision")
st.write("Upload an image or enter text to generate explanations, notes, and MCQs.")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "OCR", "Explanation", "MCQs", "Dashboard"])


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

    input_text = st.text_area("Enter the extracted text or your question:")

    if st.button("Generate Explanation"):
        if input_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("AI generating explanation..."):
                from ai_engine.llm_engine import ask_ai
                answer = ask_ai(
                    f"Explain this in simple words with examples:\n\n{input_text}"
                )

            st.subheader("📘 Explanation")
            st.write(answer)
# ---------------------- MCQ PAGE ----------------------
elif page == "MCQs":
    st.header("❓ MCQ Generator")

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



# ---------------------- DASHBOARD PAGE ----------------------
elif page == "Dashboard":
    st.header("📊 Progress Dashboard")
    st.write("Dashboard will show accuracy, weak topics, and daily activity soon.")


