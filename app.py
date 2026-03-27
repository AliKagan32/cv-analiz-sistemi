import streamlit as st
import pandas as pd
import PyPDF2
import re

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı CV Analiz", layout="wide")

st.title("Akıllı CV Analiz ve Puanlama Sistemi (AI Destekli)")
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

    benzerlik_tablosu = {
        "backend": ["backend", "arka uç", "arka plan"],
        "frontend": ["frontend", "ön uç", "ön yüz"],
        "veritabanı": ["veritabanı", "database", "db"],
        "bulut": ["aws", "docker", "kubernetes"],
        "liderlik": ["lider", "yönetim", "manager"]
    }

    cv_metni_kucuk = cv_metni.lower()

    agirliklar = {
        "beceri": 0.50,
        "deneyim": 0.20,
        "egitim": 0.20,
        "diger": 0.10
    }

    # Beceri Eşleşmesi (%50 ağırlıklı)
    beceri_puan = 0
    for kriter in kriterler:
        if kriter.lower() in cv_metni_kucuk:
            beceri_puan += 10
            bulunanlar.append(kriter)
        else:
            kriter_kucuk = kriter.lower()
            esitlendi = False
            if kriter_kucuk in benzerlik_tablosu:
                esdegerler = benzerlik_tablosu[kriter_kucuk]
                if any(esdeger in cv_metni_kucuk for esdeger in esdegerler):
                    beceri_puan += 8
                    bulunanlar.append(f"{kriter} (AI)")
                    esitlendi = True
            if not esitlendi:
                eksikler.append(kriter)

    max_beceri = len(kriterler) * 10 if kriterler else 1
    puan += (beceri_puan / max_beceri) * 100 * agirliklar["beceri"]

    # Deneyim Puanı (%20 ağırlıklı)
    yil_varyasyonlari = ["yıl", "yil", "year", "yıllık", "deneyim"]
    yil_bulundu = any(v in cv_metni_kucuk for v in yil_varyasyonlari)
    rakamlar = re.findall(r'\d+', cv_metni)
    yillar = [int(r) for r in rakamlar if 1 <= int(r) <= 40]
    max_yil = max(yillar) if yillar else 0

    if yil_bulundu and max_yil >= min_deneyim:
        deneyim_puan = 100
    elif yil_bulundu and max_yil > 0:
        deneyim_puan = (max_yil / min_deneyim) * 100 if min_deneyim > 0 else 50
    else:
        deneyim_puan = 0

    puan += min(deneyim_puan, 100) * agirliklar["deneyim"]

    # Eğitim Analizi (%20 ağırlıklı)
    egitim_puan = 0
    dereceler = {
        "doktora": 100,
        "phd": 100,
        "yüksek lisans": 80,
        "master": 80,
        "msc": 80,
        "lisans": 60,
        "bachelor": 60,
        "üniversite": 50,
        "university": 50,
        "önlisans": 30,
        "associate": 30,
    }

    for derece, skor in dereceler.items():
        if derece in cv_metni_kucuk:
            egitim_puan = max(egitim_puan, skor)

    puan += egitim_puan * agirliklar["egitim"]

    # Diğer (%10 sabit bonus)
    puan += 100 * agirliklar["diger"]

    toplam_puan = min(round(puan), 100)
    return toplam_puan, bulunanlar, eksikler

# Uygulama Akışı
if uploaded_file is not None:
    with st.expander("📄 PDF İçeriğini Görüntüle"):
        cv_metni = cv_metnini_oku(uploaded_file)
        st.text(cv_metni)
    st.success("✅ CV Başarıyla Yüklendi!")
    cv_metni = cv_metnini_oku(uploaded_file)

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