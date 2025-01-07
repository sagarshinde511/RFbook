import streamlit as st
import cv2
from PIL import Image
import numpy as np
import mysql.connector
from mysql.connector import Error

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="82.180.143.66",
            user="u263681140_students",
            password="testStudents@123",
            database="u263681140_students"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None


def read_qr_code_from_camera():
    st.title("QR Code Scanner")

    # Use Streamlit's camera input
    camera_image = st.camera_input("Take a picture to scan for QR codes")

    if camera_image:
        # Convert the captured image to OpenCV format
        image = Image.open(camera_image)
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Decode QR codes in the frame using OpenCV's QRCodeDetector
        qr_detector = cv2.QRCodeDetector()
        value, points, _ = qr_detector.detectAndDecode(frame)

        if value:
            st.success(f"Book ID is: {value}")
            st.session_state["book_id"] = int(value)  # Store in session state
        else:
            st.warning("No QR Code detected.")


def fetch_info_by_id(connection, book_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM BookInfo WHERE id = %s"
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Error as e:
        st.error(f"Error fetching information: {e}")
        return None


def display_book_info():
    st.title("Book Information Viewer")

    # Check if book ID exists in session state
    book_id = st.session_state.get("book_id")
    if not book_id:
        st.warning("No Book ID scanned yet. Please scan a QR code.")
        return

    # Connect to the database
    connection = create_connection()
    if connection:
        book_info = fetch_info_by_id(connection, book_id)
        if book_info:
            st.write("### Book Information")
            columns = ["ID", "Title", "Author", "Total Books", "Available Books"]
            for col, val in zip(columns, book_info):
                st.write(f"**{col}:** {val}")
        else:
            st.warning("No information found for the scanned Book ID.")
        connection.close()
    else:
        st.error("Failed to connect to the database.")


def main():
    # Initialize session state
    if "book_id" not in st.session_state:
        st.session_state["book_id"] = None

    # Create app layout with tabs
    tabs = st.tabs(["QR Code Scanner", "Book Information Viewer"])

    with tabs[0]:
        read_qr_code_from_camera()

    with tabs[1]:
        display_book_info()


if __name__ == "__main__":
    main()
