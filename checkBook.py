import streamlit as st
import cv2
from PIL import Image
import numpy as np
import mysql.connector
from mysql.connector import Error
bid = 0
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
            st.success(f"Book ID is : {value}")
            bid = int(value)
            if points is not None:
                # Draw a rectangle around the QR code
                points = points[0].astype(int)
                for i in range(4):
                    cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % 4]), (0, 255, 0), 3)
        else:
            st.warning("No QR Code detected.")

        # Convert the frame back to RGB for Streamlit display
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #st.image(frame, channels="RGB")
# Streamlit app
def ReadBook(bid):
    #st.title("Book Information Viewer")
    
    # Connect to the database
    connection = create_connection()
    if connection:
        # Fetch all IDs
        #ids = fetch_ids(connection)
        ids = 1
        if ids:
            # Select ID from dropdown
            selected_id = st.selectbox("Select an ID:", ids)
            if selected_id:
                # Fetch information for the selected ID
                book_info = fetch_info_by_id(connection, selected_id)
                if book_info:
                    # Display book information
                    st.write("### Book Information")
                    columns = ["ID", "Title", "Author", "Total Books", "Available Books"]  # Example columns
                    for col, val in zip(columns, book_info):
                        st.write(f"**{col}:** {val}")
                else:
                    st.warning("No information found for the selected ID.")
        else:
            st.warning("No IDs available in the BookInfo table.")
        connection.close()
    else:
        st.error("Failed to connect to the database.")

# Fetch information for a selected ID
def fetch_info_by_id(connection, selected_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM BookInfo WHERE id = %s"
        cursor.execute(query, (selected_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Error as e:
        st.error(f"Error fetching information: {e}")
        return None

# Streamlit app
def main():
    #st.title("Book Information Viewer")
    ids = bid
    # Connect to the database
    connection = create_connection()
    if connection:
        # Fetch all IDs
        #ids = fetch_ids(connection)
        #ids = 1
        if ids:
            # Select ID from dropdown
            selected_id = st.selectbox("Select an ID:", ids)
            if selected_id:
                # Fetch information for the selected ID
                book_info = fetch_info_by_id(connection, selected_id)
                if book_info:
                    # Display book information
                    st.write("### Book Information")
                    columns = ["ID", "Title", "Author", "Toatl Books", "Available Books"]  
                    for col, val in zip(columns, book_info):
                        st.write(f"**{col}:** {val}")
                else:
                    st.warning("No information found for the selected ID.")
        else:
            st.warning("No IDs available in the BookInfo table.")
        connection.close()
    else:
        st.error("Failed to connect to the database.")

if __name__ == "__main__":
    read_qr_code_from_camera()
