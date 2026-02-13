import streamlit as st
from utils.file_handler import (
    detect_file_type,
    process_csv,
    process_excel,
    process_pdf,
    process_image
)
from utils.gemini_hepler import (
    build_prompt,
    generate_text_response,
    generate_image_response
)

st.title("AI File Analyzer")

# --------------------------
# Session State
# --------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------
# Clear Chat Button
# --------------------------
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

uploaded_file = st.file_uploader(
    "Upload a file",
    type=["csv", "xlsx", "xls", "pdf", "jpg", "png"]
)

user_prompt = st.text_area("Enter your instruction")

# --------------------------
# Analyze Button
# --------------------------
if st.button("Analyze"):

    if uploaded_file is None or user_prompt.strip() == "":
        st.warning("Upload file and enter instruction")

    else:
        file_type = detect_file_type(uploaded_file)

        # Process file
        if file_type == "csv":
            extracted_content = process_csv(uploaded_file)

        elif file_type == "excel":
            extracted_content = process_excel(uploaded_file)

        elif file_type == "pdf":
            extracted_content = process_pdf(uploaded_file)

        elif file_type == "image":
            extracted_content = process_image(uploaded_file)

        else:
            st.error("Unsupported file")
            st.stop()

        # Store user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_prompt,
            "file_name": uploaded_file.name
        })

        # Gemini call
        with st.spinner("Analyzing with Gemini..."):

            if file_type == "image":
                response = generate_image_response(
                    extracted_content,
                    user_prompt
                )

            else:
                final_prompt = build_prompt(
                    extracted_content,
                    user_prompt
                )
                response = generate_text_response(final_prompt)

        # Store assistant message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "file_type": file_type,
            "image": extracted_content if file_type == "image" else None
        })

# --------------------------
# Chat Display
# --------------------------

st.subheader("Chat History")

for idx, message in enumerate(st.session_state.chat_history):

    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"**File:** {message.get('file_name','')}")
            st.markdown(message["content"])

    else:
        with st.chat_message("assistant"):

            # Show image inside chat bubble
            if message.get("image") is not None:
                st.image(message["image"], caption="Uploaded Image")

            # Markdown formatting
            st.markdown(message["content"])

            # Download button for each response
            st.download_button(
                label="Download Response",
                data=message["content"],
                file_name=f"response_{idx}.txt",
                mime="text/plain",
                key=f"download_{idx}"
            )
