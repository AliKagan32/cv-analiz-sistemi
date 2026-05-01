import streamlit as st
import PyPDF2
import re
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı CV Analiz", layout="wide")

# Session state başlat
if "aktif_kategori" not in st.session_state:
    st.session_state.aktif_kategori = None
if "aranan_kriterler" not in st.session_state:
    st.session_state.aranan_kriterler = ["Python", "SQL"]
if "min_deneyim" not in st.session_state:
    st.session_state.min_deneyim = 3
if "proje_gerekli" not in st.session_state:
    st.session_state.proje_gerekli = False
if "min_egitim" not in st.session_state:
    st.session_state.min_egitim = "Fark Etmez"
if "ortaogretim_okullar" not in st.session_state:
    st.session_state.ortaogretim_okullar = []
if "onlisans_okullar" not in st.session_state:
    st.session_state.onlisans_okullar = []
if "lisans_okullar" not in st.session_state:
    st.session_state.lisans_okullar = []
if "yukseklisans_okullar" not in st.session_state:
    st.session_state.yukseklisans_okullar = []
if "doktora_okullar" not in st.session_state:
    st.session_state.doktora_okullar = []
if "arastirma_gerekli" not in st.session_state:
    st.session_state.arastirma_gerekli = False
if "basari_gerekli" not in st.session_state:
    st.session_state.basari_gerekli = False

# Başlık
st.title("🚀 Akıllı CV Analiz ve Puanlama Sistemi")
st.markdown("CV'nizi yükleyin, kriterleri belirleyin, yapay zeka puanlasın!")
st.markdown("---")

# ─────────────────────────────────────────
# ÜST KATEGORİ BUTONLARI
# ─────────────────────────────────────────
col_b1, col_b2, col_b3 = st.columns([1, 1, 4])

with col_b1:
    if st.button("💼 İş Kriterleri", use_container_width=True,
                 type="primary" if st.session_state.aktif_kategori == "is" else "secondary"):
        st.session_state.aktif_kategori = None if st.session_state.aktif_kategori == "is" else "is"
        st.rerun()

with col_b2:
    if st.button("🎓 Eğitim Kriterleri", use_container_width=True,
                 type="primary" if st.session_state.aktif_kategori == "egitim" else "secondary"):
        st.session_state.aktif_kategori = None if st.session_state.aktif_kategori == "egitim" else "egitim"
        st.rerun()

# ─────────────────────────────────────────
# KATEGORİ PANELLERİ
# ─────────────────────────────────────────
if st.session_state.aktif_kategori == "is":
    with st.container(border=True):
        st.markdown("### 💼 İş Kriterleri")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.aranan_kriterler = st.multiselect(
                "Aranan Yetenekler",
                ["Python", "Java", "SQL", "C#", "JavaScript", "AWS", "Docker",
                 "Liderlik", "İngilizce", "React", "Node.js", "Git"],
                default=st.session_state.aranan_kriterler
            )
        with col2:
            st.session_state.min_deneyim = st.slider(
                "Minimum Deneyim (Yıl)", 0, 20, st.session_state.min_deneyim)
            st.session_state.proje_gerekli = st.toggle(
                "📁 Herhangi bir çalışmada projesi gerekli mi?",
                value=st.session_state.proje_gerekli)

