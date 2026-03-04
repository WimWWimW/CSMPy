""" ------------------------------------------------------------------
Near exact translation of the CSMP and FORTRAN functions as listed in 
tables 1 & 2 of the CSMP users Manual (1971)

status:
- interface complete
- implementation incomplete

(c) 2026 WP de Winter ------------------------------------------------
"""

import inspect, math
import random
        


class NotYetImplementedError(Exception):
    def __init__(self):
        caller = inspect.stack()[1][3]
        super().__init__("function '%s' has not been implemented yet" % caller)



greaterThanZero = lambda x: x > 0


class Library: 
    @classmethod
    def listMethods(cls):
        # create list of contained functions; to be used as list of known symbols
        return [k for  k in dir(cls) if k == k.upper() and not k.startswith("_")]
        # return [k for  k, v in cls.__dict__.items() if isinstance(v, staticmethod) and not k.startswith("_")]



class CSMP_Functions(Library):
    
    _RNDSEED_ = math.nan # None has special meaning and cannot be used here
    
    @staticmethod
    def INTGRL(ic, x):
        # integrator
        # ic: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def DERIV(ic, x):
        # derivative
        # ic: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def DELAY(n, p, x):
        # dead time (delay)
        # n: number of points sampled
        # p: delay time
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def ZHOLD(x1, x2):
        # zero-order hold
        # x1: ...
        # x2: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def IMPL(ic, p, fofy):
        # implicit function
        # ic: first guess
        # p: error bound
        # fofy: output name of last statement in algebraic loop definition
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def MODINT(ic, x1, x2, x3):
        # mode-controlled integrator
        # ic: ...
        # x1: ...
        # x2: ...
        # x3: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def REALPL(ic, p, x):
        # 1st order lag (real pole)
        # ic: ...
        # p: ...
        # x: ...
        # y(0)= ic
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def LEDLAG(p1, p, x):
        # lead - lag
        # p1: ...
        # p: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def CMPXPL(ic1, ic2, p1, p2, x):
        # 2nd order lag (complex pole)
        # ic1: ...
        # ic2: ...
        # p1: ...
        # p2: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def FCNSW(test, neg, nul, pos, epsilon = 0.):
        # function switch 
        # test: value to test
        # neg: return when test is negative
        # nul: return when test is zero
        # pos: return when test is positive
        return pos if (test > epsilon) else neg if (test < -epsilon) else nul 
    
    
    @staticmethod
    def INSW(test, neg, pos):
        # input switch (relay)
        # test: value to test
        # neg: return when test is negative
        # nul: return when test is zero
        # pos: return when test is positive
        return pos if greaterThanZero(test) else neg 
    
    
    @staticmethod
    def OUTSW(test, value):
        # output switch
        # test: value to test
        # value: return value
        return value, 0 if test < 0 else 0, value
    
    
    @staticmethod
    def COMPAR(x1, x2):
        # comparator
        # x1, x2: comparands
        return 0 if x1 < x2 else 1
    
    
    @staticmethod
    def RST(x1, x2, x3):
        # resettable flip-flop
        # x1: ...
        # x2: ...
        # x3: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def AFGEN(funct, x):
        # arbitrary function generator (linear interpolation)
        # funct: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def NLFGEN(funct, x):
        # arbitrary function generator (quadratic interpolation)
        # funct: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def LIMIT(p1, p2, x):
        # limiter: keeps x between p1 and p2
        # p1, p2: limitation points
        return max(p1, min(p2, x))
    
    
    @staticmethod
    def DEADSP(p1, p2, x):
        # dead space
        # p1, p2: limitation points
        return 0 if p1 <= x <= p2 else x - p2 if x > p2 else x - p1
    
    
    @staticmethod
    def HSTRSS(ic, p1, p2, x):
        # hysteresis loop
        # ic: ...
        # p1: ...
        # p2: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def STEP(p):
        # step function
        # p: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def RAMP(p):
        # ramp function
        # p: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def IMPULS(p1, p2):
        # impulse generator
        # p1: ...
        # p2: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def PULSE(p, x):
        # pulse generator (with x>0 as trigger)
        # p: ...
        # x: ...
        raise NotYetImplementedError() 
        return 0
    
    
    @staticmethod
    def SINE(p1, p2, p3):
        # trigonometric sine wave with delay, frequency and phase parameters
        # p1: delay
        # p2: frequency(radians per unit time)
        # p3: phase shift in radians
        raise NotYetImplementedError() 
        return 0

    @classmethod
    def _setRandomSeed_(cls, seed):    
        if seed != cls._RNDSEED_:
            cls._RNDSEED_ = seed # TODO: reset at a proper moment
            random.seed(seed)
    
    
    @classmethod
    def GAUSS(cls, seed = None, mu = 0.0, sigma = 1.0):
        # noise (random number) # generator with normal distribution
        # I regret this unfortunate order of arguments that doesn't seem wise to change now.
        # seed:  any odd integer 
        # mu:    mean
        # sigma: standard deviation
        cls._setRandomSeed_(seed) 
        return random.gauss(mu, sigma)
    
    
    @classmethod
    def RNDGEN(cls, seed = None):
        # noise (random number) # generator with uniform distribution
        # seed: random seed
        cls._setRandomSeed_(seed) 
            
        return random.uniform(0.0, 1.0)
    
    
    @staticmethod
    def AND(x1, x2):
        # and
        return (greaterThanZero(x1) and greaterThanZero(x2))
    
    
    @staticmethod
    def NAND(x1, x2):
        # not and
        return not (greaterThanZero(x1) and greaterThanZero(x2))
    
    
    @staticmethod
    def NOR(x1, x2):
        # not or
        return not(greaterThanZero(x1) or greaterThanZero(x2))
    
    
    @staticmethod
    def EOR(x1, x2):
        # exclusize or; XOR        
        return greaterThanZero(x1) != greaterThanZero(x2)
    
    
    @staticmethod
    def NOT(x):
        # not x
        return int(not(x))
    
    
    @staticmethod
    def EQUIV(x1, x2):
        # equivalent; not Xor
        return greaterThanZero(x1) == greaterThanZero(x2)
    
    
