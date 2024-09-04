import mysql.connector
import streamlit

#connecting

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 db="redbus"
 
 )

mycursor = mydb.cursor()
def view_ll_data():
    mycursor.execute("select * from busdettable order by ID asc")
    data=mycursor.fetchall()
    return data
