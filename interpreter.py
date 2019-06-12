import executor
from config import Config
import helpers as help
from logger import Log

def parse_command(line):
    line = line.replace('\n','').replace('\r','')
    for item in Config.items():
        line = line.replace(item,' ' + item + ' ')
    return [x for x in line.lower().split(' ') if x != '']

def pre_parse(words):
    pass

"""
a query in GOPREA has 3 zones ex:
zone0 = Table1 t1 * Table2 t2
zone1 = (t1.col1, t2.col1)
zone3 = [t1.col1 > 10]
query = Table1 t1 * Table2 t2 (t1.col1, t2.col1) [t1.col1 > 10]

"""
def post_parse(words):
    new_list = []
    zone0 = True
    zone1 = False
    zone2 = False

    for i,e in enumerate(words):
        # append words like table alias.Column
        if e == '(':
            zone0 = False
            zone1 = True
        if e == '[':
            zone1 = False
            zone2 = True

        if i > 0 and zone0 and e not in Config.operators and e not in Config.delimiters and new_list[-1] not in Config.operators and new_list[-1] not in Config.delimiters:
            new_list.append(new_list.pop() + ' as ' + e)
            continue
        if i > 1 and words[i-1] == '.':
            new_list.append(new_list.pop(-2) + new_list.pop(-1) + e)
            continue
        if i > 0 and words[i-1] in Config.operators and e in Config.operators:
            new_list.append(new_list.pop() + e)
            continue
        new_list.append(e)
    return new_list

"""
Get a column and parse it
Example: sum col1 -> sum(col1)
"""
def parse_column(col : str) -> str:
    split = parse_command(col)
    splited = []

    for i,e in enumerate(split):
        if e == '.':
            splited.append(splited.pop() + e + split[i+1])
            continue
        if i > 0 and split[i-1] == '.':
            continue
        splited.append(e)
        
    split = splited

    q_tasks = help.QTasks.getInstance()

    if split[0] in Config.functions:
        # execute that task later after execute phase
        q_tasks.tasks.append(split)
        # return just column name for now
        return split[-1]
    
    if len(split) == 1:
        return split[0]

    return split[0] + " ( " + split[1] + " ) "    

    None

# returns the zone1 -> the columns selected in the query
def get_selected_columns(splited : [str]) -> [str]:
    q_tasks = help.QTasks.getInstance()
    zone1 = False
    selected = []
    buffer = ""
    # get columns selected
    for i in range(len(splited)):
        if splited[i] == '(':
            zone1 = True
            continue
        if splited[i] == ')':
            if buffer != '':
                buffer = parse_column(buffer)
                selected.append(buffer)
            zone1 = False
            continue
        if zone1 and splited[i] == ',':
            buffer = parse_column(buffer) + ' ,'
            selected.append(buffer)
            buffer = ""
            continue
        if zone1:
            buffer += splited[i] + ' '
    return selected

def get_tables(splited : [str]) -> str:
    tables = ''

    for e in splited:
        if e == '(':
            break
        if e in Config.joins.keys():
            tables += Config.joins[e] + ' '
            continue 
        tables += e + ' '
        
    return tables

def get_groupby(splited : [str]) -> str:
    for i,e in enumerate(splited):
        if e == 'group':
            return help.list_to_str(splited[i:])
    return ""

def get_where(splited : [str]) -> str:
    where = ''
    flag = False
    for e in splited:
        if e == '[':
            flag = True
            continue
        if flag and e not in Config.delimiters:
            where += e + ' '
        if e == ']':
            break
    if where != '':
        where = "where " + where
    return where

def get_on(splited : [str]) -> str:
    on = ''
    zoneOn = False
    
    for i,e in enumerate(splited):
        if e == 'group':
            zoneOn = False
            return on
        if zoneOn:
            on += e + " "
            continue
        if e == 'on':
            zoneOn = True
    if on != '':
        on = "on " + on
    return on

""" 
If is a create view or create table parse it.
"""
def parse_create(splited : [str]) -> str:
    if splited[0] in ['table']:
        return "create " + help.list_to_str(splited)
    return None

def parse_view(splited : [str]) -> str:
    if splited[0] in ['view']:
        return "create view " + splited[1] + " as " + parse_query(help.list_to_str(splited[3:]))
    return None

def parse_insert(splited : [str]) -> str:
    if splited[1] == '+=':
        return "insert into " + splited[0] + " values " + help.list_to_str(splited[2:])
    return None

"""
Syntax: Table_Name -= [condition]
"""
def parse_delete(splited : [str]) -> str:
    if splited[1] == '-=':
        return "delete from " + splited[0] + " " + get_where(splited)
    return None

def parse_query(query : str) -> str:
    log = Log.getInstance()

    splited = parse_command(query)
    
    is_create = parse_create(splited)

    if is_create != None:
        return is_create

    is_view = parse_view(splited)
    log.print(is_view)
    log.print(splited)
    if is_view != None:
        return is_view
    

    splited = post_parse(splited)

    is_insert = parse_insert(splited)
    log.print(is_insert)
    log.print(splited)
    if is_insert != None:
        return is_insert
    
    is_delete = parse_delete(splited)
    log.print(is_delete)
    log.print(splited)
    if is_delete != None:
        return is_delete
    


    columns = get_selected_columns(splited)

    select_columns = 'select '
    tables = ''
    where = ''

    if columns == []:
        select_columns += '* from '
    else:
        select_columns += help.list_to_str(columns) + 'from '

    tables = get_tables(splited)

    on = get_on(splited)

    where = get_where(splited)

    groupby = get_groupby(splited)

    return select_columns + tables + on + where + groupby

if __name__ == "__main__":
    print(parse_query('Table1 t1 * Table2 t2 (cluster 3 t1.col1, t2.col1) [t1.col1 > 10]'))
    pass