class FORTRAN_Functions(Library):
        
    @staticmethod
    def EXP(x):
        # exponential function: e raised to the power x, 
        # where e = 2.718281… is the base of natural logarithms.
        return math.exp(x)
    
    
    @staticmethod
    def ALOG(x):
        # natural logorithmy = ln(x)
        return math.log(x)
    
    
    @staticmethod
    def ALOG10(x):
        # common logorithmy = log10(x)
        return math.log10(x)
    
    
    @staticmethod
    def ATAN(x):
        # arctangent --> angle in radians
        # x: tangent        
        return math.cos(x)
    
    
    @staticmethod
    def SIN(x):
        # trigonometric sine
        # x: angle in radians
        return math.sin(x)
    
    
    @staticmethod
    def COS(x):
        # trigonometric cosine
        # x: angle in radians
        return math.cos(x)
    
    
    @staticmethod
    def SQRT(x):
        # square root
        return math.sqrt(x)
    
    
    @staticmethod
    def TANH(x):
        # hyperbolic tangent
        return math.tanh(x)
    
    
    @staticmethod
    def _abs(x):
        # absolute value (real argument and output)
        return abs(x)
    
    
    @staticmethod
    def _amax(*args):
        # largest value (numeric arguments and real output)
        return max(*args)

    
    @staticmethod
    def _imax(*args):
        # largest value (numeric arguments and integer output)
        return int(max(*args))
    
    
    @staticmethod
    def _amin(*args):
        # smallest value (numeric arguments and real output)
        return min(*args)

    
    @staticmethod
    def _imin(*args):
        # smallest value (numeric arguments and integer output)
        # *args: ...
        return int(min(*args))
    
    ABS     = IABS  = _abs
    AMAX0   = AMAX1 = _amax
    MAX0    = MAX1  = _imax
    AMIN0   = AMIN1 = _amin
    MIN0    = MIN1  = _imin
    
    
                
if __name__ == '__main__':
                        
    print(CSMP_Functions.listMethods())
    print(CSMP_Functions.RNDGEN(5))
    print(CSMP_Functions.RNDGEN(5))
    
    for i in range(25):
        print(i, CSMP_Functions.DEADSP(10, 15, i))