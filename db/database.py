import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ihtisham@123",
        database="LeadManagement"
    )
    return connection


def init_db():
    """Ensure the `leads` and `customers` tables exist.
    Call this once at application startup (see main.py)."""
    conn = get_connection()
    cursor = conn.cursor()

    # create leads table if it's missing
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id VARCHAR(10) PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            PhoneNumber VARCHAR(20) NOT NULL,
            Email VARCHAR(255) NOT NULL,
            Source VARCHAR(255) NOT NULL,
            Status VARCHAR(50) NOT NULL,
            Budget INT NOT NULL,
            Notes TEXT
        )
        """
    )

    # create customers table used by convert endpoint
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id VARCHAR(10) PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            PhoneNumber VARCHAR(20) NOT NULL,
            Email VARCHAR(255) NOT NULL,
            Source VARCHAR(255),
            Budget INT,
            Notes TEXT
        )
        """
    )

    conn.commit()
    cursor.close()
    conn.close()