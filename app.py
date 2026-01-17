# import streamlit as st
# import pickle
# import re
# import nltk
# import docx2txt
# import PyPDF2

# nltk.download('punkt')
# nltk.download('stopwords')

# # ✅ Load model & vectorizer
# clf = pickle.load(open('clf.pkl', 'rb'))
# tfidf = pickle.load(open('tfidf.pkl', 'rb'))

# # ✅ Clean resume text
# def clean_resume(text):
#     text = re.sub(r'http\S+', '', text)
#     text = re.sub(r'\W', ' ', text)
#     text = text.lower()
#     return text

# # ✅ Extract text from different file types
# def extract_text(file, file_type):
#     if file_type == "pdf":
#         pdf_reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ""
#         return text
#     elif file_type == "docx":
#         return docx2txt.process(file)
#     elif file_type == "txt":
#         return file.read().decode("utf-8", errors="ignore")
#     return ""

# # ✅ Main app
# def main():
#     st.title("Resume Screening Application")
#     uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
    
#     if uploaded_file is not None:
#         file_type = uploaded_file.name.split(".")[-1]
#         resume_text = extract_text(uploaded_file, file_type)
        
#         st.subheader("Extracted Resume Text:")
#         st.write(resume_text)
        
#         if resume_text.strip() != "":
#             cleaned = clean_resume(resume_text)
#             vector_input = tfidf.transform([cleaned])
#             result = clf.predict(vector_input)[0]
#             st.success(f"✅ Predicted Resume Category: **{result}**")

# if __name__ == '__main__':
#     main()
