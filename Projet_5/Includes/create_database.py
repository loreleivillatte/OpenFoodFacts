#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script insert data from the api OpenFoodFacts into database `pur_beurre`
"""

import mysql.connector as  mdb
import json
import requests
#personal module  
import config
#open a connection to the MySQL server
con = config.get_connection()
cur = con.cursor()

url_foodstuff = "https://fr.openfoodfacts.org/api/v0/produit/{}.json"

data_sample = [["snacks sucrés", "3387390406719", "3033710070145"],
               ["snacks salés", "3336971209164", "3018930004903"],
               ["plats préparés frais", "3560070704057", "3245414668058"],
               ["plats préparés surgelés", "3270160717323", "3564700165812"]]



for category in data_sample:
    """ take first element for each line in {data_sample}
    adds it to the database"""
    category_name = category.pop(0)
    add_category = ("INSERT INTO categories "
                    "(category_name) "
                    "VALUES (%s)")
    data_category = category_name
    cur.execute(add_category, (data_category,))
    # return the AUTO_INCREMENT value for the next insert
    id = cur.lastrowid
    con.commit()
    print(f"la catégorie [{data_category}] vient d'être ajoutée")

    for code in category:
        """ take code for each line in {data_sample}
        call api
        adds it to the database"""
        data = requests.get(f"{url_foodstuff}{code}")
        if data.status_code != 200:
            print("Problème avec la requête HTTP")
        else:
            # extract some values
            data = data.json()["product"]
            foodstuff_name = data["product_name"]
            foodstuff_description = data["generic_name"]
            add_foodstuff = ("INSERT INTO foodstuffs "
                             "(id, foodstuff_name, foodstuff_category, foodstuff_description) "
                             "VALUES (%s, %s, %s, %s)")
            data_name = foodstuff_name
            data_description = foodstuff_description
            # insert values into database
            cur.execute(add_foodstuff, (id, data_name, data_category, data_description,))
            con.commit()
            print(f" -> Le produit [{foodstuff_name}] vient d'être ajouté")
            
print("Base de données [pur_beurre] créée avec succès")
