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
    path = "./a4.db"
    connect(path)
    #bool value to exit program
    endGame = False    
    #all the tasks explanations
    tasklist=['1: Q1','2: Q2','3: Q3','4: Q4','E: Exit']
    while not endGame:
        for i in tasklist:
            print(i)
        select=input("Enter your choice: ")
        if (select=='1'):
            task1()
            print('')
        elif(select=='2'):
            task2()
            print('')
        elif(select=='3'):
            task3()
            print('')
        elif(select=='4'):
            task4()
            print('')
        elif(select=='Exit'):
            endGame=True
        else:
            print('')
            print('Please enter a correct command.')
            print('')                
    
    connection.commit()
    connection.close()
    return    
    
if __name__ == "__main__":
    main()    
