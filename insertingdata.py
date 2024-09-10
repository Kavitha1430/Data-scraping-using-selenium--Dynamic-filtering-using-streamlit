import pandas as pd
df_bus=pd.read_csv(r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\allbus_bus_details2.csv")
df_bus

#changing datatypes
df_bus["departing_time"] = pd.to_datetime(df_bus["departing_time"], format="%H:%M", errors='coerce').dt.time
df_bus["departing_time"].dtype

#reaching time
df_bus["reaching_time"] = pd.to_datetime(df_bus["reaching_time"], format="%H:%M", errors='coerce').dt.time
df_bus["reaching_time"].dtype

#price removing INR
df_bus["price"]=df_bus["price"].str.replace("INR","")
df_bus["price"]=df_bus["price"].astype(float)
df_bus

#checking info for null values
df_bus.info()

#mysql connection
pip install mysql-connector-python
import mysql.connector


mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",


)
print(mydb)
mycursor = mydb.cursor(buffered=True)

#creating table

mycursor.execute('''CREATE TABLE redbus.busdettable (
                  ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                  busname VARCHAR(50) NOT NULL ,
                  bustype VARCHAR(50) NOT NULL,
                  departing_time TIME NOT NULL,
                  reaching_time TIME NOT NULL ,
                  duration VARCHAR(50) NOT NULL,
                  Price FLOAT NULL,
                  Seats_Available INT NOT NULL ,
                  star_ratings Float NULL ,
                  Route_name VARCHAR(200) NULL ,
                  Route_link VARCHAR(200) NULL
                  )''')
print("Table Created")

#selecting database
mycursor.execute("use redbus")

import numpy as np

df_bus= df_bus.replace({np.nan: None})

#inserting data into the database

insert_query = '''INSERT INTO busdettable(
                    busname  ,
                    bustype  ,
                    departing_time ,
                    duration  ,
                    reaching_time  ,
                    price ,
                    Seats_Available,
                    star_ratings ,
                    Route_name,
                    Route_link
                     ) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
data = df_bus.values.tolist()

mycursor.executemany(insert_query, data)

mydb.commit()

print("Table updated")
