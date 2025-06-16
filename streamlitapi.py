import joblib
import streamlit as st
import requests
from io import BytesIO

# Load trained model
#with open("RandomForestClassifier_model.pkl", "rb") as f:
    #model = joblib.load(f)
url = 'https://drive.google.com/drive/folders/15crWSVA2sH3KV1ZB2AcKl0vrOpqGDco-/RandomForestClassifier_model.pkl'
response = requests.get(url)
model = joblib.load(BytesIO(response.content))
    
def main():
    st.title('💼 Will the client subscribe to a term deposit?')

    # Encoding maps
    job_map = {'admin.': 0, 'technician': 1, 'services': 2, 'management': 3, 'retired': 4, 'blue-collar': 5}
    marital_map = {'married': 0, 'single': 1, 'divorced': 2}
    education_map = {'primary': 0, 'secondary': 1, 'tertiary': 2, 'unknown': 3}
    default_map = {'no': 0, 'yes': 1}
    housing_map = {'no': 0, 'yes': 1}
    loan_map = {'no': 0, 'yes': 1}
    contact_map = {'cellular': 0, 'telephone': 1}
    month_map = {'jan': 0, 'feb': 1, 'mar': 2, 'apr': 3, 'may': 4, 'jun': 5, 'jul': 6, 'aug': 7, 'sep': 8, 'oct': 9, 'nov': 10, 'dec': 11}
    poutcome_map = {'unknown': 0, 'failure': 1, 'other': 2, 'success': 3}

    # User inputs
    Age = st.number_input('Age', min_value=0)
    Job = st.selectbox('Job', list(job_map.keys()))
    Marital = st.selectbox('Marital status', list(marital_map.keys()))
    Education = st.selectbox('Education', list(education_map.keys()))
    Default = st.selectbox('Has credit in default?', list(default_map.keys()))
    Balance = st.number_input('Account balance')
    Housing = st.selectbox('Housing loan?', list(housing_map.keys()))
    Loan = st.selectbox('Personal loan?', list(loan_map.keys()))
    Contact = st.selectbox('Contact communication type', list(contact_map.keys()))
    Day = st.number_input('Last contact day of the month', min_value=1, max_value=31)
    Month = st.selectbox('Last contact month of year', list(month_map.keys()))
    Duration = st.number_input('Last contact duration (seconds)')
    Campaign = st.number_input('Number of contacts during this campaign')
    Pdays = st.number_input('Days since last contact from previous campaign')
    Previous = st.number_input('Number of contacts before this campaign')
    Poutcome = st.selectbox('Outcome of previous campaign', list(poutcome_map.keys()))

    # Encode inputs
    Job_encoded = job_map[Job]
    Marital_encoded = marital_map[Marital]
    Education_encoded = education_map[Education]
    Default_encoded = default_map[Default]
    Housing_encoded = housing_map[Housing]
    Loan_encoded = loan_map[Loan]
    Contact_encoded = contact_map[Contact]
    Month_encoded = month_map[Month]
    Poutcome_encoded = poutcome_map[Poutcome]

    # Prediction
    if st.button('Predict'):
        try:
            input_data = [[
                Age, Job_encoded, Marital_encoded, Education_encoded, Default_encoded,
                Balance, Housing_encoded, Loan_encoded, Contact_encoded, Day,
                Month_encoded, Duration, Campaign, Pdays, Previous, Poutcome_encoded
            ]]
            prediction = model.predict(input_data)
            
            if prediction[0] == 1:
                st.success("✅ Client **will subscribe** to a term deposit.")
            else:
                st.warning("❌ Client **will not subscribe** to a term deposit.")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

# Launch app
if __name__ == '__main__':
    main()
