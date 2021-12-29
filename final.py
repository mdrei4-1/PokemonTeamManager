#This is hopefully the final version of the code.
#I will start by setting up all of the Tkinter things and then
#implement each of the functions within it.
#Created by Mark Dreitzler, finished 12/09/2021

#do initial imports
import sqlite3
import tkinter as tk
from tkinter.ttk import *

def create_connection(path): #connect to the sqlite3 database. This is lifted from Assignment 7.
    connection = None
    try: #if the connection is successful, run this
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e: #output error if connection does not work
        print(f"The error '{e}' occurred")
    return connection

def sanitizeInput(inputString): #takes all of the close parenthesis and semicolons out of a string. Let's see you drop my tables now, Robert!
    inputString = inputString.replace(")","")
    inputString = inputString.replace(";","")
    inputString = inputString.replace("\"", "")
    return inputString

def searchAbility(istream, ostream):  #this is ran when an ability is searched for.
    ostream.delete("1.0", tk.END)
    abilityChoice = sanitizeInput(istream.get())
    ostream.insert("1.0","Following is a list of all Pokemon that can have the chosen ability: \n")
    result = myCursor.execute("SELECT identifier FROM (pokemon JOIN pokemon_abilities ON pokemon.id=pokemon_abilities.pokemon_id) WHERE species_id<494 AND is_default=1 AND ability_id=(SELECT ability_id FROM ability_names WHERE local_language_id = 9 AND name=\"" + sanitizeInput(abilityChoice) + "\");")
    rows = myCursor.fetchall()
    for row in rows:
        ostream.insert(tk.END, (row[0] + "\n").capitalize()) #print all the results
 
def searchMove(istream, ostream):  #this is ran when a move is searched for.
    ostream.delete("1.0", tk.END)
    moveChoice = sanitizeInput(istream.get())
    ostream.insert("1.0","Following is a list of all Pokemon that can learn the chosen move: \n")
    result = myCursor.execute("SELECT identifier FROM (pokemon JOIN pokemon_moves ON pokemon.id=pokemon_moves.pokemon_id) WHERE species_id<494 AND is_default=1 AND version_group_id=16 AND move_id=(SELECT move_id FROM move_names WHERE local_language_id = 9 AND name=\"" + sanitizeInput(moveChoice) + "\");")
    rows = myCursor.fetchall()
    if (moveChoice == "Volt Tackle"):
        ostream.insert(tk.END, "Pichu")
        return
    #this is a quick fix to an issue with the database. Effectively, Volt Tackle isn't in the database, so this code automatically overrides the standard result whenever Volt Tackle is searched. Unfortunately, I don't think this will fix the issue with the legality checker...
    for row in rows:
        ostream.insert(tk.END, (row[0] + "\n").capitalize())


def searchType(istream, ostream): #this is ran when a type is searched for
    ostream.delete("1.0", tk.END)
    typeChoice = sanitizeInput(istream.get())
    ostream.insert("1.0", "Following is a list of all Pokemon of the chosen type: \n")
    result = myCursor.execute("SELECT identifier FROM (pokemon JOIN pokemon_types ON pokemon.id=pokemon_types.pokemon_id) WHERE species_id<494 AND is_default=1 AND type_id=(SELECT type_id FROM type_names WHERE local_language_id = 9 AND name=\"" + sanitizeInput(typeChoice) + "\");")
    rows = myCursor.fetchall()
    for row in rows:
        ostream.insert(tk.END, (row[0] + "\n").capitalize()) #print all the results

def searchData(istream, ostream): #grab all data on a single mon
    ostream.delete("1.0", tk.END)
    #grab dex number first
    monChoice = sanitizeInput(istream.get())
    ostream.insert("1.0", (monChoice + "\'s National Pokedex number is "))
    result = myCursor.execute("SELECT id FROM pokemon WHERE identifier = \"" + sanitizeInput(monChoice.lower()) + "\";")
    rows = myCursor.fetchall()
    for row in rows:
        ostream.insert(tk.END, row[0])
    if (row[0] >= 494): #if at any point you want support up through Gen 6, you can delete this if statement and it'll work up through Pokedex number 720.
        ostream.insert(tk.END, ("\nThis program only has support for Pokemon through Pokedex Number 493."))
        return
    #next, types
    ostream.insert(tk.END, ("\n" + monChoice + "\'s type(s) is/are "))
    result = myCursor.execute("SELECT name FROM (type_names JOIN pokemon_types on type_names.type_id=pokemon_types.type_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput(monChoice.lower()) + "\");")
    rows = myCursor.fetchall()
    for row in rows:
        ostream.insert(tk.END, (row[0] + " ").capitalize())
    #and then, abilities
    ostream.insert(tk.END, ("\n" + monChoice + " can have the following abilities:\n"))
    result = myCursor.execute("SELECT name FROM (ability_names JOIN pokemon_abilities on ability_names.ability_id=pokemon_abilities.ability_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput(monChoice.lower()) + "\");")
    rows = myCursor.fetchall()
    for row in rows:
        ostream.insert(tk.END, (row[0] + "\n"))
    #and finally, moves
    ostream.insert(tk.END, (monChoice + " can learn the following moves:\n"))
    result = myCursor.execute("SELECT name FROM (move_names JOIN pokemon_moves on move_names.move_id=pokemon_moves.move_id) WHERE local_language_id=9 AND version_group_id=16 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput(monChoice.lower()) + "\");")
    rows = myCursor.fetchall()
    for row in rows:
        ostream.insert(tk.END, (row[0] + "\n"))
    if (monChoice.lower() == "pichu"):
        ostream.insert(tk.END, "Volt Tackle")


