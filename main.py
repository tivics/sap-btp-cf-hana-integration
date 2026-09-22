from flask import Flask
from dotenv import load_dotenv
import os
import pandas as pd
from hana_ml import ConnectionContext
from hana_ml import create_dataframe_from_pandas

load_dotenv()
app = Flask(__name__)

# Example route to test the HANA connection and write an example DataFrame
@app.route("/run", methods=["POST"])
def run():
    conn = get_hana_connection()

    # Example DataFrame to write to HANA
    data = {
        "order_id": [1001, 1002, 1003],
        "customer_name": ["Muster GmbH", "Beispiel AG", "Example KG"],
        "amount_eur": [15230.50, 8990.00, 4200.75]
    }
    df = pd.DataFrame(data)

    write_dataframe_to_hana(df, "SALES_ORDERS")  # Write the DataFrame to HANA

    return "Connected to HANA database successfully!"

# Common function to get HANA connection
def get_hana_connection():
    # Get the HANA connection parameters from environment variables
    hana_host = os.getenv("HANA_HOST")
    hana_port = os.getenv("HANA_PORT")
    hana_user = os.getenv("HANA_USER")
    hana_password = os.getenv("HANA_PASSWORD")

    # Create a connection to the HANA database
    conn = ConnectionContext(hana_host, hana_port, hana_user, hana_password)

    return conn

# Common function to write a DataFrame to HANA
def write_dataframe_to_hana(df, table_name):
    conn = get_hana_connection()
    hana_df = create_dataframe_from_pandas(conn, df)
    hana_df.save(table_name, force=True)  # Save the DataFrame to HANA

# main.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)