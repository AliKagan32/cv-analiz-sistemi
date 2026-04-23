import streamlit as st
import PyPDF2
import re

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı CV Analiz", layout="wide")

st.title("Akıllı CV Analiz ve Puanlama Sistemi (AI Destekli)")
st.markdown("CV'nizi yükleyin, yapay zeka puanlasın!")

# ─────────────────────────────────────────
# 💼 İŞ KRİTERLERİ
# ─────────────────────────────────────────
st.sidebar.header("💼 İş Kriterleri")

aranan_kriterler = st.sidebar.multiselect(
    "Aranan Yetenekler",
    ["Python", "Java", "SQL", "C#", "JavaScript", "AWS", "Docker",
     "Liderlik", "İngilizce", "React", "Node.js", "Git"],
    default=["Python", "SQL"]
)

min_deneyim = st.sidebar.slider("Minimum Deneyim (Yıl)", 0, 20, 3)

proje_gerekli = st.sidebar.toggle("📁 Herhangi bir çalışmada projesi gerekli mi?", value=False)

# ─────────────────────────────────────────
# 🎓 EĞİTİM & ARAŞTIRMA KRİTERLERİ
# ─────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.header("🎓 Eğitim & Araştırma")

# Minimum eğitim seviyesi
min_egitim = st.sidebar.radio(
    "Minimum Eğitim Seviyesi",
    ["Fark Etmez", "Ortaöğretim", "Önlisans", "Lisans", "Yüksek Lisans", "Doktora"]
)

# Okul seçimi tek expander içinde
with st.sidebar.expander("🏫 Belirli Okul Seç (opsiyonel)"):
    st.markdown("**Ortaöğretim**")
    ortaogretim_okullar = st.multiselect("", [
        "Galatasaray Lisesi", "Robert Kolej", "Kabataş Erkek Lisesi",
        "Ankara Fen Lisesi", "İTÜ Geliştirme Vakfı Okulları"
    ], key="ortaogretim")

    st.markdown("**Önlisans**")
    onlisans_okullar = st.multiselect("", [
        "Boğaziçi MYO", "İTÜ MYO", "Bilgi MYO",
        "Hacettepe MYO", "ODTÜ MYO"
    ], key="onlisans")

    st.markdown("**Lisans**")
    lisans_okullar = st.multiselect("", [
        "Boğaziçi Üniversitesi", "ODTÜ", "İTÜ",
        "Hacettepe", "Bilkent", "Koç Üniversitesi", "Sabancı Üniversitesi"
    ], key="lisans")

    st.markdown("**Yüksek Lisans**")
    yukseklisans_okullar = st.multiselect("", [
        "Boğaziçi Üniversitesi", "ODTÜ", "İTÜ",
        "Koç Üniversitesi", "Sabancı Üniversitesi", "Bilkent"
    ], key="yukseklisans")

    st.markdown("**Doktora**")
    doktora_okullar = st.multiselect("", [
        "Boğaziçi Üniversitesi", "ODTÜ", "İTÜ",
        "Koç Üniversitesi", "Sabancı Üniversitesi", "Hacettepe"
    ], key="doktora")

arastirma_gerekli = st.sidebar.toggle("🔬 Herhangi bir YZ araştırması ve projesi gerekli mi?", value=False)
basari_gerekli = st.sidebar.toggle("🏆 Başarı belgesi veya diploması gerekli mi?", value=False)

# ─────────────────────────────────────────
# CV YÜKLEME
# ─────────────────────────────────────────
uploaded_file = st.file_uploader("CV'nizi Yükleyin (PDF)", type=["pdf"])

