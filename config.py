# config file for the GOprea

class Config:
    
    operators = ['+','*','-','/','**','*>','*<','>','<','=','!=','***','**<']
    joins = {'*':'join','**':'cross join','*<':'left join','*>':'right join','***':'natural join', '**<':'natural left join'}
    delimiters = ['(',')','[',']','{','}','.',',']
    key_words = ['create','table','view','as','on','int','float','string','where']
    types = ['int','float','string']
    banned_symbols = []
    functions = ['cluster','self_cluster']

    """
    PID = primary key
    UID = uniq id
    FID = foreign key
    NAT = not a type
    """
    column_types = ['pid','uid','fid','nat']
    # constants
    ADMIN_GROUP = "ADMIN_GROUP"
    ANONIM_GROUP = "ANONIM_GROUP"
    
    GROUPS = [ADMIN_GROUP,ANONIM_GROUP]


    @staticmethod
    def items():
        return Config.operators + Config.delimiters
    
    @staticmethod
    def is_key_word(word):
        return word in Config.key_words