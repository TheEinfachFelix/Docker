from influxdb import InfluxDBClient
import json 
from datetime import datetime
import time

start_time = datetime.now()

def convert_to_UNIX (i):
    return (int(time.mktime(datetime.fromisoformat(i).timetuple())))

client = InfluxDBClient(host='192.168.178.83', port=8086)
client.switch_database("home_assistant")

Consum_Query = 'SELECT value FROM W WHERE entity_id = \'e3dc_power_consumption\'ORDER BY time DESC;'
Grid_Query = 'SELECT value FROM "sensor.e3dc_power_grid" ORDER BY time DESC;'

data_Consum = str(client.query(Consum_Query))
data_Grid = str(client.query(Grid_Query))


# clean for parser
data_Consum = data_Consum.replace("ResultSet({'('W', None)': ","").replace("})","").replace("\'", "\"").replace("Z","")
data_Grid = data_Grid.replace("ResultSet({'('sensor.e3dc_power_grid', None)': ","").replace("})","").replace("\'", "\"").replace("Z","")

# Parser
decode_data_Consum = json.loads(str(data_Consum))
decode_data_Grid = json.loads(str(data_Grid))

print(data_Grid.count("}, {"))

print(data_Grid[5])
r = 0
f = 0
i = 0


 

#print(datetime.fromtimestamp(time))



print(r)
print(f)
print(decode_data_Grid[i])
print(i)
#print(data_Consum)
#print(decode_data_Consum[1]["value"])

#print(data_Consum)
#print(len(data_Consum))
#print(len(data_Grid))


# e3dc_energy_grid_in 2
# e3dc_energy_consumption 1
# e3dc_energy_solar
# e3dc_power_consumption

#sensor.e3dc_power_grid

## 1 und 2 nach der zeit matchen
## wenn 1 > x dann 
## 2 finden und zeit zum nächsten datenpunkt notieren
## 2 zusammenzählen
# 
# 
# #query = 'SELECT value FROM kWh WHERE entity_id = \'e3dc_energy_consumption\' and value > 9 limit 5;'
#query = 'SELECT value FROM "sensor.e3dc_power_grid" WHERE value > 9000 limit 5'
#query = 'SELECT value FROM "sensor.e3dc_power_grid" WHERE value > 9000 UNION SELECT value FROM kWh WHERE entity_id = \'e3dc_energy_consumption\' and value > 9 limit 5;'
#query = 'SELECT value FROM kWh WHERE entity_id = \'e3dc_energy_consumption\' and value > 9 limit 5;SELECT value FROM "sensor.e3dc_power_grid" WHERE value > 9000 limit 5;'
#query = 'SELECT value FROM (SELECT value FROM "sensor.e3dc_power_grid" WHERE value > 9000 limit 50) , (SELECT value FROM kWh WHERE entity_id = \'e3dc_energy_consumption\' and value > 9 limit 50) ORDER BY time DESC'

print("Runtime: " + str(datetime.now() - start_time))