import streamlit as st
from datetime import datetime
import pandas as pd
import os

# Set page config and title
st.set_page_config(
    page_title="PCH - Token System",
    page_icon="🏥",
    layout="wide"
)

# File path for storing patient records
DATA_FILE = 'patient_records.csv'

# Load existing data from CSV if available
if os.path.exists(DATA_FILE):
    patient_data = pd.read_csv(DATA_FILE)
    patient_data['Date'] = pd.to_datetime(patient_data['Date'])
else:
    patient_data = pd.DataFrame(columns=['Date', 'Token', 'Doctor', 'Patient', 'Age', 'Time', 'Fee'])

# Initialize token number in session state
if 'token_number' not in st.session_state:
    st.session_state.token_number = 1

# Define Tabs
tab1, tab2, tab3 = st.tabs(["✨ Input Form", "🎫 Token Display", "📊 Patient History"])

with tab1:
    st.title("🏥 PCH Token System")
    st.subheader("Manage patient queue efficiently")
    
    st.info("Contact: 03345389032 | Address: City Karachi | Consultation Fee: Rs. 500")
    
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"### 📅 {current_date}")
    
    st.write(f"## Current Token Number: **{st.session_state.token_number}**")
    
    col1, col2 = st.columns(2)
    with col1:
        doctor_name = st.text_input("👨‍⚕️ Doctor Name")
        patient_age = st.number_input("🎂 Patient Age", min_value=0, max_value=120)
    with col2:
        patient_name = st.text_input("👤 Patient Name")
    
    if st.button("Generate Next Token ➡️"):
        if doctor_name and patient_name and patient_age:
            new_data = {
                'Date': pd.Timestamp.now(),
                'Token': st.session_state.token_number,
                'Doctor': doctor_name,
                'Patient': patient_name,
                'Age': patient_age,
                'Time': datetime.now().strftime("%I:%M %p"),
                'Fee': 500
            }
            
            patient_data = pd.concat([patient_data, pd.DataFrame([new_data])], ignore_index=True)
            patient_data.to_csv(DATA_FILE, index=False)
            
            st.session_state.token_number += 1
            st.rerun()
        else:
            st.error("⚠️ Please fill in all details (Doctor Name, Patient Name, and Age)")

with tab2:
    if patient_data.empty:
        st.info("No tokens generated yet")
    else:
        latest_token = patient_data.iloc[-1]
        st.markdown(f"""
        ## Token Number: **{latest_token['Token']}**
        - **👨‍⚕️ Doctor:** {latest_token['Doctor']}
        - **👤 Patient:** {latest_token['Patient']}
        - **🎂 Age:** {latest_token['Age']}
        - **⏰ Time:** {latest_token['Time']}
        - **💰 Fee:** Rs. 500
        """)

with tab3:
    if not patient_data.empty:
        st.markdown("### 📋 Patient History (Last 8 Days)")
        patient_data['Date'] = patient_data['Date'].dt.strftime('%B %d, %Y')
        st.dataframe(patient_data, use_container_width=True)
    else:
        st.info("No patient history available")

if st.button("🔄 Reset Token Numbers"):
    st.session_state.token_number = 1
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.success("🎉 Token numbers have been reset to 1")
    st.rerun()

if not patient_data.empty:
    csv = patient_data.to_csv(index=False)
    st.download_button("📥 Download Patient Records", data=csv, file_name='patient_records.csv', mime='text/csv')

st.markdown("""
---
👨‍⚕️ *Created with ❤️ by Shabana Basra*
""")