elif st.session_state.aktif_kategori == "egitim":
    with st.container(border=True):
        st.markdown("### 🎓 Eğitim Kriterleri")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.min_egitim = st.radio(
                "Minimum Eğitim Seviyesi",
                ["Fark Etmez", "Ortaöğretim", "Önlisans", "Lisans", "Yüksek Lisans", "Doktora"],
                index=["Fark Etmez", "Ortaöğretim", "Önlisans", "Lisans",
                       "Yüksek Lisans", "Doktora"].index(st.session_state.min_egitim),
                horizontal=True)
            st.session_state.arastirma_gerekli = st.toggle(
                "🔬 Herhangi bir YZ araştırması ve projesi gerekli mi?",
                value=st.session_state.arastirma_gerekli)
            st.session_state.basari_gerekli = st.toggle(
                "🏆 Başarı belgesi veya diploması gerekli mi?",
                value=st.session_state.basari_gerekli)
        with col2:
            st.markdown("**🏫 Belirli Okul Seç (opsiyonel)**")
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["Ortaöğretim", "Önlisans", "Lisans", "Yüksek Lisans", "Doktora"])
            with tab1:
                st.session_state.ortaogretim_okullar = st.multiselect("", [
                    "Galatasaray Lisesi", "Robert Kolej", "Kabataş Erkek Lisesi",
                    "Ankara Fen Lisesi", "İTÜ Geliştirme Vakfı Okulları"
                ], default=st.session_state.ortaogretim_okullar, key="ort")
            with tab2:
                st.session_state.onlisans_okullar = st.multiselect("", [
                    "Boğaziçi MYO", "İTÜ MYO", "Bilgi MYO",
                    "Hacettepe MYO", "ODTÜ MYO"
                ], default=st.session_state.onlisans_okullar, key="onl")
            with tab3:
                st.session_state.lisans_okullar = st.multiselect("", [
                    "Boğaziçi Üniversitesi", "ODTÜ", "İTÜ",
                    "Hacettepe", "Bilkent", "Koç Üniversitesi", "Sabancı Üniversitesi"
                ], default=st.session_state.lisans_okullar, key="lis")
            with tab4:
                st.session_state.yukseklisans_okullar = st.multiselect("", [
                    "Boğaziçi Üniversitesi", "ODTÜ", "İTÜ",
                    "Koç Üniversitesi", "Sabancı Üniversitesi", "Bilkent"
                ], default=st.session_state.yukseklisans_okullar, key="yuk")
            with tab5:
                st.session_state.doktora_okullar = st.multiselect("", [
                    "Boğaziçi Üniversitesi", "ODTÜ", "İTÜ",
                    "Koç Üniversitesi", "Sabancı Üniversitesi", "Hacettepe"
                ], default=st.session_state.doktora_okullar, key="dok")

st.markdown("---")

# ─────────────────────────────────────────
# CV YÜKLEME
# ─────────────────────────────────────────
uploaded_file = st.file_uploader("📂 CV'nizi Yükleyin (PDF)", type=["pdf"])

