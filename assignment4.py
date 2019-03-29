import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import folium
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
    #connection.row_factory ==sqlite3.Row
    #cursor = connection.cursor()
    startyear=int(input("Enter start year (YYYY):"))
    endyear=int(input("Enter end year (YYYY):"))
    crimetype=input("Enter crime type:")
    #df=pd.read_sql_query("SELECT SUM(Incidents_Count), Month FROM crime_incidents WHERE Crime_Type=:crimetype AND YEAR>=:startyear AND YEAR <=:endyear GROUP BY Month;",{"crimetype":crimetype,"startyear":startyear,"endyear":endyear},connection)
    cursor.execute("SELECT SUM(Incidents_Count), Month FROM crime_incidents WHERE Crime_Type=:crimetype AND YEAR>=:startyear AND YEAR <=:endyear GROUP BY Month;",{"crimetype":crimetype,"startyear":startyear,"endyear":endyear})
    df = pd.DataFrame(cursor.fetchall())  
    plot=df.plot.bar(x="Month")
    plot.set_xlabel("Month")
    plt.plot()
    plt.show()
    input('Please press enter to continue')   

def task2():
    global connection, cursor
    N = int(input("Enter number of locations: "))
    cursor.execute("SELECT p.Neighbourhood_Name, (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) AS 'Tot' , c.Latitude, c.Longitude FROM population p, coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name AND Tot != 0 AND c.Latitude != 0 ORDER BY Tot DESC LIMIT :number;", {"number": N}) 
    top = cursor.fetchall() 
    cursor.execute("SELECT p.Neighbourhood_Name, (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) AS 'Tott' , c.Latitude, c.Longitude FROM population p, coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name AND Tott != 0 AND c.Latitude != 0 ORDER BY Tott LIMIT :number;", {"number": N}) 
    bottom = cursor.fetchall()

    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)

    for spot in top:
        folium.Circle(location=[spot[2],spot[3]], popup= spot[0] +"<br>"+ str(spot[1]), radius= spot[1]/7, color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
   
    for spot in bottom:
        folium.Circle(location=[spot[2],spot[3]], popup= spot[0] +"<br>"+ str(spot[1]), radius= spot[1], color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
   
    m.save("sample_marker.html")

def main():
    #creates the database
    path = "./a4-sampled.db"
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
