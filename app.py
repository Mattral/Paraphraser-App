import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from PyPDF2 import PdfReader
from docx import Document
import io
import time
import textstat
from googletrans import Translator

# Ensuring that the necessary NLTK resource is downloaded
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

def paraphrase_text(input_text):
    translator = Translator()
    text_to_french = translator.translate(input_text, dest='fr').text
    text_to_german = translator.translate(text_to_french, dest='de').text
    back_to_english = translator.translate(text_to_german, dest='en').text
    return back_to_english

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
            
            # Analysis of original text
            original_analysis = analyze_text(text_input)
            st.write("Original Text Analysis:")
            st.write(f"Reading Time: {original_analysis[0]} minutes")
            st.write(f"Readability Score: {original_analysis[1]}")
            st.write(f"Lexical Diversity: {original_analysis[2]:.2f}")
            st.write(f"Number of Sentences: {original_analysis[3]}")

            # Paraphrasing using round-trip translation
            paraphrased_text = paraphrase_text(text_input)
            st.write("Paraphrased Text:")
            st.write(paraphrased_text)



            # Analysis of paraphrased text
            paraphrased_analysis = analyze_text(paraphrased_text)
            st.write("Paraphrased Text Analysis:")
            st.write(f"Reading Time: {paraphrased_analysis[0]} minutes")
            st.write(f"Readability Score: {paraphrased_analysis[1]}")
            st.write(f"Lexical Diversity: {paraphrased_analysis[2]:.2f}")
            st.write(f"Number of Sentences: {paraphrased_analysis[3]}")
        else:
            st.error("Please enter some text or upload a file to process.")

if __name__ == "__main__":
    main()
