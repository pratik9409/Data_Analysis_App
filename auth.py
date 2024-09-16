import pyrebase
import streamlit as st

# Firebase configuration (replace with your Firebase config)
firebaseConfig = {
    'apiKey': "AIzaSyDz1Z57uw4PEyabvUwXg7YNlbFYuZ0aK8s",
    'authDomain': "data-analysis-app-699db.firebaseapp.com",
    'projectId': "data-analysis-app-699db",
    'storageBucket': "data-analysis-app-699db.appspot.com",
    'messagingSenderId': "664630991608",
    'appId': "1:664630991608:web:21730777fd542449e5f90d",
    'measurementId': "G-FSHYWBZHLZ",
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login():
    st.sidebar.title("Login")
    email = st.sidebar.text_input("Enter your email", key="login_email")
    password = st.sidebar.text_input("Enter your password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.sidebar.success("Login Successful!")
            return user
        except:
            st.sidebar.error("Invalid credentials")
    return None

# def signup():
#     st.sidebar.title("SignUp")
#     email = st.sidebar.text_input("Enter your email", key="signup_email")
#     password = st.sidebar.text_input("Enter your password", type="password", key="signup_password")
#     if st.sidebar.button("Create Account"):
#         try:
#             user = auth.create_user_with_email_and_password(email, password)
#             st.success("Account Created Successfully")
#         except:
#             st.error("Error creating account")


def signup():
    st.sidebar.title("SignUp")
    email = st.sidebar.text_input("Enter your email", key="signup_email")
    password = st.sidebar.text_input("Enter your password", type="password", key="signup_password")
    if st.sidebar.button("Create Account"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("Account Created Successfully")
            return user
        except Exception as e:
            st.error(f"Error creating account: {str(e)}")  # Show the specific error message