# CV Okuma
def cv_metnini_oku(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except:
        return "CV okunamadı!"

# Analiz Fonksiyonu
def cv_analiz_et(cv_metni, kriterler, min_deneyim, min_egitim, egitim_kriterler,
                 basari_gerekli, arastirma_gerekli, proje_gerekli):
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
        "deneyim": 0.15,
        "basari": 0.05,
        "egitim": 0.15,
        "arastirma": 0.05,
        "diger": 0.05,
        "proje": 0.05,
    }

    # Beceri Eşleşmesi (%50)
    beceri_puan = 0
    for kriter in kriterler:
        if re.search(r'\b' + re.escape(kriter.lower()) + r'\b', cv_metni_kucuk):
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

    # Deneyim (%15)
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

    # Başarı Belgesi (%5)
    if basari_gerekli:
        basari_kelimeleri = ["ödül", "odul", "award", "başarı", "basari", "sertifika",
                             "certificate", "teşvik", "tesvik", "birinci", "finalist",
                             "diploma", "derece"]
        basari_var = any(k in cv_metni_kucuk for k in basari_kelimeleri)
        basari_puan = 100 if basari_var else 0
    else:
        basari_puan = 100
    puan += basari_puan * agirliklar["basari"]

    # Eğitim (%15) - Hem min seviye hem okul
    egitim_puan = 0

    derece_sirasi = {
        "Fark Etmez": 0,
        "Ortaöğretim": 1,
        "Önlisans": 2,
        "Lisans": 3,
        "Yüksek Lisans": 4,
        "Doktora": 5
    }

    derece_kelimeleri = {
        "Doktora": ["doktora", "phd", "ph.d"],
        "Yüksek Lisans": ["yüksek lisans", "master", "msc", "m.sc"],
        "Lisans": ["lisans", "bachelor", "b.sc"],
        "Önlisans": ["önlisans", "ön lisans", "associate"],
        "Ortaöğretim": ["lise", "anadolu", "meslek lisesi"]
    }

    # CV'deki en yüksek dereceyi bul
    cv_derece_sirasi = 0
    for derece, kelimeler in derece_kelimeleri.items():
        if any(k in cv_metni_kucuk for k in kelimeler):
            if derece_sirasi[derece] > cv_derece_sirasi:
                cv_derece_sirasi = derece_sirasi[derece]

    min_derece_sirasi = derece_sirasi[min_egitim]

    if min_egitim == "Fark Etmez":
        egitim_puan = 100
    elif cv_derece_sirasi >= min_derece_sirasi:
        egitim_puan = 100
    else:
        egitim_puan = (cv_derece_sirasi / min_derece_sirasi) * 100 if min_derece_sirasi > 0 else 0

    # Belirli okul seçildiyse bonus
    derece_okul_puanlar = {
        "ortaogretim": 20, "onlisans": 40, "lisans": 60,
        "yukseklisans": 80, "doktora": 100
    }
    for derece, okullar in egitim_kriterler.items():
        for okul in okullar:
            if okul.lower() in cv_metni_kucuk:
                egitim_puan = min(egitim_puan + 10, 100)

    puan += egitim_puan * agirliklar["egitim"]

    # Araştırma (%5)
    if arastirma_gerekli:
        arastirma_kelimeleri = ["yapay zeka", "yapay zekâ", "artificial intelligence",
                                "machine learning", "makine öğrenmesi", "deep learning",
                                "derin öğrenme", "araştırma", "arastirma", "research",
                                "tübitak", "tubitak", "proje", "project"]
        arastirma_var = any(k in cv_metni_kucuk for k in arastirma_kelimeleri)
        arastirma_puan = 100 if arastirma_var else 0
    else:
        arastirma_puan = 100
    puan += arastirma_puan * agirliklar["arastirma"]

    # Diğer (%5 sabit)
    puan += 100 * agirliklar["diger"]

    # Proje (%5)
    if proje_gerekli:
        proje_kelimeleri = ["proje", "project", "geliştirme", "gelistirme",
                            "development", "uygulama", "application", "sistem", "system",
                            "çalışma", "calisma"]
        proje_var = any(k in cv_metni_kucuk for k in proje_kelimeleri)
        proje_puan = 100 if proje_var else 0
    else:
        proje_puan = 100
    puan += proje_puan * agirliklar["proje"]

    toplam_puan = min(round(puan), 100)
    return toplam_puan, bulunanlar, eksikler, basari_puan, arastirma_puan, proje_puan

# ─────────────────────────────────────────
# UYGULAMA AKIŞI
# ─────────────────────────────────────────
if uploaded_file is not None:
    with st.expander("📄 PDF İçeriğini Görüntüle"):
        cv_metni = cv_metnini_oku(uploaded_file)
        st.text(cv_metni)
    st.success("✅ CV Başarıyla Yüklendi!")
    cv_metni = cv_metnini_oku(uploaded_file)

    egitim_kriterler = {
        "ortaogretim": ortaogretim_okullar,
        "onlisans": onlisans_okullar,
        "lisans": lisans_okullar,
        "yukseklisans": yukseklisans_okullar,
        "doktora": doktora_okullar
    }

    puan, bulunanlar, eksikler, basari_puan, arastirma_puan, proje_puan = cv_analiz_et(
        cv_metni, aranan_kriterler, min_deneyim, min_egitim, egitim_kriterler,
        basari_gerekli, arastirma_gerekli, proje_gerekli
    )

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

    if basari_gerekli or arastirma_gerekli or proje_gerekli:
        st.markdown("#### 📋 Ek Kategori Sonuçları")
        col4, col5, col6 = st.columns(3)
        with col4:
            if basari_gerekli:
                st.metric("🏆 Başarı / Diploma", "✅ Var" if basari_puan == 100 else "❌ Yok")
        with col5:
            if arastirma_gerekli:
                st.metric("🔬 YZ Araştırması", "✅ Var" if arastirma_puan == 100 else "❌ Yok")
        with col6:
            if proje_gerekli:
                st.metric("📁 Proje", "✅ Var" if proje_puan == 100 else "❌ Yok")

    if puan >= 70:
        st.success("🎉 Bu aday mülakata çağrılabilir!")
    elif puan >= 40:
        st.warning("⚠️ Aday değerlendirilebilir, ek mülakat önerilir.")
    else:
        st.error("❌ Aday kriterlere uygun değil.")
else:
    st.info("👈 Sol menüden kriterleri seçin ve CV yükleyin!")

st.markdown("---")