def searchPage(): #define all functionality of the Pokemon Search Page
    searchWindow = tk.Tk() #this creates a new window.
    searchWindow.title("Pokedex Search")
    searchWindow.geometry("675x500")
    infoFrameSearch = tk.Frame(master=searchWindow, height=2) #this has data for what this page does
    infoFrameSearch.pack()
    searchInfoLabel = tk.Label(infoFrameSearch, text="Input a Pokemon, Ability, Type, or Move, and press the corresponding button. \nThe search results will return in the text box below.\nIf a Pokemon's name or move appears multiple times, it means it learns that move multiple times.")
    searchInfoLabel.pack()
    userInputFrame = tk.Frame(master=searchWindow, height=25) #this frame contains user input and user-interactable buttons
    inputStream = tk.Entry(userInputFrame) #this is where you'll input something
    monButton = tk.Button(userInputFrame, text="Search Pokemon Data", command=lambda: searchData(inputStream, outputStream)) #this is the button that searches for data on a mon given that mon.
    outputStream = tk.Text(searchWindow)
    abilityButton = tk.Button(userInputFrame, text="Search by Ability", command=lambda: searchAbility(inputStream, outputStream)) #this is the button that searches for mons given an ability
    moveButton = tk.Button(userInputFrame, text="Search by Move", command=lambda: searchMove(inputStream, outputStream)) #this is the button that searches for mons given a move
    typeButton = tk.Button(userInputFrame, text="Search by Type", command=lambda: searchType(inputStream, outputStream)) #this is the button that searches for mons given a type
    inputStream.grid(column=0, row=0, padx=20, pady=20)
    monButton.grid(column=1, row=0)
    abilityButton.grid(column=2, row=0)
    moveButton.grid(column=3, row=0)
    typeButton.grid(column=4, row=0) #these all set up the columns for the options
    userInputFrame.pack()

    outputStream.pack()

def openDB(istream, mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4): #open an SQL database, and populate the teambuilder page with its data.
    print("Opening File\n")
    link2 = create_connection(sanitizeInput(istream.get()))
    myCursor2 = link2.cursor() #define a cursor object
    print("Checking all team data...\n")
    result = myCursor2.execute("SELECT * FROM teamdata;")
    result = myCursor2.fetchall()
    #first comes the fun part where I delete everything currently in each box
    mon1Name.delete(0, tk.END)
    mon2Name.delete(0, tk.END)
    mon3Name.delete(0, tk.END)
    mon4Name.delete(0, tk.END)
    mon5Name.delete(0, tk.END)
    mon6Name.delete(0, tk.END)
    mon1Ability.delete(0, tk.END)
    mon2Ability.delete(0, tk.END)
    mon3Ability.delete(0, tk.END)
    mon4Ability.delete(0, tk.END)
    mon5Ability.delete(0, tk.END)
    mon6Ability.delete(0, tk.END)
    mon1Move1.delete(0, tk.END)
    mon2Move1.delete(0, tk.END)
    mon3Move1.delete(0, tk.END)
    mon4Move1.delete(0, tk.END)
    mon5Move1.delete(0, tk.END)
    mon6Move1.delete(0, tk.END)
    mon1Move2.delete(0, tk.END)
    mon2Move2.delete(0, tk.END)
    mon3Move2.delete(0, tk.END)
    mon4Move2.delete(0, tk.END)
    mon5Move2.delete(0, tk.END)
    mon6Move2.delete(0, tk.END)
    mon1Move3.delete(0, tk.END)
    mon2Move3.delete(0, tk.END)
    mon3Move3.delete(0, tk.END)
    mon4Move3.delete(0, tk.END)
    mon5Move3.delete(0, tk.END)
    mon6Move3.delete(0, tk.END)
    mon1Move4.delete(0, tk.END)
    mon2Move4.delete(0, tk.END)
    mon3Move4.delete(0, tk.END)
    mon4Move4.delete(0, tk.END)
    mon5Move4.delete(0, tk.END)
    mon6Move4.delete(0, tk.END)
    #now comes the fun part where I have to manually assign each piece of data to a specific thing.
    mon1Name.insert(tk.END, (result[0][1]))
    mon2Name.insert(tk.END, (result[1][1]))
    mon3Name.insert(tk.END, (result[2][1]))
    mon4Name.insert(tk.END, (result[3][1]))
    mon5Name.insert(tk.END, (result[4][1]))
    mon6Name.insert(tk.END, (result[5][1]))
    mon1Ability.insert(tk.END, (result[0][2]))
    mon2Ability.insert(tk.END, (result[1][2]))
    mon3Ability.insert(tk.END, (result[2][2]))
    mon4Ability.insert(tk.END, (result[3][2]))
    mon5Ability.insert(tk.END, (result[4][2]))
    mon6Ability.insert(tk.END, (result[5][2]))
    mon1Move1.insert(tk.END, (result[0][3]))
    mon2Move1.insert(tk.END, (result[1][3]))
    mon3Move1.insert(tk.END, (result[2][3]))
    mon4Move1.insert(tk.END, (result[3][3]))
    mon5Move1.insert(tk.END, (result[4][3]))
    mon6Move1.insert(tk.END, (result[5][3]))
    mon1Move2.insert(tk.END, (result[0][4]))
    mon2Move2.insert(tk.END, (result[1][4]))
    mon3Move2.insert(tk.END, (result[2][4]))
    mon4Move2.insert(tk.END, (result[3][4]))
    mon5Move2.insert(tk.END, (result[4][4]))
    mon6Move2.insert(tk.END, (result[5][4]))
    mon1Move3.insert(tk.END, (result[0][5]))
    mon2Move3.insert(tk.END, (result[1][5]))
    mon3Move3.insert(tk.END, (result[2][5]))
    mon4Move3.insert(tk.END, (result[3][5]))
    mon5Move3.insert(tk.END, (result[4][5]))
    mon6Move3.insert(tk.END, (result[5][5]))
    mon1Move4.insert(tk.END, (result[0][6]))
    mon2Move4.insert(tk.END, (result[1][6]))
    mon3Move4.insert(tk.END, (result[2][6]))
    mon4Move4.insert(tk.END, (result[3][6]))
    mon5Move4.insert(tk.END, (result[4][6]))
    mon6Move4.insert(tk.END, (result[5][6]))

