import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import forlium

connection = None
cursor = None


def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def main():
    #creates the database
    path = "./assignment3.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()
    #bool value to exit program
    endGame = False
    #all the tasks explanations
    tasklist = ['1  Show email of all reviewers that have reviewed the paper.', '2  Show all potential reviewers for that paper.', '3  Show all reviewers whose number of reviews is in the given range.', '4  Show in how many sessions do authors participate in.', '5  Show a pie chart of the top 5 most popular areas.', '6  Show a bar chart of each reviewer average review scores for each category.', '0  Exit.']
    #while the user keeps inputting enter, the program will not exit 
    #according to user input, the task is executed
    #after a task is done, the user can press enter to preform another task
    while not endGame:
        for i in tasklist:
            print(i)
        select = input('Please enter number and press enter to enter the task or exit: ')
        if (select == '1'):
            task1()
            print('')
        elif (select == '2'):
            task2()
            print('')
        elif (select == '3'):
            task3()
            print('')
        elif (select == '4'):
            task4()
            print('')
        elif (select == '5'):
            task5()
            print('')
        elif (select == '6'):
            task6()
            print('')
        #if the user enters 0 then the program exits 
        elif (select == '0'):
            endGame = True
        else:
            print('')
            #if the user input is invalid 
            print('Please enter a correct command.')
            print('')
    
    connection.commit()
    connection.close()
    return    
    
if __name__ == "__main__":
    main()