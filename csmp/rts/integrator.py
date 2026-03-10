


class StateVariable:
    
    def __init__(self, name, initialValue):        
        self.name  = name
        self.value = initialValue
        self.rate  = 0.0
        self.temp  = None



class Integrator: 

    def __init__(self, model):
        self.model       = model
        self.timer       = model.timer
        self.isMajorStep = True
        
    TSTEP = property(lambda i: i.isMajorStep)
        
        
    def integrate(self, s): pass
    
    def initialize(self): pass
        
        
    def run(self):
        for s in self.model.stateVariables:
            self.integrate(s)
        self.timer.setTimeStep()
               
           
    def recalculateRates(self, time):
        ratesEtc = self.model.loop(time)
        if self.isMajorStep:
            self.model.ratesEtc.update(ratesEtc)
            

class Rect(Integrator):
    
    def integrate(self, s):
        self.recalculateRates(self.timer.time)
        s.value += s.rate * self.timer.delt

    

class Trapz(Integrator):

    class TempData:
        def __init__(self, previousRate = 0):
            self.previousRate = previousRate


    def initialize(self):
        for s in self.model.stateVariables:
            s.temp = self.TempData(s.rate)
            
            
    def run(self):
        self.recalculateRates(self.timer.time)
        super().run()

        
    def integrate(self, s):
        rate     = (s.rate + s.temp.previousRate) / 2
        s.value += rate * self.timer.delt
        s.temp.previousRate = rate

    
class RksFx(Integrator):

    class TempData:
        def __init__(self, previousRate = 0, previousValue = 0):
            self.previousValue  = previousValue
            self.previousRate   = previousRate


    def initialize(self):
        self.model.loop(self.timer.time)
        for s in self.model.stateVariables:
            s.temp = self.TempData(s.rate)


    def run(self):
        self.model.loop(self.timer.time)
        for s in self.model.stateVariables:
            self.estimate(s)
            
        self.isMajorStep = False
        self.model.loop(self.timer.time + self.timer.delt / 2)
        self.isMajorStep = True
        
        for s in self.model.stateVariables:
            self.integrate(s)
        self.timer.setTimeStep()
               
           
    def estimate(self, s):
        s.temp.previousValue = s.value
        k1       = s.temp.previousRate
        s.value += 0.5 * k1 * self.timer.delt
        
        
    def integrate(self, s):
        X       = s.temp.previousValue
        k2      = s.rate
        s.value = X + k2* self.timer.delt
        s.temp.previousRate = k2
        

        