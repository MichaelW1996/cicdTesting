import os
from dotenv import load_dotenv
import psycopg2
###pip install psycopg2-binary

# Setup
def init_sql():
    load_dotenv()

def get_db_connection():
    host_name = os.environ.get("POSTGRES_HOST")
    database_name = os.environ.get("POSTGRES_DB")
    user_name = os.environ.get("POSTGRES_USER")
    user_password = os.environ.get("POSTGRES_PASSWORD")

    if not all([host_name, database_name, user_name, user_password]):
        raise ValueError("Database credentials are not fully set in the environment variables.")

    connection = psycopg2.connect(
        host=host_name,
        database=database_name,
        user=user_name,
        password=user_password,
        port=os.environ.get("POSTGRES_PORT", "5432")  # Default to 5432 if POSTGRES_PORT is not set
    )
    return connection

def setup_database(db_schema: dict):
    try:
        # Connect to the server (without specifying a database)
        connection = get_db_connection()
        database_name = os.getenv("POSTGRES_DB")

        with connection:
            with connection.cursor() as cursor:
                # Check if the database exists
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
                result = cursor.fetchone()

                if result:
                    # Database exists, ask user to confirm it is safe to continue
                    response = input(f"The database {database_name} exists. Are you sure it is empty? (yes/no): ").strip().lower()
                    if response != 'yes' and response != 'y':
                        # User does not want to run the schema
                        print("User did not want to continue to implement the schema.")
                        return
                else:
                    print("Database does not exist. Cannot implement schema. To continue, please create the database {database_name}.")
                    return

        # Connect to the new database
        connection = get_db_connection()

        with connection:
            with connection.cursor() as cursor:
                # Create tables based on the provided schema
                for table_name in db_schema.keys():
                    fields = db_schema[table_name]["Fields"]
                    field_definitions = [f"{field[0]} {field[1]}" for field in fields]
                    fields_str = ", ".join(field_definitions)

                    constraints = db_schema[table_name].get("Constraints", [])
                    constraints_str = ", ".join(constraints) if constraints else ""

                    create_table_query = f"CREATE TABLE {table_name} ({fields_str}{(', ' + constraints_str) if constraints_str else ''})"
                    
                    print(f"\n\n{create_table_query}\n\n")
                    
                    cursor.execute(create_table_query)
                    print(f"Table {table_name} created with fields and constraints:\n{fields_str}, {constraints_str}\n")

                connection.commit()
                print("Database setup completed.")

    except psycopg2.Error as e:
        raise Exception(f"Error setting up the database: {e}")

# Example usage / product_name, product_price, available_stock
if __name__ == '__main__':
    init_sql()
    db_schema = {
         "Orders": {
            "Fields" : [
                ("order_id", "SERIAL PRIMARY KEY"),
                ("date_time", "TIMESTAMP"),
                ("branch_location", "VARCHAR(100)"),
                ("payment_total", "INT"),
                ("payment_type", "VARCHAR(4)"),
            ],
            "Constraints" : []
        },
       
        "Products": {
            "Fields" : [
                ("product_id", "SERIAL PRIMARY KEY"),
                ("name","VARCHAR(100)"),
                ("size", "VARCHAR(100)"),
                ("price", "INT"),
               
            ],
            "Constraints" : []    
       
        },
 
        "Order_Products": {
            "Fields" : [
                ("order_products_id", "SERIAL NOT NULL"),        
                ("product_id", "INT NOT NULL"),
                ("order_id", "INT NOT NULL"),
            ],
            "Constraints" : [
                "PRIMARY KEY (order_products_id)",
                "FOREIGN KEY (order_id) REFERENCES Orders(order_id)",
                "FOREIGN KEY (product_id) REFERENCES Products(product_id)",
            ]
        }
    }
    setup_database(db_schema)