def saveDB(istream, mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4): #Create a new SQL database, take data from the team manager, populate it, and then export it.
    #start with creating a new file if it doesn't exist
    print("Opening File\n")
    link2 = create_connection(sanitizeInput(istream.get()))
    myCursor2 = link2.cursor() #define a cursor object
    #then we delete everything in this database
    deleteEnd = myCursor2.execute("DROP TABLE IF EXISTS teamdata;") #drop the entire database table if it exists
    createTable = myCursor2.execute("CREATE TABLE teamdata (team_slot INT PRIMARY KEY UNIQUE, pokemon_name CHAR, ability CHAR, move1 CHAR, move2 CHAR, move3 CHAR, move4 CHAR);") #create a new table
    #then, we pump every piece of info from the program into this database.
    print("Adding mon 1\n")
    inputData = myCursor2.execute("INSERT INTO teamdata(team_slot, pokemon_name, ability, move1, move2, move3, move4) VALUES (1, \"" + sanitizeInput(mon1Name.get()) + "\", \"" + sanitizeInput(mon1Ability.get()) + "\", \"" + sanitizeInput(mon1Move1.get()) + "\", \"" + sanitizeInput(mon1Move2.get()) + "\", \"" + sanitizeInput(mon1Move3.get()) + "\", \"" + sanitizeInput(mon1Move4.get()) + "\");")
    print("Adding mon 2\n")
    inputData = myCursor2.execute("INSERT INTO teamdata(team_slot, pokemon_name, ability, move1, move2, move3, move4) VALUES (2, \"" + sanitizeInput(mon2Name.get()) + "\", \"" + sanitizeInput(mon2Ability.get()) + "\", \"" + sanitizeInput(mon2Move1.get()) + "\", \"" + sanitizeInput(mon2Move2.get()) + "\", \"" + sanitizeInput(mon2Move3.get()) + "\", \"" + sanitizeInput(mon2Move4.get()) + "\");")
    print("Adding mon 3\n")
    inputData = myCursor2.execute("INSERT INTO teamdata(team_slot, pokemon_name, ability, move1, move2, move3, move4) VALUES (3, \"" + sanitizeInput(mon3Name.get()) + "\", \"" + sanitizeInput(mon3Ability.get()) + "\", \"" + sanitizeInput(mon3Move1.get()) + "\", \"" + sanitizeInput(mon3Move2.get()) + "\", \"" + sanitizeInput(mon3Move3.get()) + "\", \"" + sanitizeInput(mon3Move4.get()) + "\");")
    print("Adding mon 4\n")
    inputData = myCursor2.execute("INSERT INTO teamdata(team_slot, pokemon_name, ability, move1, move2, move3, move4) VALUES (4, \"" + sanitizeInput(mon4Name.get()) + "\", \"" + sanitizeInput(mon4Ability.get()) + "\", \"" + sanitizeInput(mon4Move1.get()) + "\", \"" + sanitizeInput(mon4Move2.get()) + "\", \"" + sanitizeInput(mon4Move3.get()) + "\", \"" + sanitizeInput(mon4Move4.get()) + "\");")
    print("Adding mon 5\n")
    inputData = myCursor2.execute("INSERT INTO teamdata(team_slot, pokemon_name, ability, move1, move2, move3, move4) VALUES (5, \"" + sanitizeInput(mon5Name.get()) + "\", \"" + sanitizeInput(mon5Ability.get()) + "\", \"" + sanitizeInput(mon5Move1.get()) + "\", \"" + sanitizeInput(mon5Move2.get()) + "\", \"" + sanitizeInput(mon5Move3.get()) + "\", \"" + sanitizeInput(mon5Move4.get()) + "\");")
    print("Adding mon 6\n")
    inputData = myCursor2.execute("INSERT INTO teamdata(team_slot, pokemon_name, ability, move1, move2, move3, move4) VALUES (6, \"" + sanitizeInput(mon6Name.get()) + "\", \"" + sanitizeInput(mon6Ability.get()) + "\", \"" + sanitizeInput(mon6Move1.get()) + "\", \"" + sanitizeInput(mon6Move2.get()) + "\", \"" + sanitizeInput(mon6Move3.get()) + "\", \"" + sanitizeInput(mon6Move4.get()) + "\");")
    #finally, commit changes
    link2.commit()
    
