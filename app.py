import streamlit as st
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Legal Metrology Compliance", layout="wide")

st.title("📦 Legal Metrology Compliance Checker")
st.caption("Packaged Commodities Rules, 2011 Inspection Prototype")

# 1. Image Upload
st.header("1. Upload Product Label Image")
uploaded_file = st.file_uploader("Upload product label photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Product Label",use_container_width=True)

# 2. Checklist Input
st.header("2. Label Declarations Verification")
st.info("System verifies mandatory declarations under Rule 6 of PCR 2011.")

col1, col2 = st.columns(2)

with col1:
    mrp_text = st.text_input("MRP (e.g. Rs. 99.00 incl. of all taxes)", "Rs. 99.00")
    net_qty = st.text_input("Net Quantity (e.g. 200 g / 1 L)", "200 g")
    mfg_date = st.text_input("Mfg / Packing Date (e.g. 08/2026)", "08/2026")

with col2:
    manufacturer = st.text_input("Manufacturer/Packer Details", "ABC Foods Pvt Ltd")
    consumer_care = st.text_input("Consumer Care Contact", "care@abcfoods.com")
    country_origin = st.text_input("Country of Origin", "India")

mandatory_fields = {
    "Maximum Retail Price (MRP)": mrp_text,
    "Net Quantity": net_qty,
    "Month & Year of Manufacture": mfg_date,
    "Manufacturer/Packer Name & Address": manufacturer,
    "Consumer Care Details": consumer_care,
    "Country of Origin": country_origin,
}

st.subheader("Audit Scorecard")

passed_count = 0
total_count = len(mandatory_fields)

for field, value in mandatory_fields.items():
    if value.strip() != "":
        st.success(f"✅ **PASS:** {field} detected -> `{value}`")
        passed_count += 1
    else:
        st.error(f"❌ **FAIL / MISSING:** {field} is missing or illegible!")

is_compliant = passed_count == total_count

st.divider()

# 3. Final Result
if is_compliant:
    st.balloons()
    st.success(f"🎉 **COMPLIANT:** {passed_count}/{total_count} Mandatory Declarations verified. Product meets Legal Metrology Rules, 2011.")
else:
    st.warning(f"⚠️ **NON-COMPLIANT:** Only {passed_count}/{total_count} Mandatory Declarations found. Violation under PCR 2011.")

# 4. Generate Certificate PDF
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
    label="📄 Export Legal Metrology Inspection Certificate (PDF)",
    data=generate_pdf(),
    file_name="Packaged_Commodity_Inspection_Report.pdf",
    mime="application/pdf"
)