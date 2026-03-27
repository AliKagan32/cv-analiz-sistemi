import streamlit as st
import pandas as pd
import PyPDF2
import re

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı CV Analiz", layout="wide")

st.title("🚀 Akıllı CV Analiz ve Puanlama Sistemi (AI Destekli)")
st.markdown("CV'nizi yükleyin, yapay zeka puanlasın!")

# Şirket Kriterleri
st.sidebar.header("📋 Şirket Kriterleri")
aranan_kriterler = st.sidebar.multiselect(
    "Aranan Yetenekler",
    ["Python", "Java", "SQL", "C#", "JavaScript", "AWS", "Docker", "Liderlik", "İngilizce", "React", "Node.js", "Git"],
    default=["Python", "SQL"]
)

min_deneyim = st.sidebar.slider("Minimum Deneyim (Yıl)", 0, 20, 3)

# CV Yükleme
uploaded_file = st.file_uploader("CV'nizi Yükleyin (PDF)", type=["pdf"])

# CV Okuma Fonksiyonu
def cv_metnini_oku(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except:
        return "CV okunamadı!"

# AI Destekli Analiz Fonksiyonu
def cv_analiz_et(cv_metni, kriterler, min_deneyim):
    puan = 0
    bulunanlar = []
    eksikler = []
    
    # AI Benzerlik Tablosu
    benzerlik_tablosu = {
        "backend": ["backend", "arka uç", "arka plan"],
        "frontend": ["frontend", "ön uç", "ön yüz"],
        "veritabanı": ["veritabanı", "database", "db"],
        "bulut": ["aws", "docker", "kubernetes"],
        "liderlik": ["lider", "yönetim", "manager"]
    }
    
    cv_metni_kucuk = cv_metni.lower()
    
    # Anahtar Kelime + AI Eşleşmesi
    for kriter in kriterler:
        if kriter.lower() in cv_metni_kucuk:
            puan += 10
            bulunanlar.append(kriter)
        else:
            esitlendi = False
            for anahtar, esdegerler in benzerlik_tablosu.items():
                if anahtar in cv_metni_kucuk and any(esdeger in cv_metni_kucuk for esdeger in esdegerler):
                    puan += 8
                    bulunanlar.append(f"{kriter} (AI)")
                    esitlendi = True
                    break
            if not esitlendi:
                eksikler.append(kriter)
    
    # Geliştirilmiş Yıl Algılama
    yil_varyasyonlari = ["yıl", "yil", "year", "yıllık", "deneyim"]
    yil_bulundu = False
    
    for varyasyon in yil_varyasyonlari:
        if varyasyon in cv_metni_kucuk:
            yil_bulundu = True
            break
    
    # Rakam kontrolü (1 yıl, 3 yıl)
    rakamlar = re.findall(r'\d+', cv_metni)
    if len(rakamlar) > 0:
        yil_bulundu = True
    
    if yil_bulundu:
        puan += 15
    else:
        puan -= 5
    
    toplam_puan = min(puan, 100)
    return toplam_puan, bulunanlar, eksikler
# Uygulama Akışı
if uploaded_file is not None:
    st.success("✅ CV Başarıyla Yüklendi!")
    cv_metni = cv_metnini_oku(uploaded_file)
    
    with st.expander("CV İçeriğini Görüntüle"):
        st.text(cv_metni[:500] + "...")
        cv_metni = cv_metnini_oku(upload_file)
    # DEBUG: Yıl algılama testi
    st.markdown("### 🔍 DEBUG BİLGİLERİ")
    st.write("**CV Metni (İlk 200 karakter):**")
    st.text(cv_metni[:200] + "...")
    
    cv_metni_kucuk = cv_metni.lower()
    yil_varyasyonlari = ["yıl", "yil", "year", "yıllık", "deneyim"]
    yil_bulundu = any(varyasyon in cv_metni_kucuk for varyasyon in yil_varyasyonlari)
    
    rakamlar = re.findall(r'\d+', cv_metni)
    
    st.write(f"**Yıl kelimesi bulundu:** {yil_bulundu}")
    st.write(f"**Rakamlar bulundu:** {rakamlar}")
    st.write("---")

    puan, bulunanlar, eksikler = cv_analiz_et(cv_metni, aranan_kriterler, min_deneyim)

    st.markdown("### 📊 Analiz Sonuçları")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Uyumluluk Puanı", f"{puan}/100")
    with col2:
        st.metric("Bulunan Yetenekler", len(bulunanlar))
    with col3:
        st.metric("Eksik Yetenekler", len(eksikler))
    
    st.markdown("#### ✅ Bulunan Yetenekler")
    for yetenek in bulunanlar:
        st.write(f"✅ {yetenek}")
    
    st.markdown("#### ❌ Eksik Yetenekler")
    for yetenek in eksikler:
        st.write(f"❌ {yetenek}")
    
    if puan >= 70:
        st.success("🎉 Bu aday mülakata çağrılabilir!")
    elif puan >= 40:
        st.warning("⚠️ Aday değerlendirilebilir, ek mülakat önerilir.")
    else:
        st.error("❌ Aday kriterlere uygun değil.")
else:
    st.info("👈 Sol menüden kriterleri seçin ve CV yükleyin!")

st.markdown("---")
st.markdown("© 2024 Akıllı CV Analiz Sistemi - AI Destekli")