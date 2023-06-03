from influxdb import InfluxDBClient
client = InfluxDBClient(host='192.168.178.83', port=8086)
client.switch_database("iobroker")

datenquelle = "modbus.0.holdingRegisters.40070_Batterie_Leistung"
query = 'SELECT * FROM "' + datenquelle + '"'

data = str(client.query(query))
cleaner_data = data.replace("ResultSet({'('" + datenquelle + "', None)': [{","")
clean_data = cleaner_data.replace("]})","")
split_data = clean_data.split("}, {")

for index in range(len(split_data)):
    input = split_data[index]
    #print(input)
    input_split = input.split(", ")

    client.switch_database("testDB")
    value = float(input_split[4].split(": ")[1].replace("}","").replace("'",""))

    point = {
        "measurement": "test2",
        "time": input_split[0].split(": ")[1].replace("'",""),
        "fields": {
            'domain': 'sensor',
            'entity_id': 'e3dc_power_battery_old',
            'friendly_name_str': 'e3dc_power_battery_old',
            'state_class_str': 'measurement',
            "value": value,
        }
    }
    print(point)
    client.write_points(points=[point])


#client.write_points(points=[point])    
#print(client.query('SELECT * FROM "%" WHERE entity_id = \'e3dc_soc_battery\''))

#daten von iobroker
#SELECT * FROM "modbus.0.holdingRegisters.40070_Batterie_Leistung"
#{'time': '2023-04-11T08:49:55.621000Z', 'ack': True, 'from': 'system.adapter.modbus.0', 'q': 0.0, 'value': 1671.0}
#
#homeassistant
#'SELECT * FROM "%" WHERE entity_id = \'e3dc_soc_battery\''
#{'time': '2023-05-09T15:19:40.860834Z', 'domain': 'sensor', 'entity_id': 'e3dc_soc_battery', 
# 'friendly_name_str': 'e3dc_soc_battery', 'state_class_str': 'measurement', 'value': 53.0}]}
#{'time': '2023-05-09T15:19:40.860834Z', 'domain': 'sensor', 'entity_id': 'e3dc_soc_battery', 'friendly_name_str': 'e3dc_soc_battery', 'state_class_str': 'measurement', 'value': 53.0}]}
#{'time': '2023-04-11T08:49:55.621000Z', 'domain': 'sensor', 'entity_id': 'e3dc_soc_battery', 'friendly_name_str': 'e3dc_soc_battery', 'state_class_str': 'measurement', 'value': '1671.0'}
#{'time': '2023-04-11T08:49:55.621000Z', 'domain': 'sensor', 'entity_id': 'e3dc_power_battery_old', 'friendly_name_str': 'e3dc_power_battery_old', 'state_class_str': 'measurement', 'value': 1671.0}}



#SELECT * INTO "testDB"."autogen".:MEASUREMENT FROM "home_assistant"."autogen"./.*/ GROUP BY *   