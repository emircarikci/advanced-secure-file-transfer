# 🔐 Advanced Secure File Transfer System

Bu proje, bilgisayar ağlarında **güvenli dosya aktarımı** sağlamak amacıyla RSA, AES ve SHA-256 algoritmalarını kullanarak hem **şifreleme** hem de **veri bütünlüğü doğrulaması** yapan bir sistemdir.

---

## 🚀 Proje Özellikleri

- ✅ RSA ile anahtar paylaşımı
- ✅ AES ile dosya şifreleme
- ✅ SHA-256 ile bütünlük kontrolü
- ✅ TCP ve UDP üzerinden dosya gönderimi
- ✅ GUI (grafik arayüz) desteği
- ✅ IP başlık analizi ve manipülasyonu

---

## 📁 Dosya Yapısı

```
.
├── client.py                # İstemci ana uygulama
├── server.py                # Sunucu ana uygulama
├── create_keys.py           # RSA anahtar üretimi
├── gui.py                   # Kullanıcı arayüzü (Tkinter)
├── udp_server.py            # UDP sunucu alternatifi
├── tcp_server.py            # TCP sunucu alternatifi
├── ip_header_test.py        # IP başlık kontrolü
├── README.md                # Proje açıklaması

---

## ⚙️ Kurulum

1. Gerekli bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

2. RSA anahtarlarını oluşturun:
```bash
python create_keys.py
```

3. Sunucuyu başlatın:
```bash
python server.py
```

4. İstemciyi çalıştırın:
```bash
python client.py
```

5. GUI versiyonunu başlatmak için:
```bash
python gui.py
```

---

## 🔄 Nasıl Çalışır?

1. **RSA ile şifrelenmiş AES anahtarı sunucuya gönderilir.**
2. **Sunucu, bu anahtarla AES çözümlemesi yapar.**
3. **İstemci dosyayı AES ile şifreleyip yollar.**
4. **SHA-256 ile özet alınır ve dosya bütünlüğü doğrulanır.**
5. **Transfer başarılı ise, dosya sunucuya kaydedilir.**

---

## 🖼️ Örnek Ekran Görüntüsü

> *(Buraya `docs/` klasörüne koyacağınız bir GUI veya terminal çıktısı görselini ekleyebilirsiniz)*

---

## 📌 Notlar

- **Anahtar dosyaları (`.pem`) güvenlik nedeniyle GitHub'a eklenmemiştir.**
- GUI çalışmıyorsa: Linux kullanıcıları için `sudo apt install python3-tk` komutu gerekebilir.

---

## 🧑‍💻 Geliştirici

**Emir Çarıkçı**  
Bilgisayar Ağları Dönem Projesi  
Bursa Teknik Üniversitesi  
2024-2025 Bahar Dönemi  
Student No: `21360859060`