def checkLegality(mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4): #Check if there are any problems with the moves or abilities Pokemon have.
    #We'll start with abilities. And after that, we'll move on to moves.
    #Note that this function outputs to the console, due to basically being entirely text and there not being a good place to put it within the Team Manager window.
    print("\n\n\n\n\n\n")
    #Mon 1
    dexNum = myCursor.execute("SELECT id FROM pokemon WHERE identifier = \"" + sanitizeInput(mon1Name.get()).lower() + "\";") #this grabs the dex number of the Pokemon which may or may not help us later.
    getAbilities = myCursor.execute("SELECT name FROM (ability_names JOIN pokemon_abilities on ability_names.ability_id=pokemon_abilities.ability_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon1Name.get()).lower()) + "\");") #grab the abilities of the chosen mon in this slot
    rows = myCursor.fetchall()
    isLegal = False
    for row in rows: #check each ability
        if (row[0] == mon1Ability.get()): #if the ability is the same:
            isLegal = True
    if (isLegal == True):
        print(mon1Name.get() + "'s ability is LEGAL: " + mon1Ability.get())
    else:
        print(mon1Name.get() + "'s ability is ILLEGAL: " + mon1Ability.get())
    #Mon 2
    dexNum = myCursor.execute("SELECT id FROM pokemon WHERE identifier = \"" + sanitizeInput(mon2Name.get()).lower() + "\";") #this grabs the dex number of the Pokemon which may or may not help us later.
    getAbilities = myCursor.execute("SELECT name FROM (ability_names JOIN pokemon_abilities on ability_names.ability_id=pokemon_abilities.ability_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon2Name.get()).lower()) + "\");") #grab the abilities of the chosen mon in this slot
    rows = myCursor.fetchall()
    isLegal = False
    for row in rows: #check each ability
        if (row[0] == mon2Ability.get()): #if the ability is the same:
            isLegal = True
    if (isLegal == True):
        print(mon2Name.get() + "'s ability is LEGAL: " + mon2Ability.get())
    else:
        print(mon2Name.get() + "'s ability is ILLEGAL: " + mon2Ability.get())
    #Mon 3
    dexNum = myCursor.execute("SELECT id FROM pokemon WHERE identifier = \"" + sanitizeInput(mon3Name.get()).lower() + "\";") #this grabs the dex number of the Pokemon which may or may not help us later.
    getAbilities = myCursor.execute("SELECT name FROM (ability_names JOIN pokemon_abilities on ability_names.ability_id=pokemon_abilities.ability_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon3Name.get()).lower()) + "\");") #grab the abilities of the chosen mon in this slot
    rows = myCursor.fetchall()
    isLegal = False
    for row in rows: #check each ability
        if (row[0] == mon3Ability.get()): #if the ability is the same:
            isLegal = True
    if (isLegal == True):
        print(mon3Name.get() + "'s ability is LEGAL: " + mon3Ability.get())
    else:
        print(mon3Name.get() + "'s ability is ILLEGAL: " + mon3Ability.get())
    #Mon 4
    dexNum = myCursor.execute("SELECT id FROM pokemon WHERE identifier = \"" + sanitizeInput(mon4Name.get()).lower() + "\";") #this grabs the dex number of the Pokemon which may or may not help us later.
    getAbilities = myCursor.execute("SELECT name FROM (ability_names JOIN pokemon_abilities on ability_names.ability_id=pokemon_abilities.ability_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon4Name.get()).lower()) + "\");") #grab the abilities of the chosen mon in this slot
    rows = myCursor.fetchall()
    isLegal = False
    for row in rows: #check each ability
        if (row[0] == mon4Ability.get()): #if the ability is the same:
            isLegal = True
    if (isLegal == True):
        print(mon4Name.get() + "'s ability is LEGAL: " + mon4Ability.get())
    else:
        print(mon4Name.get() + "'s ability is ILLEGAL: " + mon4Ability.get())
    #Mon 5
    dexNum = myCursor.execute("SELECT id FROM pokemon WHERE identifier = \"" + sanitizeInput(mon5Name.get()).lower() + "\";") #this grabs the dex number of the Pokemon which may or may not help us later.
    getAbilities = myCursor.execute("SELECT name FROM (ability_names JOIN pokemon_abilities on ability_names.ability_id=pokemon_abilities.ability_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon5Name.get()).lower()) + "\");") #grab the abilities of the chosen mon in this slot
    rows = myCursor.fetchall()
    isLegal = False
    for row in rows: #check each ability
        if (row[0] == mon5Ability.get()): #if the ability is the same:
            isLegal = True
    if (isLegal == True):
        print(mon5Name.get() + "'s ability is LEGAL: " + mon5Ability.get())
    else:
        print(mon5Name.get() + "'s ability is ILLEGAL: " + mon5Ability.get())
    #Mon 6
    dexNum = myCursor.execute("SELECT id FROM pokemon WHERE identifier = \"" + sanitizeInput(mon6Name.get()).lower() + "\";") #this grabs the dex number of the Pokemon which may or may not help us later.
    getAbilities = myCursor.execute("SELECT name FROM (ability_names JOIN pokemon_abilities on ability_names.ability_id=pokemon_abilities.ability_id) WHERE local_language_id=9 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon6Name.get()).lower()) + "\");") #grab the abilities of the chosen mon in this slot
    rows = myCursor.fetchall()
    isLegal = False
    for row in rows: #check each ability
        if (row[0] == mon6Ability.get()): #if the ability is the same:
            isLegal = True
    if (isLegal == True):
        print(mon6Name.get() + "'s ability is LEGAL: " + mon6Ability.get())
    else:
        print(mon6Name.get() + "'s ability is ILLEGAL: " + mon6Ability.get())
    #And now we get to moves.
    #I think the way I want to go about this is to just check if the current Pokemon can learn the move. I wanted to initially write a SQLite command to grab all prior evolutions but I'm not sure I'm going to have time to implement that, so I'm going to just focus on the current stage of the evolutionary line.
    #Mon 1's data:
    getLegalMoves = myCursor.execute("SELECT name FROM (move_names JOIN pokemon_moves on move_names.move_id=pokemon_moves.move_id) WHERE local_language_id=9 AND version_group_id=16 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon1Name.get()).lower()) + "\");") #grab all the legal moves the mon can know
    rows = myCursor.fetchall() 
    isLegal = False #MOVE 1
    for row in rows: #check each move
        if (row[0] == mon1Move1.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon1Name.get() + "'s move is LEGAL: " + mon1Move1.get())
    else:
        print(mon1Name.get() + "'s move is ILLEGAL: " + mon1Move1.get())
    isLegal = False #MOVE 2
    for row in rows: #check each move
        if (row[0] == mon1Move2.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon1Name.get() + "'s move is LEGAL: " + mon1Move2.get())
    else:
        print(mon1Name.get() + "'s move is ILLEGAL: " + mon1Move2.get())
    isLegal = False #MOVE 3
    for row in rows: #check each move
        if (row[0] == mon1Move3.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon1Name.get() + "'s move is LEGAL: " + mon1Move3.get())
    else:
        print(mon1Name.get() + "'s move is ILLEGAL: " + mon1Move3.get())
    isLegal = False #MOVE 4
    for row in rows: #check each move
        if (row[0] == mon1Move4.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon1Name.get() + "'s move is LEGAL: " + mon1Move4.get())
    else:
        print(mon1Name.get() + "'s move is ILLEGAL: " + mon1Move4.get())
    #Mon 2's data:
    getLegalMoves = myCursor.execute("SELECT name FROM (move_names JOIN pokemon_moves on move_names.move_id=pokemon_moves.move_id) WHERE local_language_id=9 AND version_group_id=16 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon2Name.get()).lower()) + "\");") #grab all the legal moves the mon can know
    rows = myCursor.fetchall() 
    isLegal = False #MOVE 1
    for row in rows: #check each move
        if (row[0] == mon2Move1.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon2Name.get() + "'s move is LEGAL: " + mon2Move1.get())
    else:
        print(mon2Name.get() + "'s move is ILLEGAL: " + mon2Move1.get())
    isLegal = False #MOVE 2
    for row in rows: #check each move
        if (row[0] == mon2Move2.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon2Name.get() + "'s move is LEGAL: " + mon2Move2.get())
    else:
        print(mon2Name.get() + "'s move is ILLEGAL: " + mon2Move2.get())
    isLegal = False #MOVE 3
    for row in rows: #check each move
        if (row[0] == mon2Move3.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon2Name.get() + "'s move is LEGAL: " + mon2Move3.get())
    else:
        print(mon2Name.get() + "'s move is ILLEGAL: " + mon2Move3.get())
    isLegal = False #MOVE 4
    for row in rows: #check each move
        if (row[0] == mon2Move4.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon2Name.get() + "'s move is LEGAL: " + mon2Move4.get())
    else:
        print(mon2Name.get() + "'s move is ILLEGAL: " + mon2Move4.get())
    #Mon 3's data:
    getLegalMoves = myCursor.execute("SELECT name FROM (move_names JOIN pokemon_moves on move_names.move_id=pokemon_moves.move_id) WHERE local_language_id=9 AND version_group_id=16 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon3Name.get()).lower()) + "\");") #grab all the legal moves the mon can know
    rows = myCursor.fetchall() 
    isLegal = False #MOVE 1
    for row in rows: #check each move
        if (row[0] == mon3Move1.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon3Name.get() + "'s move is LEGAL: " + mon3Move1.get())
    else:
        print(mon3Name.get() + "'s move is ILLEGAL: " + mon3Move1.get())
    isLegal = False #MOVE 2
    for row in rows: #check each move
        if (row[0] == mon3Move2.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon3Name.get() + "'s move is LEGAL: " + mon3Move2.get())
    else:
        print(mon3Name.get() + "'s move is ILLEGAL: " + mon3Move2.get())
    isLegal = False #MOVE 3
    for row in rows: #check each move
        if (row[0] == mon3Move3.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon3Name.get() + "'s move is LEGAL: " + mon3Move3.get())
    else:
        print(mon3Name.get() + "'s move is ILLEGAL: " + mon3Move3.get())
    isLegal = False #MOVE 4
    for row in rows: #check each move
        if (row[0] == mon3Move4.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon3Name.get() + "'s move is LEGAL: " + mon3Move4.get())
    else:
        print(mon3Name.get() + "'s move is ILLEGAL: " + mon3Move4.get())
    #Mon 4's data:
    getLegalMoves = myCursor.execute("SELECT name FROM (move_names JOIN pokemon_moves on move_names.move_id=pokemon_moves.move_id) WHERE local_language_id=9 AND version_group_id=16 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon4Name.get()).lower()) + "\");") #grab all the legal moves the mon can know
    rows = myCursor.fetchall() 
    isLegal = False #MOVE 1
    for row in rows: #check each move
        if (row[0] == mon4Move1.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon4Name.get() + "'s move is LEGAL: " + mon4Move1.get())
    else:
        print(mon4Name.get() + "'s move is ILLEGAL: " + mon4Move1.get())
    isLegal = False #MOVE 2
    for row in rows: #check each move
        if (row[0] == mon4Move2.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon4Name.get() + "'s move is LEGAL: " + mon4Move2.get())
    else:
        print(mon4Name.get() + "'s move is ILLEGAL: " + mon4Move2.get())
    isLegal = False #MOVE 3
    for row in rows: #check each move
        if (row[0] == mon4Move3.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon4Name.get() + "'s move is LEGAL: " + mon4Move3.get())
    else:
        print(mon4Name.get() + "'s move is ILLEGAL: " + mon4Move3.get())
    isLegal = False #MOVE 4
    for row in rows: #check each move
        if (row[0] == mon4Move4.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon4Name.get() + "'s move is LEGAL: " + mon4Move4.get())
    else:
        print(mon4Name.get() + "'s move is ILLEGAL: " + mon4Move4.get())
    #Mon 5's data:
    getLegalMoves = myCursor.execute("SELECT name FROM (move_names JOIN pokemon_moves on move_names.move_id=pokemon_moves.move_id) WHERE local_language_id=9 AND version_group_id=16 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon5Name.get()).lower()) + "\");") #grab all the legal moves the mon can know
    rows = myCursor.fetchall() 
    isLegal = False #MOVE 1
    for row in rows: #check each move
        if (row[0] == mon5Move1.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon5Name.get() + "'s move is LEGAL: " + mon5Move1.get())
    else:
        print(mon5Name.get() + "'s move is ILLEGAL: " + mon5Move1.get())
    isLegal = False #MOVE 2
    for row in rows: #check each move
        if (row[0] == mon5Move2.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon5Name.get() + "'s move is LEGAL: " + mon5Move2.get())
    else:
        print(mon5Name.get() + "'s move is ILLEGAL: " + mon5Move2.get())
    isLegal = False #MOVE 3
    for row in rows: #check each move
        if (row[0] == mon5Move3.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon5Name.get() + "'s move is LEGAL: " + mon5Move3.get())
    else:
        print(mon5Name.get() + "'s move is ILLEGAL: " + mon5Move3.get())
    isLegal = False #MOVE 4
    for row in rows: #check each move
        if (row[0] == mon5Move4.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon5Name.get() + "'s move is LEGAL: " + mon5Move4.get())
    else:
        print(mon5Name.get() + "'s move is ILLEGAL: " + mon5Move4.get())
    #Mon 6's data:
    getLegalMoves = myCursor.execute("SELECT name FROM (move_names JOIN pokemon_moves on move_names.move_id=pokemon_moves.move_id) WHERE local_language_id=9 AND version_group_id=16 AND pokemon_id=(SELECT id from pokemon where identifier=\"" + sanitizeInput((mon6Name.get()).lower()) + "\");") #grab all the legal moves the mon can know
    rows = myCursor.fetchall() 
    isLegal = False #MOVE 1
    for row in rows: #check each move
        if (row[0] == mon6Move1.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon6Name.get() + "'s move is LEGAL: " + mon6Move1.get())
    else:
        print(mon6Name.get() + "'s move is ILLEGAL: " + mon6Move1.get())
    isLegal = False #MOVE 2
    for row in rows: #check each move
        if (row[0] == mon6Move2.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon6Name.get() + "'s move is LEGAL: " + mon6Move2.get())
    else:
        print(mon6Name.get() + "'s move is ILLEGAL: " + mon6Move2.get())
    isLegal = False #MOVE 3
    for row in rows: #check each move
        if (row[0] == mon6Move3.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon6Name.get() + "'s move is LEGAL: " + mon6Move3.get())
    else:
        print(mon6Name.get() + "'s move is ILLEGAL: " + mon6Move3.get())
    isLegal = False #MOVE 4
    for row in rows: #check each move
        if (row[0] == mon6Move4.get()): #if the move is the same:
            isLegal = True
    if (isLegal == True):
        print(mon6Name.get() + "'s move is LEGAL: " + mon6Move4.get())
    else:
        print(mon6Name.get() + "'s move is ILLEGAL: " + mon6Move4.get())
