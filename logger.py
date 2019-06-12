
class Log():
    
    __instance = None
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Log.__instance == None:
            Log()
        return Log.__instance
   
    def __init__(self):
        """ Virtually private constructor. """
        
        if Log.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.on = True
            Log.__instance = self

    def print(self, s : str) -> None:
        if self.on:
            print(s)
