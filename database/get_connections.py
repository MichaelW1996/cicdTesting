import psycopg2 as psy
import boto3
import json

ssm_client = boto3.client('ssm')

# Get the SSM Param from AWS and turn it into JSON
# Don't log the password!
def get_ssm_param(param_name):
    print(f'get_ssm_param: getting param_name={param_name}')
    parameter_details = ssm_client.get_parameter(Name=param_name)
    redshift_details = json.loads(parameter_details['Parameter']['Value'])

    # The JSON should have this structure:
    # {
    #   "database-name": "<team name>_cafe_db",
    #   "host": "<redshift address>.eu-west-1.redshift.amazonaws.com",
    #   "port": 5439,
    #   "password": "<password>",
    #   "user": "<team name>_user"
    # }

    host = redshift_details['host']
    user = redshift_details['user']
    db = redshift_details['database-name']
    port = redshift_details['port']
    print(f'get_ssm_param loaded for db={db}, user={user}, host={host}, port={port}')
    return redshift_details

# Use the redshift details json to connect
def open_sql_database_connection_and_cursor(redshift_details):
    try:
        print('open_sql_database_connection_and_cursor: new connection starting...')
        db_connection = psy.connect(host=redshift_details['host'],
                                    database=redshift_details['database-name'],
                                    user=redshift_details['user'],
                                    password=redshift_details['password'],
                                    port=redshift_details['port'])
        cursor = db_connection.cursor()
        print('open_sql_database_connection_and_cursor: connection ready')
        return db_connection, cursor
    except ConnectionError as ex:
        print(f'open_sql_database_connection_and_cursor: failed to open connection: {ex}')
        raise ex
