import streamlit as st
import requests

st.set_page_config(page_title="Predictive Attrition Engine", layout="centered")
st.title("🏦 Customer Attrition Risk Engine")
st.markdown("Enter customer details to predict churn probability.")


with st.form("churn_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        
        credit_score = st.number_input("Credit Score", min_value=350, max_value=850, value=650)
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        tenure = st.slider("Tenure (Years)", 0, 10, 5)
        balance = st.number_input("Account Balance ($)", min_value=0.0, value=50000.0)
        estimated_salary = st.number_input("Estimated Salary ($)", min_value=0.0, value=60000.0)
        
    with col2:
        country = st.selectbox("Country", ["France", "Spain", "Germany"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        products_number = st.selectbox("Number of Products", [1, 2, 3, 4])
        credit_card = st.selectbox("Has Credit Card? (1=Yes, 0=No)", [0, 1])
        active_member = st.selectbox("Is Active Member? (1=Yes, 0=No)", [0, 1])

    submitted = st.form_submit_button("Analyze Risk", type="primary", use_container_width=True)


if submitted:
    
    payload = {
        "credit_score": credit_score,
        "country": country,
        "gender": gender,
        "age": age,
        "tenure": tenure,
        "balance": balance,
        "products_number": products_number,
        "credit_card": credit_card,
        "active_member": active_member,
        "estimated_salary": estimated_salary
    }
    
    API_URL = "http://127.0.0.1:8000/predict"
    
    try:
        with st.spinner("Analyzing attrition risk..."):
            response = requests.post(API_URL, json=payload)
            
        if response.status_code == 200:
            result = response.json()
            
            
            prediction = result.get("churn_prediction")
            probability = result.get("churn_probability")
            
            st.divider()
            
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric(label="Churn Probability", value=f"{probability * 100:.2f}%")
                
            with metric_col2:
                if prediction == 1:
                    st.error("⚠️ HIGH RISK: Customer is likely to churn.")
                else:
                    st.success("✅ LOW RISK: Customer is likely to stay.")
                
            with st.expander("View Raw Output"):
                st.json(result)
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Connection Failed. Is the Project 2 FastAPI server running on port 8000?")