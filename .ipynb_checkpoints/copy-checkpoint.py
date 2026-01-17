import streamlit as st
import pickle
import re
import nltk
import docx2txt
import PyPDF2

nltk.download('punkt')
nltk.download('stopwords')

# Load model & vectorizer
clf = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))


# ------------------------
# CLEAN RESUME TEXT
# ------------------------
def cleanResume(txt):

    txt = re.sub(r"http\S+\s", " ", txt)
    txt = re.sub(r"RT|cc", " ", txt)
    txt = re.sub(r"#\S+\s", " ", txt)
    txt = re.sub(r"@\S+", " ", txt)

    # Remove special characters but keep new lines
    txt = re.sub(r"[%s]" % re.escape("""!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""), " ", txt)

    txt = re.sub(r"[^\x00-\x7f]", " ", txt)

    # Do NOT remove line breaks (formatting)
    txt = re.sub(r"[ ]{2,}", " ", txt)

    return txt


# ------------------------
# EXTRACT TEXT FROM FILE
# ------------------------
def extract_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    # PDF
    if file_name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
        return text

    # DOCX
    elif file_name.endswith(".docx"):
        return docx2txt.process(uploaded_file)

    # TXT
    else:
        try:
            return uploaded_file.read().decode("utf-8")
        except:
            return uploaded_file.read().decode("latin-1")


# ------------------------
# MAIN STREAMLIT APP
# ------------------------
def main():

    st.title("Smart Resume Screening Application ✅")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:

        resume_text = extract_text(uploaded_file)

        st.subheader("Extracted Resume Text:")
        st.text_area("Resume Content", resume_text, height=300)

        cleaned_resume = cleanResume(resume_text)

        vector_input = tfidf.transform([cleaned_resume])

        prediction_id = clf.predict(vector_input)[0]

        # CATEGORY MAPPING
        category_mapping = {
            15: "Java Developer",
            23: "Testing",
            8: "DevOps Engineer",
            20: "Python Developer",
            24: "Web Designing",
            12: "HR",
            13: "Hadoop",
            3: "Blockchain",
            10: "ETL Developer",
            18: "Operation Manager",
            6: "Data Science",
            22: "Sales",
            16: "Mechanical Engineer",
            1: "Arts",
            7: "Database",
            11: "Electrical Engineer",
            14: "Health and Fitness",
            19: "PMO",
            4: "Business Analyst",
            9: "Dotnet Developer",
            2: "Automation Testing",
            17: "Network Security Engineer",
            21: "SAP Developer",
            5: "Civil Engineer",
            0: "Advocate"
        }

        category_name = category_mapping.get(prediction_id, "Unknown")

        st.success(f"✅ Predicted Resume Category: **{category_name}**")


if __name__ == '__main__':
    main()
