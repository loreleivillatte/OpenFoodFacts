#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mdb

def get_connection():
    """
    The connect() constructor creates a connection to the MySQL server
    and returns a MySQLConnection object.
    """
    connection = mdb.connect(host='localhost',
                             user='root',
                             passwd='password',
                             database='pur_beurre')
    return connection
