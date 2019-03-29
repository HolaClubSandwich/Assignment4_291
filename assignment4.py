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

    m = folium.Map(location=[53.532407, -113.493805], zoom_start=12)

    for spot in top:
        folium.Circle(location=[spot[2],spot[3]], popup= spot[0] +"<br>"+ str(spot[1]), radius= spot[1]/7, color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
   
    for spot in bottom:
        folium.Circle(location=[spot[2],spot[3]], popup= spot[0] +"<br>"+ str(spot[1]), radius= spot[1], color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
   
    m.save("sample_marker.html")

def task3():
    global connection, cursor
    input("Enter")
    #asks the user for a year range, type of crime, and number of locations
    start_year = int(input("Start year: "))
    end_year = int(input("End year: "))
    crime = input("Enter a crime type: ")
    N = int(input("Enter number of locations: "))
    #runs a query to find the top N locations where the specific crime in the year range is highest
    cursor.execute("SELECT cr.Crime_Type, SUM(cr.Incidents_Count), cr.Neighbourhood_Name, co.Latitude, co.Longitude FROM crime_incidents cr, coordinates co WHERE cr.Crime_Type = :crime AND cr.Year >= :year1 AND cr.Year <= :year2 AND cr.Neighbourhood_Name = co.Neighbourhood_Name GROUP BY cr.Neighbourhood_Name ORDER BY SUM(cr.Incidents_Count) DESC Limit :number;", {"number": N, "crime": crime, "year1": start_year, "year2": end_year}) 
    top = cursor.fetchall() 
    #creates the base map of edmonton
    m = folium.Map(location=[53.532407, -113.493805], zoom_start=12)
    #plots the top N points on the map including information such as neighbourhood names and number of the specific crime
    for spot in top:
        folium.Circle(location=[spot[3],spot[4]], popup= spot[2] +"<br>"+ str(spot[1]), radius= spot[1], color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
    #saves the uodated map
    m.save("sample_marker2-.html")
    
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
