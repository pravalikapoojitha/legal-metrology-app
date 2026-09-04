import streamlit as st
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import datetime

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Legal Metrology Compliance", layout="wide")

# Initialize Session State for Image/Audit History
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------------------------
# TRANSLATION DICTIONARY
# -----------------------------------------------------------------------------
LANGUAGES = {
    "English": {
        "title": "📦 Legal Metrology Compliance Checker",
        "caption": "Packaged Commodities Rules, 2011 Inspection Prototype",
        "nav_label": "Navigation",
        "nav_checker": "Compliance Checker",
        "nav_history": "Upload & Audit History",
        "upload_header": "1. Upload Product Label Image",
        "upload_prompt": "Upload product label photo...",
        "label_header": "2. Label Declarations Verification",
        "info_text": "System verifies mandatory declarations under Rule 6 of PCR 2011.",
        "mrp_label": "MRP (e.g. Rs. 99.00 incl. of all taxes)",
        "net_qty_label": "Net Quantity (e.g. 200 g / 1 L)",
        "mfg_date_label": "Mfg / Packing Date (e.g. 08/2026)",
        "mfr_label": "Manufacturer/Packer Details",
        "care_label": "Consumer Care Contact",
        "coo_label": "Country of Origin",
        "scorecard": "Audit Scorecard",
        "compliant_msg": "🎉 **COMPLIANT:** {passed}/{total} Mandatory Declarations verified. Product meets Legal Metrology Rules, 2011.",
        "non_compliant_msg": "⚠️ **NON-COMPLIANT:** Only {passed}/{total} Mandatory Declarations found. Violation under PCR 2011.",
        "download_btn": "📄 Export Legal Metrology Inspection Certificate (PDF)",
        "history_title": "📜 Upload & Audit History",
        "no_history": "No records found yet. Upload and submit a product label to see history.",
        "clear_history": "Clear History",
    },
    "Hindi (हिंदी)": {
        "title": "📦 लीगल मेट्रोलॉजी अनुपालन जांचकर्ता",
        "caption": "पैक्ड कमोडिटीज रूल्स, 2011 निरीक्षण प्रोटोटाइप",
        "nav_label": "नेविगेशन",
        "nav_checker": "अनुपालन जांच",
        "nav_history": "अपलोड एवं ऑडिट इतिहास",
        "upload_header": "1. उत्पाद लेबल छवि अपलोड करें",
        "upload_prompt": "उत्पाद लेबल फ़ोटो अपलोड करें...",
        "label_header": "2. लेबल घोषणाओं का सत्यापन",
        "info_text": "सिस्टम पीसीआर 2011 के नियम 6 के तहत अनिवार्य घोषणाओं का सत्यापन करता है।",
        "mrp_label": "एमआरपी (उदा. रु 99.00 सभी करों सहित)",
        "net_qty_label": "शुद्ध मात्रा (उदा. 200 ग्राम / 1 लीटर)",
        "mfg_date_label": "निर्माण / पैकिंग तिथि (उदा. 08/2026)",
        "mfr_label": "निर्माता / पैकर का विवरण",
        "care_label": "उपभोक्ता देखभाल संपर्क",
        "coo_label": "मूल देश (Country of Origin)",
        "scorecard": "ऑडिट स्कोरकार्ड",
        "compliant_msg": "🎉 **अनुपालन संपन्न:** {passed}/{total} अनिवार्य घोषणाएं सत्यापित। उत्पाद विधिक मापविज्ञान नियमों का पालन करता है।",
        "non_compliant_msg": "⚠️ **गैर-अनुपालन:** केवल {passed}/{total} अनिवार्य घोषणाएं मिलीं। पीसीआर 2011 के तहत उल्लंघन।",
        "download_btn": "📄 लीगल मेट्रोलॉजी निरीक्षण प्रमाण पत्र निर्यात करें (PDF)",
        "history_title": "📜 अपलोड एवं ऑडिट इतिहास",
        "no_history": "अभी तक कोई रिकॉर्ड नहीं मिला। इतिहास देखने के लिए उत्पाद लेबल अपलोड करें।",
        "clear_history": "इतिहास साफ करें",
    },
    "Telugu (తెలుగు)": {
        "title": "📦 లీగల్ మెట్రాలజీ కాంప్లైయన్స్ చెకర్",
        "caption": "ప్యాక్ చేసిన వస్తువుల నిబంధనలు, 2011 తనిఖీ ప్రోటోటైప్",
        "nav_label": "నావిగేషన్",
        "nav_checker": "తనిఖీ కేంద్రం",
        "nav_history": "అప్‌లోడ్ & ఆడిట్ చరిత్ర",
        "upload_header": "1. ఉత్పత్తి లేబుల్ చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "upload_prompt": "ఉత్పత్తి లేబుల్ ఫోటోను అప్‌లోడ్ చేయండి...",
        "label_header": "2. లేబుల్ ప్రకటనల ధృవీకరణ",
        "info_text": "సిస్టమ్ PCR 2011 యొక్క రూల్ 6 ప్రకారం తప్పనిసరి ప్రకటనలను తనిఖీ చేస్తుంది.",
        "mrp_label": "MRP (ఉదా. రూ. 99.00 పన్నులతో కలిపి)",
        "net_qty_label": "నికర పరిమాణం (ఉదా. 200 గ్రా / 1 లీటర్)",
        "mfg_date_label": "తయారీ / ప్యాకింగ్ తేదీ (ఉదా. 08/2026)",
        "mfr_label": "తయారీదారు / ప్యాకర్ వివరాలు",
        "care_label": "వినియోగదారు సంరక్షణ సంప్రదింపు",
        "coo_label": "తయారీ దేశం (Country of Origin)",
        "scorecard": "ఆడిట్ స్కోర్‌కార్డ్",
        "compliant_msg": "🎉 **నిబంధనలకు లోబడి ఉంది:** {passed}/{total} తప్పనిసరి వివరాలు ధృవీకరించబడ్డాయి.",
        "non_compliant_msg": "⚠️ **నిబంధనల ఉల్లంఘన:** కేవలం {passed}/{total} తప్పనిసరి వివరాలు మాత్రమే కనుగొనబడ్డాయి.",
        "download_btn": "📄 లీగల్ మెట్రాలజీ ఇన్స్‌పెక్షన్ సర్టిఫికేట్‌ను ఎగుమతి చేయండి (PDF)",
        "history_title": "📜 అప్‌లోడ్ & ఆడిట్ చరిత్ర",
        "no_history": "ఇంకా ఎలాంటి రికార్డులు లేవు.",
        "clear_history": "చరిత్రను తొలగించు",
    }
}

