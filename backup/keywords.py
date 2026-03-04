from methods import IntegrationMethod

def symbols():
    return [n for n in globals() if n == n.upper() and not n.startswith("_") ]






# DATA stateements:
def PARAM(value): return value 
def CONSTANT(value): return value 
def INCON(value): return value 
def FUNCTION(*xyPairs): return
def TABLE(**data): return 
# OVERLAY     * not supported *


# CONTROL statements:
def RENAME(**synonyms): return
# FIXED       (obsolete)
# MEMORY      * undecided *
# HISTORY     * undecided *
# STORAGE     (obsolete)
# DECK        * not supported *
# MACRO       * not supported *
# INITIAL
# DYNAMIC
# TERMINAL
# END         * not supported *
# CONTINUE    * not supported *
# SORT
# NOSORT
# PROCEDURE   (obsolete)
# STOP        * not supported *
# ENDJOB      * not supported *
# ENDJOB STACK* not supported *
# COMMON      * undecided *
# COMMON MEM  * undecided *
# DATA        (obsolete)


# Execution control statements:
def TIMER(PRDEL = None, OUTDEL = None, FINTIM = None, DELT = None, DELMIN = None): return
def FINISH(**conditions): return
def RELERR(**epsila): return
def ABSERR(**errors): return
def METHOD(method: IntegrationMethod|str): return


# Output control statements:
def PRINT(*varNames): return
def OUTPUT(*varNames): return
def TITLE(simulationTitle): return
def PREPARE(*varNames): return
# PRTPLOT     * undecided *
def LABEL(printPlotCaption): return
def RANGE(*varNames): return
 
# RESET       * not supported *    

