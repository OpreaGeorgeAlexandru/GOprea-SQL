import sqlite3
from helpers import QTasks
from functions import *
from copy import deepcopy

CONN = sqlite3.connect('database.db')

#cur.execute('CREATE TABLE PRODUCT(product_ID INTEGER PRIMARY KEY, description TEXT, price INTEGER, old_price INTEGER);')
#cur.execute('insert into product values(1,\'adidasi\',12,23)')
#prods = cur.execute('select * from product')
#tables = cur.execute('SELECT name, sql FROM sqlite_master WHERE type=\'table\' ORDER BY name;')

def get_index(title : [str], column_name) -> int:
    for i,e in enumerate(title):
        if e == column_name:
            return i
    return -1

def execute_query(query : str):
    global CONN
    q_tasks = QTasks.getInstance().tasks
    cur = CONN.cursor()
    print("executing query: " + query)
    cur.execute(query)
    CONN.commit()
    
    rows_r = cur.fetchall()
    
    rows = []

    for e in rows_r:
        rows.append(e)
    print(rows)
    print("TODOs: " + str(q_tasks))

    title = [i[0] for i in cur.description]
    print(title)

    # execute each task
    for task in q_tasks:
        col = []
        index = get_index(title,task[-1])
        
        if index == -1:
            raise NameError("Incorrect column name")

        for row in rows:
            col.append(list(row)[0])
        

        col = apply_funct(task[0],task[1:-1],col)
        new_rows = []
        for i_row, row in enumerate(rows):
            new_row = []
            for i,e in enumerate(list(row)):
                if i != index:
                    new_row.append(e)
                else:
                    new_row.append(col[i_row])
            new_rows.append(tuple(new_row))        
        rows = new_rows
        
    for row in rows:
        print(row)

if __name__ == "__main__":
    execute_query('insert into product values(3, \'muie tuicu\',40,50)')
    #execute_query('SELECT name, sql FROM sqlite_master WHERE type=\'table\' ORDER BY name;')

