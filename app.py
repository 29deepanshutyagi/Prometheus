import streamlit as st
import google.generativeai as genai
import time
import firebase_admin
from firebase_admin import credentials, firestore

capitalize_sidebar_style = """
    <style>
    [data-testid="stSidebar"] * {
        text-transform: capitalize !important;
    }
    </style>
"""

st.markdown(capitalize_sidebar_style, unsafe_allow_html=True)


st.title("Prometheus - Login")

genai_api = st.secrets["GEMINI_API"]
sambanova_api = st.secrets["SAMBA_API"]

# Initialize Firestore DB
cred = credentials.Certificate("firebase.json")

# cache the Firebase initialization to avoid reinitializing the app. 
# subsequent calls will return the cached Firestore client.
@st.cache_resource
def init_firebase():
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    # Test connection with a Firestore operation
    try:
        test_ref = db.collection("test").document("connection_check")
        test_ref.set({"status": "connected"})
        print(test_ref.get().to_dict())
        st.success("Connected to Firestore successfully!")
    except Exception as e:
        st.error(f"Failed to connect to Firestore: {e}")
    
    return db

db = init_firebase()
print(db)

username = st.text_input("Enter your username")

if username:
    st.session_state.username = username
    st.success(f"Welcome, {username}! Please proceed to the home page.")
    st.switch_page("pages/home.py")

else:
    st.info("Please fill in all fields to proceed.")
