#ask the TA how to save bar plot 
#ask the TA why months start at 0 
#ask the TA about data not entered
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
    startyear = int(input("Enter start year (YYYY): "))
    endyear = int(input("Enter end year (YYYY): "))
    crimetype = input("Enter crime type: ")
    #df=pd.read_sql_query("SELECT SUM(Incidents_Count), Month FROM crime_incidents WHERE Crime_Type=:crimetype AND YEAR>=:startyear AND YEAR <=:endyear GROUP BY Month;",{"crimetype":crimetype,"startyear":startyear,"endyear":endyear},connection)
    cursor.execute("SELECT SUM(Incidents_Count), Month FROM crime_incidents WHERE Crime_Type=:crimetype AND YEAR>=:startyear AND YEAR <=:endyear GROUP BY Month;",{"crimetype":crimetype,"startyear":startyear,"endyear":endyear})
    df = pd.DataFrame(cursor.fetchall())  
    plot = df.plot.bar(x = "Month")
    plot.set_xlabel("Month")
    plt.plot()
    plt.show()  


def task2(count):
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
   
    m.save("Q2-"+str(count)+".html")

def task3(count):
    global connection, cursor
    #asks the user for a year range, type of crime, and number of locations
    start_year = int(input("Enter start year (YYYY): "))
    end_year = int(input("Enter end year (YYYY): "))
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
    m.save("Q3-"+str(count)+".html")

def main():
    #creates the database
    path = "a4.db"
    connect(path)
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    #bool value to exit program
    endGame = False    
    #all the tasks explanations
    tasklist = ['1: Q1','2: Q2','3: Q3','4: Q4','E: Exit']
    for i in tasklist:
        print(i)
    while not endGame:
        choice = input('Enter your choice: ')
        if (choice == '1'):
            task1()
        elif (choice == '2'):
            count2 += 1
            task2(count2) 
        elif (choice == '3'):
            count3 += 1
            task3(count3)
        elif (choice == 'E'):
            endGame = True
    connection.commit()
    connection.close()
    return    
    
if __name__ == "__main__":
    main()    
   
