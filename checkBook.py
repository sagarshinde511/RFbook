import streamlit as st
import cv2
from PIL import Image
import numpy as np
import mysql.connector
from mysql.connector import Error

# MySQL database connection details
host = "82.180.143.66"
user = "u263681140_students"
passwd = "testStudents@123"
db_name = "u263681140_students"

# Function to fetch book information from the database
def fetch_data(book_id):
    try:
        # Establish connection to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=db_name
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # Query to fetch book information
            query = "SELECT BookName, Author, InStock, AvailableStock FROM BooksInfo WHERE id = %s"
            cursor.execute(query, (book_id,))
            result = cursor.fetchone()
            return result
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to read QR code from camera
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
            return value
        else:
            st.warning("No QR Code detected.")
            return None

# Main function
def main():
    # Create tabs for the app
    tab1, tab2 = st.tabs(["QR Code Scanner", "Book Information Viewer"])

    with tab1:
        book_id = read_qr_code_from_camera()
        if book_id:
            st.session_state["book_id"] = book_id

    with tab2:
        if "book_id" in st.session_state:
            book_id = st.session_state["book_id"]
            book_info = fetch_data(book_id)
            if book_info:
                st.subheader("Book Information")
                st.write(f"**Book Name:** {book_info['BookName']}")
                st.write(f"**Author:** {book_info['Author']}")
                st.write(f"**In Stock:** {book_info['InStock']}")
                st.write(f"**Available Stock:** {book_info['AvailableStock']}")
            else:
                st.error("Book information could not be retrieved. Please check the Book ID.")
        else:
            st.info("Please scan a QR code to view book information.")

if __name__ == "__main__":
    main()
