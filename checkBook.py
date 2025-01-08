import streamlit as st

# Set the title of the application
st.set_page_config(page_title="RFID-Based Bus Ticket System", layout="wide")

# Sidebar for the login page
st.sidebar.title("RFID-Based Bus Ticket System")
st.sidebar.write("Please log in to continue.")

# Login Form in Sidebar
with st.sidebar.form(key="login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.form_submit_button("Login")

# Main Page
if login_button:
    if username == "admin" and password == "admin":  # Example credentials
        st.sidebar.success(f"Welcome, {username}!")

        # Tabs after login
        tabs = st.tabs(["Recharge Card", "Check Live Status", "Check History", "Register Passenger"])

        # 1st Tab: Recharge Card
        with tabs[0]:
            st.subheader("Recharge Card")
            st.write("Redirecting to Google...")
            st.markdown('<a href="https://www.google.com" target="_blank">Click here if not redirected</a>', unsafe_allow_html=True)

        # 2nd Tab: Check Live Status
        with tabs[1]:
            st.subheader("Check Live Status")
            st.write("This tab will display live status information.")

        # 3rd Tab: Check History
        with tabs[2]:
            st.subheader("Check History")
            st.write("This tab will display the user's transaction or travel history.")

        # 4th Tab: Register Passenger
        with tabs[3]:
            st.subheader("Register Passenger")
            st.write("This tab will allow the admin to register new passengers.")
    else:
        st.sidebar.error("Invalid credentials. Please try again.")
else:
    st.write("Please log in from the sidebar to access the system.")
