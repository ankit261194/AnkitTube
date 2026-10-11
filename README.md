# 🎬 AnkitTube & Core Plugin Automated Builder

यह प्रोजेक्ट आपके **खुद के नाम (AnkitTube), ankitchaudhary (Developer), और कॉन्टैक्ट नंबर्स (8533955333, 89006518960)** के साथ पूरी तरह कस्टमाइज़्ड YouTube और उसका कंपैनियन प्लगइन तैयार करता है।

---

## 🌟 मुख्य विशेषताएँ (Key Features)

1. **100% AnkitTube की अपनी ब्रांडिंग:**
   - ऐप का नाम: **AnkitTube**
   - पैकेज नेम: `com.ankitchaudhary.ankittube`
   - डेवलपर: **ankitchaudhary**
   - कॉन्टैक्ट सपोर्ट: **8533955333, 89006518960**
   - ऐप के अंदर "ReVanced" या किसी भी अन्य प्रोजेक्ट का नाम या लिंक पूरी तरह से हटा दिया गया है।
2. **MicroG बना "AnkitTube Core Services" (Plugin):**
   - यूज़र को "MicroG" या "GmsCore" नहीं दिखेगा।
   - यह आपके ऐप के प्लगइन (`AnkitTube Core Services`) की तरह दिखेगा और इसका लोगो भी आपके ऐप की थीम से मैच करेगा।
3. **कस्टम स्टार्टअप स्क्रीन & लोगो (Splash Screen & Logo):**
   - ऐप का कस्टम 3D लोगो और ऐप खोलते समय दिखने वाला लक्ज़री **Splash Screen** पूरी तरह तैयार है।
4. **ऑटो-अपडेट सपोर्ट (Auto-Sync):**
   - जब भी कोई नया फीचर या YouTube का नया पैच आएगा, आपका GitHub Actions वर्कफ़्लो अपने आप नया कोड उठाएगा, लेकिन **आपका नाम, लोगो और नंबर कभी नहीं बदलेगा**।

---

## 📁 प्रोजेक्ट स्ट्रक्चर (Project Structure)

```text
custom-tube-builder/
├── config.json                     <-- अपनी ब्रांडिंग और कॉन्टैक्ट नंबर यहाँ बदलें
├── assets/
│   ├── app_icon.png                <-- आपका मुख्य ऐप लोगो (512x512 PNG)
│   └── plugin_icon.png             <-- आपके प्लगइन का लोगो (512x512 PNG)
├── scripts/
│   ├── purge_revanced.py           <-- ReVanced की सारी ब्रांडिंग मिटाने की स्क्रिप्ट
│   ├── rebrand_microg.py           <-- MicroG को कंपैनियन प्लगइन में बदलने की स्क्रिप्ट
│   ├── generate_keystore.py        <-- आपके नाम की डिजिटल साइनिंग की बनाने की स्क्रिप्ट
│   └── build_local.py              <-- अपने कंप्यूटर पर ऑफलाइन बिल्ड करने की स्क्रिप्ट
└── .github/workflows/
    └── auto_build.yml              <-- GitHub का ऑटोमेशन (Free Cloud Builder)
```

---

## 🚀 इस्तेमाल कैसे करें (How to Use)

### स्टेप 1: अपनी डिटेल्स सेट करें (`config.json`)
`config.json` फाइल खोलें और अपनी इच्छा अनुसार वैल्यूज बदलें:
```json
{
  "app_name": "MeraTube",
  "app_package_name": "com.meratube.android",
  "developer_name": "Rahul Sharma",
  "contact_number": "+91 9876543210",
  "contact_email": "support@meratube.com",
  "website_or_social": "https://t.me/mychannel",
  "plugin_app_name": "MeraTube Core Services"
}
```

### स्टेप 2: अपना लोगो (Logo) लगाएं
* `assets/app_icon.png` को अपने ऐप के लोगो से बदलें (512x512 पारदर्शी PNG सबसे अच्छा है)।
* `assets/plugin_icon.png` को अपने प्लगइन लोगो से बदलें।

---

## ☁️ तरीका A: GitHub Actions (सबसे आसान & ऑटोमैटिक — सिफारिश की जाती है)

आपको अपने कंप्यूटर पर भारी टूल्स इंस्टॉल करने की ज़रूरत नहीं है:

1. **GitHub पर नया रिपॉजिटरी बनाएं:**
   - [GitHub.com](https://github.com) पर जाएं और एक नया **Private** या **Public** रिपॉजिटरी बनाएं।
2. **यह कोड GitHub पर पुश करें:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for branded tube builder"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```
3. **ऑटोमैटिक बिल्ड चलाएं:**
   - GitHub रिपो में **Actions** टैब पर जाएं।
   - बाएं तरफ **"Automated Branded App & Plugin Builder"** पर क्लिक करें।
   - **"Run workflow"** बटन दबाएं।
4. **APK डाउनलोड करें:**
   - 3 से 5 मिनट में GitHub खुद ऐप कंपाइल करेगा।
   - रिपॉजिटरी के **Releases** सेक्शन में आपको 2 APKs डाउनलोड के लिए मिलेंगी:
     1. `MeraTube-Core-Plugin.apk` (पहले इसे इंस्टॉल करने को कहें)
     2. `MeraTube-Official.apk` (मुख्य ऐप)

---

## 💻 तरीका B: अपने कंप्यूटर (Local PC) पर चलाना

अगर आप इसे अपने कंप्यूटर पर ऑफलाइन चलाना चाहते हैं:

1. सुनिश्चित करें कि आपके PC में **Java 17** और **Python 3** इंस्टॉल हैं।
2. किसी भी ट्रस्टेड सोर्स (जैसे APKMirror) से एक क्लीन YouTube APK डाउनलोड करके इस फोल्डर में `youtube.apk` नाम से रख दें।
3. टर्मिनल / PowerShell में कमांड चलाएं:
   ```bash
   python scripts/build_local.py
   ```
4. तैयार APKs आपको `output/` फोल्डर में मिल जाएँगी।

---

## ⚠️ ज़रूरी सलाह (Important Advice)

* **Google Play Store:** इसे Google Play Store पर कभी अपलोड न करें (Google का कॉपीराइट होने के कारण अकाउंट तुरंत बंद हो सकता है)।
* **डिस्ट्रीब्यूशन:** इसे आप अपनी वेबसाइट, टेलीग्राम चैनल, या गूगल ड्राइव लिंक के माध्यम से अपने दोस्तों या ऑडियंस के साथ शेयर कर सकते हैं।
