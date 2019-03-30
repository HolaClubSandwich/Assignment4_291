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

def task1(count):
    global connection, cursor
    #take input of start_year,end_year and crime_type
    startyear = int(input("Enter start year (YYYY): "))
    endyear = int(input("Enter end year (YYYY): "))
    crimetype = input("Enter crime type: ")
    #SQL STATAMENT TO GET THE HOW MANY TIMES A CRTIME HAPPENS IN THE RANGE GIVEN
    cursor.execute("SELECT SUM(Incidents_Count), Month FROM crime_incidents WHERE Crime_Type=:crimetype AND YEAR>=:startyear AND YEAR <=:endyear GROUP BY Month;",{"crimetype":crimetype,"startyear":startyear,"endyear":endyear})
    #Plot the graph and save it in the same folder as the assignment.
    df = pd.DataFrame(cursor.fetchall())  
    #plots the month as the x-axis
    plot = df.plot.bar(x = 1)
    plot.set_xlabel("Month")
    #changes the legend to count
    plot.legend(['count'])
    plt.plot()
    #save as we go
    plt.savefig("Q1-"+str(count)+".png")
    plt.show()    


def task2(count):
    global connection, cursor
    #asks the user for a number of locations
    N = int(input("Enter number of locations: "))
    #runs a query to find the 3 most populous locations in edmonton returning their name, population, and coordinates
    cursor.execute("SELECT p.Neighbourhood_Name, (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) AS 'Tot' , c.Latitude, c.Longitude FROM population p, coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name AND Tot != 0 AND c.Latitude != 0 ORDER BY Tot DESC;") 
    top = cursor.fetchall() 
    #runs a query to find the 3 least populous location in edmonton returning their name, population, and coordinates
    cursor.execute("SELECT p.Neighbourhood_Name, (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) AS 'Tott' , c.Latitude, c.Longitude FROM population p, coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name AND Tott != 0 AND c.Latitude != 0 ORDER BY Tott;") 
    bottom = cursor.fetchall()
    #instantiates the map of edmonton
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)
    #creates markers for the top 3 populations in edmonton
    index = 0
    population = 0
    position = 0
    while index != N:
        folium.Circle(location=[top[position][2],top[position][3]], popup= top[position][0] +"<br>"+ str(top[position][1]), radius= top[position][1]/7, color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
        #includes ties
        if population != top[position][1]:
            index += 1
            population = top[position][1]
        position += 1 
    #creates markers for the bottom 3 populations in edmonton
    index2 = 0
    population2 = 0
    position2 = 0
    while index2 != N:
        folium.Circle(location=[bottom[position2][2],bottom[position2][3]], popup= bottom[position2][0] +"<br>"+ str(bottom[position2][1]), radius= bottom[position2][1], color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
        #includes ties
        if population2 != bottom[position2][1]:
            index2 += 1
            population2 = bottom[position2][1]
        position2 += 1
    #saves the positions on the map
    m.save("Q2-"+str(count)+".html")

def task3(count):
    global connection, cursor
    #asks the user for a year range, type of crime, and number of locations
    start_year = int(input("Enter start year (YYYY): "))
    end_year = int(input("Enter end year (YYYY): "))
    crime = input("Enter a crime type: ")
    N = int(input("Enter number of locations: "))
    #runs a query to find the top N locations where the specific crime in the year range is highest
    cursor.execute("SELECT cr.Crime_Type, SUM(cr.Incidents_Count), cr.Neighbourhood_Name, co.Latitude, co.Longitude FROM crime_incidents cr, coordinates co WHERE cr.Crime_Type = :crime AND cr.Year >= :year1 AND cr.Year <= :year2 AND cr.Neighbourhood_Name = co.Neighbourhood_Name GROUP BY cr.Neighbourhood_Name ORDER BY SUM(cr.Incidents_Count) DESC ;", {"crime": crime, "year1": start_year, "year2": end_year}) 
    top = cursor.fetchall() 
    #creates the base map of edmonton
    m = folium.Map(location=[53.532407, -113.493805], zoom_start=12)
    #plots the top N points on the map including information such as neighbourhood names and number of the specific crime
    index = 0
    incident_count = 0
    position = 0
    while index != N:
        folium.Circle(location=[top[position][3],top[position][4]], popup= top[position][2] +"<br>"+ str(top[position][1]), radius= top[position][1]*7, color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
        #includes ties
        if incident_count != top[position][1]: 
            index += 1
            incident_count = top[position][1]
        position += 1  
    #saves the uodated map
    m.save("Q3-"+str(count)+".html")

def task4(count):
    global connection, cursor
    #asks the user for a year range, and number of locations
    start_year = int(input("Enter start year (YYYY): "))
    end_year = int(input("Enter end year (YYYY): "))
    N = int(input("Enter number of locations: "))
    #finds the neighbourhood name 
    cursor.execute("SELECT p.Neighbourhood_Name, SUM(c.Incidents_Count), CAST(SUM(c.Incidents_Count) AS float) / CAST((p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) AS float) AS 'Ratio', (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) AS 'Pop', co.Latitude, co.Longitude FROM crime_incidents c, population p, coordinates co WHERE Pop != 0 AND c.Year >= :year1 AND c.Year <= :year2 AND p.Neighbourhood_Name = c.Neighbourhood_Name AND c.Neighbourhood_Name = co.Neighbourhood_Name GROUP BY p.Neighbourhood_Name ORDER BY ratio DESC LIMIT :number;", {"year1": start_year, "year2": end_year, "number": N})
    locations = cursor.fetchall()
    m = folium.Map(location=[53.532407, -113.493805], zoom_start=12)
    #adds markers to the map showing the neighbourhood_name, most common crime type, and the ratio of crime to population
    index = 0
    ratio = 0
    position = 0   
    while index != N:
        index2 = 0
        incident_count = 0
        position2 = 0
        crime_type = ''
        #query to find the most common crime in an area
        cursor.execute("SELECT Crime_Type, SUM(Incidents_count)as 'tot' FROM crime_incidents WHERE Neighbourhood_Name = :location GROUP BY Crime_Type ORDER BY tot DESC;", {"location":locations[position][0]})
        crime = cursor.fetchall()
        while index2 != 1:
            #makes sure if two crimes are both as common to list both
            if crime[position2][1] != incident_count:
                index2 += 1
                incident_count = crime[position2][1]
            crime_type += crime[position2][0]
         
        folium.Circle(location=[locations[position][4],locations[position][5]], popup= locations[position][0] +"<br>"+ crime_type + "<br>" + str(locations[position][2]), radius= locations[position][2]*600, color= 'crimson', fill= True, fill_color= "crimson").add_to(m)
        #makes sure that duplicate ratios will be counted
        if ratio != locations[position][1]: 
            index += 1
            ratio = locations[position][1]
        position += 1   
    #saves the marked positions on the map
    m.save("Q4-"+str(count)+".html")
       
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
    while not endGame:
        for i in tasklist:
            print(i)
        choice = input('Enter your choice: ')
        if (choice == '1'):
            count1 += 1
            task1(count1)
        elif (choice == '2'):
            count2 += 1
            task2(count2) 
        elif (choice == '3'):
            count3 += 1
            task3(count3)
        elif (choice == '4'):
            count4 += 1
            task4(count4)
        elif (choice == 'E'):
            endGame = True
    connection.commit()
    connection.close()
    return    
    
if __name__ == "__main__":
    main()    
