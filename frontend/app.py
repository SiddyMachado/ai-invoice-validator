import streamlit as st

from api import upload_file

st.title("AI Document Reader")

uploaded_file = st.file_uploader(
    "Upload document",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    if st.button("Process document"):

        with st.spinner("Processing document..."):
            try:
                res = upload_file(uploaded_file)
            except Exception as e:
                st.error(f"Upload failed: {e}")
                st.stop()

        # Direct result (no polling needed)
        document_id = res["document_id"]
        result = res["result"]

        st.success("Done")
        st.write("Document ID:", document_id)
        st.json(result)