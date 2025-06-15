import streamlit as st
import pyrebase

# Firebase configuration
firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com",
    "messagingSenderId": "YOUR_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Streamlit app
st.title("Streamlit + Pyrebase Demo")

# Sidebar: Authentication
st.sidebar.header("Authentication")
mode = st.sidebar.selectbox("Choose action", ["Sign In", "Sign Up"])
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button(mode):
    try:
        if mode == "Sign Up":
            user = auth.create_user_with_email_and_password(email, password)
            st.sidebar.success("Account created successfully!")
        else:
            user = auth.sign_in_with_email_and_password(email, password)
            st.sidebar.success("Signed in successfully!")
            st.session_state['user'] = user
    except Exception as e:
        st.sidebar.error(f"Authentication error: {e}")

# Main content for signed-in users
def main_app(user):
    st.header(f"Welcome, {user['email']}")
    st.write("This is a simple demo of storing and retrieving data from Firebase.")

    # Input form
    with st.form(key="data_form"):
        note = st.text_area("Enter a note to save")
        submit = st.form_submit_button("Save Note")

    if submit and note:
        data = {"email": user['email'], "note": note}
        db.child("notes").push(data, user['idToken'])
        st.success("Note saved to Firebase!")

    # Fetch and display notes
    notes = db.child("notes").get(user['idToken']).val()
    if notes:
        st.subheader("All Notes")
        for key, val in notes.items():
            st.write(f"- {val['email']}: {val['note']}")

# Run main app if user is authenticated
if 'user' in st.session_state:
    main_app(st.session_state['user'])
else:
    st.info("Please sign in or sign up in the sidebar to use the app.")

# To run this app: streamlit run streamlit_pyrebase_app.py
