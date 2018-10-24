#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script contains 8 functions.

1) display_menu()      : displays input() commands for the user
2) user_select()       : add input() user choice for SQL statement with (WHERE)
3) select_table()      : SQL statement to select table from database
4) select_id()         : SQL statement to select table from database, call function user_select()
5) row_foodstuff()     : call select_id() and return values of row[]
6) save_substitute()   : for save substitutes in database
7) search_substitute() : send request to the api OpenFoodFacts and return data
8) healthy_substitute(): call search_substitute(), check if request get products
                         then display them and call save_substitute()
"""

import mysql.connector as mdb
import json
import requests

import includes.config as config

# connect to database
con = config.get_connection()
# cursor
cur = con.cursor()

def display_menu():
    main_menu = ("\
+-----------------------------------------------+\n\
|                      MENU                     |\n\
+-----------------------------------------------+\n\
+-----------------------------------------------+\n\
|  Tappez 1  |   Pour chercher un substitut     |\n\
+-----------------------------------------------+\n\
|  Tappez 2  |   Afficher favoris               |\n\
+-----------------------------------------------+\n\
|  Tappez Q  |   Quitter                        |\n\
+-----------------------------------------------+\n")
    return main_menu

def user_select():
    # add input user for request sql
    data = []
    user_input = input("Votre choix : ")
    data.append(user_input)  
    return data


def select_table(show_table):
    # select table from database
    cur.execute(show_table)
    data_result = cur.fetchall()
    return data_result


def select_id(use_id, user_choice):
    # request sql --> WHERE id
    cur.execute(use_id, user_choice)
    data_result = cur.fetchall()
    return data_result


def row_foodstuff():
    # display data of foodstuffs table
    sql_id = ("SELECT * FROM foodstuffs WHERE id = %s ")
    # call function user_select()
    sql_choice = user_select()
    select_id(sql_id, sql_choice)
    for value in select_id(sql_id, sql_choice):
        print (f"|  Tappez {value[1]}  |  {value[4]}")

def save_substitute(*data_substitute):
    # save result into database
    input_choice = True
    while input_choice:
        user_choice = input("Souhaitez vous enregistrer ce substitut?\n\
| [ Tappez 1 pour oui ] | [ Tappez 2 pour non ]\n")
        if user_choice == "1":
            add_substitute = ("INSERT INTO substitutes "
                              "(substitute_name, substitute_nutriscore, "
                              "substitute_description, substitute_store, substitute_url) "
                              "VALUES (%s, %s, %s, %s, %s)")
            cur.execute(add_substitute, (*data_substitute,))
            con.commit()
            print("Substitut enregistré dans vos favoris")
            input_choice = False
        elif user_choice == "2":
            print("Ce substitut ne sera pas enregistré")
            input_choice = False
        else:
            print("Commande invalide")
            
    
def search_substitute(): 
    sql_id = ("SELECT * FROM foodstuffs WHERE foodstuff_id = %s ")
    sql_choice = user_select()
    # call function (select_id)
    select_id(sql_id, sql_choice)
    data_result = select_id(sql_id, sql_choice)
    
    for value in data_result:
        #extract some values from Table foodstuffs
        search_terms = value[4]
        tag_category = value[3]
    
    url = "https://fr.openfoodfacts.org/cgi/search.pl?"
    # parameter for requests
    payloads = {'action': 'process',
                'search_terms': '',#user search
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': '',#category
                'tagtype_1': 'nutrition_grades',
                'tag_contains_1': 'contains',
                'tag_1': 'a',
                'json': '1'}

    payloads['search_terms'] = search_terms
    payloads['tag_0'] = tag_category
    response = requests.get(url, params=payloads)
     
    if response.status_code != 200:
        print("pb")
    else:
        # call api
        json_data = response.json()
        return json_data

        
                                                 
def healthy_substitute():
    # call function search_substitute()
    result_search = search_substitute()
    # select [key] of requests 
    count_result = result_search['count']
    products_result = result_search['products']
    index = 0
    
    if count_result == 0:
        print("Aucun substitus trouvé")
        
    else:
        print(f"{count_result} substitut(s) trouvé(s)")
        for value in products_result:
            index += 1
            sub_name = value['product_name']
            sub_score = value['nutrition_grades']
            sub_desc = value['generic_name']
            if sub_desc == '':
                #change value
                sub_desc = 'incomplet'
            sub_store = value['stores']
            if sub_store == '':
                sub_store = 'incomplet'
            sub_url = value['url']
            print(f"\
+-----------------------------------------------+\n\
--------------[Substitut n°{index}]--------------\n\
Nom         : {sub_name}\n\
Store       : {sub_store}\n\
Nutri Score : {sub_score}\n\
URL         : {sub_url}\n\
+-----------------------------------------------+\n")
            # call function save_substitute()
            save_substitute(sub_name, sub_score, sub_desc, sub_store, sub_url)
