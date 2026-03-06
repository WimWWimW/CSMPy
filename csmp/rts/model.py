from abc import ABC, abstractmethod
import sys
        
class StateVariable:
    
    def __init__(self, name, initialValue):        
        self.name  = name
        self.value = initialValue
        self.rate  = 0.0


class Integrator: pass

class Rect(Integrator):
    
    def __init__(self, delta = 1.):
        self.delta = delta
        
        
    def run(self, states):
        for s in states:
            s.value += s.rate * self.delta

    
    def setDeltaTime(self, delt):
        if delt > 0:
            self.delta = delt
    
    
            

class Timer:
    
    def __init__(self, time = 0.0, delt = 1.0, finTim = 10.0, prDel = 1.0, outDel = 1.0):
        self.time   = time
        self.delt   = delt
        self.finTim = finTim
        self.prDel  = prDel
        self.outDel = outDel
        
        
    def changeParameters(self, **params):
        attribs = [name for name in dir(self) if not name.startswith("_")]
        lattrib = [name.lower() for name in attribs]
        try:
            for name, value in params.items():
                i     = lattrib.index(name.lower())
                vName = attribs[i]
                setattr(self, vName, value)
        except ValueError:
            raise RuntimeError("unknown argument", name)
        
        
    def start(self):
        self.time = 0.0
        self._outTimes = [i * self.outDel for i in range(round(self.finTim/self.outDel + 2))]
        self._prnTimes = [i * self.prDel  for i in range(round(self.finTim/self.prDel  + 2))]
        
        
    def printRequired(self):
        return self.time >= self._prnTimes[0]
    
    
    def setTimeStep(self):
        while self._prnTimes[0] <= self.time:
            self._prnTimes.pop(0)
            
        self.time += self.delt
        return self.time < self.finTim
    
        
class CSMP_Model(ABC):
    
    def __init__(self):
        self.title          = 'simulation'
        self.timer          = Timer()
        self.globals        = {}
        self.stateVariables = {}
        self.stateNames     = {}
        self.integrator     = Rect()
    
                
    def createStateVariable(self, index, name, initialValue):
        if index in self.stateVariables:
            raise Exception("attempt to redefine state variable with index %d ('%s')" % (index, name))
        newState = StateVariable(name, initialValue)
        self.stateVariables[index]  = newState
        self.stateNames[name]       = newState
        return newState
    
    
    def getState(self, index):
        return self.stateVariables[index].value
    
    
    def setCurrentRate(self, index, rate):
        self.stateVariables[index].rate = rate
        
        
    def setTimer(self, **params):
        try:
            self.timer.changeParameters(**params)
            self.integrator.setDeltaTime(params.get("DELT", -1))
        except RuntimeError as rte:
            rte.args = ("%s in setTimer() (%s)" % rte.args,)
            raise 
    
            
    def setMethod(self, integrationMethod):
        pass
    
    
    def setPrint(self, *varNames):
        pass
    
    
    def setOutput(self, *varnames):
        pass
    
    
    def setTitle(self, title):
        self.title = title
    
    @abstractmethod
    def defineConstants(self):      return {}
    
    @abstractmethod
    def defineParameters(self):     return {}
    
    @abstractmethod
    def initial(self):              return {}
        
    @abstractmethod
    def loop(self, time):           return
        
    @abstractmethod
    def final(self):                return
        
        