#and with that, it is done



def exportShowdown(mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4): #export the current data to a format readable by Pokemon Showdown
    print("Opening output stream as teamexport.txt...\n")
    fw = open("teamexport.txt", "w")
    fw.write((mon1Name.get()) + "\n") #this line writes in the Pokemon's name
    fw.write("Ability: " + (mon1Ability.get()) + "\n") #this line writes in the Pokemon's ability
    fw.write("- " + (mon1Move1.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon1Move2.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon1Move3.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon1Move4.get()) + "\n\n") #this line writes in the Pokemon's attack
    fw.write((mon2Name.get()) + "\n") #this line writes in the Pokemon's name
    fw.write("Ability: " + (mon2Ability.get()) + "\n") #this line writes in the Pokemon's ability
    fw.write("- " + (mon2Move1.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon2Move2.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon2Move3.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon2Move4.get()) + "\n\n") #this line writes in the Pokemon's attack
    fw.write((mon3Name.get()) + "\n") #this line writes in the Pokemon's name
    fw.write("Ability: " + (mon3Ability.get()) + "\n") #this line writes in the Pokemon's ability
    fw.write("- " + (mon3Move1.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon3Move2.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon3Move3.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon3Move4.get()) + "\n\n") #this line writes in the Pokemon's attack
    fw.write((mon4Name.get()) + "\n") #this line writes in the Pokemon's name
    fw.write("Ability: " + (mon4Ability.get()) + "\n") #this line writes in the Pokemon's ability
    fw.write("- " + (mon4Move1.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon4Move2.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon4Move3.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon4Move4.get()) + "\n\n") #this line writes in the Pokemon's attack
    fw.write((mon5Name.get()) + "\n") #this line writes in the Pokemon's name
    fw.write("Ability: " + (mon5Ability.get()) + "\n") #this line writes in the Pokemon's ability
    fw.write("- " + (mon5Move1.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon5Move2.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon5Move3.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon5Move4.get()) + "\n\n") #this line writes in the Pokemon's attack
    fw.write((mon6Name.get()) + "\n") #this line writes in the Pokemon's name
    fw.write("Ability: " + (mon6Ability.get()) + "\n") #this line writes in the Pokemon's ability
    fw.write("- " + (mon6Move1.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon6Move2.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon6Move3.get()) + "\n") #this line writes in the Pokemon's attack
    fw.write("- " + (mon6Move4.get()) + "\n\n") #this line writes in the Pokemon's attack


