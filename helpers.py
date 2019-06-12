def list_to_str(l : []) -> str:
    s = ''
    for e in l:
        s += e + ' '
    return s


"""
In the tasks list we will have: function_name arg1, arg2 ..., column_name
the tasks will be resolved after the execute query phase
"""
class QTasks():
    
    __instance = None
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if QTasks.__instance == None:
            QTasks()
        return QTasks.__instance
   
    def __init__(self):
        """ Virtually private constructor. """
        
        if QTasks.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.tasks = []
            QTasks.__instance = self

