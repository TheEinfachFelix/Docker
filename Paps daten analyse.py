from influxdb import InfluxDBClient
import json 
from datetime import datetime
import time

start_time = datetime.now()

def convert_to_UNIX (i):
    date_time = datetime(int(i[0] + i[1] + i[2] + i[3]),
               int(i[5] + i[6]),
               int(i[8] + i[9]),
               int(i[11] + i[12]),
               int(i[14] + i[15]),
               int(i[17] + i[18]),
               int(i[20] + i[21] + i[22] + i[23] + i[24] + i[25]))

    return((time.mktime(date_time.timetuple())*1e3 + date_time.microsecond/1e3)*9000)
    #return (int(time.mktime(datetime.fromisoformat(i).timetuple())))

client = InfluxDBClient(host='192.168.178.83', port=8086)
client.switch_database("home_assistant")

Consum_Query = 'SELECT value FROM W WHERE entity_id = \'e3dc_power_consumption\'ORDER BY time DESC;'
Grid_Query = 'SELECT value FROM W WHERE entity_id = \'e3dc_power_grid_in\'ORDER BY time DESC; '

#SELECT value FROM "sensor.e3dc_power_grid" ORDER BY time DESC;

data_Consum = str(client.query(Consum_Query))
data_Grid = str(client.query(Grid_Query))

#print(data_Grid)

# clean for parser
data_Consum = data_Consum.replace("ResultSet({'('W', None)': ","").replace("})","").replace("\'", "\"").replace("Z","")
data_Grid = data_Grid.replace("ResultSet({'('W', None)': ","").replace("})","").replace("\'", "\"").replace("Z","")


# Parser
decode_data_Consum = json.loads(str(data_Consum))
decode_data_Grid = json.loads(str(data_Grid))

# counts the power consumed for self test
power_consumed_total = 0
one_higher = convert_to_UNIX(decode_data_Grid[0]["time"])
for index,wert in enumerate(decode_data_Grid):
    power_consumed_total = power_consumed_total + (abs(decode_data_Grid[index]["value"])*abs((one_higher - convert_to_UNIX(decode_data_Grid[index]["time"]))/(60*60)))
    one_higher = convert_to_UNIX(decode_data_Grid[index]["time"])
    print(abs((one_higher - convert_to_UNIX(decode_data_Grid[index]["time"]))/(60*60)))


power_consumed = 0
for index_consum,wert_consum in enumerate(decode_data_Consum):
    distance = 99999999999999999999999
    distance_to = 0
    if decode_data_Consum[index_consum]["value"] >= 900:

        #print(decode_data_Consum[index_consum]["value"])
        for index_grid,wert_grid in enumerate(decode_data_Grid):
            #print("b")
            if distance > abs(convert_to_UNIX(decode_data_Grid[index_grid]["time"]) - convert_to_UNIX(decode_data_Consum[index_consum]["time"])):
                one_higher = convert_to_UNIX(decode_data_Grid[distance_to]["time"])
                distance_to = index_grid
                
                distance = abs(convert_to_UNIX(decode_data_Consum[index_consum]["time"]) - convert_to_UNIX(decode_data_Grid[index_grid]["time"]))
                #print("")
                #print(distance_to)
                #print(distance)
                #print(abs((one_higher - convert_to_UNIX(decode_data_Grid[distance_to]["time"]))/(60*60)))  ####### das ist gaube ich das problem gute nacht
                
   
        power_consumed = power_consumed + (abs(decode_data_Grid[distance_to]["value"])*abs((one_higher - convert_to_UNIX(decode_data_Grid[distance_to]["time"]))/(60*60)))
    #print(index_consum)



    
print(power_consumed/10000000) #106041369.91350251  40303402.179463275 4503.313516190337 28030.020619451854

print(power_consumed_total/10000000)


#print(convert_to_UNIX(decode_data_Grid[0]["time"]))
#print((decode_data_Grid[0]["time"]))
#
#print(power_consumed /1000000 + 744.1)


# start 744.1 now 1899.4 

#print(decode_data_Grid[1500]["value"])


#print(len(data_Consum))
#print(len(data_Grid))
#
#print(data_Consum.count("}, {"))
#
#print(len(str(data_Grid[80])))


 

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