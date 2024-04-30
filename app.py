import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from PyPDF2 import PdfReader
from docx import Document
import io
import time
import textstat

nltk.download('punkt')

# Function to read PDF file
def read_pdf(file):
    pdf_reader = PdfReader(file)
    full_text = []
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text.append(page_text)
    return "\n".join(full_text)

# Function to read DOCX file
def read_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def analyze_text(text):
    reading_time = textstat.reading_time(text)
    readability_score = textstat.flesch_reading_ease(text)
    tokens = word_tokenize(text)
    lexical_diversity = len(set(tokens)) / len(tokens) if tokens else 0
    number_of_sentences = textstat.sentence_count(text)
    return reading_time, readability_score, lexical_diversity, number_of_sentences

def main():
    st.title("Text Paraphrasing and Analysis Tool")

    text_input = st.text_area("Type or paste your text here:", height=200)
    file = st.file_uploader("Or upload your text file, DOCX, or PDF", type=["txt", "docx", "pdf"])

    if file:
        if file.type == "application/pdf":
            text_input = read_pdf(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text_input = read_docx(file)
        elif file.type == "text/plain":
            text_input = str(file.read(), "utf-8")
        
    if st.button("Process Text"):
        if text_input:
            st.write("Original Text:")
            st.write(text_input)

            # Paraphrasing (simple round-trip translation example, replace with a real model in production)
            # This part should be replaced with a real NLP model for paraphrasing
            translated_text = text_input[::-1]  # Dummy reverse to simulate change
            st.write("Paraphrased Text:")
            st.write(translated_text)

            # Analysis of original text
            original_analysis = analyze_text(text_input)
            st.write("Original Text Analysis:")
            st.write(f"Reading Time: {original_analysis[0]} minutes")
            st.write(f"Readability Score: {original_analysis[1]}")
            st.write(f"Lexical Diversity: {original_analysis[2]:.2f}")
            st.write(f"Number of Sentences: {original_analysis[3]}")

            # Analysis of paraphrased text
            paraphrased_analysis = analyze_text(translated_text)
            st.write("Paraphrased Text Analysis:")
            st.write(f"Reading Time: {paraphrased_analysis[0]} minutes")
            st.write(f"Readability Score: {paraphrased_analysis[1]}")
            st.write(f"Lexical Diversity: {paraphrased_analysis[2]:.2f}")
            st.write(f"Number of Sentences: {paraphrased_analysis[3]}")
        else:
            st.error("Please enter some text or upload a file to process.")

if __name__ == "__main__":
    main()
