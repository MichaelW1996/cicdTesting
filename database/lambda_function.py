import boto3
import csv
import json
import psycopg2

from extract_load_transform.get_connections import *
import os

# Name of the environment variable which has the SSM parameter name as its value.
# The SSM parameter name will be "<team name>_redshift_settings".
ssm_env_var_name = 'ssm_env_var_name'

last_order = 0
product_table=[]

def convert_csv(file):
    list_type= list()
    id = 0 
    try:
        for row in csv.DictReader(file, fieldnames = ['date_time', 'branch_location', 'customer_name', 'order_details_string', 'payment_total', 'payment_type', 'card_number']):
            row_cleaned = row
            row_cleaned['id'] = id
            del row_cleaned['card_number'] # remove card number field
            del row_cleaned['customer_name'] # remove name
            list_type.append(row_cleaned)
            id += 1
        return list_type
        #Try to catch common errors then have a catchall for any other errors
    except KeyError as e:
        raise Exception(f"Key not found: {e}")
    except ValueError as e:
        raise Exception(f"Value error: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
        
def first_nf(dict_list):
    output_dict_list = []   
    try:
        for dict in dict_list:
            product_list = dict['order_details_string'].split(',') 
            dict['order_details_string'] = product_list
            for product in product_list:
                new_dict = dict.copy()
                new_dict['order_details_string'] = product
                output_dict_list.append(new_dict)
        return output_dict_list
    except KeyError as e:
        raise Exception(f"Key not found: {e}")
    except ValueError as e:
        raise Exception(f"Value error: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
        

def second_nf(dict_list):
    try:
        for dict in dict_list:
            product = dict['order_details_string']
            product_list = product.split('-')
            product_name = '-'.join(product_list[0:-1]).strip()
            product_price = product_list[-1].strip()
            dict['product_name'] = product_name
            dict['product_price'] = product_price
            del dict['order_details_string']
        return dict_list
    except KeyError as e:
        raise Exception(f"Key not found: {e}")
    except ValueError as e:
        raise Exception(f"Value error: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
        

def third_nf(data):
    order_table = []
    order_products = []
    product_id = 0
    try:
        # loop through the data
        for entry in data:
            order_id = entry['id']

            #  Create dictionary for orders
            #  Check if order already exists in order_table
            order_exists = False
            for order in order_table:
                if order['order_id'] == order_id:
                    order_exists = True
                    break
            if not order_exists:
                order_table.append({
                    'order_id': order_id,
                    'date_time': entry['date_time'],
                    'branch_location': entry['branch_location'],
                    'payment_total':int(float(entry['payment_total'])*100),
                    'payment_type': entry['payment_type']
                })

            # split products to name and size
            prod_split = entry['product_name'].split(' ', 1)
            entry_product_size = prod_split[0]
            entry_product_name = prod_split[1]

            # Check if the product already exists in product_table
            product_exists = False
            for product in product_table:
                if product['name'] == entry_product_name and product['size'] == entry_product_size:
                    product_exists = True
                    break

            # Add new product if it's not already in product_table
            if not product_exists:
                product_table.append({
                    'product_id': product_id,
                    'name': entry_product_name,
                    'size': entry_product_size,
                    'price': int(float(entry['product_price'])*100)
                })
                product_id += 1
            
            # get product id for current record based on product_name and product_size
            for product in product_table:
                if product['name'] == entry_product_name and product['size'] == entry_product_size:
                    current_product_id = product['product_id']
                    break
            order_products.append({
                'order_id': order_id,
                'product_id': current_product_id
            })


        return order_table, product_table, order_products
    except KeyError as e:
        raise Exception(f"Key not found: {e}")
    except ValueError as e:
        raise Exception(f"Value error: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
        

        
def load_orders(connection, orders): 
    try:
        with connection:
            with connection.cursor() as cursor:
                add_sql = "INSERT INTO orders (order_id, date_time, branch_location, payment_total, payment_type) VALUES "
                values =[]
                for item in orders:
                    query_string= f"('{item['order_id']}','{item['date_time']}', '{item['branch_location']}', '{item['payment_total']}', '{item['payment_type']}')"
                    values.append(query_string)
                add_sql+= ", ".join(values) +";"
                cursor.execute(add_sql)
                connection.commit()
    except psycopg2.errors.UndefinedTable as e:
        raise Exception(f"Table not found: {e}")
        
def load_products(connection,products):
    try:
        with connection:
            with connection.cursor() as cursor:
                add_sql = "INSERT INTO products (product_id, name, size, price) VALUES " 
                values = []
                for item in products:
                    query_string = f"('{item['product_id']}', '{item['name']}', '{item['size']}', '{item['price']}')"
                    values.append(query_string)
                add_sql+=", ".join(values) + ";"
                cursor.execute(add_sql)
                connection.commit()
    except psycopg2.errors.UndefinedTable as e:
        raise Exception(f"Table not found: {e}")

 
def load_order_products(connection,order_products):
    try: 
        with connection:
            with connection.cursor() as cursor:
                add_sql = "INSERT INTO order_products (product_id, order_id) VALUES "
                values=[]
                for item in order_products:
                    query_string=f"('{item['product_id']}', '{item['order_id']}')"
                    values.append(query_string)
                add_sql+= ", ".join(values) +";"
                cursor.execute(add_sql)
                connection.commit()
    except psycopg2.errors.UndefinedTable as e:
        raise Exception(f"Table not found: {e}")


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    #Read the CSV file from S3
    obj = s3.get_object(Bucket=bucket, Key=key)
    file = obj['Body'].read().decode('utf-8').split('\n')
    data = convert_csv(file)


    try:

        ssm_param_name = os.environ[ssm_env_var_name] or 'NOT_SET'
        print(f'lambda_handler: ssm_param_name={ssm_param_name} from ssm_env_var_name={ssm_env_var_name}')

        # connection
        redshift_details = get_ssm_param(ssm_param_name)
        conn, cur = open_sql_database_connection_and_cursor(redshift_details)
        
        # Fetch the last ID from the "order" table
        cur.execute("SELECT MAX(order_id) FROM orders")
        last_order = cur.fetchone()[0] or 0
        # Fetch the last ID from the "products" table
        cur.execute("SELECT * FROM products")
        product_columns = [desc[0] for desc in cur.description]
        global product_table
        product_table = [dict(zip(product_columns, row)) for row in cur.fetchall()]


        
        output = third_nf(second_nf(first_nf(data)))
        orders=output[0]
        products=output[1]
        order_products=output[2]
        load_orders(conn, orders)
        load_products(conn, products)
        load_order_products(conn,order_products)
        cur.close()
        conn.close()


        print(f'lambda_handler: done')

    except Exception as whoopsy:
        # ...exception reporting
        print(f'lambda_handler: failure, error=${whoopsy}')
        raise whoopsy
        
