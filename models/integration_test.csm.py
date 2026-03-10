from csmp import MACRO, TITLE, PARAM, CONSTANT, METHOD, TIMER, OUTPUT, PRINT
from csmp import EXP, AMIN1
from csmp import Clip
from csmp.keywords import INCON

TITLE("INTEGRATION TEST")

x       = INTGRL(ix, dxdt)
ix      = INCON(1.0)
dxdt    = 1.1 * x
xt      = x

TIMER(FINTIM = 10., DELT = 1., PRDEL = 1.)
METHOD("RECT")
PRINT(x, xt, dxdt)