def cv_metnini_oku(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except:
        return "CV okunamadı!"

def kisisel_bilgi_cikart(cv_metni):
    bilgiler = {}
    satirlar = cv_metni.split('\n')

    for satir in satirlar[:20]:
        satir = satir.strip()
        if "ad soyad" in satir.lower() and ":" in satir:
            isim = satir.split(":")[-1].strip()
            if isim:
                bilgiler["Ad Soyad"] = isim
                break

    tel = re.search(r'(\+?90[\s\-]?)?(\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2})', cv_metni)
    if tel:
        bilgiler["Telefon"] = tel.group(0).strip()

    tc = re.search(r'\b[1-9][0-9]{10}\b', cv_metni)
    if tc:
        bilgiler["TC Kimlik No"] = tc.group(0)

    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cv_metni)
    if email:
        bilgiler["E-posta"] = email.group(0)

    dogum = re.search(r'\b(\d{2}[.\/\-]\d{2}[.\/\-]\d{4})\b', cv_metni)
    if dogum:
        bilgiler["Doğum Tarihi"] = dogum.group(0)

    return bilgiler

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
        "beceri": 0.50, "deneyim": 0.15, "basari": 0.05,
        "egitim": 0.15, "arastirma": 0.05, "diger": 0.05, "proje": 0.05,
    }

    # Beceri (%50)
    beceri_puan = 0
    for kriter in kriterler:
        if re.search(r'\b' + re.escape(kriter.lower()) + r'\b', cv_metni_kucuk):
            beceri_puan += 10
            bulunanlar.append(kriter)
        else:
            kriter_kucuk = kriter.lower()
            esitlendi = False
            if kriter_kucuk in benzerlik_tablosu:
                if any(e in cv_metni_kucuk for e in benzerlik_tablosu[kriter_kucuk]):
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

    # Başarı (%5)
    if basari_gerekli:
        basari_kelimeleri = ["ödül", "odul", "award", "başarı", "basari", "sertifika",
                             "certificate", "teşvik", "tesvik", "birinci", "finalist", "diploma"]
        basari_puan = 100 if any(k in cv_metni_kucuk for k in basari_kelimeleri) else 0
    else:
        basari_puan = 100
    puan += basari_puan * agirliklar["basari"]

    # Eğitim (%15)
    derece_sirasi = {
        "Fark Etmez": 0, "Ortaöğretim": 1, "Önlisans": 2,
        "Lisans": 3, "Yüksek Lisans": 4, "Doktora": 5
    }
    derece_kelimeleri = {
        "Doktora": ["doktora", "phd", "ph.d"],
        "Yüksek Lisans": ["yüksek lisans", "master", "msc"],
        "Lisans": ["lisans", "bachelor"],
        "Önlisans": ["önlisans", "ön lisans", "associate"],
        "Ortaöğretim": ["lise", "anadolu"]
    }

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

    for derece, okullar in egitim_kriterler.items():
        for okul in okullar:
            if okul.lower() in cv_metni_kucuk:
                egitim_puan = min(egitim_puan + 10, 100)

    puan += egitim_puan * agirliklar["egitim"]

    # Araştırma (%5)
    if arastirma_gerekli:
        arastirma_kelimeleri = ["yapay zeka", "yapay zekâ", "artificial intelligence",
                                "machine learning", "deep learning", "araştırma",
                                "research", "tübitak", "tubitak", "proje", "project"]
        arastirma_puan = 100 if any(k in cv_metni_kucuk for k in arastirma_kelimeleri) else 0
    else:
        arastirma_puan = 100
    puan += arastirma_puan * agirliklar["arastirma"]

    # Diğer (%5 sabit)
    puan += 100 * agirliklar["diger"]

    # Proje (%5)
    if proje_gerekli:
        proje_kelimeleri = ["proje", "project", "geliştirme", "development",
                            "uygulama", "application", "sistem", "system", "çalışma"]
        proje_puan = 100 if any(k in cv_metni_kucuk for k in proje_kelimeleri) else 0
    else:
        proje_puan = 100
    puan += proje_puan * agirliklar["proje"]

    return min(round(puan), 100), bulunanlar, eksikler, basari_puan, arastirma_puan, proje_puan

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
        "ortaogretim": st.session_state.ortaogretim_okullar,
        "onlisans": st.session_state.onlisans_okullar,
        "lisans": st.session_state.lisans_okullar,
        "yukseklisans": st.session_state.yukseklisans_okullar,
        "doktora": st.session_state.doktora_okullar
    }

    puan, bulunanlar, eksikler, basari_puan, arastirma_puan, proje_puan = cv_analiz_et(
        cv_metni,
        st.session_state.aranan_kriterler,
        st.session_state.min_deneyim,
        st.session_state.min_egitim,
        egitim_kriterler,
        st.session_state.basari_gerekli,
        st.session_state.arastirma_gerekli,
        st.session_state.proje_gerekli
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

    if st.session_state.basari_gerekli or st.session_state.arastirma_gerekli or st.session_state.proje_gerekli:
        st.markdown("#### 📋 Ek Kategori Sonuçları")
        col4, col5, col6 = st.columns(3)
        with col4:
            if st.session_state.basari_gerekli:
                st.metric("🏆 Başarı / Diploma", "✅ Var" if basari_puan == 100 else "❌ Yok")
        with col5:
            if st.session_state.arastirma_gerekli:
                st.metric("🔬 YZ Araştırması", "✅ Var" if arastirma_puan == 100 else "❌ Yok")
        with col6:
            if st.session_state.proje_gerekli:
                st.metric("📁 Proje", "✅ Var" if proje_puan == 100 else "❌ Yok")

    if puan >= 70:
        st.success("🎉 Bu aday mülakata çağrılabilir!")
    elif puan >= 40:
        st.warning("⚠️ Aday değerlendirilebilir, ek mülakat önerilir.")
    else:
        st.error("❌ Aday kriterlere uygun değil.")

    # ─────────────────────────────────────────
    # NOT ALMA BÖLÜMÜ
    # ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📝 Aday Notu")

    # Kişisel bilgileri çıkart
    kisisel = kisisel_bilgi_cikart(cv_metni)
    aday_adi = kisisel.get("Ad Soyad", "Bilinmiyor")

    # Kişisel bilgileri düzenli göster
    with st.container(border=True):
        st.markdown("**📋 CV'den Algılanan Bilgiler**")
        if kisisel:
            cols = st.columns(len(kisisel))
            for i, (anahtar, deger) in enumerate(kisisel.items()):
                cols[i].markdown(f"**{anahtar}**  \n{deger}")
        else:
            st.info("CV'den kişisel bilgi algılanamadı.")

    # Not alanı — session state ile anında kaydedilir
    if "not_metni" not in st.session_state:
        st.session_state.not_metni = ""

    st.session_state.not_metni = st.text_area(
        "Adaya dair notlarınızı buraya yazın (otomatik kaydedilir):",
        value=st.session_state.not_metni,
        placeholder="Örn: Mülakat için uygun, deneyimi yeterli ancak Python bilgisi zayıf...",
        height=150
    )

    # TXT içeriği oluştur
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
    dosya_tarih = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
    dosya_adi = f"{aday_adi.replace(' ', '_')}_{dosya_tarih}.txt"

    txt_icerik  = "============================================================\n"
    txt_icerik += "           ADAY DEGERLENDİRME NOTU\n"
    txt_icerik += f"           Tarih: {tarih}\n"
    txt_icerik += "============================================================\n\n"

    txt_icerik += "--- KİSİSEL BİLGİLER ---\n"
    for anahtar, deger in kisisel.items():
        txt_icerik += f"  {anahtar:15}: {deger}\n"

    txt_icerik += "\n--- ANALİZ SONUÇLARI ---\n"
    txt_icerik += f"  Uyumluluk Puani   : {puan}/100\n"
    txt_icerik += f"  Bulunan Yetenekler: {', '.join(bulunanlar) if bulunanlar else 'Yok'}\n"
    txt_icerik += f"  Eksik Yetenekler  : {', '.join(eksikler) if eksikler else 'Yok'}\n"

    txt_icerik += "\n--- DEGERLENDİRME ---\n"
    txt_icerik += ("  >> Mulakata cagrilabilir\n" if puan >= 70 else
                   "  >> Degerlendirilebilir, ek mulakat onerilir\n" if puan >= 40 else
                   "  >> Kriterlere uygun degil\n")

    txt_icerik += "\n" + "=" * 60 + "\n"
    txt_icerik += "                        N O T\n"
    txt_icerik += "=" * 60 + "\n\n"
    txt_icerik += (st.session_state.not_metni if st.session_state.not_metni.strip() else "(Not girilmedi)")
    txt_icerik += "\n\n" + "=" * 60 + "\n"

    st.download_button(
        label="💾 Notu TXT Olarak İndir",
        data=txt_icerik.encode("utf-8"),
        file_name=dosya_adi,
        mime="text/plain"
    )

else:
    st.info("👆 Önce kriterleri belirleyin, ardından CV yükleyin!")

st.markdown("---")
