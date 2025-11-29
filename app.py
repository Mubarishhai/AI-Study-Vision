import streamlit as st

st.set_page_config(page_title="AI StudyVision", layout="wide")

st.title("📘 AI StudyVision")
st.write("Upload an image or enter text to generate explanations, notes, and MCQs.")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "OCR", "Explanation", "MCQs", "Dashboard"])

if page == "Home":
    st.header("Welcome to AI StudyVision")
    st.write("This AI tool helps you learn faster using OCR + AI + MCQs.")
elif page == "OCR":

    st.header("📷 OCR - Image to Text")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        import ocr_engine.ocr as ocr

        if st.button("Extract Text"):
            with st.spinner("Extracting text..."):
                text = ocr.extract_text_from_image(uploaded_image)

            st.subheader("📝 Extracted Text")
            st.write(text)

    st.header("📷 OCR - Image to Text")
elif page == "Explanation":
    st.header("🧠 AI Explanation")
elif page == "MCQs":
    st.header("❓ MCQ Generator")
elif page == "Dashboard":
    st.header("📊 Progress Dashboard")

