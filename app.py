import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

os.makedirs("output", exist_ok=True)

def generate_salary_slip(row, month):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 20)
    pdf.set_fill_color(41, 128, 185)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "SALARY SLIP", ln=True, align="C", fill=True)
    pdf.ln(3)

    # Month
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Month: {month}", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    # Employee Info
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 8, f"Name: {row['Name']}", ln=True)
    pdf.cell(95, 8, f"Email: {row['Email']}", ln=True)
    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    # Earnings
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, "Earnings", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 8, "Basic Salary", ln=False)
    pdf.cell(95, 8, f"Rs. {row['Basic']}", ln=True)
    pdf.cell(95, 8, "HRA", ln=False)
    pdf.cell(95, 8, f"Rs. {row['HRA']}", ln=True)
    pdf.cell(95, 8, "Bonus", ln=False)
    pdf.cell(95, 8, f"Rs. {row['Bonus']}", ln=True)
    pdf.cell(95, 8, "Gross Salary", ln=False)
    pdf.cell(95, 8, f"Rs. {row['Gross Salary']}", ln=True)
    pdf.ln(3)

    # Deductions
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(255, 200, 200)
    pdf.cell(0, 10, "Deductions", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 8, "PF (12%)", ln=False)
    pdf.cell(95, 8, f"Rs. {row['PF (12%)']}", ln=True)
    pdf.cell(95, 8, "Income Tax (10%)", ln=False)
    pdf.cell(95, 8, f"Rs. {row['Income Tax (10%)']}", ln=True)
    pdf.cell(95, 8, "Total Deductions", ln=False)
    pdf.cell(95, 8, f"Rs. {row['Total Deductions']}", ln=True)
    pdf.ln(3)

    # Net Salary
    pdf.set_font("Arial", "B", 13)
    pdf.set_fill_color(41, 128, 185)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(95, 12, "NET SALARY", fill=True, ln=False)
    pdf.cell(95, 12, f"Rs. {row['Net Salary']}", fill=True, ln=True)

    filename = f"output/{row['Name'].replace(' ', '_')}_slip.pdf"
    pdf.output(filename)
    return filename

def send_email(to_email, name, pdf_path, sender_email, sender_password, month):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = f"Salary Slip - {month}"

    body = f"""Dear {name},

Please find attached your salary slip for {month}.

Regards,
HR Team"""
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_path, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()

# Streamlit UI
st.title("💰 Salary Slip Generator")
st.write("Upload your employee Excel file to generate and send salary slips!")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

month = st.text_input("Enter Month (e.g. April 2026)", "April 2026")

st.subheader("📧 Email Settings")
sender_email = st.text_input("Your Gmail Address")
sender_password = st.text_input("Your Gmail App Password", type="password")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    st.success(f"✅ Found {len(df)} employees!")
    st.dataframe(df)

    if st.button("Generate & Send Salary Slips"):
        if not sender_email or not sender_password:
            st.error("Please enter your Gmail and App Password!")
        else:
            with st.spinner("Generating and sending salary slips..."):
                pdf_files = []
                failed = []
                for _, row in df.iterrows():
                    try:
                        filename = generate_salary_slip(row, month)
                        pdf_files.append(filename)
                        send_email(row['Email'], row['Name'], filename, sender_email, sender_password, month)
                        st.success(f"✅ Sent to {row['Name']} ({row['Email']})")
                    except Exception as e:
                        failed.append(row['Name'])
                        st.error(f"❌ Failed for {row['Name']}: {str(e)}")

                # ZIP for download
                zip_path = "output/all_salary_slips.zip"
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for f in pdf_files:
                        zipf.write(f, os.path.basename(f))

            st.success(f"🎉 Done! {len(pdf_files) - len(failed)} slips sent successfully!")

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 Download All Salary Slips (ZIP)",
                    data=f,
                    file_name="salary_slips.zip",
                    mime="application/zip"
                )