import pandas as pd
import pyodbc
import numpy as np
from prettytable import from_db_cursor, PrettyTable
from ddl import *
from dml import *

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=OMENDEJOSE;'
                      'Database=tsunami_historical;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


def menu():
    print("---------------------------------------------------------")
    options = PrettyTable()
    options.field_names = ["Number", "Options"]
    options.add_rows([
        ["1.", "Create tables"],
        ["2.", "Select Queries"],
        ["3.", "Drop tables"],
        ["4.", "Bulk Load"]
    ])
    print(options)
    value = input("Enter option number:\n")
    if value == '1':
        createTables()
    elif value == '2':
        queries()
    elif value == '3':
        dropTables()
    elif value == '4':
        bulkload()

    value2 = input("Exit from menu (y/n):")
    if not value2 == 'y':
        menu()


def queries():
    options = PrettyTable()
    options.field_names = ["Number", "Options"]
    options.add_rows([
        ["1.", "Count cargas en modelo"],
        ["2.", "Tsunamis agrupados por año y paises en lo que ha ocurrido"],
        ["3.", "Tsunamis agrupados por pais y paises en lo que ha ocurrido"],
        ["4.", "Promedio de total damage por pais"],
        ["5.", "Top 5 de paises con mas muertes"],
        ["6.", "Top 5 de años con mas muertes"],
        ["7.", "Top 5 de años que mas tsunamis han tenido"],
        ["8.", "Top 5 de años con mayor numero de casa destruidas"],
        ["9.", "Top 5 de paises con mayor numero de casas dañadas"],
        ["10.", "Promedio de altura maxima del agua por cada pais"]
    ])
    print(options)
    value = input("Enter query number:")
    if value == '1':
        cursor.execute(Q1)
    elif value == '2':
        cursor.execute(Q2)
    elif value == '3':
        cursor.execute(Q3)
    elif value == '4':
        cursor.execute(Q4)
    elif value == '5':
        cursor.execute(Q5)
    elif value == '6':
        cursor.execute(Q6)
    elif value == '7':
        cursor.execute(Q7)
    elif value == '8':
        cursor.execute(Q8)
    elif value == '9':
        cursor.execute(Q9)
    elif value == '10':
        cursor.execute(Q10)

    if value == '':
        print('ERROR: Ingresa una opcion valida')
    else:
        result = from_db_cursor(cursor)
        f = open("results/querie"+value+".txt", "w+")
        f.write(result.get_string())
        f.close()

    value2 = input("Exit from Queries menu (y/n):")
    if not value2 == 'y':
        queries()


def createTables():
    cursor.execute(CREATE_TABLE)
    conn.commit()


def dropTables():
    cursor.execute(DROP_TABLE)
    conn.commit()


def bulkload():
    path = input("Enter path:")
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    for row in list(df.itertuples())[1:]:
        cursor.execute('''
                    INSERT INTO temp (year_, month_, day_, hour_, min_, sec_, event_validity, cause_code, magnitud, deposits, country, 
                    location_, latitude,longuitude, maxWaterHeight, runups, tsunameMagnitud, intensity, deaths, missing, missingDescription,
                    injuries, damage, damageDescription, housesDestroyed, housesDamage)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''',
                       int(row.Year) if not (np.isnan(row.Year)) else None,
                       int(row.Mo) if not (np.isnan(row.Mo)) else None,
                       int(row.Dy) if not (np.isnan(row.Dy)) else None,
                       int(row.Hr) if not (np.isnan(row.Hr)) else None,
                       int(row.Mn) if not (np.isnan(row.Mn)) else None,
                       int(row.Sec) if not (np.isnan(row.Sec)) else None,
                       int(row[7]) if not (np.isnan(row[7])) else None,
                       int(row[8]) if not (np.isnan(row[8])) else None,
                       row[9] if not (np.isnan(row[9])) else None,
                       int(row[10]) if not (np.isnan(row[10])) else None,
                       row[11],
                       str(row[12]) if not (str(row[12]) == '') else None,
                       row[13] if not (np.isnan(row[13])) else None,
                       row[14] if not (np.isnan(row[14])) else None,
                       row[15] if not (np.isnan(row[15])) else None,
                       int(row[16]) if not (np.isnan(row[16])) else None,
                       row[17] if not (np.isnan(row[17])) else None,
                       row[18] if not (np.isnan(row[18])) else None,
                       int(row[19]) if not (np.isnan(row[19])) else None,
                       int(row[20]) if not (np.isnan(row[20])) else None,
                       int(row[21]) if not (np.isnan(row[21])) else None,
                       int(row[22]) if not (np.isnan(row[22])) else None,
                       row[23] if not (np.isnan(row[23])) else None,
                       int(row[24]) if not (np.isnan(row[24])) else None,
                       int(row[25]) if not (np.isnan(row[25])) else None,
                       int(row[26]) if not (np.isnan(row[26])) else None,

                       )
    cursor.execute(BULK_LOAD)
    conn.commit()


print("\nPRACTICA 1 - SEMINARIO 2")
print("JOSE MORAN - 201807455")
menu()

# https://datatofish.com/import-csv-sql-server-python/