def teamPage(): #define all functionality of the Teambuilder Page
    teamWindow = tk.Tk()
    teamWindow.title("Team Manager")
    teamWindow.geometry("1050x400")
    infoFrameTeam = tk.Frame(master=teamWindow, height=2) #this has data for what this page does
    infoFrameTeam.pack()
    teamInfoLabel = tk.Label(infoFrameTeam, text="Please input a team in the boxes below, or import a team from a file. \nThen, you may save your team, check legality, or export to Showdown.\nThe input box in the top right corner is for the file to be opened or saved to.")
    teamInfoLabel.pack() #put in info for what this page does
    #and now, the fun part where I define entirely too many things!
    tbInputFrame = tk.Frame(master=teamWindow, height=25)
    #I'll start with the labels.
    slotOneLabel = tk.Label(tbInputFrame, text="1")
    slotTwoLabel = tk.Label(tbInputFrame, text="2")
    slotThreeLabel = tk.Label(tbInputFrame, text="3")
    slotFourLabel = tk.Label(tbInputFrame, text="4")
    slotFiveLabel = tk.Label(tbInputFrame, text="5")
    slotSixLabel = tk.Label(tbInputFrame, text="6")
    monNameLabel = tk.Label(tbInputFrame, text="Pokemon")
    abilityLabel = tk.Label(tbInputFrame, text="Ability")
    moveOneLabel = tk.Label(tbInputFrame, text="Move1")
    moveTwoLabel = tk.Label(tbInputFrame, text="Move2")
    moveThreeLabel = tk.Label(tbInputFrame, text="Move3")
    moveFourLabel = tk.Label(tbInputFrame, text="Move4")
    #next, we'll define all the input streams.
    #this first one is for opening files.
    fileNameStream = tk.Entry(tbInputFrame)
    #the next 36 things are all individual pieces of data
    mon1Name = tk.Entry(tbInputFrame)
    mon2Name = tk.Entry(tbInputFrame)
    mon3Name = tk.Entry(tbInputFrame)
    mon4Name = tk.Entry(tbInputFrame)
    mon5Name = tk.Entry(tbInputFrame)
    mon6Name = tk.Entry(tbInputFrame)
    mon1Ability = tk.Entry(tbInputFrame)
    mon2Ability = tk.Entry(tbInputFrame)
    mon3Ability = tk.Entry(tbInputFrame)
    mon4Ability = tk.Entry(tbInputFrame)
    mon5Ability = tk.Entry(tbInputFrame)
    mon6Ability = tk.Entry(tbInputFrame)
    mon1Move1 = tk.Entry(tbInputFrame)
    mon2Move1 = tk.Entry(tbInputFrame)
    mon3Move1 = tk.Entry(tbInputFrame)
    mon4Move1 = tk.Entry(tbInputFrame)
    mon5Move1 = tk.Entry(tbInputFrame)
    mon6Move1 = tk.Entry(tbInputFrame)
    mon1Move2 = tk.Entry(tbInputFrame)
    mon2Move2 = tk.Entry(tbInputFrame)
    mon3Move2 = tk.Entry(tbInputFrame)
    mon4Move2 = tk.Entry(tbInputFrame)
    mon5Move2 = tk.Entry(tbInputFrame)
    mon6Move2 = tk.Entry(tbInputFrame)
    mon1Move3 = tk.Entry(tbInputFrame)
    mon2Move3 = tk.Entry(tbInputFrame)
    mon3Move3 = tk.Entry(tbInputFrame)
    mon4Move3 = tk.Entry(tbInputFrame)
    mon5Move3 = tk.Entry(tbInputFrame)
    mon6Move3 = tk.Entry(tbInputFrame)
    mon1Move4 = tk.Entry(tbInputFrame)
    mon2Move4 = tk.Entry(tbInputFrame)
    mon3Move4 = tk.Entry(tbInputFrame)
    mon4Move4 = tk.Entry(tbInputFrame)
    mon5Move4 = tk.Entry(tbInputFrame)
    mon6Move4 = tk.Entry(tbInputFrame)
    #finally, we define a few buttons that will be useful to us.
    legalityCheckButton = tk.Button(tbInputFrame, text="Check Legality", command=lambda: checkLegality(mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4))
    openFileButton = tk.Button(tbInputFrame, text="Open DB", command=lambda: openDB(fileNameStream, mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4))
    exportButton = tk.Button(tbInputFrame, text="Export to Showdown", command=lambda: exportShowdown(mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4))
    saveFileButton = tk.Button(tbInputFrame, text="Save to DB", command=lambda: saveDB(fileNameStream, mon1Name, mon2Name, mon3Name, mon4Name, mon5Name, mon6Name, mon1Ability, mon2Ability, mon3Ability, mon4Ability, mon5Ability, mon6Ability, mon1Move1, mon2Move1, mon3Move1, mon4Move1, mon5Move1, mon6Move1, mon1Move2, mon2Move2, mon3Move2, mon4Move2, mon5Move2, mon6Move2, mon1Move3, mon2Move3, mon3Move3, mon4Move3, mon5Move3, mon6Move3, mon1Move4, mon2Move4, mon3Move4, mon4Move4, mon5Move4, mon6Move4))
    #and now we put all of this into the grid.
    slotOneLabel.grid(column=0, row=1, padx=10, pady=10)
    slotTwoLabel.grid(column=0, row=2, padx=10, pady=10)
    slotThreeLabel.grid(column=0, row=3, padx=10, pady=10)
    slotFourLabel.grid(column=0, row=4, padx=10, pady=10)
    slotFiveLabel.grid(column=0, row=5, padx=10, pady=10)
    slotSixLabel.grid(column=0, row=6, padx=10, pady=10)
    monNameLabel.grid(column=1, row=0, padx=10, pady=10)
    abilityLabel.grid(column=2, row=0, padx=10, pady=10)
    moveOneLabel.grid(column=3, row=0, padx=10, pady=10)
    moveTwoLabel.grid(column=4, row=0, padx=10, pady=10)
    moveThreeLabel.grid(column=5, row=0, padx=10, pady=10)
    moveFourLabel.grid(column=6, row=0, padx=10, pady=10)
    mon1Name.grid(column=1, row=1, padx=10, pady=10)
    mon2Name.grid(column=1, row=2, padx=10, pady=10)
    mon3Name.grid(column=1, row=3, padx=10, pady=10)
    mon4Name.grid(column=1, row=4, padx=10, pady=10)
    mon5Name.grid(column=1, row=5, padx=10, pady=10)
    mon6Name.grid(column=1, row=6, padx=10, pady=10)
    mon1Ability.grid(column=2, row=1, padx=10, pady=10)
    mon2Ability.grid(column=2, row=2, padx=10, pady=10)
    mon3Ability.grid(column=2, row=3, padx=10, pady=10)
    mon4Ability.grid(column=2, row=4, padx=10, pady=10)
    mon5Ability.grid(column=2, row=5, padx=10, pady=10)
    mon6Ability.grid(column=2, row=6, padx=10, pady=10)
    mon1Move1.grid(column=3, row=1, padx=10, pady=10)
    mon2Move1.grid(column=3, row=2, padx=10, pady=10)
    mon3Move1.grid(column=3, row=3, padx=10, pady=10)
    mon4Move1.grid(column=3, row=4, padx=10, pady=10)
    mon5Move1.grid(column=3, row=5, padx=10, pady=10)
    mon6Move1.grid(column=3, row=6, padx=10, pady=10)
    mon1Move2.grid(column=4, row=1, padx=10, pady=10)
    mon2Move2.grid(column=4, row=2, padx=10, pady=10)
    mon3Move2.grid(column=4, row=3, padx=10, pady=10)
    mon4Move2.grid(column=4, row=4, padx=10, pady=10)
    mon5Move2.grid(column=4, row=5, padx=10, pady=10)
    mon6Move2.grid(column=4, row=6, padx=10, pady=10)
    mon1Move3.grid(column=5, row=1, padx=10, pady=10)
    mon2Move3.grid(column=5, row=2, padx=10, pady=10)
    mon3Move3.grid(column=5, row=3, padx=10, pady=10)
    mon4Move3.grid(column=5, row=4, padx=10, pady=10)
    mon5Move3.grid(column=5, row=5, padx=10, pady=10)
    mon6Move3.grid(column=5, row=6, padx=10, pady=10)
    mon1Move4.grid(column=6, row=1, padx=10, pady=10)
    mon2Move4.grid(column=6, row=2, padx=10, pady=10)
    mon3Move4.grid(column=6, row=3, padx=10, pady=10)
    mon4Move4.grid(column=6, row=4, padx=10, pady=10)
    mon5Move4.grid(column=6, row=5, padx=10, pady=10)
    mon6Move4.grid(column=6, row=6, padx=10, pady=10)
    fileNameStream.grid(column=7, row=0, padx=10, pady=10)
    legalityCheckButton.grid(column=7, row=1, padx=10, pady=10)
    openFileButton.grid(column=7, row=2, padx=10, pady=10)
    saveFileButton.grid(column=7, row=3, padx=10, pady=10)
    exportButton.grid(column=7, row=4, padx=10, pady=10)
    #and finally, pack it in
    tbInputFrame.pack()
    

    
#this is the main program.
window = tk.Tk() #define window stuffs for the main window. This is the title screen, so to speak.
window.geometry("400x350")
window.title("Mark's BDSP Teambuilder")
titleLabel = tk.Label(window, text="Welcome to Mark's BDSP Teambuilder. Please select an option below.") #displays title text. If I can get one done maybe I'll add in a logo here too.
titleLabel.pack()

searchButton = tk.Button(window, text="Pokedex Search", command=searchPage) #button that opens the search page.
searchButton.pack(pady=75)

teamButton = tk.Button(window, text="Team Manager", command=teamPage) #button that opens the teambuilder page
teamButton.pack()
#now, set up the SQLite3 stuffs
print("Opening File\n")
link = create_connection("veekun-pokedex.sqlite")
myCursor = link.cursor() #define a cursor object
tk.mainloop() #proceed into main loop
