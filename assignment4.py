import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
connection = None
cursor = None

#connect sqlite and the python code 
def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return
def task1():
    global connection, cursor
    startyear=int(input("Enter start year (YYYY):"))
    endyear=int(input("Enter end year (YYYY):"))
    crimetype=input("Enter crime type:")
    df=pd.read_sql_query('SELECT SUM(Incidents_Count) FROM crime_incidents WHERE Crime_Type=crimetype AND YEAR>=startyear AND YEAR <=endyear GROUP BY Month;',{"crimetype":crimetype,"startyear":startyear,"endyear":endyear})
    plot=df.plot.bar(x='Month')
    plt.plot()
    plt.show()
    input('Please press enter to continue')
def main():
    #creates the database
    path = "a4.db"
    connect(path)
    #bool value to exit program
    endGame = False    
    #all the tasks explanations
    tasklist=['1: Q1','2: Q2','3: Q3','4: Q4','E: Exit']
    task1()
    connection.commit()
    connection.close()
    return    
    
if __name__ == "__main__":
    main()    
