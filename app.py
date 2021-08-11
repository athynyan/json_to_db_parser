import json
import db

config_file = 'configClear_v2.json'
config = [
    'frinx-uniconfig-topology:configuration',
    'Cisco-IOS-XE-native:native',
    'interface'
]
interface_type = [
    'Port-channel',
    'TenGigabitEthernet',
    'GigabitEthernet'
]
data = None

# LOAD JSON FROM FILE
def load_json_file(name):
    with open(name) as json_file:
        return json.load(json_file)

# GET INTERFACES AND THEIR CONFIGURATIONS FROM 
def get_interface_configuration(interface):
    if data is None:
        return None
    return [configuration for configuration in data[interface]]

if __name__=='__main__':
    # CREATE A NEW TABLE IF IT DOESN'T EXISTS
    db.create_tables()

    # INITIALIZE NEW DICTIONARY FOR INTERFACES
    interfaces = {}

    # LOAD JSON FROM CONFIG_FILE AND PULL INTERFACE INFO FROM IT 
    data = load_json_file(config_file)[config[0]][config[1]][config[2]]

    # PULL SPECIFIC INTERFACE TYPE FROM DATA
    for type in interface_type:
        interfaces[type] = get_interface_configuration(type)
    
    # ADD INTERFACE TO DATABASE
    db.add_interface(interfaces, interface_type)

    for i in db.get_interfaces():
        print(i['name'])