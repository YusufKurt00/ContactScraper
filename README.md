# ContactScraper 🔍

**Otomatik Web Scraping ile İletişim Bilgisi Toplayıcı**

----------

## 🚀 Proje Açıklaması

**ContactScraper**, web sitelerinden **e-posta, telefon numarası ve iletişim bilgilerini** otomatik olarak toplayan bir Python aracıdır.

-   Google üzerinden şirketleri arar
-   İlk çıkan web sitesine gider
-   HTML kaynak kodunu analiz ederek iletişim bilgilerini toplar
-   Bilgiler bulunamazsa **İletişim (Contact)** sayfasını kontrol eder
-   Sonuçları **Excel** dosyasına kaydeder

### Kullanım Alanları

-   Dijital Pazarlama
-   Veri Madenciliği
-   Pazar Araştırmaları
-   SEO & Reklamcılık

----------

## 🛠 Kullanılan Teknolojiler

-   **Python** – Ana dil
-   **Selenium** – Web gezintisi & Google araması
-   **BeautifulSoup** – HTML veri çekme
-   **Pandas** – Excel işlemleri
-   **OpenPyXL** – Excele yazma
-   **Regex (re)** – E-posta & Telefon ayıklama

----------

## 📌 Kurulum

Öncelikle kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt

```

**requirements.txt** içeriği:

```txt
selenium==4.28.1
beautifulsoup4==4.13.3
pandas==2.2.3
openpyxl==3.1.5
lxml==4.9.3

```

----------

## 🚀 Nasıl Çalışır?

1.  `example.xlsx` dosyasına şirket isimlerini girin:

```
Tesla
Microsoft
Apple
Amazon
Netflix

```

2.  Programı çalıştırın:

```bash
python main.py

```

3.  Sonuçlar **result.xlsx** dosyasına kaydedilecektir.

----------

## 🎯 Özellikler

-   Google Üzerinden Otomatik Arama
-   HTML Kaynağından Bilgi Çekme
-   E-posta & Telefon Bulma
-   İletişim Sayfası Tarama
-   Excel Formatında Çıktı
-   User-Agent Spoofing

----------

## ⚠️ Yasal Uyarı

**Bu proje yalnızca eğitim ve araştırma amaçlıdır.** Veri toplamak bazı web sitelerinin **Gizlilik Politikalarına** aykırı olabilir. Lütfen **robots.txt** kurallarına uyarak kullanın.

----------

## 📜 Lisans

Bu proje **MIT Lisansı** altında yayınlanmıştır. Tüm hakları saklıdır © 2025 **Yusuf Kurt**.

----------

## 🤝 Katkıda Bulunma

Pull request'lere açığım! Geliştirme önerileriniz için **Issue** açabilirsiniz.

----------

## İletişim

Yusuf Kurt – [YusufKurt00](https://github.com/YusufKurt00)  
Proje Linki: [ContactScraper](https://github.com/YusufKurt00/ContactScraper)

⭐ Projeyi beğendiyseniz, lütfen **beğenmeyi** unutmayın!
