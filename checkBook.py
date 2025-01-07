import streamlit as st
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

# Fetch all IDs from the BookInfo table
def fetch_ids(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM BookInfo")
        ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return ids
    except Error as e:
        st.error(f"Error fetching IDs: {e}")
        return []

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
    st.title("Book Information Viewer")
    
    # Connect to the database
    connection = create_connection()
    if connection:
        # Fetch all IDs
        ids = fetch_ids(connection)
        if ids:
            # Select ID from dropdown
            selected_id = st.selectbox("Select an ID:", ids)
            if selected_id:
                # Fetch information for the selected ID
                book_info = fetch_info_by_id(connection, selected_id)
                if book_info:
                    # Display book information
                    st.write("### Book Information")
                    columns = ["ID", "Title", "Author", "Toatl Books", "Available Books"]  # Example columns
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
    main()
