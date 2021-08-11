from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
import json

#LOAD .ENV TO ENVIRONMENT
load_dotenv()

# DATABASE CONFIGURATIONS
db_name = getenv('DB_NAME')
db_user = getenv('DB_USER')
db_pass = getenv('DB_PASS')
db_host = getenv('DB_HOST')
db_port = getenv('DB_PORT')

# CONNECTING TO POSTGRES DATABASE
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

# CREATE INTERFACE TABLE IF IT DOESN'T EXIST
def create_tables():
    db.execute("""CREATE TABLE IF NOT EXISTS interface (
                    id SERIAL PRIMARY KEY,
                    connection INTEGER,
                    name VARCHAR(255) NOT NULL,
                    description VARCHAR(255),
                    config json,
                    type VARCHAR(50),
                    infra_type VARCHAR(50),
                    port_channel_id INTEGER,
                    max_frame_size INTEGER
                    );"""
                )

# ADD SPECIFIC INTERFACE
def add_interface(interfaces, types):
    # CLEAR TABLE IF THERE ARE ROWS
    if db.execute("SELECT * FROM interface").fetchall is not None:
        db.execute("DELETE FROM interface")

    for type in types:
        for i in interfaces[type]: 
            # CHECK IF STRING EXISTS AS KEY IN DICTIONARY
            if 'description' not in i.keys():
                i['description'] = None
            if 'mtu' not in i.keys():
                i['mtu'] = None

            # INSERT QUERY 
            db.execute("INSERT INTO interface(name, description, config, max_frame_size) " +\
                    "VALUES (%s, %s, %s, %s);", (type+str(i['name']), i['description'], json.dumps(i), i['mtu']))

    # UPDATE QUERY FOR PORT_CHANNEL_ID
    interfaces = get_column_to_update()
    for interface in interfaces:
        db.execute("UPDATE interface " +\
                "SET port_channel_id=new_data.id " +\
                "FROM (SELECT id FROM interface WHERE name=%s) new_data WHERE name=%s", ('Port-channel'+interface['description'][-2:], interface['name']))

# UPDATE PORT_CHANNEL_ID COLUMN
def get_column_to_update():
    result = db.execute("SELECT id, name, description FROM interface").fetchall()
    interfaces = []
    for interface in result:
        if interface['description'] is not None:
            if 'Portchannel' in interface['description']:
                interfaces.append(interface)
    return interfaces

# SELECT QUERY 
def get_interfaces():
    return db.execute("SELECT * FROM interface").fetchall()