# -----------------------------------------------------------------------------
# SIDEBAR: LANGUAGE & NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ Settings / సెట్టింగ్‌లు")

# 1. Language Selector
selected_lang = st.sidebar.selectbox("🌐 Select Language / भाषा चुनें", list(LANGUAGES.keys()))
t = LANGUAGES[selected_lang]

# 2. Navigation Bar
st.sidebar.divider()
st.sidebar.title(t["nav_label"])
page = st.sidebar.radio(
    "Go to",
    [t["nav_checker"], t["nav_history"]],
    label_visibility="collapsed"
)

# -----------------------------------------------------------------------------
# PAGE 1: COMPLIANCE CHECKER
# -----------------------------------------------------------------------------
if page == t["nav_checker"]:
    st.title(t["title"])
    st.caption(t["caption"])

    # 1. Image Upload
    st.header(t["upload_header"])
    uploaded_file = st.file_uploader(t["upload_prompt"], type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Product Label", use_container_width=True)

    # 2. Checklist Input
    st.header(t["label_header"])
    st.info(t["info_text"])

    col1, col2 = st.columns(2)

    with col1:
        mrp_text = st.text_input(t["mrp_label"], "Rs. 99.00")
        net_qty = st.text_input(t["net_qty_label"], "200 g")
        mfg_date = st.text_input(t["mfg_date_label"], "08/2026")

    with col2:
        manufacturer = st.text_input(t["mfr_label"], "ABC Foods Pvt Ltd")
        consumer_care = st.text_input(t["care_label"], "care@abcfoods.com")
        country_origin = st.text_input(t["coo_label"], "India")

    mandatory_fields = {
        "Maximum Retail Price (MRP)": mrp_text,
        "Net Quantity": net_qty,
        "Month & Year of Manufacture": mfg_date,
        "Manufacturer/Packer Name & Address": manufacturer,
        "Consumer Care Details": consumer_care,
        "Country of Origin": country_origin,
    }

    st.subheader(t["scorecard"])

    passed_count = 0
    total_count = len(mandatory_fields)

    for field, value in mandatory_fields.items():
        if value.strip() != "":
            st.success(f"✅ **PASS:** {field} -> `{value}`")
            passed_count += 1
        else:
            st.error(f"❌ **FAIL / MISSING:** {field}")

    is_compliant = passed_count == total_count

    # Save current run to Session State History
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        record_exists = any(item["name"] == uploaded_file.name and item["passed"] == passed_count for item in st.session_state.history)
        
        if not record_exists:
            st.session_state.history.append({
                "filename": uploaded_file.name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "image_data": file_bytes,
                "passed": passed_count,
                "total": total_count,
                "status": "COMPLIANT" if is_compliant else "NON-COMPLIANT",
                "details": mandatory_fields.copy()
            })

    st.divider()

    # 3. Final Result
    if is_compliant:
        st.balloons()
        st.success(t["compliant_msg"].format(passed=passed_count, total=total_count))
    else:
        st.warning(t["non_compliant_msg"].format(passed=passed_count, total=total_count))

    # 4. Generate Certificate PDF Function
    def generate_pdf():
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "LEGAL METROLOGY COMPLIANCE CERTIFICATE")
        p.setFont("Helvetica", 10)
        p.drawString(100, 735, "Under Legal Metrology (Packaged Commodities) Rules, 2011")
        p.line(100, 725, 500, 725)
        
        y = 690
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Mandatory Verification Checklist:")
        y -= 25
        
        p.setFont("Helvetica", 10)
        for field, val in mandatory_fields.items():
            status = "PRESENT" if val.strip() != "" else "MISSING"
            p.drawString(100, y, f"• {field}: {status}")
            y -= 20
            
        p.line(100, y, 500, y)
        y -= 30
        
        verdict_str = "FULLY COMPLIANT" if is_compliant else "NON-COMPLIANT (VIOLATION)"
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, f"FINAL STATUS: {verdict_str}")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    st.download_button(
        label=t["download_btn"],
        data=generate_pdf(),
        file_name="Packaged_Commodity_Inspection_Report.pdf",
        mime="application/pdf"
    )

# -----------------------------------------------------------------------------
# PAGE 2: HISTORY & AUDIT LOGS
# -----------------------------------------------------------------------------
elif page == t["nav_history"]:
    st.title(t["history_title"])

    if st.button(t["clear_history"]):
        st.session_state.history = []
        st.rerun()

    if not st.session_state.history:
        st.info(t["no_history"])
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"📷 {item['filename']} — {item['timestamp']} ({item['status']})"):
                col_img, col_data = st.columns([1, 2])
                with col_img:
                    st.image(Image.open(io.BytesIO(item["image_data"])), use_container_width=True)
                with col_data:
                    st.write(f"**Status:** {item['status']} ({item['passed']}/{item['total']})")
                    st.write("**Parsed Declarations:**")
                    for k, v in item["details"].items():
                        if v.strip():
                            st.write(f"- **{k}:** {v}")
                        else:
                            st.write(f"- **{k}:** ❌ *Missing*")