<div align="center">

<img src="banner.png" alt="Nexus Vanguard Banner" width="100%">

<br><br>

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-ffffff?style=flat-square&logo=flask&logoColor=black)](https://flask.palletsprojects.com)
[![SocketIO](https://img.shields.io/badge/Socket.IO-WebSocket-010101?style=flat-square&logo=socket.io&logoColor=white)](https://socket.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/badge/CI%2FCD-Passing-22c55e?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/ziyaguner/nexus-vanguard/actions)

<br>

![Ports](https://img.shields.io/badge/Port_Tarama-1--65535-00ff88?style=flat-square&labelColor=0a1628)
![CVE](https://img.shields.io/badge/CVE_Veritabani-25_Imza-ff3c5a?style=flat-square&labelColor=0a1628)
![Threads](https://img.shields.io/badge/Max_Thread-100-00b4ff?style=flat-square&labelColor=0a1628)
![Version](https://img.shields.io/badge/Surum-V7.0_Enterprise-a855f7?style=flat-square&labelColor=0a1628)

<br>

> **Gercek zamanli WebSocket akisi &nbsp;·&nbsp; 25 CVE imzasi &nbsp;·&nbsp; Canvas topoloji haritasi &nbsp;·&nbsp; Kalici tarama gecmisi &nbsp;·&nbsp; PDF rapor &nbsp;·&nbsp; Docker hazir**

<br>

</div>

---

## Ozellikler

<table>
<tr>
<td width="50%">

### Gercek Zamanli Tarama
- **WebSocket akisi** — Her acik port sayfa yenilenmeden aninda gelir
- **100 eszamanli thread** — Yuksek hizli port tarama motoru
- **Banner yakalama** — Servis versiyonu otomatik tespit edilir
- **5 hazir profil** — Std / Full / Known / Web / DB

</td>
<td width="50%">

### Guvenlik & Analiz
- **25 CVE imzasi** — Heartbleed, EternalRed, Ghostcat ve daha fazlasi
- **Otomatik risk siniflandirmasi** — CRITICAL / HIGH / MEDIUM / LOW
- **Flask-Login kimlik dogrulama** — Yetkisiz erisim tamamen engellenir
- **SQLite gecmis** — Her tarama kalici olarak kaydedilir

</td>
</tr>
<tr>
<td width="50%">

### Arayuz
- **Canvas topoloji haritasi** — Canli ag grafigi
- **Hacker terminali** — Gercek zamanli log konsolu
- **CRITICAL nabiz animasyonu** — Yuksek riskli portlar kirmizi yanar
- **PDF rapor** — Tek tikla kurumsal rapor indir

</td>
<td width="50%">

### DevOps
- **Docker & Compose** — Tek komutla ayaga kalkar
- **Kalici volume** — Veritabani konteyner silinse de korunur
- **GitHub Actions CI/CD** — Her push'ta otomatik test & build
- **REST API** — `/api/history` ile tarama gecmisi JSON

</td>
</tr>
</table>

---

## Hizli Baslangic

### Python ile (Gelistirme)

```bash
git clone https://github.com/ziyaguner/nexus-vanguard.git
cd nexus-vanguard
pip install -r requirements.txt
python app.py
```

> Uygulama otomatik baslar: **http://127.0.0.1:5001**

### Docker ile (Uretim)

```bash
docker-compose up -d        # Baslat
docker-compose logs -f      # Loglari izle
docker-compose down         # Durdur
```

---

## Giris Bilgileri

> [!WARNING]
> Asagidaki varsayilan bilgileri halka acik bir sunucuya deploy etmeden once `app.py` icinde degistirin.

| Alan | Deger |
|:---:|:---:|
| Kullanici Adi | `admin` |
| Sifre | `nexus2026` |

---

## Nasil Kullanilir?

> [!TIP]
> Kendi sisteminizi taramak icin `127.0.0.1` girin. Ag cihazlari icin yerel IP adresini kullanin.

**1.** Giris yapin &nbsp;**2.** Hedef IP girin &nbsp;**3.** Profil secin &nbsp;**4.** Taramayi baslatın

| Profil | Port Araligi | Kullanim Amaci |
|:---:|:---:|:---|
| `Std` | 1 - 1024 | Yaygin servisler (HTTP, SSH, FTP...) |
| `Full` | 1 - 65535 | Tam tarama |
| `Known` | 1 - 1023 | IANA bilinen portlar |
| `Web` | 8000 - 9999 | Web uygulamalari ve API'lar |
| `DB` | 3306 - 3399 | Veritabani sunuculari |

---

## CVE Veritabani

<details>
<summary><b>25 CVE imzasini gormek icin tiklayin</b></summary>

<br>

| CVE | Servis | Ciddiyet | Aciklama |
|---|---|:---:|---|
| CVE-2014-0160 | OpenSSL 1.0.1 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Heartbleed - ozel anahtar bellek sizintisi |
| CVE-2021-41773 | Apache 2.4.49 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Dizin gecisi ve Uzaktan Kod Calistirma |
| CVE-2021-42013 | Apache 2.4.50 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | CVE-2021-41773 yamasi icin RCE atlatma |
| CVE-2017-7494 | Samba 3.5 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | EternalRed - rastgele kutuphane yukleme |
| CVE-2011-2523 | vsftpd 2.3.4 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Arka kapi komutu calistirma |
| CVE-2020-1938 | Tomcat 9.0.0 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Ghostcat - AJP rastgele dosya okuma |
| CVE-2019-15846 | Exim 4.87 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | TLS SNI uzerinden heap tasmasi RCE |
| CVE-2019-10149 | Exim 4.92 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | MAIL FROM uzerinden uzaktan komut |
| CVE-2017-7269 | IIS 6.0 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | WebDAV buffer overflow RCE |
| CVE-2020-7247 | OpenSMTPD 6.6 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Root olarak yerel/uzaktan RCE |
| CVE-2018-7600 | Drupal 7 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Drupalgeddon2 kimlik dogrulamasiz RCE |
| CVE-2022-0543 | Redis 4.0 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Lua sandbox kacisi RCE |
| CVE-2017-12617 | Tomcat 7.0 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | JSP yukleme atlatmasi RCE |
| CVE-2019-11043 | PHP 5.6 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | FPM yolu alt tasma RCE |
| CVE-2010-4221 | ProFTPD 1.3.3 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Telnet IAC heap tasmasi |
| CVE-2015-3306 | ProFTPD 1.3.5 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | SITE CPFR ile rastgele dosya kopyalama |
| CVE-2016-6515 | OpenSSH 7.2 | ![](https://img.shields.io/badge/YUKSEK-f97316?style=flat-square) | Sinir tanimayan kimlik dogrulama DoS |
| CVE-2018-15473 | OpenSSH 7.7 | ![](https://img.shields.io/badge/ORTA-facc15?style=flat-square) | Zamanlama farki ile kullanici adi tespiti |
| CVE-2016-2107 | OpenSSL 1.0.2 | ![](https://img.shields.io/badge/YUKSEK-f97316?style=flat-square) | Dolgu oracle MITM saldirisi |
| CVE-2021-23017 | nginx 1.16.1 | ![](https://img.shields.io/badge/YUKSEK-f97316?style=flat-square) | DNS cozumleyicide off-by-one heap tasmasi |
| CVE-2014-6271 | bash 4.3 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Shellshock - ortam degiskeni RCE |
| CVE-2017-0144 | SMB v1 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | EternalBlue - WannaCry RCE |
| CVE-2021-44228 | Log4j 2.x | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | Log4Shell - JNDI injection RCE |
| CVE-2020-0796 | SMBv3 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | SMBGhost - istemci/sunucu RCE |
| CVE-2019-0708 | RDP 3389 | ![](https://img.shields.io/badge/KRITIK-ff3c5a?style=flat-square) | BlueKeep - kimlik dogrulamasiz RCE |

</details>

---

## Mimari

```
Tarayici (Socket.IO Istemcisi)
  Giris Ekrani --> Cyberpunk Dashboard
       |               |-- Port Tablosu (canli)
       |               |-- Canvas Topoloji Haritasi
       |               |-- Hacker Terminal Konsolu
       |               `-- PDF Rapor / Gecmis Modali
       |
       | WebSocket (cift yonlu, gercek zamanli)
       v
Flask-SocketIO Sunucusu [app.py]
  Flask-Login Auth  |  REST /api/history  |  WS Events
       |
       | Python geri cagirma (on_port, on_progress, on_done)
       v
Tarama Motoru [scanner.py]
  ThreadPoolExecutor (max 100)  |  Banner Yakalama
  CVE Analizi (VULN_DB, 25 imza)
       |
       | SQLAlchemy ORM
       v
Veritabani [database.py]
  ScanRecord + PortRecord --> SQLite (Docker kalici volume)
```

---

## Proje Yapisi

```
nexus-vanguard/
├── app.py                   # Sunucu, kimlik dogrulama, REST API
├── scanner.py               # Tarama motoru + CVE veritabani
├── database.py              # SQLAlchemy modelleri
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── banner.png
├── templates/
│   ├── index.html           # Cyberpunk dashboard
│   └── login.html           # Giris ekrani
└── .github/workflows/
    └── docker-build.yml     # CI/CD pipeline
```

---

## Teknoloji Yigini

<div align="center">

| Katman | Teknoloji |
|:---:|:---:|
| Backend | `Python 3.12` `Flask 3.0` `Flask-SocketIO` |
| Kimlik Dogrulama | `Flask-Login` |
| Veritabani | `SQLAlchemy` `SQLite` |
| Gercek Zamanli | `Socket.IO` WebSocket |
| Frontend | `HTML5` `CSS3` `JavaScript ES6+` |
| Gorsellestirme | `HTML5 Canvas` |
| PDF | `jsPDF` `autoTable` |
| Konteyner | `Docker` `Docker Compose` |
| CI/CD | `GitHub Actions` |

</div>

---

## Yapilandirma

```python
# app.py
ADMIN_USER = "admin"       # Kullanici adi
ADMIN_PASS = "nexus2026"   # Sifre - deploy oncesi degistirin!
PORT       = 5001          # Sunucu portu
```

```python
# scanner.py
TIMEOUT = 0.5    # Port basina soket zaman asimi (saniye)
# Max thread sayisi: 100
```

---

## CI/CD Pipeline

> [!NOTE]
> Her `main` branch push'unda asagidaki adimlar otomatik calisir.

```
Push --> [1] Python Lint (flake8)
     --> [2] Docker Build + Container Test
```

---

## Yasal Uyari

> [!CAUTION]
> **Bu arac yalnizca egitim ve etik guvenliktestleri amaclidir.**
>
> - Yalnizca **kendi sisteminizi** veya **yazili izin aldiginiz** ag ve cihazlari tarayabilirsiniz.
> - Yetkisiz port taramasi, **Turk Ceza Kanunu** ve pek cok ulkenin bilisim mevzuati kapsaminda **suctur**.
> - Bu yazilimi kullananlar, tum hukuki sorumlulugu **tamamen kendileri kabul etmis** sayilir.
> - Gelistiriciler, yazilimin amac disi veya yetkisiz kullanimindan doğan hicbir zarardan sorumlu tutulamaz.

---

<div align="center">

**Guvenlik toplulugu icin tutkuyla gelistirildi**

Projeyi faydali bulduysaniz yildiz vermeyi unutmayin!

[![Star](https://img.shields.io/github/stars/ziyaguner/nexus-vanguard?style=social)](https://github.com/ziyaguner/nexus-vanguard)

</div>
