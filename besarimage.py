import streamlit as str
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN STREAMLIT ---
str.set_page_config(page_title="Dropship US Spy Agent", page_icon="🥷", layout="wide")

str.title("🥷 Dropship US Spy Agent (Mode Otomatis)")
str.write("Mesin riset produk winning pasar Amerika Serikat. 100% Gratis menggunakan Gemini API.")

# --- 2. SIDEBAR: PENGATURAN KUNCI API ---
with str.sidebar:
    str.header("⚙️ Pengaturan Agen")
    gemini_key = str.text_input("Google Gemini API Key:", type="password", placeholder="Masukkan key AIzaSy... Anda")
    str.markdown("---")
    str.caption("Aplikasi berjalan lokal di laptop Anda. 100% Hemat biaya.")

# --- 3. FORMULIR INPUT RISET ---
col1, col2 = str.columns(2)

with col1:
    kategori = str.selectbox(
        "📦 Pilih Kategori Produk:",
        ["Gadget Unik / Elektronik", "Perlengkapan Hewan (Pet Supplies)", "Alat Rumah Tangga Inovatif", "Aksesoris Mobil/Motor", "Kecantikan & Kesehatan"]
    )

with col2:
    target_masalah = str.text_input(
        "Target Masalah Spesifik (Opsional):",
        placeholder="Contoh: Mengatasi bulu kucing rontok, hobi camping, dll..."
    )

# --- 4. TOMBOL EKSEKUSI ---
if str.button("🔥 Perintahkan Agen Berburu Tren & Prompt"):
    if not gemini_key:
        str.warning("⚠️ Tolong masukkan Gemini API Key Anda di sidebar kiri terlebih dahulu!")
    else:
        with str.spinner("🕵️‍♂️ Agen sedang mencari jalur model aktif di akun Anda..."):
            try:
                # Daftarkan API Key ke library Google
                genai.configure(api_key=gemini_key)
                
                # --- TRICK OTOMATIS: Cari model teks yang aktif di akun user ---
                model_aktif = None
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        # Cari model terbaru yang didukung (Gemini 1.5 atau 2.0 atau 2.5)
                        if 'flash' in m.name or 'pro' in m.name:
                            model_aktif = m.name
                            break
                
                # Jika tidak ada flash/pro, ambil model teks pertama apa saja yang tersedia
                if not model_aktif:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            model_aktif = m.name
                            break

                if not model_aktif:
                    raise Exception("Tidak ada model generateContent yang aktif di akun API ini.")
                
                # Tampilkan model apa yang akhirnya dipakai (Biar kita tahu)
                str.info(f"🤖 Menggunakan Otak AI Aktif: `{model_aktif}`")
                
                # Pasang model pilihan otomatis tersebut
                model = genai.GenerativeModel(model_aktif)

                # Draft instruksi perintah (Prompt)
                prompt_perintah = f"""
                Bertindaklah sebagai Konsultan Dropship Profesional spesialis pasar Amerika Serikat (US).
                Lakukan riset mendalam untuk kategori: '{kategori}' dengan fokus masalah: '{target_masalah if target_masalah else 'Masalah umum sehari-hari'}'.
                
                Berikan 3 rekomendasi produk spesifik dari AliExpress yang berpotensi menjadi 'Winning Product' jika diiklankan di Facebook Ads saat ini.
                
                Format Output wajib terstruktur seperti ini:
                ---
                ### 📦 PILIHAN PRODUK: [Nama Produk dalam Bahasa Inggris]
                * **Mengapa Produk Ini? (The Problem Solved):** (Penjelasan masalah)
                * **Target Audiens Ideal di FB Ads:** (Demografi & Interests)
                * **Sudut Pandang Iklan (Marketing Angle):** (Ide video/gambar)
                * **Contoh Copywriting Iklan (Primary Text):** "[Text iklan versi US]"
                ---
                """

                # Kirim data ke Google
                response = model.generate_content(prompt_perintah)
                
                # Tampilkan hasil jika sukses
                str.success("🎯 Analisis Selesai! Berikut adalah laporan produk Anda:")
                str.markdown(response.text)

            except Exception as e:
                str.error(f"🚨 Terjadi kendala teknis: {e}")
                str.info("Jika eror Quota Exceeded (429) muncul lagi setelah nama model terdeteksi, mohon tunggu 1 menit lalu klik ulang tanpa mengubah kode.")