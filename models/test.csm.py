#@PydevCodeAnalysisIgnore
from csmp import MACRO, TITLE, PARAM, CONSTANT, METHOD, TIMER, OUTPUT, PRINT
from csmp import EXP, AMIN1
from csmp import Clip


X = INTGRL(0., RX)
RX = 1
FN = FUNCTION(0, 0, 5, 1, 10, 0)
T = NLFGEN(FN, X)
TITLE("CSMPy-TEST")
TIMER(FINTIM = 10., DELT = 1., PRDEL = 0.5)
METHOD("RECT")
PRINT(X, RX, T, DELT, step)
OUTPUT(TWT)
RENAME(TIME = "Distance", DELT = "step")