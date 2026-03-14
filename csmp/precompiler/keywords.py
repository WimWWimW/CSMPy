# from csmp.customTypes import IntegrationMethod
from enum import Enum
from csmp.errors import PrecompilerError
from _warnings import warn
from unicodedata import category

def symbols():
    return [n for n in globals() if n == n.upper() and not n.startswith("_") ]


class KeywordStatus(Enum):
    OK                  = 0
    toINIT              = 1
    IGNORED             =-2
    NOT_YET_SUPPORTED   =-3
    OBSOLETE            =-4
    NOT_SUPPORTED       =-5
    UNDECIDED           =-6
    
    def humanReadable(self):
        return self.name.lower().replace("_", " ")


class MetaFunction(type):
    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls.__execute__(*args, **kwargs)


class Keyword(metaclass = MetaFunction):    
    status  = KeywordStatus.IGNORED
    varList = False
    transl  = ""
    
    @classmethod
    def inPlace(cls, node):
        if cls.status == KeywordStatus.NOT_SUPPORTED:
            raise PrecompilerError(f"{cls.__name__} is not supported in CSMPy")
        
        if cls.status == KeywordStatus.IGNORED:
            warn(f"{cls.__name__} is ignored", category=SyntaxWarning)
            return None
        
        if cls.status.value <= KeywordStatus.NOT_YET_SUPPORTED.value:
            warn(f"{cls.__name__} has status '{cls.status.humanReadable()}' in CSMPy and will not be proceessed now", category=SyntaxWarning)
            return None

        return node
    

# DATA statements:
class PARAM(Keyword):
    status  = KeywordStatus.OK
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(value):
        return value 

    

class CONSTANT(Keyword):
    status  = KeywordStatus.OK
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(value):
        return value 


class INCON(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(value):
        return value 


class FUNCTION(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*xyPairs):
        return


class TABLE(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(**data):
        return 


class OVERLAY(Keyword):
    status  = KeywordStatus.NOT_SUPPORTED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return




# CONTROL statements:
class RENAME(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(**synonyms):
        return


class FIXED(Keyword):
    status  = KeywordStatus.OBSOLETE
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class MEMORY(Keyword):
    status  = KeywordStatus.UNDECIDED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class HISTORY(Keyword):
    status  = KeywordStatus.UNDECIDED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class STORAGE(Keyword):
    status  = KeywordStatus.OBSOLETE
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class DECK(Keyword):
    status  = KeywordStatus.NOT_SUPPORTED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class MACRO(Keyword):
    status  = KeywordStatus.OK
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return



# INITIAL
# DYNAMIC
# TERMINAL
# SORT
# NOSORT

class END(Keyword):
    status  = KeywordStatus.IGNORED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class CONTINUE(Keyword):
    status  = KeywordStatus.NOT_SUPPORTED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class PROCEDURE(Keyword):
    status  = KeywordStatus.OBSOLETE
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class STOP(Keyword):
    status  = KeywordStatus.IGNORED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class ENDJOB(Keyword):
    status  = KeywordStatus.IGNORED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


# ENDJOB STACK
class COMMON(Keyword):
    status  = KeywordStatus.UNDECIDED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


# COMMON MEM  
class DATA(Keyword):
    status  = KeywordStatus.OBSOLETE
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return




# Execution control statements:
class TIMER(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(PRDEL = None, OUTDEL = None, FINTIM = None, DELT = None, DELMIN = None):
        return


class FINISH(Keyword):
    status  = KeywordStatus.OK
    varList = False
    transl  = 'self.checkEndConditions'

    @staticmethod
    def __execute__(**conditions):
        return


class RELERR(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(**epsila):
        return


class ABSERR(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(**errors):
        return


class METHOD(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(method: IntegrationMethod|str):
        return




# Output control statements:
class PRINT(Keyword):
    status  = KeywordStatus.toINIT
    varList = True
    transl  = ""

    @staticmethod
    def __execute__(*varNames):
        print(varNames)
        return


class OUTPUT(Keyword):
    status  = KeywordStatus.toINIT
    varList = True
    transl  = ""

    @staticmethod
    def __execute__(*varNames):
        return


class TITLE(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(simulationTitle):
        return


class PREPARE(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*varNames):
        return


class PRTPLOT(Keyword):
    status  = KeywordStatus.UNDECIDED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return


class LABEL(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(printPlotCaption):
        return


class RANGE(Keyword):
    status  = KeywordStatus.toINIT
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*varNames):
        return


class RESET(Keyword):
    status  = KeywordStatus.NOT_SUPPORTED
    varList = False
    transl  = ""

    @staticmethod
    def __execute__(*args, **kwargs):
        return





if __name__ == '__main__':
    import re
    
    CONTINUE.inPlace(None)