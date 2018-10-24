#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main script

External moduls
-----------------------
time            : to pause the execution of the program
                  for a specified time.
mysql.connector : is a standardized database driver
                  for Python platforms and development

Personal moduls
-----------------------
function        : all functions that the program need for work successfully
                  more details (function.py)
config          : identifiers to connect to the database `pur_beurre`

Program operation
-----------------------
1) call function get_connection() for display menu
2) loop main    : data_load

Loop contral statements
-----------------------
Ask at the user to make a choice with input fonction
tree possibilities :

>  press 1 for find a heathly substitute
1) the programm displays `categories` table of database
2) the user must choose a number to select a category
3) the programm displays rows of `foodstuffs` table corresponding to the chosen category
4) select foodstuff in order to find an healthy substitute
   - no substitute was found : back to the beginning of the loop
   - substitute found : the user sees the products one by one and chooses to record them or not
5) back to the beginning of the loop.

>  press 2 for see favorites
1) the programm displays `substitutes` table of database
2) back to the beginning of the loop.

>  press Q for Exit
   end of the program
"""

import time
import mysql.connector as mdb

from function import display_menu, select_table, select_id, row_foodstuff, search_substitute, healthy_substitute
from includes.config import get_connection
# connection to the MySQL server
con = get_connection()
#cursor
cur = con.cursor()

data_load = True
#displays menu
menu = display_menu()

while data_load:
    print(menu)
    user_choice = input("Votre choix : ")

    if user_choice == "1":
        #search substitutes 
        cmd_sql = ("SELECT * From categories ")
        select_table(cmd_sql)
        for value in select_table(cmd_sql):
            print (f"|  Tappez {value[0]}  |  {value[1]}")
        row_foodstuff()
        healthy_substitute()
        
    elif user_choice == "2":
        #displays favorites
        cmd_sql = ("SELECT * From substitutes ")
        select_table(cmd_sql)
        index = 0
        for value in select_table(cmd_sql):
            index += 1
            print (f"\n\
----------------[Favoris n°{value[0]}]----------------\n\
Nom         : {value[1]}\n\
Nutri Score : {value[2]}\n\
Store       : {value[4]}\n\
Description : {value[3]}\n\
URL         : {value[5]}\n\
\n")
            
    elif user_choice == "Q":
        #finish
        data_load = False
        print("Au revoir")
        time.sleep(1)

    else:
        print(f"La commande [{user_choice}] n'est pas valide :")

