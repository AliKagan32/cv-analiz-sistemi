import streamlit as st
import PyPDF2
import re

st.set_page_config(layout="wide")
st.title("🤖 CV Analiz AI - Reis Edition")

st.sidebar.header("🎯 Kriterler")
kriterler = st.sidebar.multiselect("Yetenekler", 
    ["Python","Java","SQL","React","AWS","Docker","Liderlik"], 
    ["Python","SQL"])

cv_file = st.file_uploader("📄 CV PDF Yükle", ["pdf"])

def pdf_oku(pdf):
    try:
        reader = PyPDF2.PdfReader(pdf)
        return "".join(p.extract_text() for p in reader.pages)
    except:
        return ""

if cv_file:
    metin = pdf_oku(cv_file).lower()
    
    st.success("✅ CV Yüklendi!")
    st.text(metin[:300]+"...")
    
    # AI Matching
    ai_map = {
        "backend":["python","java","django"],
        "frontend":["react","javascript","vue"],
        "db":["sql","mysql","postgresql"],
        "cloud":["aws","docker","k8s"]
    }
    
    eslesen = []
    ai_eslesen